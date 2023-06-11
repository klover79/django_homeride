from django.urls import path
from . import views 

app_name = 'dependents'

urlpatterns = [
    path('dependent/create/', views.dependent_create, name='dependent-create'),
    path('dependent/<int:pk>/update/', views.dependent_update,  name='dependent-update'),
    path('dependent/<int:pk>/delete/', views.DependentDeleteView.as_view(),  name='dependent-delete'),
    path('get_dependent_choices/', views.get_dependent_choices, name='get_dependent_choices'),
    path('approve_or_reject_dependent_organisation/', views.approve_or_reject_dependent_organisation, name='approve_or_reject_dependent_organisation'),
    path('dependent_organisation/list/', views.DependentOrganisationListView.as_view(), name='dependent-organisation-list'),
    path('dependent_organisation/<int:pk>/update/', views.DependentOrganisationUpdateView.as_view(),  name='dependent-organisation-update'),
]