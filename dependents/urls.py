from django.urls import path
from . import views 

app_name = 'dependents'

urlpatterns = [
    path('dependent/create/', views.dependent_create, name='dependent-create'),
    path('dependent/<int:pk>/update/', views.dependent_update,  name='dependent-update'),
    path('dependent/<int:pk>/delete/', views.DependentDeleteView.as_view(),  name='dependent-delete'),
    path('get_dependent_choices/', views.get_dependent_choices, name='get_dependent_choices'),
    # path('dependent-class/list-view/', views.ListDependentClassListView.as_view(), name="dependent-class-list"),
    # path('dependent-class/<int:pk>/update-view/', views.UpdateDependentClassUpdateView.as_view(), name="dependent-class-update"),
]