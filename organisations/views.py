from typing import Any, Dict
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.db.models import Q
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, reverse , redirect
from django.views import generic
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
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
    paginate_by = 5

    def get_queryset(self,**kwargs):
        q = self.request.GET.get("q")
        queryset = super().get_queryset()
        if q != None:
            queryset = queryset.filter(Q(name__icontains = q)|
                                        Q(grade__icontains = q)
                                        ).order_by('-grade','name')
            queryset = queryset.filter(organisation__organisationmanager__user=self.request.user) #filter data by organisation
        else:
            queryset = OrganisationClass.objects.filter(organisation__organisationmanager__user=self.request.user).order_by('-grade','name')
        
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ClassroomListView,self).get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '')

        queryset = queryset = OrganisationClass.objects.filter(organisation__organisationmanager__user=self.request.user).order_by('-grade','name')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains = search_query)  |
                Q(grade__icontains = search_query) 
            )
        
        count_class = queryset.count
        paginator = Paginator(queryset, self.paginate_by)
        # Get the current page number from the request's GET parameters
        page = self.request.GET.get('page')
        # Get the corresponding page object from the Paginator
        page_obj = paginator.get_page(page)

        context = {
        'dependent_classes' :   page_obj,
        'search_query'      :   search_query,
        'count_class'       :   count_class, 
        } 
        return context
    

    
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
    
def ClassroomDeleteSelected(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_rows')
        count = len(selected_ids)
        OrganisationClass.objects.filter(pk__in=selected_ids).delete()
        if count > 0:
            messages.add_message(request, messages.SUCCESS, f"{count}{': Selected Classroom Deleted'}")
        else:
            messages.add_message(request, messages.ERROR, f"{count}{' record selected!'}")
        return redirect('organisations:classroom-list')  # Redirect to a success page after deletion

    # Handle GET request or render a form to select rows for deletion
    queryset = OrganisationManager.objects.get(user=request.user).organisation
    return render(request, 'organisations/classroom-list.html', {'queryset': queryset})

    
    
# view to create user ==> auto create profile organisation and setup organisation in which organisations'''
