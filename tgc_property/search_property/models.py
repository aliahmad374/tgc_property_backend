from django.db import models
from django.utils import timezone

class Area(models.Model):
    area_id = models.AutoField(primary_key=True)
    neighbour = models.TextField()
    class Meta:
        managed = False
        db_table = 'area'

class location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_name = models.TextField()
    class Meta:
        managed = False
        db_table = 'location'        

class Properties(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    location = models.ForeignKey(location, on_delete=models.CASCADE)
    property_detail = models.TextField()
    characteristics = models.TextField()
    title = models.TextField()
    location_property = models.TextField()
    neighbours = models.TextField()
    image_urls = models.TextField()
    living_space = models.TextField()
    bedrooms = models.TextField()
    price = models.TextField()
    house_type = models.TextField()
    construction_type = models.TextField()
    construction_year = models.TextField()
    roof_type = models.TextField()
    plot_area = models.TextField()
    contents = models.TextField()
    living_area = models.TextField()
    external_storage_space = models.TextField()
    energy_label = models.TextField()
    insulation = models.TextField()
    heating = models.TextField()
    warm_water = models.TextField()
    cv_ketel = models.TextField()
    Buitenruimte_location = models.TextField()
    garden = models.TextField()
    backyard = models.TextField()
    location_of_garden = models.TextField()
    neighbourhood_facilities = models.TextField()
    price_per_mSq = models.TextField()
    asking_price = models.TextField()
    url = models.TextField()
    price_per_meter_sq_on_plotcore = models.TextField()
    phone_number = models.TextField()
    is_good_property = models.TextField()
    margin = models.TextField()
    date_time = models.DateTimeField(default=timezone.now)
    status_property = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'properties'


