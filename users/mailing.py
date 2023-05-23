from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from users.models import User, UserProfile

# import for activation 
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

def send_activation_email(user_email, request):

    user = get_object_or_404(User,email__exact=user_email)
    if user is not None:

        # create the activation URL
        # generate an activation token
        token_generator = default_token_generator
        uid             = urlsafe_base64_encode(force_bytes(user.pk))
        token           = token_generator.make_token(user)

        #construct the activation URL
        current_site    = get_current_site(request).domain
        activation_url  = reverse_lazy('activate', kwargs={'uidb64': uid, 'token': token})
        activation_url  = f"{current_site}{activation_url}"
  
        # Send an activation email to the user
        subject = 'Activate Your Account'
        message = render_to_string('registration/mailing/email_activation.html', {
            'user': user,
            'activation_url': activation_url,
        })
        send_mail(subject, message, 'noreply@example.com', [user.email])
        messages.add_message(request, messages.INFO, "We have resent your activation link. Please check your email")
    else:
        messages.add_message(request, messages.ERROR, "Link was not sent. Please contact application administrator")
    


def activate_profile(request, uidb64, token):  
        try:
            uid         = force_str(urlsafe_base64_decode(uidb64))
            user        = User.objects.get(pk=uid)
            userprofile = UserProfile.objects.get(user=user) 
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        token_generator = default_token_generator

        if user is not None and token_generator.check_token(user, token):
            # Activate the userpofile
            userprofile.is_active = True
            userprofile.save()
            messages.add_message(request, messages.SUCCESS, "Activation successful. Please refresh page to get full access to the system")
        else:
            messages.add_message(request, messages.ERROR, "Invalid activation link or link has expired")
    
