from django.http import HttpResponse


def index(request):
    return HttpResponse("Index")

def prediction_1(request):
    return HttpResponse("Prediction method 1")

def prediction_2(request):
    return HttpResponse("Prediction method 2")