from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import Property
from .choices import state_choices, price_choices, bedroom_choices


def index(request):
    """
    renders the page with all the property listings in the database passed into a paginator.
    only the published properties are listed here and sorted by list date descending.
    :param request:
    :return: HttpResponse renders the properties page
    """
    listings = Property.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings,
    }
    return render(request, 'properties/properties.html', context)


def property_single_listing(request, property_id):
    """
    renders the single listing page when a user clicks on More info for any listing. if the passes in id of the
    listing doesn't exist, a 404 error is thrown.
    :param request:
    :param property_id: unique id passed to identify any single listing
    :return: HttpResponse renders single property page
    """
    listing = get_object_or_404(Property, pk=property_id)
    context = {
        'listing': listing
    }
    return render(request, 'properties/property.html', context)


def search(request):
    """
    searches the database for any available property with matching criteria. can be called from the homepage or
    the search page.
    :param request:
    :return: HttpResponse renders the search page
    """
    queryset_list = Property.objects.order_by('-list_date')
    # keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # city
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
    """
    adds a new property with the form values under the authenticated seller. only an authenticated seller can add
    a new property
    :param request:
    :return: HttpResponse renders the add new property form
    """
    context = {
        'state_choices': state_choices,
    }
    if request.user.is_authenticated:
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
    else:
        messages.error(request, "you are not authenticated to visit this page.")
        return redirect('index')


def delete_property(request, property_id):
    """
    deletes the property from the database with the passed in property_id. Only the authenticated seller who
    created the property can delete the property
    :param request:
    :param property_id: unique id to identify properties
    :return: HttpResponse renders back to dashboard with error or success message
    """
    property_listing = get_object_or_404(Property, id=property_id)
    seller = property_listing.seller.username

    if request.user.is_authenticated and request.user.username == seller:
        property_listing.delete()
        messages.success(request, "Post Successfully Deleted!")
        return redirect('dashboard')
    else:
        messages.error(request, "Cannot delete this property")
        return redirect('dashboard')


def delete_property_confirmation(request, property_id):
    """
    takes the user to a confirmation screen if the property is to be deleted or not.
    :param request:
    :param property_id:
    :return: HttpResponse renders the deletion page
    """
    if request.user.is_authenticated:
        property_listing = get_object_or_404(Property, id=property_id)
        seller = property_listing.seller.username
        if request.user.username == seller:
            context = {
                'listing': property_listing
            }
            return render(request, 'properties/delete_property.html', context)
        else:
            messages.error(request, "you are not authorized to delete this.")
            return redirect('index')
    else:
        messages.error(request, "you are not authenticated to visit this page.")
        return redirect('index')


def update_property(request, property_id):
    """
    updates the existing property with new form values. only the authenticated seller who created the property can
    update it.
    :param request:
    :param property_id:
    :return: HttpResponse renders the dashboard or index page if success or error for POST request.
    If the request is GET, user is taken to updation form
    """
    property_listing = get_object_or_404(Property, id=property_id)
    seller = property_listing.seller.username

    context = {
        'listing': property_listing,
        'state_choices': state_choices

    }
    if request.user.is_authenticated and request.user.username == seller:
        if request.method == 'POST':
            seller_id = property_listing.seller.id
            property_listing.title = request.POST['title']
            property_listing.address = request.POST['address']
            property_listing.city = request.POST['city']
            property_listing.state = request.POST['state']
            property_listing.zip_code = request.POST['zip_code']
            property_listing.description = request.POST['description']
            property_listing.price = request.POST['price']
            property_listing.bedrooms = request.POST['bedrooms']
            property_listing.bathrooms = request.POST['bathrooms']
            property_listing.garage = request.POST['garage']
            property_listing.square_ft = request.POST['square_ft']
            property_listing.lot_size = request.POST['lot_size']
            # Property.objects.filter(id=property_id).update(title=title, address=address, city=city, state=state,
            #                                                zip_code=zip_code, description=description, price=price,
            #                                                bedrooms=bedrooms, bathrooms=bathrooms, garage=garage,
            #                                                square_ft=square_ft, lot_size=lot_size)
            property_listing.photo_main = request.FILES.get('photo_main', property_listing.photo_main)
            property_listing.photo_1 = request.FILES.get('photo_1', property_listing.photo_1)
            property_listing.photo_2 = request.FILES.get('photo_2', property_listing.photo_2)
            property_listing.photo_3 = request.FILES.get('photo_3', property_listing.photo_3)
            property_listing.photo_4 = request.FILES.get('photo_4', property_listing.photo_4)
            property_listing.photo_5 = request.FILES.get('photo_5', property_listing.photo_5)
            property_listing.photo_6 = request.FILES.get('photo_6', property_listing.photo_6)
            property_listing.save()

            messages.success(request, 'Your property has been updated successfully')
            return redirect('dashboard')
        else:
            return render(request, 'properties/update_property.html', context)
    else:
        messages.error(request, "You are not authorized to update this property")
        return redirect('index')


def publish(request, property_id):
    """
    changes the is_published flag to True if it is False.
    :param request:
    :param property_id:
    :return:
    """
    if request.user.is_authenticated:
        property_listing = get_object_or_404(Property, id=property_id)
        property_listing.is_published = True
        property_listing.save()
        return redirect('dashboard')


def unpublish(request, property_id):
    """
    changes the is_published flag to False if it is True.
    :param request:
    :param property_id:
    :return:
    """
    if request.user.is_authenticated:
        property_listing = get_object_or_404(Property, id=property_id)
        property_listing.is_published = False
        property_listing.save()
        return redirect('dashboard')

