import pandas as pd

# Get the end of season stats for each team (no duplicates)
def get_end_of_season_standings():
    # Load the training data
    df = pd.read_csv('./backend/data/Training_Schedule_RF1.csv')

    standings_df = {}

    current_team = df.iloc[0]["Team"]

    # Go throught all games in training schedule
    # It's sorted by teams so keep last game each 
    # team played to get their stats for the end of the season
    for i, r in df.iterrows():
        if df.iloc[i]["Team"] != current_team:
            standings_df[current_team] = df.iloc[i - 1]
            current_team = df.iloc[i]["Team"]
            

    return standings_df