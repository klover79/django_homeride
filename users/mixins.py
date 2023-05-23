# TODO: organisation and login mixin

from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import redirect

class OrganiserAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and organiser."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organiser:
            return redirect("users:unauthorized-access")
        return super().dispatch(request, *args, **kwargs)
    

class OrganiserAdminManagerAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated with both admin/manager of the organisation"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.userprofile.is_manager 
                                                     and request.user.profile.is_org_admin) :
            return redirect("users:unauthorized-access")
        return super().dispatch(request, *args, **kwargs)
    
class OrganiserAdminOnlyAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and admin only."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.userprofile.is_org_admin :
            return redirect("users:unauthorized-access")
        return super().dispatch(request, *args, **kwargs)

