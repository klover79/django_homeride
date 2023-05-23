from typing import Any, Dict
from django.db import IntegrityError, Error, models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, reverse 
from django.views import generic
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from users.forms import CustomUserCreationForm
from .forms import OrganisationClassForm
from organisations.models import OrganisationManager, Organisation
from .models import Organisation, OrganisationClass, OrganisationManager


# Create your views here.
# TODO: organisation and login mixin
# TODO: parents to register student with organisation
# TODO: admin of organisation to approve student registration
# TODO: admin to create class

'''list view for organisation class room'''
class ClassroomListView(generic.ListView):
    model = OrganisationClass
    template_name   = 'organisations/classroom-list.html'
    context_object_name = 'dependent_classes'

    def get_queryset(self):
        organisation = OrganisationManager.objects.get(user=self.request.user).organisation.id
        queryset     = OrganisationClass.objects.filter(organisation=organisation).order_by('-grade','name')
        return queryset
    

    
'''create view for organisation class room'''
class ClassroomCreateView(generic.CreateView):
    model           = OrganisationClass
    form_class      = OrganisationClassForm
    template_name   = 'organisations/classroom-create.html'

    def get_success_url(self):
        return reverse('organisations:classroom-list')
 
    def form_valid(self, form, ):
        # update organisation to class room data
        organisation_manager    = OrganisationManager.objects.get(user=self.request.user)
        organisation            = Organisation.objects.get(id=organisation_manager.organisation.id)
        class_room              = form.save(commit=False)
        class_room.organisation = organisation
        try:
            class_room.save()       
        except (IntegrityError, AssertionError) as e: 
            messages.add_message(self.request, messages.ERROR, f"{'Classroom already exists for '}{organisation}")
            error_message = str(e)
            return render(self.request, 'error.html', {'error_message': error_message})
        messages.add_message(self.request, messages.INFO, f"{'Classroom added for '}{organisation}")
        return super().form_valid(form)
    
class ClassroomUpdateView(generic.UpdateView):
    model           = OrganisationClass
    form_class      = OrganisationClassForm
    template_name   = 'organisations/classroom-update.html'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = OrganisationClass.objects.filter(id=self.kwargs['pk'])
        return queryset

    def get_success_url(self):
        return reverse('organisations:classroom-list')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.add_message(self.request, messages.INFO, f"{'Classroom updated'}")
        return super().form_valid(form)
    
class ClassroomDeleteView(generic.DeleteView):
    template_name = "organisations/classroom-delete.html"
    context_object_name = "classroom"
    model = OrganisationClass

    def get_queryset(self):
        organisation = OrganisationManager.objects.get(user=self.request.user).organisation
        return OrganisationClass.objects.filter(organisation=organisation)
    
    def get_success_url(self):
        return reverse("organisations:classroom-list")
    
    
# view to create user ==> auto create profile organisation and setup organisation in which organisations'''
