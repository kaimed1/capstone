import pandas as pd
import math

ELO_K = 100

CONFERENCE_ELO = {
    'Atlantic Coast Conference': 1500,
    'Big Ten Conference': 1500,
    'Big 12 Conference': 1500,
    'Independent': 1500,
    'Pacific 12 Conference': 1500,
    'Southeastern Conference': 1500,
    'American Athletic Conference': 1400,
    'Mid-American Conference': 1350,
    'Mountain West Conference': 1350,
    'Sun Belt Conference': 1350,
    'Conference USA': 1300
}

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

    elo_df['elo'] = elo_df['Conference'].map(CONFERENCE_ELO).fillna(1500)

    return elo_df

def CalculateElo(elo, schedule):
    schedule = schedule.iloc[::2]
    
    for game in schedule.itertuples(index=True):
        team_elo = int(elo.loc[elo['Team'] == game.Team, 'elo'].iloc[0])
        opp_elo = int(elo.loc[elo['Team'] == game.Opponent, 'elo'].iloc[0])
        
        e_team = 1 / (1 + 10 ** ((opp_elo - team_elo) / 400))
        e_opp = 1 / (1 + 10 ** ((team_elo - opp_elo) / 400))

        new_team = int(team_elo + ELO_K * (game.Result - e_team))
        new_opp = int(opp_elo + ELO_K * ((1 - game.Result) - e_opp))

        elo.loc[elo['Team'] == game.Team, 'elo'] = new_team
        elo.loc[elo['Team'] == game.Opponent, 'elo'] = new_opp
    
    elo.sort_values(by='elo', ascending=False ,inplace=True)
    elo.reset_index(drop=True, inplace=True)

def main():
    teams, schedule = LoadTeams()
    elo = CreateEloTable(teams, schedule)
    CalculateElo(elo, schedule)

main()