from django.shortcuts import render
from properties.choices import bedroom_choices, state_choices, price_choices
from properties.models import Property
from accounts.models import Users
from django.core.paginator import Paginator
from django.shortcuts import render_to_response
from django.template import RequestContext


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
    paginator = Paginator(sellers, 6)
    page = request.GET.get('page')
    paged_sellers = paginator.get_page(page)
    context = {
        'listings': paged_sellers,
    }
    return render(request, 'pages/about.html', context)


def handler404(request, exception, template_name="error_404.html"):
    response = render_to_response('pages/error_404.html')
    response.status_code = 404
    return response

#
# def handler500(request, exception, template_name="error_500.html"):
#     response = render_to_response('pages/error_500.html')
#     response.status_code = 500
#     return response
#
