from django.shortcuts import render
from django.http import HttpResponse
from properties.choices import bedroom_choices, state_choices, price_choices
from properties.models import Property
# Create your views here.


def index(request):
    listings = Property.objects.order_by('-list_date').filter(is_published=True)[:3]
    context = {
        'listings' : listings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices
    }
    return render(request, 'pages/index.html', context)


def about(request):
    return render(request, 'pages/about.html')


