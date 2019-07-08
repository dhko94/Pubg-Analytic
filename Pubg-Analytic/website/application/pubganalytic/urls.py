from django.urls import path
from . import views

app_name = "pubganalytic"

urlpatterns = [
    path("pubganalyticHome/", views.pubganalyticHome, name="pubganalyticHome"),
    path("pubganalyticAdd/", views.pubganalyticAdd, name="pubganalyticAdd"),
    path("pubganalyticHome/<single_slug>", views.single_slug, name="single_slug"),
]
