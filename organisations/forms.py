from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import OrganisationClass

class OrganisationClassForm(forms.ModelForm):
   
    name = forms.CharField(
    label="Classroom Name",
    widget=forms.TextInput(attrs={'placeholder': 'Ex: 5 Electrical Engineering 1' ,'class': 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'}),
    )

    grade = forms.CharField(
    label="Class Grade",
    widget=forms.TextInput(attrs={'placeholder': 'Ex: Form 5' ,'class': 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'}),
    )

    class Meta:
        model = OrganisationClass
        fields = ('name', 'grade')
