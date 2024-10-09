import random

def random_prediction(home_team: str, away_team: str):
    
    # Home team is winner, away team is loser
    winner_name = home_team
    loser_name = away_team

    r = random.random()

    # Random chance to swap winner and loser
    if r >= 0.5:
        temp = winner_name
        winner_name = loser_name
        loser_name = temp

    # Random scores
    winner_score = round(r * 50)
    loser_score = round(r * 20)

    return (winner_name, loser_name, winner_score, loser_score)