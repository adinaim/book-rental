from django.urls import path
from .views import (
    AccountActivationView, 
    RegistrationView, 
    PasswordChangeView, 
    RestorePasswordView,
    ResetPasswordView,
    DeleteAccountView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('activate/<str:activation_code>/', AccountActivationView.as_view(), name='activation'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-change/', PasswordChangeView.as_view(), name='change password'),
    path('restore-password/', RestorePasswordView.as_view(), name='restore pssword'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset password'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete account'),
]