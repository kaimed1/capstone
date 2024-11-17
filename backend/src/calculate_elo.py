import pandas as pd

def LoadTeams():
    teams_file = 'backend/data/Teams.csv'
    schedule_file = 'backend/data/Schedule_Stats.csv'

    teams_df = pd.read_csv(teams_file)
    schedule_df = pd.read_csv(schedule_file)    

    return teams_df, schedule_df


def CreateEloTable(teams, schedule):
    elo_df = pd.DataFrame(schedule['Team'].unique(), columns=['Team'])
    elo_df.sort_values(by='Team', inplace=True)
    elo_df.reset_index(drop=True, inplace=True)

    elo_df = pd.merge(elo_df, teams[['team_id','School', 'Conference']], left_on='Team', right_on='team_id', how='left').drop(columns='team_id')

    elo_df['elo'] = 1500

    return elo_df

def CalculateElo(elo, schedule):
    for game in schedule.itertuples(index=True):

        delta = 30 if game.Result else -30
        
        elo['elo'] += (elo['Team'] == game.Team) * delta
    
    elo.sort_values(by='elo', ascending=False ,inplace=True)
    elo.to_csv('backend/data/Elo.csv', index=False)

def main():
    teams, schedule = LoadTeams()
    elo = CreateEloTable(teams, schedule)
    CalculateElo(elo, schedule)

main()