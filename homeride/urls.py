from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from users.views import (SignupView,
                        LandingPageView, 
                        ContactPageView,
                        activate,
                        resend_activation,
                        )
from django.contrib.auth.views import (
    LoginView,
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('users/', include('users.urls', namespace='users')),
    path('organisations/', include('organisations.urls', namespace='organisations')),
    path('dependents/', include('dependents.urls', namespace='dependents')),
    path('signup/', SignupView.as_view(), name="sign-up"),
    path('password_reset', PasswordResetView.as_view(template_name='registration/password_reset_form.html'),name='password_reset'),
    path('password_reset_done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('activate/<uidb64>/<token>/', activate,  name="activate"),
    path('activate_resend/', resend_activation,  name="resend-activate"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)