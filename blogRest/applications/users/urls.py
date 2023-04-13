from django.urls import path

# import views
from .views import RegisterView, VerifyAccountView, ListInterstsView

from rest_framework_simplejwt.views import (
    # Authentication views
    TokenObtainPairView,
    TokenRefreshView
)

from .views import (
        UserDetailsView, 
        UpdateUserInformationView, 
        UpdateUserView, 
        UpdatePassWordRequestView, 
        UpdatePasswordView,
        VerifyCode)


urlpatterns = [
    # Authentication urls
    path(
        'auth/login',
        TokenObtainPairView.as_view(),
        name='login'
    ),path(
        'auth/refresh-token',
        TokenRefreshView.as_view(),
        name='refresh-token'
    ),
    path(
        'auth/register',
        RegisterView.as_view(),
        name='register'
    ),
    path(
        'auth/account-verification',
        VerifyAccountView.as_view(),
        name='verification-account'
    ),
    # update password urls
    path(
        'auth/update-password-request',
        UpdatePassWordRequestView.as_view(),
        name='update-password-request'
    ),
    path(
        'auth/update-password',
        UpdatePasswordView.as_view(),
        name='update-password'
    ),
    path(
        'auth/verify-code',
        VerifyCode.as_view(),
        name='verify-code'
    ),
    # custom urls
    path(
        'api/user/details',
        UserDetailsView.as_view(),
        name='user-details'
    ),
    path(
        'api/user/update/<pk>',
        UpdateUserInformationView.as_view(),
        name='update-information'
    ),
    path(
        'api/user/update-user/<pk>',
        UpdateUserView.as_view(),
        name='update-user'
    ),
    # Intersts rls
    path(
        'api/interest',
        ListInterstsView.as_view(),
        name='intersts'
    )
]