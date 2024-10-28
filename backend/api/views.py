from django.http import HttpResponse, JsonResponse
from django.db import connection

from api.methods.random_prediction import random_prediction as random_prediction_method
from api.methods.random_forest_prediction import random_forest_prediction as random_forest_prediction_method
from api.methods.chatgpt_prediction import chatgpt_prediction as chatgpt_prediction_method
from api.helpers.get_end_of_season_standings import get_end_of_season_standings

end_of_season_standings = get_end_of_season_standings()

def index(request):
    return HttpResponse("Index")

# Just randomly choose a winner and loser lol
def random_prediction(request):

    # Get home team param
    home_team = request.GET.get("home")

    # Get away team param
    away_team = request.GET.get("away")

    # Make random prediction
    winner_name, loser_name, winner_score, loser_score = random_prediction_method(home_team, away_team)

    res = {
        "winner_name": winner_name,
        "loser_name": loser_name,
        "winner_score": winner_score,
        "loser_score": loser_score
    }

    return JsonResponse(res)

# Predict using random forest classifier model (first method we did)
def random_forest_prediction(request):
     # Get home team param
    home_team = request.GET.get("home").replace("_", " ")

    # Get away team param
    away_team = request.GET.get("away").replace("_", " ")

    home_team_standing = ""
    away_team_standing = ""

    # Make sure team names are valid
    try:
        home_team_standing = end_of_season_standings[home_team]
        away_team_standing = end_of_season_standings[away_team]
    except:
        return JsonResponse({
            "error": "Invalid team name"
        })
    
    try:

        # Make prediction using RF1 model
        winner_name, loser_name, winner_score, loser_score = random_forest_prediction_method(home_team_standing, away_team_standing)

        res = {
            "winner_name": winner_name,
            "loser_name": loser_name,
            "winner_score": winner_score,
            "loser_score": loser_score,
            "error": None
        }
        
        return JsonResponse(res)
    except:
        return JsonResponse({
            "error": "Error occured when predicting game outcome"
        })

# Predict using chatgpt
def chatgpt_prediction(request):
    # Get home team param
    home_team = request.GET.get("home")

    # Get away team param
    away_team = request.GET.get("away")

    # Make chatgpt prediction
    winner_name, loser_name, winner_score, loser_score, prediction_error = chatgpt_prediction_method(home_team, away_team)

    res = {
        "winner_name": winner_name,
        "loser_name": loser_name,
        "winner_score": winner_score,
        "loser_score": loser_score,
        "error": prediction_error
    }

    return JsonResponse(res)

# Returns all teams with ids
def get_teams(request):
    cursor = connection.cursor()

    # Select all teams
    cursor.execute("SELECT * FROM teams")

    # Get the actual rows
    teams = cursor.fetchall()
    
    return JsonResponse({
        'teams': teams
    })