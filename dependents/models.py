from django.db import models

from organisations.models import Organisation,OrganisationClass
from users.models import User

class Dependent(models.Model):
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation        = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    identity            = models.CharField(max_length=50)
    organisation_class  = models.ForeignKey(OrganisationClass, null=True, on_delete=models.SET_NULL)
    created_date        = models.DateTimeField(auto_now_add=True)     
    modified_date       = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'organisation')
