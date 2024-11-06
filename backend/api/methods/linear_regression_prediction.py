import joblib
import pandas as pd

def linear_regression_prediction(home_team_standing, away_team_standing, home_id, away_id):

    # Load model and encoders from model trained
    model = joblib.load('./backend/data/trained_models/linear_regression_model.pkl')

    # Difference of stats
    new_game = home_team_standing.values - away_team_standing.values

    # Predict new game
    predictions = model.predict([new_game])

    # 1 => home team wins, 0 => home team loses
    result = (predictions[0] > 0.47).astype(int)

    winner = home_id if result == 1 else away_id
    loser = away_id if result == 1 else home_id

    return winner, loser, -1, -1, None