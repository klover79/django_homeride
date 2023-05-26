from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from dependents.models import Dependent
from users.models import User



class DependentsCreateForm(forms.ModelForm):
    # organisation = forms.CharField(
    # label="Orangisation",
    # widget=forms.ChoiceField(attrs={'placeholder': 'John' ,'class': 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'}),
    # )

    identity = forms.CharField(
    label="Identity Card",
    widget=forms.TextInput(attrs={'placeholder': 'XXXXXX-XX-XXXX' ,'class': 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'}),
    )

    # organisation_class = forms.ChoiceField(
    # label="Class Room",
    # widget=forms.ChoiceField(attrs={'placeholder': 'John' ,'class': 'block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40'}),
    # )
    class Meta:
        model = Dependent
        fields = ('organisation', 'identity', 'organisation_class')


class DependentCustomUserCreationForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name' , 'email', 'phone_number' )
        exclude = ('username', 'password1', 'password2')
        field_classes = {"email": UsernameField}
    



    
        
