from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.core.paginator import Paginator
from .models import Users
from contacts.models import Contact
from properties.models import Property


def register(request):
    """
    Takes the values from the form if it is a POST request and
    creates a new user with form values if passwords match and
    username and email are unique.
    :param request:
    :return: HTTPResponse returns to index page if successful otherwise
    redirects to register form with error.
    """
    if request.method == "POST":
        # Get form values to register user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        photo = request.FILES.get('photo', '/default.jpg')
        description = request.POST['description']
        phone = request.POST['phone']
        is_seller = request.POST.get('is_seller', False)

        # Check if passwords match
        if password == password2:
            # check username and email duplicates
            if Users.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                if Users.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    # if passwords match, and username and email are unique, create user
                    user = Users.objects.create_user(username=username, password=password, email=email,
                                                     first_name=first_name, last_name=last_name, photo=photo,
                                                     phone=phone, description=description, is_seller=is_seller)

                    user.save()
                    messages.success(request, 'You are now registered and can log in')
                    return redirect('index')

        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    """
    Gets the username and password from the form if it's a POST request
    and if the user is authenticated, user is logged in to dashboard,
    otherwise redirects back to login page.
    :param request:
    :return: HttpResponse renders the dashboard if authenticated otherwise
    returns login page.
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('dashboard')

        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    """
    Logs out the authenticated user
    :param request:
    :return: HttpResponse renders index page
    """
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'you are now logged out')
        return redirect('index')


def dashboard(request):
    """
    If the user is a seller, redirects them to dashboard with enquiries
    and properties posted by the seller.
    If the user is a buyer, redirects them to the buyer dashboard.
    :param request:
    :return: HttpResponse renders dashboard where the user can edit profile
    or post new properties.
    """
    if request.user in Users.objects.filter(is_seller=True):
        seller_contacts = Contact.objects.order_by('-contact_date').filter(seller_id=request.user.id)
        listings = Property.objects.order_by('-list_date').filter(seller=request.user.id)
        paginator = Paginator(listings, 3)
        page = request.GET.get('page')
        paged_listings = paginator.get_page(page)

        paginator = Paginator(seller_contacts, 10)
        contact_page = request.GET.get('enquiry_page')
        paged_contacts = paginator.get_page(contact_page)

        context = {
            'contacts': paged_contacts,
            'listings': paged_listings
        }
    else:

        user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

        context = {
            'contacts': user_contacts,

        }
    return render(request, 'accounts/dashboard.html', context)


def update_user(request, user_id):
    """
    Updates the user details with new details in the form if the user
    is authenticated.
    :param request:
    :param user_id: takes in the authenticated user id.
    :return: HttpResponse renders index if user is not authenticated,
    update_user_details if user is authenticated, and back to dashboard
    if user updates details.
    """
    if request.user.is_authenticated:
        if request.method == 'POST':

            Users.objects.filter(id=user_id).update(first_name = request.POST['first_name'],
                                                    last_name = request.POST['last_name'],
                                                    username=request.POST['username'],
                                                    description=request.POST['description'],
                                                    phone=request.POST['phone'],
                                                    email=request.POST['email']
                                                    )
            current_user = get_object_or_404(Users, id=request.user.id)
            current_user.photo = request.FILES.get('photo', current_user.photo)
            current_user.save()
            messages.success(request, "Successfully updated your profile")
            return redirect('dashboard')
        else:
            return render(request, 'accounts/update_user_details.html')

    else:
        messages.error(request, "you are not authenticated to visit ths page.")
        return redirect('index')

