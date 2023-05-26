from django.db import models
from users.models import User


class Organisation(models.Model):
    organisation_name   = models.CharField(max_length=100, unique=True, blank=False, null=False)
    address_line_1      = models.CharField(max_length=100, blank=True, null=True)
    address_line_2      = models.CharField(max_length=100, blank=True, null=True)
    state               = models.CharField(max_length=100, blank=True, null=True)
    city                = models.CharField(max_length=100, blank=True, null=True)
    postcode            = models.CharField(max_length=10,  blank=True, null=True)
    country             = models.CharField(max_length=100, blank=True, null=True)
    contact_number      = models.CharField(max_length=100, blank=True, null=True)
    email_address       = models.EmailField(max_length=100, unique=True)
    account_number      = models.CharField(max_length=100, blank=True, null=True)
    is_active           = models.BooleanField(default=False)
    active_start_date   = models.DateTimeField()
    active_end_date     = models.DateTimeField()
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organisation_name


class OrganisationManager(models.Model):
    role = (
        ('admin','admin'),
        ('manager','manager')
    )
    organisation        = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    organisation_role   = models.CharField(max_length=50, choices=role)
    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now_add=True)
    modified_date       = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.organisation.organisation_name
    
    class Meta:
        verbose_name        = 'Organisation Manager'
        verbose_name_plural = 'Organisation Managers'


class OrganisationPayment(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    method = models.CharField(max_length=100)
    confirmation_code = models.CharField(max_length=100)
    amount = float
    status = models.TextField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.payment_id


class OrganisationClass(models.Model):
    name            = models.CharField(max_length=50, null=False, blank=False)
    grade           = models.CharField(max_length=50, null=False, blank=False)
    organisation    = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)     
    modified_date   = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together     = ('name', 'grade', 'organisation')
        verbose_name        = 'Organisation Classroom'
        verbose_name_plural = 'Organisation Classrooms'
       

    def __str__(self) -> str:
        return f"{self.grade} : {self.name}"