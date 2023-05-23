from django.urls import path
from . import views

app_name = 'organisations'

urlpatterns = [
    # path('', views.xxx.as_view(), name='organisation-information'),
    path('classroom/list', views.ClassroomListView.as_view(), name='classroom-list'),
    path('classroom/create', views.ClassroomCreateView.as_view(), name='classroom-create'),
    path('classroom/<int:pk>/update', views.ClassroomUpdateView.as_view(), name='classroom-update'),
    path('classroom/<int:pk>/delete', views.ClassroomDeleteView.as_view(), name='classroom-delete'),
]
