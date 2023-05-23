from typing import Any, Dict
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse, Http404
from django.shortcuts import render, reverse, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.views import generic
from .forms import CustomUserCreationForm, UserProfileUpdateForm, UserUpdateForm, UserProfilePictureForm
from .models import User, UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# import for activation 
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . import mailing



class LandingPageAuthenticatedView(LoginRequiredMixin, generic.TemplateView):
    template_name = "users/user_profile_detail.html"

class UnauthorizedAccessView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'users/unauthorized_access.html'

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

class ContactPageView(generic.TemplateView):
    template_name = "contact.html"

class SignupView(generic.CreateView):
    template_name   = "registration/signup.html"
    form_class      = CustomUserCreationForm
    model           = User

    def get_success_url(self) -> str:
        return reverse("login")
    
    def form_valid(self,form):
        user            = form.save(commit=True)
        user.is_active  = True # let user to login and setup their profile with limit access.
        user.username   = user.email #set username = email since email is use to login and should be unique
        user.save()
        
        # send activation_url 
        # mailing.send_activation_email(user.email, self.request)
        
        return super(SignupView, self).form_valid(form)

# update user and user profile and send email to verify user information    
@login_required(login_url = 'login')
def update_user_userprofile(request):

    current_user = request.user
    profile     = get_object_or_404(UserProfile, user=current_user.id)
    
    if request.method == 'POST':
        form_user           = UserUpdateForm(request.POST, instance=current_user)
        form_profile        = UserProfileUpdateForm(request.POST, instance=profile)
        form_profile_pic    = UserProfilePictureForm(request.POST, request.FILES, instance=profile)
        
        if form_user.is_valid() and form_profile.is_valid() and form_profile_pic.is_valid():
            user            = form_user.save(commit=False)
            user.username   = user.email # (in the case user updated email and username must be sync) TODO: sync the updates in user model using signals
            user.save()            
            userprofile = form_profile.save(commit=False)            
            if userprofile.is_active == False:                           
               userprofile.save()   
               mailing.send_activation_email(current_user.email,request)               
               return redirect('users:home')
            else:
                form_profile.save()
                messages.add_message(request, messages.WARNING, 'Your profile has been updated.')
                return redirect('users:home')               
        else:
            messages.add_message(request, messages.WARNING, 'Please provide valid information for your account to be activated.')
    else:
        form_user   = UserUpdateForm(instance=current_user)
        form_profile= UserProfileUpdateForm(instance=profile)
        form_profile_pic = UserProfilePictureForm(instance=profile)

    context = {
        'form_user'         : form_user,
        'form_profile'      : form_profile,
        'form_profile_pic'  : form_profile_pic,
        'profile'           : profile,

    }
    return render(request, 'users/user_profile_update.html', context)    


def activate(request, uidb64, token):
    mailing.activate_profile(request, uidb64, token)
    return redirect('login')

# resending activation link request
def resend_activation(request):
    if request.method =='POST':
        email = request.POST['email']
        try:
            user = get_object_or_404(User,email__exact=email)  
        except(Http404, User.DoesNotExist,TypeError, ValueError, OverflowError):
            messages.add_message(request, messages.ERROR, "User not found!")
            return redirect('resend-activate')
        if user is not None:
            mailing.send_activation_email(user.email, request)
            return redirect('resend-activate')                                
        else:
            messages.add_message(request, messages.ERROR, "User not found!")   
            return redirect('resend-activate')         
    else:
        return render(request, 'registration/activation_resend.html')
 