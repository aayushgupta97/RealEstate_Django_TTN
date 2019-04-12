from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name="properties"),
    path('<int:property_id>', views.property_single_listing, name="property"),
    path('search/', views.search, name="search"),
    path('add/', views.add_property, name="add_property"),

]

