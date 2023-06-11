from typing                 import Any, Dict, Optional, Type
from django.db.models.query import QuerySet 
from django.db.models       import Q
from django.forms.models    import BaseModelForm
from django.http            import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts       import render, redirect, reverse
from django.views           import generic
from .forms                 import (DependentsCreateForm, 
                                    DependentCustomUserCreationForm, 
                                    DependentUpdateForm, 
                                    SearchOrganisationsDependentForm,
                                    DependentOrganisationUpdateForm
                                    )
from .models                import Dependent
from users.models           import User, UserProfile
from organisations.models   import Organisation, OrganisationClass, OrganisationManager
from django.utils.crypto    import get_random_string
from django.contrib         import messages
from django.utils           import timezone
from django.core.paginator  import Paginator


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


# TODO:organisationmixin
class DependentOrganisationUnverifiedListView(generic.ListView):
    model               = Dependent
    template_name       = 'dependents/dependent-list-organisation-unverified.html'
    context_object_name = 'dependents'
    paginate_by = 50
    
    
    def get_queryset(self) -> QuerySet[Any]:    
        #find dependent that is within user organisation with student dependent info is_approved is false and is_rejected is false
        # queryset = Dependent.objects.filter(user__userprofile__is_active=False, organisation__organisationmanager__user=self.request.user)     
        queryset = Dependent.objects.filter(is_approved=False, is_rejected=False, organisation__organisationmanager__user=self.request.user)
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(DependentOrganisationUnverifiedListView, self).get_context_data(**kwargs)
        
        search_query = self.request.GET.get('q', '')  
        queryset = Dependent.objects.filter(is_approved=False, is_rejected=False, organisation__organisationmanager__user=self.request.user).order_by('user__first_name','organisation_class__name')
        
        if search_query:
            queryset = queryset.filter(
                Q(identity__icontains = search_query)   |
                Q(user__first_name__icontains = search_query)   |
                Q(user__last_name__icontains = search_query)    |
                Q(organisation_class__name__icontains = search_query) |
                Q(organisation_class__grade__icontains = search_query) |
                Q(parent__first_name__icontains = search_query) |
                Q(parent__last_name__icontains = search_query) 
            ).order_by('user__first_name','organisation_class__name')
        
        count_dependents = queryset.count
        paginator = Paginator(queryset, self.paginate_by)
        # Get the current page number from the request's GET parameters
        page = self.request.GET.get('page')
        # Get the corresponding page object from the Paginator
        page_obj = paginator.get_page(page)

        context = {
        'custom_page_obj'   :   page_obj,
        'dependents'        :   page_obj,
        'search_query'      :   search_query,
        'count_dependents'  :   count_dependents, 
        } 

        return context

class DependentOrganisationListView(generic.ListView):
    model               = Dependent
    template_name       = 'dependents/dependent-list-organisation.html'
    context_object_name = 'dependents'
    paginate_by = 50
    
    
    def get_queryset(self) -> QuerySet[Any]:    
        #find dependent that is within user organisation with student dependent info is_approved is false and is_rejected is false
        # queryset = Dependent.objects.filter(user__userprofile__is_active=False, organisation__organisationmanager__user=self.request.user)     
        queryset = Dependent.objects.filter(is_approved=False, is_rejected=False, organisation__organisationmanager__user=self.request.user)
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(DependentOrganisationUnverifiedListView, self).get_context_data(**kwargs)
        
        search_query = self.request.GET.get('q', '')  
        queryset = Dependent.objects.filter(is_approved=False, is_rejected=False, organisation__organisationmanager__user=self.request.user).order_by('user__first_name','organisation_class__name')
        
        if search_query:
            queryset = queryset.filter(
                Q(identity__icontains = search_query)   |
                Q(user__first_name__icontains = search_query)   |
                Q(user__last_name__icontains = search_query)    |
                Q(organisation_class__name__icontains = search_query) |
                Q(organisation_class__grade__icontains = search_query) |
                Q(parent__first_name__icontains = search_query) |
                Q(parent__last_name__icontains = search_query) 
            ).order_by('user__first_name','organisation_class__name')
        
        count_dependents = queryset.count
        paginator = Paginator(queryset, self.paginate_by)
        # Get the current page number from the request's GET parameters
        page = self.request.GET.get('page')
        # Get the corresponding page object from the Paginator
        page_obj = paginator.get_page(page)

        context = {
        'custom_page_obj'   :   page_obj,
        'dependents'        :   page_obj,
        'search_query'      :   search_query,
        'count_dependents'  :   count_dependents, 
        } 

        return context

