from django.template.loader import render_to_string
from django.template import Context
from django.core.mail import EmailMessage
from django.conf import settings



def send_coupon_email(name, email, coupon):
    context = {
        'name':name,
        'email':email,
        'coupon':coupon}
    
    email_subject = 'thank you for having trust in our products'
    email_body = render_to_string('email_message.txt',context)

    email = EmailMessage(
        email_subject,email_body,
        settings.DEFAULT_FROM_EMAIL,[email,],

    )
    return email.send(fail_silently=False)