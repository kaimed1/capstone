import pandas
import numpy as np
import joblib
import sqlite3

pandas.options.mode.chained_assignment = None

# Create a connection to the sqlite database
sqlite_connection = sqlite3.connect('./backend/data/football.db')


def reset_running_stats():
    # Load all teams from the sqlite database
    teams = pandas.read_sql_query('SELECT * FROM teams', sqlite_connection)
    stats_df = pandas.DataFrame(columns=['team_id', 'school', 'PrevWeekBYE', 'RunningAvgScore', 'Wins', 'Losses', 'Home_Win_Rate', 'Away_Win_Rate',
                                'OSRS', 'DSRS', 'SRS', 'Off_Score', 'Def_Score', 'Off_Pass', 'Def_Pass', 'Off_Rush', 'Def_Rush', 'Off_Total', 'Def_Total'])

    adv_stats_2024 = pandas.read_csv(
        './backend/data/december5_2024_fbs_advanced.csv')
    # Loop over each team
    for index, row in teams.iterrows():
        team_id = row['team_id']
        team = row['School']
        prev_week_bye = 1

        team_adv = adv_stats_2024.loc[adv_stats_2024['School'] == team]
        # All other stats are 0
        running_avg_score = 0
        wins = 0
        losses = 0
        home_win_rate = 0
        away_win_rate = 0

        if team_adv.empty:
            osrs = 0
            dsrs = 0
            srs = 0
            off_score = 0
            def_score = 0
            off_pass = 0
            def_pass = 0
            off_rush = 0
            def_rush = 0
            off_total = 0
            def_total = 0
        else:
            osrs = team_adv['OSRS'].values[0]
            dsrs = team_adv['DSRS'].values[0]
            srs = team_adv['SRS'].values[0]
            off_score = team_adv['Off_Score'].values[0]
            def_score = team_adv['Def_Score'].values[0]
            off_pass = team_adv['Off_Pass'].values[0]
            def_pass = team_adv['Def_Pass'].values[0]
            off_rush = team_adv['Off_Rush'].values[0]
            def_rush = team_adv['Def_Rush'].values[0]
            off_total = team_adv['Off_Total'].values[0]
            def_total = team_adv['Def_Total'].values[0]

        # Add the stats to the dataframe
        stats_df.loc[index] = [team_id, team, prev_week_bye, running_avg_score, wins, losses, home_win_rate, away_win_rate,
                               osrs, dsrs, srs, off_score, def_score, off_pass, def_pass, off_rush, def_rush, off_total, def_total]
    # Save the stats to a csv file
    stats_df.to_csv('./backend/data/running_season_stats.csv', index=False)


def format_schedule():
    schedule = pandas.read_csv('./backend/data/Full_Schedule.csv')
    schedule.drop(columns=['Rk', 'Date', 'Time', 'Day', 'Notes'], inplace=True)

    # Loop over each row in the schedule, and determine which is the home team
    for index, row in schedule.iterrows():
        home_team = ''
        away_team = ''
        if row['Unnamed: 7'] == '@':
            home_team = row['Loser']
            away_team = row['Winner']
        else:
            home_team = row['Winner']
            away_team = row['Loser']

        # Remove any leading rankings from the team names
        home_team = home_team.split(') ')[-1]
        away_team = away_team.split(') ')[-1]
        schedule.at[index, 'Winner'] = schedule.at[index,
                                                   'Winner'].split(') ')[-1]
        schedule.at[index, 'Loser'] = schedule.at[index,
                                                  'Loser'].split(') ')[-1]

        schedule.at[index, 'Home'] = home_team
        schedule.at[index, 'Away'] = away_team

    # Add a column for the prediction
    schedule['Predicted Winner'] = np.nan

    # Reorder columns
    schedule = schedule[['Wk', 'Home', 'Away',
                         'Predicted Winner', 'Winner', 'Pts', 'Loser', 'Pts.1']]

    return schedule


def predict_game(home_team_stats, away_team_stats, home_id, away_id):
    # Load the model and encoders
    model = joblib.load(
        './backend/data/trained_models/random_forest_model_v2.pkl')

    stats_diff = home_team_stats.values[0] - away_team_stats.values[0]
    prediction = model.predict([stats_diff])

    result = (prediction[0] > 0.47).astype(int)

    winner = home_id if result == 1 else away_id
    loser = away_id if result == 1 else home_id

    return winner, loser


