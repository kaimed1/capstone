import joblib
import pandas as pd

def random_forest_prediction(home_team_standing, away_team_standing):

    # Load model and encoders
    model = joblib.load('./backend/data/trained_models/rf_model_1.pkl')
    encoders = joblib.load('./backend/data/trained_models/encoders.pkl')

    # Create a new game using the standings from last season
    new_game = home_team_standing.copy()
    new_game["Date"] = new_game["Date"]
    new_game["Day"] = new_game["Day"]
    new_game["Location"] = new_game["Location"]
    new_game["Conference"] = new_game["Conference"]
    new_game['Team'] = new_game['Team']
    new_game['PrevWeekBYE'] = new_game['PrevWeekBYE']
    new_game['RunningAvgScore'] = new_game['RunningAvgScore']
    new_game['Wins'] = new_game['Wins']
    new_game['Losses'] = new_game['Losses']
    new_game['Home_Win_Rate'] = new_game['Home_Win_Rate']
    new_game['Away_Win_Rate'] = new_game['Away_Win_Rate']
    new_game["Opponent"] = away_team_standing["Team"]
    new_game["Opponent_RunningAvgScore"] = away_team_standing["RunningAvgScore"]
    new_game["Opponent_Wins"] = away_team_standing["Wins"]
    new_game["Opponent_Losses"] = away_team_standing["Losses"]
    new_game["Opponent_Home_Win_Rate"] = away_team_standing["Home_Win_Rate"]
    new_game["Opponent_Away_Win_Rate"] = away_team_standing["Away_Win_Rate"]

    le_team = encoders['Team']
    le_opponent = encoders['Opponent']
    le_location = encoders['Location']

    new_game['Team_encoded'] = le_team.transform([new_game['Team']])[0]
    new_game['Opponent_encoded'] = le_opponent.transform([new_game['Opponent']])[0]
    new_game['Location_encoded'] = le_location.transform([new_game['Location']])[0]

    features = ['Team_encoded', 'Location_encoded', 'Opponent_encoded', 'PrevWeekBYE', 'Wins', 'Losses',
            'RunningAvgScore', 'Home_Win_Rate', 'Away_Win_Rate', 'Opponent_Wins', 'Opponent_Losses']
        
    new_game_df = pd.DataFrame([new_game], columns=features)
        
    predictions = model.predict(new_game_df)

    winner_name = new_game["Team"] if predictions[0] == 1 else new_game["Opponent"]
    loser_name = new_game["Opponent"] if predictions[0] == 1 else new_game["Team"]

    return (winner_name, loser_name, -1, -1)
