from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Users
from contacts.models import Contact
from properties.models import Property


# Create your views here.

def register(request):
    if request.method == "POST":
        # get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        photo = request.FILES.get('photo', '/default.jpg')
        description = request.POST['description']
        phone = request.POST['phone']
        is_seller = request.POST['is_seller']


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
                    # looks good
                    user = Users.objects.create_user(username=username, password=password, email=email,
                                                     first_name=first_name, last_name=last_name, photo=photo,
                                                     phone=phone, description=description, is_seller=is_seller)
                    # Login after register
                    # auth.login(request, user)
                    # messages.success(request, 'you are now logged in ')
                    # return redirect('index')
                    user.save()
                    messages.success(request, 'You are now registered and can log in')
                    return redirect('index')

        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')



    else:
        return render(request, 'accounts/register.html')


def login(request):
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
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'you are now logged out')
        return redirect('index')


def dashboard(request):

    # else:
    # sellers = Users.objects.filter(is_seller=True)
    # session_user = request.user
    # context = {
    #     'User': session_user,
    #     'sellers': sellers
    # }
    # if not request.user.photo:
    #     request.user.photo = '/default.jpg'
    # if request.user.is_seller:


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

