from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.
from .models import Properties,Area,location
from .serializers import PropertiesSerializer,AreaSerializer,LocationSerializer
from rest_framework import status
from django.db.models import Q
from django.db.models import F
from django.db.models import FloatField, F, Value
from django.db.models.functions import Cast
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@api_view(['GET'])
def search_by_area(request, *args, **kwargs):
    try:
        property_name = request.GET.get('property_name')
        # location_name = request.GET.get('location_name')
        if property_name!=None:
            if property_name!=None and len(property_name) > 1:
                property_name = property_name.replace('%20'," ")
                location_name = property_name.replace('%20'," ")
                # Convert input property_name to lowercase for case-insensitive search
                property_name = property_name.lower()
                location_name = location_name.lower()
                # Perform a case-insensitive search for property name in the database
                property_instance = Area.objects.filter(Q(neighbour__istartswith=property_name))
                location_instance = location.objects.filter(Q(location_name__istartswith=location_name))
                if property_instance or location_instance:
                    # Serialize the property instance to retrieve its ID
                    serializer_property = AreaSerializer(property_instance,many=True)
                    serializer_location = LocationSerializer(location_instance,many=True)

                    return Response({'property_info': serializer_property.data+serializer_location.data},status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Property not found'},status=status.HTTP_200_OK)
            else:
                return Response({'message': 'missing property name or string must be of length 2'},status=status.HTTP_400_BAD_REQUEST)
        # if location_name !=None:
        #     if location_name!=None and len(location_name) > 1:
        #         location_name = location_name.replace('%20'," ")
        #     # Convert input property_name to lowercase for case-insensitive search
        #     location_name = location_name.lower()
        #     # Perform a case-insensitive search for property name in the database
        #     property_instance = location.objects.filter(Q(location_name__istartswith=location_name))
        #     if property_instance:
        #         # Serialize the property instance to retrieve its ID
        #         serializer = LocationSerializer(property_instance,many=True)
        #         return Response({'property_info': serializer.data},status=status.HTTP_200_OK)
        #     else:
        #         return Response({'message': 'Property not found'},status=status.HTTP_200_OK)
        # else:
        #     return Response({'message': 'missing location name or string must be of length 2'},status=status.HTTP_400_BAD_REQUEST)





    except Exception as E:
        print(E)
        return Response({'error':'error'},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def search_property_by_area(request, *args, **kwargs):
    try:
        area_id = request.GET.get('area_id')
        location_id = request.GET.get('location_id')
        bedrooms = request.GET.get('beds')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        min_area = request.GET.get('min_area')
        max_area = request.GET.get('max_area')
        
        if area_id!=None:
            filters = {'area_id':area_id}
            if bedrooms!=None:
                filters['bedrooms']=bedrooms
            if min_price!=None and max_price!=None:
                filters['price__gte'] = min_price
                filters['price__lte'] = max_price
            if min_area!=None and max_area!=None:
                filters['living_area__gte'] = min_area
                filters['living_area__lte'] = max_area

            # Perform a case-insensitive search for property name in the database
            property_instance = Properties.objects.filter(**filters).order_by(-F('margin'))
            paginator = Paginator(property_instance, 10)  # Number of items per page
            page = request.GET.get('page')
            try:
                properties = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                properties = paginator.page(1)
            except EmptyPage:
                # If page is out of range, deliver last page of results.
                properties = paginator.page(paginator.num_pages)

            if properties:
                serialized_data = PropertiesSerializer(properties, many=True).data
                # Serialize the property instance to retrieve its ID
                return Response({'property_info': serialized_data,'total_count':len(property_instance)},status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Property not found'},status=status.HTTP_200_OK)
        
        elif location_id!=None:

            filters = {'location_id':location_id}
            if bedrooms!=None:
                filters['bedrooms']=bedrooms
            if min_price!=None and max_price!=None:
                filters['price__gte'] = min_price
                filters['price__lte'] = max_price
            if min_area!=None and max_area!=None:
                filters['living_area__gte'] = min_area
                filters['living_area__lte'] = max_area

            # Perform a case-insensitive search for property name in the database
            property_instance = Properties.objects.filter(**filters).order_by(-F('margin'))
            paginator = Paginator(property_instance, 10)  # Number of items per page
            page = request.GET.get('page')
            try:
                properties = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                properties = paginator.page(1)
            except EmptyPage:
                # If page is out of range, deliver last page of results.
                properties = paginator.page(paginator.num_pages)

            if properties:
                serialized_data = PropertiesSerializer(properties, many=True).data
                # Serialize the property instance to retrieve its ID
                return Response({'property_info': serialized_data,'total_count':len(property_instance)},status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Property not found'},status=status.HTTP_200_OK)
        else:
            return Response({'message': 'missing area or location id'},status=status.HTTP_400_BAD_REQUEST)



    except Exception as E:
        print(E)
        return Response({'error':'error'},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def top_properties_by_margin(request, *args, **kwargs):
    try:
        property_instance = Properties.objects.annotate(numeric_margin=Cast('margin', FloatField())).filter(status_property=0).order_by('-numeric_margin')
        paginator = Paginator(property_instance, 20)  # Number of items per page
        page = request.GET.get('page')
        try:
            properties = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            properties = paginator.page(1)
        except EmptyPage:
            # If page is out of range, deliver last page of results.
            properties = paginator.page(paginator.num_pages)

        if properties:
            # serialized_data = list(properties.values('id','title', 'price','bedrooms','living_area','location_property','image_urls')) if properties else []
            serialized_data = PropertiesSerializer(properties, many=True)
            filtered_data = [{'id': item['id'], 'title': item['title'], 'price': item['price'],
                      'bedrooms': item['bedrooms'], 'living_area': item['living_area'],
                      'location_property': item['location_property'], 'image_urls': item['image_urls'],'price_per_meter_sq_on_plotcore':item['price_per_meter_sq_on_plotcore'],'price_per_mSq':item['price_per_mSq'],'status_property':item['status_property'],'date_time':item['date_time']}
                     for item in serialized_data.data]
            return Response({'property_info': filtered_data,'total_count':len(property_instance)},status=status.HTTP_200_OK)

        else:
            return Response({'message': 'Property not found'},status=status.HTTP_200_OK)
        

    except Exception as E:
        print(E)
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
        # Extract area_id values from the result
        top_area_ids = [area['area_id'] for area in query_result]        
        top_properties = Area.objects.filter(area_id__in=top_area_ids).values('area_id', 'neighbour')

        return Response({'property_info': top_properties},status=status.HTTP_200_OK)
    except Exception as E:
        print(E)
        return Response({'error':'error'},status=status.HTTP_400_BAD_REQUEST)
    

    

@api_view(['GET'])
def search_property_by_location(request, *args, **kwargs):
    try:
        location_id = request.GET.get('location_id')
        bedrooms = request.GET.get('beds')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        min_area = request.GET.get('min_area')
        max_area = request.GET.get('max_area')
        
        if location_id!=None:
            filters = {'area_id':location_id}
            if bedrooms!=None:
                filters['bedrooms']=bedrooms
            if min_price!=None and max_price!=None:
                filters['price__gte'] = min_price
                filters['price__lte'] = max_price
            if min_area!=None and max_area!=None:
                filters['living_area__gte'] = min_area
                filters['living_area__lte'] = max_area

            # Perform a case-insensitive search for property name in the database
            property_instance = Properties.objects.filter(**filters).order_by(-F('margin'))
            paginator = Paginator(property_instance, 10)  # Number of items per page
            page = request.GET.get('page')
            try:
                properties = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                properties = paginator.page(1)
            except EmptyPage:
                # If page is out of range, deliver last page of results.
                properties = paginator.page(paginator.num_pages)

            if properties:
                serialized_data = PropertiesSerializer(properties, many=True).data
                # Serialize the property instance to retrieve its ID
                return Response({'property_info': serialized_data,'total_count':len(property_instance)},status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Property not found'},status=status.HTTP_200_OK)
        else:
            return Response({'message': 'missing area id'},status=status.HTTP_400_BAD_REQUEST)



    except Exception as E:
        print(E)
        return Response({'error':'error'},status=status.HTTP_400_BAD_REQUEST)    


@api_view(['GET'])
def top_property_by_location(request, *args, **kwargs):
    try:
        # Assuming your model name is Property and the field name is area_id
        query_result = Properties.objects.values('location_id').annotate(repetitions=Count('location_id')).order_by('-repetitions')[:16]
        # Extract area_id values from the result
        top_area_ids = [area['location_id'] for area in query_result]        
        top_properties = location.objects.filter(location_id__in=top_area_ids).values('location_id', 'location_name')

        return Response({'property_info': top_properties},status=status.HTTP_200_OK)
    except Exception as E:
        print(E)
        return Response({'error':'error'},status=status.HTTP_400_BAD_REQUEST)