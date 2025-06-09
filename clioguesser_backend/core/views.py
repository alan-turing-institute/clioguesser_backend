from django.contrib.gis.db.models.functions import AsGeoJSON
from django.http import JsonResponse
from .models import Cliopatria

def get_polities_for_year(displayed_year):
    """
    This function returns the polity geoms for a given year for the map.

    Args:
        displayed_year (int): The year to display the polities for.

    Returns:
        dict: The content for the polity shapes.
    """
    rows = Cliopatria.objects.filter(
        polity_start_year__lte=displayed_year, polity_end_year__gte=displayed_year
    )

    # Convert 'geom' to GeoJSON in the database query
    rows = rows.annotate(geom_json=AsGeoJSON("geom"))
    # Filter the rows to return
    rows = rows.values(
        # "id",
        "seshat_id",  # Can use this for querying the Seshat database
        "name",
        # "start_year",
        # "end_year",
        "polity_start_year",
        "polity_end_year",
        # "area",
        "geom_json",
        # "components",
        # "member_of",
        # "wikipedia_name",
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
