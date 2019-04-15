from django.shortcuts import render
from properties.choices import bedroom_choices, state_choices, price_choices
from properties.models import Property
from accounts.models import Users
# Create your views here.


def index(request):
    """
    Shows the home page of the app. Passes in the latest 3 listings into context and renders it onto homepage
    :param request:
    :return: HttpResponse renders index page of the app
    """
    listings = Property.objects.order_by('-list_date').filter(is_published=True)[:3]
    context = {
        'listings': listings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices
    }
    return render(request, 'pages/index.html', context)


def about(request):
    """
    Shows the about page of the app. Passes in the verified seller accounts into context and renders it.
    :param request:
    :return: HttpResponse renders the about page of the app.
    """
    sellers = Users.objects.order_by('-id').filter(is_verified=True)
    context = {
        'sellers': sellers,
    }
    return render(request, 'pages/about.html', context)


