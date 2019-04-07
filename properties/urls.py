from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name="properties"),
    path('<int:property_id>', views.property, name="property"),
    path('search/', views.search, name="search"),
]