def main():
    # Reset the running stats to reflect the start of a new season
    reset_running_stats()

    # Load the full schedule
    schedule = format_schedule()

    # # Loop over each week in the schedule
    curr_week = 1
    last_week = schedule['Wk'].max()

    total_predicted_correct = 0
    total_games = 0

    while curr_week <= last_week:
        print("Predicting week {}".format(curr_week))
        curr_week_schedule = schedule[schedule['Wk'] == curr_week]
        all_stats = pandas.read_csv('./backend/data/running_season_stats.csv')
        teams_played_this_week = []
        for index, row in curr_week_schedule.iterrows():
            home_team = row['Home']
            away_team = row['Away']

            home_team_id = None
            away_team_id = None

            home_team_stats = None
            away_team_stats = None

            try:
                # Get team IDs from the sqlite database
                home_team_id = pandas.read_sql_query('SELECT team_id FROM teams WHERE School = "{}"'.format(
                    home_team), sqlite_connection).values[0][0].astype(int)
                away_team_id = pandas.read_sql_query('SELECT team_id FROM teams WHERE School = "{}"'.format(
                    away_team), sqlite_connection).values[0][0].astype(int)

                home_team_stats = all_stats.loc[all_stats['team_id']
                                                == home_team_id]
                away_team_stats = all_stats.loc[all_stats['team_id']
                                                == away_team_id]

                home_team_stats.drop(
                    columns=['team_id', 'school'], inplace=True)
                away_team_stats.drop(
                    columns=['team_id', 'school'], inplace=True)

                home_team_stats['HomeTeamAdvantage'] = 1
                away_team_stats['HomeTeamAdvantage'] = 0

                # Reorder columns to match the model
                home_team_stats = home_team_stats[['HomeTeamAdvantage', 'PrevWeekBYE', 'RunningAvgScore', 'Wins', 'Losses', 'Home_Win_Rate', 'Away_Win_Rate',
                                                   'OSRS', 'DSRS', 'SRS', 'Off_Score', 'Def_Score', 'Off_Pass', 'Def_Pass', 'Off_Rush', 'Def_Rush', 'Off_Total', 'Def_Total']]
                away_team_stats = away_team_stats[['HomeTeamAdvantage', 'PrevWeekBYE', 'RunningAvgScore', 'Wins', 'Losses', 'Home_Win_Rate', 'Away_Win_Rate',
                                                   'OSRS', 'DSRS', 'SRS', 'Off_Score', 'Def_Score', 'Off_Pass', 'Def_Pass', 'Off_Rush', 'Def_Rush', 'Off_Total', 'Def_Total']]

                total_games += 1
            except:
                print("Invalid team name")
                continue

            winner, loser = predict_game(
                home_team_stats, away_team_stats, home_team_id, away_team_id)

            winning_team = pandas.read_sql_query('SELECT School FROM teams WHERE team_id = {}'.format(
                winner), sqlite_connection).values[0]

            print("Week {}: {} vs. {} - Winner: {}".format(curr_week,
                  home_team, away_team, winning_team[0]))

            if winning_team[0] == row['Winner']:
                total_predicted_correct += 1

                # Add teams to 'teams_played_this_week' to keep track of who has played and their results
                winning_team_id = None
                losing_team_id = None

                if home_team == row['Winner']:
                    winning_team_id = home_team_id
                    losing_team_id = away_team_id
                else:
                    winning_team_id = away_team_id
                    losing_team_id = home_team_id

                winning_team_result = {
                    'team_id': winning_team_id,
                    'win': 1,
                    'loss': 0,
                    'score': row['Pts'],
                    'at_home': 1 if home_team == row['Winner'] else 0
                }

                losing_team_result = {
                    'team_id': losing_team_id,
                    'win': 0,
                    'loss': 1,
                    'score': row['Pts.1'],
                    'at_home': 1 if home_team != row['Loser'] else 0
                }

                teams_played_this_week.append(winning_team_result)
                teams_played_this_week.append(losing_team_result)

        # TODO: Update the running stats for each team
        for team in teams_played_this_week:
            team_id = team['team_id']
            win = team['win']
            loss = team['loss']
            score = team['score']
            at_home = team['at_home']

            team_stats = all_stats.loc[all_stats['team_id'] == team_id]

            team_stats['PrevWeekBYE'] = 0
            team_stats['RunningAvgScore'] = (
                team_stats['RunningAvgScore'] + score) / 2
            team_stats['Wins'] += win
            team_stats['Losses'] += loss

            # Save the updated stats
            all_stats.loc[all_stats['team_id'] == team_id] = team_stats

        # Save the updated stats to the csv file
        all_stats.to_csv(
            './backend/data/running_season_stats.csv', index=False)

        curr_week += 1

        teams_played_this_week = []

    print("Total games predicted correctly: {}/{}".format(
        total_predicted_correct, total_games))


if __name__ == '__main__':
    main()
