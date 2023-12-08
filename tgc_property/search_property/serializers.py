from rest_framework import serializers

from .models import Properties,Area


class PropertiesSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Properties
        fields = '__all__'
class AreaSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Area
        fields = ['area_id','neighbour']