from django.http import HttpResponse, JsonResponse
from django.db import connection

from api.methods.random_prediction import random_prediction as random_prediction_method
from api.methods.random_forest_prediction import random_forest_prediction as random_forest_prediction_method
from api.methods.chatgpt_prediction import chatgpt_prediction as chatgpt_prediction_method
from api.methods.linear_regression_prediction import linear_regression_prediction as linear_regression_prediction_method
from api.methods.logistic_regression_prediction import logistic_regression_prediction as logistic_regression_prediction_method
from api.helpers.get_end_of_season_standings import get_end_of_season_standings
from api.helpers.get_new_standings import get_new_standings
from api.helpers.get_team_by_id import get_team_by_id

end_of_season_standings = get_end_of_season_standings()
advanced_standings = get_new_standings()

def index(request):
    return HttpResponse("Index")

# Just randomly choose a winner and loser lol
def random_prediction(request):

    # Get home team param
    home_id = request.GET.get("home")

    # Get away team param
    away_id = request.GET.get("away")

    # Get teams by id
    home_team = get_team_by_id(home_id)
    away_team = get_team_by_id(away_id)

    # If a team id is invalid
    if not home_team or not away_team:
        return JsonResponse({
            "error": "Invalid team name"
        })

    # Make random prediction
    winner, loser, winner_score, loser_score = random_prediction_method(home_id, away_id)

    res = {
        "winner": winner,
        "loser": loser,
        "winner_score": winner_score,
        "loser_score": loser_score
    }

    return JsonResponse(res)

# Predict using random forest classifier model (first method we did)
def random_forest_prediction(request):
     # Get home team param
    home_id = request.GET.get("home").replace("_", " ")

    # Get away team param
    away_id = request.GET.get("away").replace("_", " ")

    # Get teams by id
    home_team = get_team_by_id(home_id)
    away_team = get_team_by_id(away_id)

    home_team_standing = None
    away_team_standing = None

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
        winner, loser, winner_score, loser_score = random_forest_prediction_method(home_team_standing, away_team_standing, home_id, away_id)

        res = {
            "winner": winner,
            "loser": loser,
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
    home_id = request.GET.get("home")

    # Get away team param
    away_id = request.GET.get("away")

    # Get teams by id
    home_team = get_team_by_id(home_id)
    away_team = get_team_by_id(away_id)

    # If a team id is invalid
    if not home_team or not away_team:
        return JsonResponse({
            "error": "Invalid team name"
        })

    # Make chatgpt prediction
    winner, loser, winner_score, loser_score, prediction_error = chatgpt_prediction_method(home_team, away_team, home_id, away_id)

    res = {
        "winner": winner,
        "loser": loser,
        "winner_score": winner_score,
        "loser_score": loser_score,
        "error": prediction_error
    }

    return JsonResponse(res)

# Predict use linear regression model
def linear_prediction(request):
    # Get home team param
    home_id = request.GET.get("home")

    # Get away team param
    away_id = request.GET.get("away")

    home_team_standing = None
    away_team_standing = None

    # Make sure team names are valid
    try:
        home_team_standing = advanced_standings[int(home_id)]
        away_team_standing = advanced_standings[int(away_id)]
    except:
        return JsonResponse({
            "error": "Invalid team name"
        })

    # Make chatgpt prediction
    winner, loser, winner_score, loser_score, prediction_error = linear_regression_prediction_method(home_team_standing, away_team_standing, home_id, away_id)

    res = {
        "winner": winner,
        "loser": loser,
        "winner_score": winner_score,
        "loser_score": loser_score,
        "error": prediction_error
    }

    return JsonResponse(res)

# Predict use logistic regression model
def logistic_prediction(request):
    # Get home team param
    home_id = request.GET.get("home")

    # Get away team param
    away_id = request.GET.get("away")

    home_team_standing = None
    away_team_standing = None

    # Make sure team names are valid
    try:
        home_team_standing = advanced_standings[int(home_id)]
        away_team_standing = advanced_standings[int(away_id)]
    except:
        return JsonResponse({
            "error": "Invalid team name"
        })

    # Make chatgpt prediction
    winner, loser, winner_score, loser_score, prediction_error = logistic_regression_prediction_method(home_team_standing, away_team_standing, home_id, away_id)

    res = {
        "winner": winner,
        "loser": loser,
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

# Returns all available prediction methods
def get_prediction_methods(request):
    return JsonResponse({
        "prediction_methods": [
            {
            "name": "Flip a Coin",
            "description": "a random prediction that is not based on any statistics",
            "path": "api/random"
        },
        {
            "name": "ChatGPT Prediction",
            "description": "utilize ChatGPT to predict the outcome of a game",
            "path": "api/chatgpt"
        },
        {
            "name": "Random Forest Model",
            "description": "a random forest model trained on season long statistics",
            "path": "api/random_forest_2023"
        },
        {
            "name": "Decision Tree Model",
            "description": "a decision tree model trained on season long statistics",
            "path": "api/random_forest_2023"
        },
        {
            "name": "Linear Regression Model",
            "description": "a linear regression model trained on season long statistics",
            "path": "api/linear"
        },
        {
            "name": "Logistic Regression Model",
            "description": "a logistic regression model trained on season long statistics",
            "path": "api/logistic"
        }
        ]
    })

# Returns all teams with ids and available prediciton methods (for frontend app initialization)
def get_settings(request):

    cursor = connection.cursor()

    # Select all teams
    cursor.execute("SELECT * FROM teams")

    # Get the actual rows
    teams = cursor.fetchall()

    return JsonResponse({
        "teams": teams,
        "prediction_methods": [
            {
            "name": "Flip a Coin",
            "description": "a random prediction that is not based on any statistics",
            "path": "api/random"
        },
        {
            "name": "ChatGPT Prediction",
            "description": "utilize ChatGPT to predict the outcome of a game",
            "path": "api/chatgpt"
        },
        {
            "name": "Random Forest Model",
            "description": "a random forest model trained on season long statistics",
            "path": "api/random_forest_2023"
        },
        {
            "name": "Decision Tree Model",
            "description": "a decision tree model trained on season long statistics",
            "path": "api/random_forest_2023"
        },
        {
            "name": "Linear Regression Model",
            "description": "a linear regression model trained on season long statistics",
            "path": "api/linear"
        },
        {
            "name": "Logistic Regression Model",
            "description": "a logistic regression model trained on season long statistics",
            "path": "api/logistic"
        }
        ]
    })