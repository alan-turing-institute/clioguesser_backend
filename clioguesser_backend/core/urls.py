from django.urls import path

from .views import (
    get_score_api,
    leaderboard_api,
    leaderboard_stream_api,
    polities_for_year_api,
    update_leaderboard_api,
)

urlpatterns = [
    path("api/polities/", polities_for_year_api, name="polities_for_year_api"),
    path(
        "api/leaderboard/update/", update_leaderboard_api, name="update_leaderboard_api"
    ),
    path("api/leaderboard/", leaderboard_api, name="leaderboard_api"),
    path("api/score/", get_score_api, name="get_score_api"),
    path("api/leaderboard/stream/", leaderboard_stream_api),
]
