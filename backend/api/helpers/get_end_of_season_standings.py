import pandas as pd

def get_end_of_season_standings():
    df = pd.read_csv('./backend/data/Training_Schedule.csv')

    standings_df = {}

    current_team = df.iloc[0]["Team"]

    for i, r in df.iterrows():
        if df.iloc[i]["Team"] != current_team:
            standings_df[current_team] = df.iloc[i - 1]
            current_team = df.iloc[i]["Team"]
            

    return standings_df