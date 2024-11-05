import pandas as pd
import joblib

def decision_tree_prediction(home_team, away_team, home_id, away_id):
    '''
    :param home_team: String team playing at home
    :param away_team: String team playing away
    :return: the winner and loser team with the predicted score
    '''

    # Load model and encoders from model trained
    model = joblib.load('./backend/data/trained_models/dt_model_1.pkl')
    encoders = joblib.load('./backend/data/trained_models/dt_encoders.pkl')

    # Create a new game using the standings from last season for both of the teams
    new_game = home_team.copy()
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
    new_game["Opponent"] = away_team["Team"]
    new_game["Opponent_RunningAvgScore"] = away_team["RunningAvgScore"]
    new_game["Opponent_Wins"] = away_team["Wins"]
    new_game["Opponent_Losses"] = away_team["Losses"]
    new_game["Opponent_Home_Win_Rate"] = away_team["Home_Win_Rate"]
    new_game["Opponent_Away_Win_Rate"] = away_team["Away_Win_Rate"]

    # Load from encoders variable
    le_team = encoders['Team']
    le_opponent = encoders['Opponent']
    le_location = encoders['Location']

    new_game['Team_encoded'] = le_team.transform([new_game['Team']])[0]
    new_game['Opponent_encoded'] = le_opponent.transform([new_game['Opponent']])[0]
    new_game['Location_encoded'] = le_location.transform([new_game['Location']])[0]

    # Attributes used in prediction
    features = ['Team_encoded', 'Location_encoded', 'Opponent_encoded', 'PrevWeekBYE', 'Wins', 'Losses',
                'RunningAvgScore', 'Home_Win_Rate', 'Away_Win_Rate', 'Opponent_Wins', 'Opponent_Losses']

    # Create a pandas dataframe for the game
    new_game_df = pd.DataFrame([new_game], columns=features)

    # Make prediction
    predictions = model.predict(new_game_df)

    #Assign winner and loser based on model prediction
    winner = home_id if predictions[0] == 1 else away_id
    loser = away_id if predictions[0] == 1 else home_id

    # Return winner and loser (-1 for the scores because this is not yet being used)
    return winner, loser, -1, -1