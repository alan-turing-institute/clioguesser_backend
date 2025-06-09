from django.db import models
from django.contrib.gis.db import models as geomodels

class Cliopatria(models.Model):
    """
    Model representing Cliopatria polity borders dataset.
    """

    id = models.AutoField(primary_key=True)
    geom = geomodels.MultiPolygonField()
    simplified_geom = geomodels.MultiPolygonField()
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