import joblib
import pandas as pd


def logistic_regression_prediction(home_team_standing, away_team_standing, home_id, away_id):

    # Load model and encoders from model trained
    model = joblib.load('./backend/data/trained_models/logistic_regression_model.pkl')

    # Need to drop teams ids and opponent ids
    fixed_home_team = home_team_standing.drop("Team")
    fixed_home_team = fixed_home_team.drop("Opponent")
    fixed_away_team = away_team_standing.drop("Team")
    fixed_away_team = fixed_away_team.drop("Opponent")

    # Difference of stats
    new_game = fixed_home_team.values - fixed_away_team.values

    # Predict new game
    predictions = model.predict([new_game])

    # 1 => home team wins, 0 => home team loses
    result = (predictions[0] > 0.47).astype(int)

    winner = home_id if result == 1 else away_id
    loser = away_id if result == 1 else home_id

    return winner, loser, -1, -1, None