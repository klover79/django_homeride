from django.db import models

from organisations.models import Organisation,OrganisationClass
from users.models import User

class Dependent(models.Model):
    parent              = models.ForeignKey(User,on_delete=models.CASCADE, related_name='dependents.parent+')
    user                = models.OneToOneField(User,on_delete=models.CASCADE)
    organisation        = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    identity            = models.CharField(max_length=50)
    organisation_class  = models.ForeignKey(OrganisationClass, null=True, on_delete=models.SET_NULL)
    created_date        = models.DateTimeField(auto_now_add=True)     
    modified_date       = models.DateTimeField(auto_now=True)
    is_approved         = models.BooleanField(default=False)
    approved_date       = models.DateTimeField(null=True)
    approved_by         = models.CharField(max_length=50, null=True, blank=True)
    is_rejected         = models.BooleanField(default=False)
    rejected_date       = models.DateTimeField(null=True)
    rejected_by         = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'organisation')

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"   
        
