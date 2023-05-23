from organisations.models import OrganisationManager, Organisation

'''get details of the organisation manager. context is use for class organisation manager mixin'''
def organisation_manager(request):
    organisation_manager = OrganisationManager.objects.get(user=request.user)
    organisation = Organisation.objects.get(id=organisation_manager.organisation.id)
    context = {
        'manager_organisation_name' : organisation.organisation_name, 
        'manager_organisation_role' : organisation_manager.organisation_role
    }    
    return  context

