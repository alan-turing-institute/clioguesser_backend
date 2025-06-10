from django.contrib.gis.db.models.functions import AsGeoJSON
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cliopatria

def get_polities_for_year(displayed_year):
    """
    This function returns the polity geoms for a given year for the map.

    Args:
        displayed_year (int): The year to display the polities for.

    Returns:
        dict: The content for the polity shapes.
    """
    # rows = Cliopatria.objects.filter(
    #     polity_start_year__lte=displayed_year, polity_end_year__gte=displayed_year
    # )

    # We only want shapes that are active in the displayed year
    rows = Cliopatria.objects.filter(
        start_year__lte=displayed_year, end_year__gte=displayed_year
    )

    # Convert 'geom' to GeoJSON in the database query
    rows = rows.annotate(geom_json=AsGeoJSON("geom"))
    # Filter the rows to return
    rows = rows.values(
        "id",
        "seshat_id",  # Can use this for querying the Seshat database
        "name",
        "start_year",
        "end_year",
        "polity_start_year",
        "polity_end_year",
        "area",
        "geom_json",
        "components",
        "member_of",
        "wikipedia_name",
    )
    shapes = list(rows)
    content = {
        "shapes": shapes
    }
    return content


def polities_for_year_api(request):
    year = request.GET.get("year")
    if year is None:
        return JsonResponse({"error": "Missing 'year' parameter"}, status=400)
    try:
        year = int(year)
    except ValueError:
        return JsonResponse({"error": "'year' must be an integer"}, status=400)
    data = get_polities_for_year(year)
    return JsonResponse(data)


def update_leaderboard(initials, score):
    """
    Update the leaderboard with a new score for the given initials.
    If the initials already exist, update the score if the new score is higher.
    If not, create a new entry.

    Args:
        initials (str): The player's initials.
        score (int): The player's score.
    """
    from .models import Leaderboard

    leaderboard_entry, created = Leaderboard.objects.get_or_create(initials=initials)
    if created or leaderboard_entry.score < score:
        leaderboard_entry.score = score
        leaderboard_entry.save()


@csrf_exempt
def update_leaderboard_api(request):
    """
    API endpoint to update the leaderboard with a new score.
    Expects 'initials' and 'score' as POST parameters.

    Returns:
        JsonResponse: A response indicating success or failure.
    """
    if request.method == "POST":
        initials = request.POST.get("initials")
        score = request.POST.get("score")

        if not initials or not score:
            return JsonResponse({"error": "Missing 'initials' or 'score' parameter"}, status=400)

        try:
            score = int(score)
        except ValueError:
            return JsonResponse({"error": "'score' must be an integer"}, status=400)

        update_leaderboard(initials, score)
        return JsonResponse({"message": "Leaderboard updated successfully"})

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_leaderboard():
    """
    Retrieve the current leaderboard entries, sorted by score in descending order.

    Returns:
        list: A list of dictionaries containing initials and scores.
    """
    from .models import Leaderboard

    leaderboard_entries = Leaderboard.objects.all().order_by("-score")
    return [{"initials": entry.initials, "score": entry.score} for entry in leaderboard_entries]


def leaderboard_api(request):
    """
    API endpoint to retrieve the leaderboard.

    Returns:
        JsonResponse: A response containing the leaderboard entries.
    """
    data = get_leaderboard()
    return JsonResponse({"leaderboard": data})
