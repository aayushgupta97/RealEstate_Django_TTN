from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'properties/properties.html')

def property(request, property_id):
    return render(request, 'properties/property.html')

def search(request):
    return render(request, 'properties/search.html')