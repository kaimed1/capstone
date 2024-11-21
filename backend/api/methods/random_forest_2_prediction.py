import joblib
import pandas as pd

def random_forest_2_prediction(home_team_standing, away_team_standing, home_id, away_id):

    # Load model and encoders from model trained
    model = joblib.load('./backend/data/trained_models/random_forest_model_v2.pkl')

    # Difference of stats
    new_game = home_team_standing.values - away_team_standing.values

    # Predict new game
    predictions = model.predict([new_game])

    # Determine winner and loser 
    winner = home_id if predictions[0] == 1 else away_id
    loser = away_id if predictions[0] == 1 else home_id

    return winner, loser, -1, -1, None