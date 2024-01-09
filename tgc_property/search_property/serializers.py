from rest_framework import serializers

from .models import Properties,Area,location


class PropertiesSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Properties
        fields = '__all__'
class AreaSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Area
        fields = ['area_id','neighbour']

class LocationSerializer(serializers.ModelSerializer): 
    class Meta:
        model=location
        fields = ['location_id','location_name']        