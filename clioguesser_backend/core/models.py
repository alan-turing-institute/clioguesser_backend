from django.db import models
from django.contrib.gis.db import models as geomodels

class Cliopatria(models.Model):
    """
    Model representing Cliopatria polity borders dataset.
    """

    id = models.AutoField(primary_key=True)
    geom = geomodels.MultiPolygonField()
    # simplified_geom = geomodels.MultiPolygonField()
    name = models.CharField(max_length=100)
    wikipedia_name = models.CharField(max_length=100, null=True)
    seshat_id = models.CharField(max_length=100)
    area = models.FloatField()
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    polity_start_year = models.IntegerField()
    polity_end_year = models.IntegerField()
    components = models.CharField(max_length=500, null=True)
    member_of = models.CharField(max_length=500, null=True)

    def __str__(self):
        return "Name: %s" % self.name
    
class Leaderboard(models.Model):
    """
    Model representing an arcade style leaderboard entry.
    Each entry corresponds to a player's score and initials.
    """

    initials = models.CharField(max_length=3, unique=True, primary_key=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.initials}: {self.score}"