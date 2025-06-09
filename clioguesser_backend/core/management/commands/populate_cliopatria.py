import os
import json
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.core.management.base import BaseCommand
from django.db import connection
from core.models import Cliopatria
import re
import geopandas as gpd


class Command(BaseCommand):
    help = "Populates the database with Shapefiles"

    def add_arguments(self, parser):
        parser.add_argument("geojson_file", type=str, help="Path to the geojson file")

    def handle(self, *args, **options):
        # Ensure the file exists
        cliopatria_geojson_path = options["geojson_file"]
        if not os.path.exists(cliopatria_geojson_path):
            self.stdout.write(
                self.style.ERROR(f"File {cliopatria_geojson_path} does not exist")
            )
            return
        # Skip if already populated
        if Cliopatria.objects.exists():
            self.stdout.write(
                self.style.WARNING("Cliopatria table already populated — skipping.")
            )
            return

        # Load the Cliopatria shape dataset with JSON
        self.stdout.write(
            self.style.SUCCESS(
                f"Loading Cliopatria shape dataset from {cliopatria_geojson_path}..."
            )
        )
        with open(cliopatria_geojson_path) as f:
            cliopatria_data = json.load(f)
        gdf = gpd.read_file(cliopatria_geojson_path)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully loaded Cliopatria shape dataset from {cliopatria_geojson_path}"
            )
        )

        # Clear the Cliopatria table
        self.stdout.write(self.style.SUCCESS("Clearing Cliopatria table..."))
        Cliopatria.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Cliopatria table cleared"))

        self.stdout.write(self.style.SUCCESS("Determining polity start and end years..."))

        # Add a column called 'PolityStartYear' to the GeoDataFrame which is the minimum 'FromYear' of all shapes with the same 'Name'
        gdf['PolityStartYear'] = gdf.groupby('Name')['FromYear'].transform('min')

        # Add a column called 'PolityEndYear' to the GeoDataFrame which is the maximum 'ToYear' of all shapes with the same 'Name'
        gdf['PolityEndYear'] = gdf.groupby('Name')['ToYear'].transform('max')

        self.stdout.write(self.style.SUCCESS("Determined polity start and end years."))

        # Iterate through the data and create Cliopatria instances
        self.stdout.write(self.style.SUCCESS("Adding data to the database..."))
        for feature in cliopatria_data["features"]:
            properties = feature["properties"]
            properties['PolityStartYear'] = gdf.loc[gdf['Name'] == properties['Name'], 'PolityStartYear'].values[0]
            properties['PolityEndYear'] = gdf.loc[gdf['Name'] == properties['Name'], 'PolityEndYear'].values[0]

            # Generate DisplayName for each shape based on the 'Name' field
            properties["DisplayName"] = re.sub(r"[\[\]\(\)]", "", properties["Name"])

            # Ensure that polities where properties['MemberOf'] is not empty but the 'SeshatID' of the parent includes a ';' are ignored
            if properties["MemberOf"]:
                # Find the parent polity where "Name" is the same as the "MemberOf" value
                parent_polity = next(
                    (
                        f
                        for f in cliopatria_data["features"]
                        if f["properties"]["Name"] == properties["MemberOf"]
                    ),
                    None,
                )
                # If the parent polity exists and its 'SeshatID' includes a ';', then set 'MemberOf' to empty
                if parent_polity and ";" in parent_polity["properties"]["SeshatID"]:
                    properties["MemberOf"] = ""
                    self.stdout.write(
                        self.style.WARNING(
                            f"Updating Cliopatria instance for {properties['DisplayName']} ({properties['FromYear']} - {properties['ToYear']}) to have not be a member of anything, since it is a member of a Supra-polity"
                        )
                    )

            # Ignore Cliopatria Supra-polities since we will use the Seshat data to represent them
            if ";" not in properties["SeshatID"]:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Creating Cliopatria instance for {properties['DisplayName']} ({properties['FromYear']} - {properties['ToYear']})"
                    )
                )

                # Save geom and convert Polygon to MultiPolygon if necessary
                geom = GEOSGeometry(json.dumps(feature["geometry"]))
                if geom.geom_type == "Polygon":
                    geom = MultiPolygon(geom)

                Cliopatria.objects.create(
                    geom=geom,
                    name=properties["DisplayName"],
                    wikipedia_name=properties["Wikipedia"],
                    seshat_id=properties["SeshatID"],
                    area=properties["Area"],
                    start_year=properties["FromYear"],
                    end_year=properties["ToYear"],
                    polity_start_year=properties["PolityStartYear"],
                    polity_end_year=properties["PolityEndYear"],
                    components=properties["Components"],
                    member_of=properties["MemberOf"],
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully imported all data from {cliopatria_geojson_path}"
            )
        )

