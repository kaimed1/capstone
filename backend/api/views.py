from django.http import HttpResponse, JsonResponse
from api.methods.random_prediction import random_prediction as random_prediction_method

def index(request):
    return HttpResponse("Index")


def random_prediction(request):

    # Get home team param
    home_team = request.GET.get("home")

    # Get away team param
    away_team = request.GET.get("away")

    winner_name, loser_name, winner_score, loser_score = random_prediction_method(home_team, away_team)

    res = {
        "winner_name": winner_name,
        "loser_name": loser_name,
        "winner_score": winner_score,
        "loser_score": loser_score
    }

    return JsonResponse(res)