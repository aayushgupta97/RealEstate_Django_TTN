from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact

def contact(request):
    if request.method == 'POST':
        property_id = request.POST['property_id']
        property = request.POST['property']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        seller_email = request.POST['seller_email']

        contact = Contact(property=property, property_id=property_id, name=name,
                         email=email, phone=phone, message=message, user_id=user_id )

        contact.save()

        messages.success(request, 'Your request has been submitted, the seller will get back to you soon')

        return redirect('/properties/' + property_id)