# TODO: OrganisationMixin
class DependentOrganisationListView(generic.ListView):
    model               = Dependent
    template_name       = 'dependents/dependent-list-organisation.html'
    context_object_name = 'dependents'
    paginate_by = 50 
    
    
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context             = super().get_context_data(**kwargs) 
        type_record         = self.request.GET.get('type_record', 'pending')
        search_field        = self.request.GET.get('search_field', '')
        page_record         = int(self.request.GET.get('page_record','10'))
        rec_type_reject     = False
        rec_type_approve    = False 
        button_approve      = ''
        button_reject       = ''
        current_data        = {
                'type_record'   :   type_record,
                'search_field'  :   search_field,
                'page_record'   :   page_record,
                }  
        form_search         = SearchOrganisationsDependentForm(current_data) #maybe delete this line 
        
        if  type_record == 'approved':
            rec_type_reject     = False
            rec_type_approve    = True
            button_approve      = 'Disabled'
            button_reject       = ''
        elif type_record == 'rejected':
            rec_type_reject     = True
            rec_type_approve    = False
            button_approve      = ''
            button_reject       = 'Disabled'
        else: #record pending for verification
            rec_type_reject     = False
            rec_type_approve    = False

        queryset = Dependent.objects.filter(is_approved=rec_type_approve,
                                            is_rejected=rec_type_reject, 
                                            organisation__organisationmanager__user=self.request.user
                                            ).order_by('user__first_name','organisation_class__name')

        if search_field:
            queryset = queryset.filter(
                Q(identity__icontains = search_field)   |
                Q(user__first_name__icontains = search_field)   |
                Q(user__last_name__icontains = search_field)    |
                Q(organisation_class__name__icontains = search_field) |
                Q(organisation_class__grade__icontains = search_field) |
                Q(parent__first_name__icontains = search_field) |
                Q(parent__last_name__icontains = search_field) 
            ).order_by('user__first_name','organisation_class__name')

        count_dependents = queryset.count
        paginator = Paginator(queryset, page_record)
        # Get the current page number from the request's GET parameters
        page = self.request.GET.get('page')
        # Get the corresponding page object from the Paginator
        page_obj = paginator.get_page(page)
        

        context = {
        'custom_page_obj'   :   page_obj,
        'dependents'        :   page_obj,
        'count_dependents'  :   count_dependents,
        'form_search'       :   form_search, 
        'button_approve'    :   button_approve,
        'button_reject'     :   button_reject,
        } 

        return context
    


def approve_or_reject_dependent_organisation(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_rows')
        if check_row_is_selected(request,selected_ids):
            count = len(selected_ids)       
            dependents = Dependent.objects.filter(pk__in=selected_ids)
            #approved
            if 'approve' in request.POST:
                dependents.update(is_approved=True, 
                                  approved_date=timezone.now(), 
                                  approved_by=request.user.id,
                                  is_rejected=False,
                                  rejected_date=None, 
                                  rejected_by=None,
                                  )
                messages.add_message(request, messages.SUCCESS, f"{count}{' dependent(s) approved'}") 
            #rejected       
            elif 'reject' in request.POST: 
                dependents.update(is_rejected=True,
                                  rejected_date=timezone.now(), 
                                  rejected_by=request.user.id,
                                  is_approved=False, 
                                  approved_date=None, 
                                  approved_by=None
                                  )
                messages.add_message(request, messages.ERROR, f"{count}{' dependent(s) rejected'}")
            elif 'delete' in request.POST: 
                # dependents.delete() #TODO: TEST delete
                messages.add_message(request, messages.ERROR, f"{count}{' dependent(s) deleted'}")
            else:
                messages.add_message(request, messages.ERROR, "Unspecified action")
            return redirect('dependents:dependent-organisation-list')  
        else:
            messages.add_message(request, messages.ERROR, "No record selected!")
            return redirect('dependents:dependent-organisation-list')       
    else: 
        return redirect('dependents:dependent-organisation-list')     
    
'''check if row is selected in grid'''
def check_row_is_selected(request, list_ids):
    if len(list_ids) <= 0: 
        return False
    else:
        return True
    

class DependentOrganisationUpdateView(generic.UpdateView):
    model               = Dependent
    template_name       = 'dependents/dependent-update-organisation.html'
    context_object_name = 'dependent'
    form_class          =  DependentOrganisationUpdateForm

    def get_success_url(self):
        return reverse("dependents:dependent-organisation-list")
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.add_message(self.request, messages.SUCCESS, f"{'Dependent updated'}")
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['organisation_class'].queryset = OrganisationClass.objects.filter(organisation__organisationmanager__id=self.request.user.id)
        return form