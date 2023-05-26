from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from dependents.models import Dependent
from users.models import User
from organisations.models import Organisation, OrganisationClass
from crispy_forms.helper import FormHelper



class DependentsCreateForm(forms.ModelForm):
    # TODO: proper selection for organisation
    # TODO: proper selection from classroom in the organisation and order by

    
    organisation = forms.ModelChoiceField(queryset=Organisation.objects.all())
    organisation_class = forms.ModelChoiceField(queryset=OrganisationClass.objects.none())

    identity = forms.CharField(
    label="Identity Card",
    widget=forms.TextInput(attrs={'placeholder': 'XXXXXX-XX-XXXX' ,'class': 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'}),
    )

    class Meta:
        model = Dependent
        fields = ('organisation', 'identity', 'organisation_class')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organisation'].label = 'Organisation/College/School'
        self.fields['organisation'].widget.attrs.update({'class': 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'})
        self.fields['organisation_class'].label = 'Classroom'
        self.fields['organisation_class'].widget.attrs.update({'class': 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'})
      


class DependentCustomUserCreationForm(forms.ModelForm):
    first_name = forms.CharField(
    label="First Name",
    widget=forms.TextInput(attrs={'placeholder': 'Ex:John' ,'class': 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'}),
    )

    last_name = forms.CharField(
    label="Last Name",
    widget=forms.TextInput(attrs={'placeholder': 'Ex:Doe' ,'class': 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'}),
    )

    email = forms.CharField(
    label="Email",
    widget=forms.TextInput(attrs={'placeholder': 'example@example.com' ,'class': 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'}),
    )

    phone_number = forms.CharField(
    label="phone_number",
    widget=forms.TextInput(attrs={'placeholder': 'XXX-XXXXXXX' ,'class': 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name' , 'email', 'phone_number' )
        exclude = ('username', 'password1', 'password2')
        field_classes = {"email": UsernameField}
    
   


    
        
