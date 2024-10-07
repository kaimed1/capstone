import pandas as pd

stat_order = [
    'Rk',
    'team_id',
    'School',
    'Conference',
    'AP Rank',
    'W',
    'L',
    'OSRS',
    'DSRS',
    'SRS',
    'Off_Score',
    'Def_Score',
    'Off_Pass',
    'Def_Pass',
    'Off_Rush',
    'Def_Rush',
    'Off_Total',
    'Def_Total',
]

def ChangeStatsFile():
    stats_df = pd.read_csv('../data/2023FBSAdvanced.csv')

    teams_df = pd.read_csv('../data/Teams.csv')

    merged_df = pd.merge(stats_df, teams_df[['Conference', 'team_id', 'School']], left_on='School', right_on='School', how='left')

    merged_df['AP Rank'] = merged_df['AP Rank'].astype('int')

    merged_df = merged_df[stat_order]

    merged_df.to_csv('../data/Combined_2023_Team_Stats.csv', index=False)

def ChangeScheduleFile():
    schedule_df = pd.read_csv('../data/Training_Schedule.csv')

    team_df = pd.read_csv('../data/Teams.csv')

    schedule_df = schedule_df.merge(team_df, left_on='Team', right_on='Team', how='left')

    schedule_df['Team'] = schedule_df['team_id']

    schedule_df.drop(columns=['team_id', 'School', 'Conference'], inplace=True)

    team_df.rename(columns={'Team': 'Opponent'}, inplace=True)

    schedule_df = schedule_df.merge(team_df, left_on='Opponent', right_on='Opponent', how='left')

    schedule_df['Opponent'] = schedule_df['team_id'].fillna(-1).astype('int')

    schedule_df.drop(columns=['team_id', 'School', 'Conference'], inplace=True)

    schedule_df.drop(schedule_df[schedule_df['Opponent'] == -1].index, inplace=True)

    schedule_df.to_csv('../data/ID_Schedule.csv', index=False)

def AddStatsToSchedule():
    schedule_df = pd.read_csv('../data/ID_Schedule.csv')

    stats_df = pd.read_csv('../data/Combined_2023_Team_Stats.csv')

    stats_df.drop(columns=['Rk'], inplace=True)

    schedule_df = schedule_df.merge(stats_df, left_on='Team', right_on='team_id', how='left')

    schedule_df.dropna(subset=['Conference'], inplace=True)
    
    schedule_df.drop(columns=['School', 'team_id', 'Conference'], inplace=True) #Eventually add columns back in


    schedule_df['W'] = schedule_df['W'].astype('int')

    schedule_df['L'] = schedule_df['L'].astype('int')

    schedule_df['AP Rank'] = pd.to_numeric(schedule_df['AP Rank'], errors='coerce')

    schedule_df['AP Rank'] = schedule_df['AP Rank'].astype('Int64')

    schedule_df.to_csv('../data/Schedule_Stats.csv', index=True, index_label='game_id')

AddStatsToSchedule()