from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail


def contact(request):
    """
    Takes the input form enquiry form where the buyer can make an enquiry on a property.
    The seller gets this enquiry on his dashboard and an email is sent to the seller with the
    enquiry details.
    Duplicate enquiry is not allowed for authenticated users.
    :param request:
    :return: HttpResponse renders the listing page with success message if enquiry is made, otherwise with error message
    """
    if request.method == 'POST':
        property_id = request.POST['property_id']
        property = request.POST['property']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        seller_email = request.POST['seller_email']
        seller_id = request.POST['seller_id']

        # Check if user has made enquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(property_id=property_id, user_id=user_id)
            if has_contacted:
                messages.error(request, "You have already made an enquiry for this property listing.")
                return redirect('/properties/' + property_id)

        contact = Contact(property=property, property_id=property_id, name=name,
                          email=email, phone=phone, message=message, user_id=user_id, seller_id=seller_id)

        contact.save()

        # send mail
        send_mail(
            'Property Listing Enquiry',
            'There has been an enquiry for ' + property + ' by ' + name + '. \n\n' + 'Buyer\'s contact: ' + '\nEmail :'
            + email + '\nPhone: ' + phone + '\nLogin to see more details.',
            'contact.realestate.information@gmail.com',
            [seller_email],
            fail_silently=False
        )

        messages.success(request, 'Your request has been submitted, the seller will get back to you soon')

        return redirect('/properties/' + property_id)

