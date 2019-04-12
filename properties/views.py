from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.contrib import messages
from .models import Property
from .choices import state_choices, price_choices, bedroom_choices
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
    queryset_list = Property.objects.order_by('-list_date')
    #keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    #city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
            # queryset_list = queryset_list.filter(city__iexact=city)

    # state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms).order_by('-bedrooms')

    # price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price).order_by('-price')

    context = {
        'bedroom_choices': bedroom_choices,
        'state_choices': state_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET
    }

    return render(request, 'properties/search.html', context)

def add_property(request):
    context = {
        'state_choices': state_choices,
    }


    if request.method == "POST":
        seller = request.POST['seller_id']
        title = request.POST['title']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        description = request.POST['description']
        price = request.POST['price']
        bedrooms = request.POST['bedrooms']
        bathrooms = request.POST['bathrooms']
        garage = request.POST['garage']
        square_ft = request.POST['square_ft']
        lot_size = request.POST['lot_size']
        photo_main = request.FILES['photo_main']
        photo_1 = request.FILES.get('photo_1', '')
        photo_2 = request.FILES.get('photo_2', '')
        photo_3 = request.FILES.get('photo_3', '')
        photo_4 = request.FILES.get('photo_4', '')
        photo_5 = request.FILES.get('photo_5', '')
        photo_6 = request.FILES.get('photo_6', '')
        # photo_2 = request.FILES.get['photo_2']
        # photo_3 = request.FILES.get['photo_3']
        # photo_4 = request.FILES.get['photo_4']
        # photo_5 = request.FILES.get['photo_5']
        # photo_6 = request.FILES.get['photo_6']
        new_property = Property(seller_id=seller, title=title, address=address, city=city, state=state,
                                zip_code=zip_code, description=description, price=price,
                                bedrooms=bedrooms, bathrooms=bathrooms, garage=garage,
                                square_ft=square_ft, lot_size=lot_size, photo_main=photo_main,
                                photo_1=photo_1, photo_2=photo_2, photo_3=photo_3, photo_4=photo_4,
                                photo_5=photo_5, photo_6=photo_6)
        new_property.save()
        messages.success(request, 'Your new property has been posted successfully')
        return redirect('index')

    else:
        return render(request, 'properties/add_property.html', context)