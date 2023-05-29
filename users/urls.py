from django.urls import path
from . import views 

app_name = 'users'

urlpatterns =[
    path('unauthorized-access', views.UnauthorizedAccessView.as_view(), name='unauthorized-access'),
    path('user-profile/update', views.update_user_userprofile, name='user-profile-update'),

]