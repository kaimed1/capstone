import pandas as pd


# Get the new end of season stats for each team (no duplicates)
# The data structure was changed from Training_Schedule csv's, this is using the new data structure
def get_new_standings():
    # Load the training data
    df = pd.read_csv('./backend/data/Schedule_Stats.csv').drop(columns=['game_id', 'Result'])

    standings_df = {}

    current_team = df.iloc[0]["Team"]

    sorted_by_teams = df.sort_values(by='Team')

    for i, r in sorted_by_teams.iterrows():
        if df.iloc[i]["Team"] != current_team:
            standings_df[int(current_team)] = df.iloc[i - 1]
            current_team = df.iloc[i]["Team"]

    return standings_df