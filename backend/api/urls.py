from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random_prediction, name="random_prediction"),
    path("random_forest", views.random_forest_prediction, name="random_forest"),
    path("decision_tree", views.decision_tree_prediction, name="decision_tree"),
    path("chatgpt", views.chatgpt_prediction , name="chatgpt"),
    path("linear", views.linear_prediction, name="linear_prediction"),
    path("logistic", views.logistic_prediction, name="logistic_prediction"),
    path("get_teams", views.get_teams, name="get_teams"),
    path("get_prediction_methods", views.get_prediction_methods, name="get_prediction_methods"),
    path("get_settings", views.get_settings, name="get_settings")
]