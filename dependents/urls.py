from django.urls import path
from . import views 

app_name = 'dependents'

urlpatterns = [
    path('dependent-create/create/', views.dependent_create, name='dependent-create'),
    # path('dependent-class/list-view/', views.ListDependentClassListView.as_view(), name="dependent-class-list"),
    # path('dependent-class/<int:pk>/update-view/', views.UpdateDependentClassUpdateView.as_view(), name="dependent-class-update"),
]