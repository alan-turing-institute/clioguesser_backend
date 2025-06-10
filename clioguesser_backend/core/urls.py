from django.urls import path
from .views import polities_for_year_api, update_leaderboard_api, leaderboard_api

urlpatterns = [
    path("api/polities/", polities_for_year_api, name="polities_for_year_api"),
    path("api/leaderboard/update/", update_leaderboard_api, name="update_leaderboard_api"),
    path("api/leaderboard/", leaderboard_api, name="leaderboard_api"),
]
