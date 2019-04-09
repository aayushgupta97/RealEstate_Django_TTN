from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from .models import Property

# Create your views here.


def index(request):
    listings = Property.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)


    context = {
        'listings': paged_listings,
    }
    return render(request, 'properties/properties.html', context)


def property_single_listing(request, property_id):
    listing = get_object_or_404(Property, pk=property_id)
    context = {
        'listing': listing
    }
    return render(request, 'properties/property.html', context)


def search(request):
    return render(request, 'properties/search.html')