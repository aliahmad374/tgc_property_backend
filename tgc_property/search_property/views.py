from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
from .models import Properties,Area
from .serializers import PropertiesSerializer,AreaSerializer
from rest_framework import status
from django.db.models import Q
from django.db.models import F
from django.db.models import FloatField, F, Value
from django.db.models.functions import Cast
from django.db.models import Count
@api_view(['GET'])
def search_by_area(request, *args, **kwargs):
    try:
        property_name = request.GET.get('property_name')
        if property_name!=None and len(property_name) > 1:
            property_name = property_name.replace('%20'," ")
            # Convert input property_name to lowercase for case-insensitive search
            property_name = property_name.lower()
            # Perform a case-insensitive search for property name in the database
            property_instance = Area.objects.filter(Q(neighbour__istartswith=property_name))
            if property_instance:
                # Serialize the property instance to retrieve its ID
                serializer = AreaSerializer(property_instance,many=True)
                return Response({'property_info': serializer.data},status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Property not found'},status=status.HTTP_200_OK)
        else:
            return Response({'message': 'missing property name or string must be of length 2'},status=status.HTTP_400_BAD_REQUEST)



    except:
        return Response({'error':'error'},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def search_property_by_area(request, *args, **kwargs):
    try:
        area_id = request.GET.get('area_id')
        if area_id!=None:

            # Perform a case-insensitive search for property name in the database
            property_instance = Properties.objects.filter(area_id=area_id).order_by(-F('margin'))
            if property_instance:
                # Serialize the property instance to retrieve its ID
                # serializer = PropertiesSerializer(property_instance,many=True)
                serialized_data = list(property_instance.values('id','title' ,'price','bedrooms','living_area','location','image_urls')) if property_instance else []
                return Response({'property_info': serialized_data},status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Property not found'},status=status.HTTP_200_OK)
        else:
            return Response({'message': 'missing area id'},status=status.HTTP_400_BAD_REQUEST)



    except:
        return Response({'error':'error'},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def top_properties_by_margin(request, *args, **kwargs):
    try:
        property_instance = Properties.objects.annotate(numeric_margin=Cast('margin', FloatField())).order_by('-numeric_margin')[:20]
        if property_instance:
            serialized_data = list(property_instance.values('id','title', 'price','bedrooms','living_area','location','image_urls')) if property_instance else []
            return Response({'property_info': serialized_data},status=status.HTTP_200_OK)

        else:
            return Response({'message': 'Property not found'},status=status.HTTP_200_OK)
        

    except:
        return Response({'error':'error'},status=status.HTTP_400_BAD_REQUEST)    
    
@api_view(['GET'])
def search_property_by_id(request, *args, **kwargs):
    try:
        property_id = request.GET.get('property_id')
        if property_id!=None:

            # Perform a case-insensitive search for property name in the database
            property_instance = Properties.objects.filter(id=property_id)
            if property_instance:
                # Serialize the property instance to retrieve its ID
                serializer = PropertiesSerializer(property_instance,many=True)
                return Response({'property_info': serializer.data},status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Property not found'},status=status.HTTP_200_OK)
        else:
            return Response({'message': 'missing property id'},status=status.HTTP_400_BAD_REQUEST)



    except:
        return Response({'error':'error'},status=status.HTTP_400_BAD_REQUEST)    
    

@api_view(['GET'])
def top_property_by_ares(request, *args, **kwargs):
    try:
        # Assuming your model name is Property and the field name is area_id
        query_result = Properties.objects.values('area_id').annotate(repetitions=Count('area_id')).order_by('-repetitions')[:16]
        return Response({'property_info': [ {'area_id':v['area_id']} for v in query_result]},status=status.HTTP_200_OK)
    except Exception as E:
        print(E)
        return Response({'error':'error'},status=status.HTTP_400_BAD_REQUEST)         