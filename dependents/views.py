from typing import Any, Dict
from django.forms.models    import BaseModelForm
from django.http            import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts       import render, redirect
from django.views           import generic
from .forms                 import DependentsCreateForm, DependentCustomUserCreationForm
from .models                import Dependent
from users.models           import User, UserProfile
from organisations.models   import Organisation, OrganisationClass
from django.utils.crypto import get_random_string


def get_dependent_choices(request):
    organisation_id = request.GET.get('controlling_id')
    print(request.GET)
    dependent_choices = OrganisationClass.objects.filter(organisation_id=organisation_id).values('id', 'name')
    print(organisation_id)
    return JsonResponse(list(dependent_choices), safe=False)


def dependent_create(request):
    user = request.user
    form_user = DependentCustomUserCreationForm
    form_dependent = DependentsCreateForm

    if request.method == 'POST':
        form_user       = DependentCustomUserCreationForm(request.POST)
        form_dependent  = DependentsCreateForm(request.POST)
        # user            = User()
        # dependent       = Dependent()
        print(request.POST or None)
        if form_user.is_valid() and form_dependent.is_valid():
            user            = form_user.save(commit=False)   
            password        = get_random_string(10)  # Generate a random password  
            username        = form_user.cleaned_data['email']  #ensure username is set same with password    
            user.set_password(password)
            user.save()
  
            # set user created as student profile 
            userprofile             = UserProfile.objects.get(user=user)
            userprofile.is_student  = True           
            userprofile.save()
            # set guardian of the dependent 
            dependent                       = form_dependent.save(commit=False)
            dependent.user                  = user #set user link to guardian in the dependent's data
            dependent.parent                = request.user
            dependent.organisation          = form_dependent.cleaned_data['organisation']
            dependent.organisation_class    = form_dependent.cleaned_data['organisation_class']
            dependent.save()

            return redirect('users:home')
        else:
            return redirect('dependents:dependent-create')
    else:
        context = {
            'form_user'     : form_user,
            'form_dependent': form_dependent,
        }
        return render(request, 'dependents/dependent-create.html', context)
