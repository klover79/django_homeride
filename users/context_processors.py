from organisations.models import OrganisationManager, Organisation
from django.core.exceptions import ObjectDoesNotExist

'''get details of the organisation manager. context is use for class organisation manager mixin'''
def organisation_manager(request):
    if request.user.is_authenticated:
        try:
            organisation_manager =  OrganisationManager.objects.get(user=request.user) 
            if organisation_manager:
                organisation = Organisation.objects.get(id=organisation_manager.organisation.id)
            else:
                organisation = None
            context = {
                'manager_organisation_name' : organisation.organisation_name, 
                'manager_organisation_role' : organisation_manager.organisation_role
            }
        except(ObjectDoesNotExist):
            context = {
            'manager_organisation_name' : None, 
            'manager_organisation_role' : None
        }
    else:
        context = {
            'manager_organisation_name' : None, 
            'manager_organisation_role' : None
        }
    return context


