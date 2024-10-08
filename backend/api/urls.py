from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random_prediction, name="random_prediction"),
    path("random_forest_2023", views.random_forest_prediction, name="random_forest_2023")
]