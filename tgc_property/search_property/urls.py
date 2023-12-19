from django.urls import path
from search_property import views

urlpatterns = [
    path('search/', views.search_by_area,name='search_by_area'),
    path('property/', views.search_property_by_area,name='search_property_by_area'),
    path('topproperty/', views.top_properties_by_margin,name='top_properties_by_margin'),
    path('property_id/', views.search_property_by_id,name='search_property_by_id'),
    path('topareaproperty/', views.top_property_by_ares,name='topareaproperty'),
]
