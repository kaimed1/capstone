from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("prediction-1", views.prediction_1, name="prediction_1"),\
    path("prediction-2", views.prediction_2, name="prediction_2"),
]