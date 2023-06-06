from django.urls import path
from . import views 

app_name = 'dependents'

urlpatterns = [
    path('dependent/create/', views.dependent_create, name='dependent-create'),
    path('dependent/<int:pk>/update/', views.dependent_update,  name='dependent-update'),
    path('dependent/<int:pk>/delete/', views.DependentDeleteView.as_view(),  name='dependent-delete'),
    path('dependent/list', views.DependentOrganisationUnverifiedListView.as_view(), name='dependent-unverified-list'),
    path('get_dependent_choices/', views.get_dependent_choices, name='get_dependent_choices'),
    path('approve_or_reject_dependent_organisation/', views.approve_or_reject_dependent_organisation, name='approve_or_reject_dependent_organisation'),
    # path('dependent-class/list-view/', views.ListDependentClassListView.as_view(), name="dependent-class-list"),
    # path('dependent-class/<int:pk>/update-view/', views.UpdateDependentClassUpdateView.as_view(), name="dependent-class-update"),
]