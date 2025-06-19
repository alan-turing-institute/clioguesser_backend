import json
import os
import time

from azure.data.tables import TableClient
from azure.identity import DefaultAzureCredential
from django.contrib.gis.db.models.functions import AsGeoJSON
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from shapely.geometry import shape as shapely_shape

from .models import Cliopatria

STORAGE_ACCOUNT_NAME = (
    f"https://{os.getenv("DB_STORAGE_ACCOUNT_NAME")}.table.core.windows.net/"
)
TABLE_NAME = os.getenv("DB_TABL_NAME", "leaderboard")
TABLE_CLIENT = TableClient(
    endpoint=STORAGE_ACCOUNT_NAME,
    table_name=TABLE_NAME,
    credential=DefaultAzureCredential(),
)


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
    # Omit any rows where the "member_of" field is not empty or a blank string.
    rows = [row for row in rows if not row["member_of"]]
    shapes = list(rows)
    shapes = get_colours(shapes)
    content = {"shapes": shapes}
    return content


def get_colours(shapes):
    """
    Assign colours to shapes so that no two adjacent polygons share the same colour.
    If the number of colours is insufficient, add more.

    Args:
        shapes (list): A list of shape dictionaries.

    Returns:
        list: The list of shapes with added colour information.
    """
    base_colours = [
        "#008000",  # green
        "#40E0D0",  # turquoise
        "#FF0000",  # red
        "#FFFF00",  # yellow
        "#A52A2A",  # brown
        "#FFA500",  # orange
    ]
    # Convert GeoJSON to Shapely geometries
    geometries = [shapely_shape(json.loads(s["geom_json"])) for s in shapes]

    # Build adjacency list
    adjacency = [[] for _ in shapes]
    for i, geom1 in enumerate(geometries):
        for j in range(i + 1, len(geometries)):
            geom2 = geometries[j]
            if geom1.touches(geom2) or geom1.intersects(geom2):
                adjacency[i].append(j)
                adjacency[j].append(i)

    # Greedy colouring
    colours = base_colours.copy()
    assigned_colours = [None] * len(shapes)
    for i, neighbors in enumerate(adjacency):
        # Find used colours among neighbors
        used = set(
            assigned_colours[n] for n in neighbors if assigned_colours[n] is not None
        )
        # Find the first available colour
        for c in colours:
            if c not in used:
                assigned_colours[i] = c
                break
        else:
            # If all colours are used, add a new random colour
            import colorsys
            import random

            # Generate a new random colour
            while True:
                h = random.random()
                s = 0.7 + 0.3 * random.random()
                v = 0.7 + 0.3 * random.random()
                rgb = colorsys.hsv_to_rgb(h, s, v)
                hex_colour = "#%02x%02x%02x" % (
                    int(rgb[0] * 255),
                    int(rgb[1] * 255),
                    int(rgb[2] * 255),
                )
                if hex_colour not in colours:
                    colours.append(hex_colour)
                    assigned_colours[i] = hex_colour
                    break

    # Assign colours to shapes
    for i, shape in enumerate(shapes):
        shape["colour"] = assigned_colours[i]
    return shapes


@ratelimit(key="ip", rate="1000/h")
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
    # from .models import Leaderboard

    # leaderboard_entry, created = Leaderboard.objects.get_or_create(initials=initials)
    # if created or leaderboard_entry.score < score:
    #     leaderboard_entry.score = score
    #     leaderboard_entry.save()
    # TABLE_CLIENT.list_entities()
    for entry in TABLE_CLIENT.query_entities("initials eq ?", initials):
        if entry["score"] < score:
            entry["score"] = score
            TABLE_CLIENT.update_entity(entry, mode="MERGE")
            return

    previous = list(
        TABLE_CLIENT.query_entities(
            "RowKey eq @initials", parameters={"initials": "IAN"}
        )
    )
    if previous and previous[0]["score"] < score:
        previous[0]["score"] = score
        TABLE_CLIENT.update_entity(previous[0], mode="MERGE")
    else:
        # Create a new entry if it doesn't exist or the score is higher
        entity = {
            "PartitionKey": "my-partition",
            "RowKey": initials,
            "score": score,
        }
        TABLE_CLIENT.create_entity(entity)


@ratelimit(key="ip", rate="1000/h")
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
            return JsonResponse(
                {"error": "Missing 'initials' or 'score' parameter"}, status=400
            )

        try:
            score = int(score)
        except ValueError:
            return JsonResponse({"error": "'score' must be an integer"}, status=400)

        update_leaderboard(initials, score)

        return JsonResponse({"message": "Leaderboard updated successfully"})

    return JsonResponse(
        {"error": f"Invalid request method {request.method}"}, status=405
    )


def get_leaderboard():
    """
    Retrieve the current leaderboard entries, sorted by score in descending order.

    Returns:
        list: A list of dictionaries containing initials and scores.
    """

    # leaderboard_entries = Leaderboard.objects.all().order_by("-score")
    leaderboard_entries = TABLE_CLIENT.list_entities()
    return [
        {"initials": entry["RowKey"], "score": entry["score"]}
        for entry in sorted(leaderboard_entries, key=lambda x: x["score"], reverse=True)
    ]


@ratelimit(key="ip", rate="1000/h")
def leaderboard_api(request):
    """
    API endpoint to retrieve the leaderboard.

    Returns:
        JsonResponse: A response containing the leaderboard entries.
    """
    data = get_leaderboard()
    return JsonResponse({"leaderboard": data})


def calculate_score(min_year, max_year, true_year, guess_year, multiplier):
    """
    Calculate the score based on the difference between the true year and the guessed year.
    The score is calculated as the range of years (max_year - min_year) minus the absolute difference
    between the true year and the guessed year, multiplied by the multiplier, which will be less when
    the player has used hints.
    If the guessed year is outside the range, throw an error.

    Args:
        min_year (int): The minimum year of the range of years in the game.
        max_year (int): The maximum year of the range of years in the game.
        true_year (int): The year displayed in the game, which is the correct answer.
        guess_year (int): The guessed year by the player.
    Returns:
        int: The calculated score.
    """
    if guess_year < min_year or guess_year > max_year:
        raise ValueError("Guessed year is outside the valid range.")

    score = ((max_year - min_year) * multiplier) - (
        abs(true_year - guess_year) * multiplier
    )
    return score


@ratelimit(key="ip", rate="1000/h")
def get_score_api(request):
    """
    API endpoint to calculate the score based on the provided parameters.
    Expects 'min_year', 'max_year', 'true_year', and 'guess_year' as GET parameters.

    Returns:
        JsonResponse: A response containing the calculated score or an error message.
    """
    try:
        min_year = int(request.GET.get("min_year", 0))
        max_year = int(request.GET.get("max_year", 0))
        true_year = int(request.GET.get("true_year", 0))
        guess_year = int(request.GET.get("guess_year", 0))
        multiplier = int(request.GET.get("multiplier", 365))

        score = calculate_score(min_year, max_year, true_year, guess_year, multiplier)
        return JsonResponse({"score": score})

    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)


def leaderboard_event_stream():
    """
    Generator that yields the leaderboard as a server-sent event every 1 second.
    """
    while True:
        data = get_leaderboard()
        json_data = json.dumps(data)
        yield f"data: {json_data}\n\n"
        time.sleep(1)


@csrf_exempt
def leaderboard_stream_api(request):
    """
    SSE endpoint that continuously streams leaderboard data.
    """
    response = StreamingHttpResponse(
        leaderboard_event_stream(), content_type="text/event-stream"
    )
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"  # For nginx, ensures unbuffered streaming
    return response
