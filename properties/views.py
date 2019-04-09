from django.shortcuts import render
from django.http import HttpResponse
from .models import Property

# Create your views here.


def index(request):
    listings = Property.objects.all()
    context = {
        'listings': listings,
    }
    return render(request, 'properties/properties.html', context)


def property_single_listing(request, property_id):
    return render(request, 'properties/property.html')


def search(request):
    return render(request, 'properties/search.html')