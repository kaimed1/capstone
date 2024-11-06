import random

def random_prediction(home_team: str, away_team: str):
    
    # Home team is winner, away team is loser
    winner = home_team
    loser = away_team

    r = random.random()

    # Random chance to swap winner and loser
    if r >= 0.5:
        temp = winner
        winner = loser
        loser = temp

    # Random scores
    winner_score = round(r * 50)
    loser_score = round(r * 20)

    # Return winner, loser, and fake scores
    return (winner, loser, winner_score, loser_score)