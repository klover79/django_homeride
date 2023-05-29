from typing import Any, Dict
from django.forms.models    import BaseModelForm
from django.http            import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts       import render, redirect, reverse
from django.views           import generic
from .forms                 import DependentsCreateForm, DependentCustomUserCreationForm, DependentUpdateForm
from .models                import Dependent
from users.models           import User, UserProfile
from organisations.models   import Organisation, OrganisationClass
from django.utils.crypto    import get_random_string
from django.contrib         import messages


def get_dependent_choices(request):
    organisation_id = request.GET.get('controlling_id')
    dependent_choices = OrganisationClass.objects.filter(organisation_id=organisation_id).values('id', 'name')
    return JsonResponse(list(dependent_choices), safe=False)

'''Create Dependent and Link with Parent'''
def dependent_create(request):
    user = request.user
    form_user = DependentCustomUserCreationForm
    form_dependent = DependentsCreateForm

    if request.method == 'POST':
        organisation        = Organisation.objects.get(id=request.POST['organisation'])
        organisation_class  = OrganisationClass.objects.get(id=request.POST['organisation_class'])        
        form_user           = DependentCustomUserCreationForm(request.POST)
        form_dependent      = DependentsCreateForm(request.POST)
        if form_user.is_valid() and form_dependent.is_valid():
            user            = form_user.save(commit=False)   
            password        = get_random_string(10)  # Generate a random password  
            user.username   = form_user.cleaned_data['email']  #ensure username is set same with password    
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
            dependent.organisation          = organisation
            dependent.organisation_class    = organisation_class
            dependent.save()
            messages.add_message(request, messages.SUCCESS, 'Dependent record created.')
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, form_dependent.errors)
            messages.add_message(request, messages.ERROR, form_user.errors)
            return redirect('dependents:dependent-create')
    else:
        context = {
            'form_user'     : form_user,
            'form_dependent': form_dependent,
        }
        return render(request, 'dependents/dependent-create.html', context)
    

'''Update Dependent'''
def dependent_update(request, pk):
    user            = request.user
    dependent_user  = User.objects.get(id=pk)
    dependent       = Dependent.objects.get(user=dependent_user)

    if request.method == 'POST':       
        form_user           = DependentCustomUserCreationForm(request.POST, instance=dependent_user)
        form_dependent      = DependentUpdateForm(request.POST,instance=dependent)
        if form_user.is_valid() and form_dependent.is_valid():
            user            = form_user.save(commit=False)   
            user.username   = form_user.cleaned_data['email']  #ensure username is set same with password    
            user.save()          
            dependent       = form_dependent.save(commit=False)
            dependent.save()
            messages.add_message(request, messages.SUCCESS, 'Dependent record updated.')
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, form_dependent.errors)
            messages.add_message(request, messages.ERROR, form_user.errors)
            return redirect('dependents:dependent-update', pk)
    else:
        form_user           = DependentCustomUserCreationForm(instance=dependent_user)
        form_dependent      = DependentUpdateForm(instance=dependent)
        context = {
            'form_user'     : form_user,
            'form_dependent': form_dependent,
            'dependent'     : dependent,
        }
        return render(request, 'dependents/dependent-update.html', context)
    
class DependentDeleteView(generic.DeleteView):
    template_name = 'dependents/dependent-delete.html'
    model = User
    context_object_name = 'user'

    def get_success_url(self) -> str:
        return reverse('home')



'''Get list of dependents of current authenticated user'''
def get_parent_dependent_list(request):
    if request.user.is_authenticated:
        is_dependent_exists = Dependent.objects.filter(parent=request.user).exists()

        if is_dependent_exists:
            dependent_list = Dependent.objects.filter(parent=request.user)

        else:
            dependent_list = None

        context = {
            'dependent_exists'  : is_dependent_exists,
            'dependent_list'    : dependent_list,
        }
        return context
    else:
        pass 


