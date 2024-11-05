from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random_prediction, name="random_prediction"),
    path("random_forest_2023", views.random_forest_prediction, name="random_forest_2023"),
    path("chatgpt", views.chatgpt_prediction , name="chatgpt"),
    path("linear", views.linear_prediction, name="linear_prediction"),
    path("logistic", views.logistic_prediction, name="logistic_prediction"),
    path("get_teams", views.get_teams, name="get_teams")
]