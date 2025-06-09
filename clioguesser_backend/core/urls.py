from django.urls import path
from .views import polities_for_year_api

urlpatterns = [
    path("api/polities/", polities_for_year_api, name="polities_for_year_api"),
]