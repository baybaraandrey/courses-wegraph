from django.urls import re_path

from rest_framework.routers import SimpleRouter

from .views import (
    AdminObtainUserTokenView,
    AdminUserListView,
    AdminUserViewSet,
    CheckPasswordStrengthView,
    CheckUsernameAvailabilityView,
    RecoveryPasswordView,
    RequestPasswordRecoveryEmailView,
    UserRegistrationView,
    UserViewSet,
)


user_router = SimpleRouter()
admin_user_router = SimpleRouter()


admin_user_router.register(
    'admin/users',
    AdminUserViewSet,
    basename='admin-users',
)
user_router.register(
    'users',
    UserViewSet,
    basename='users',
)


app_name = 'users'
api_urlpatterns = [
    re_path(
        r'^admin/users/list/$',
        AdminUserListView.as_view(),
        name='filtered-users-list',
    ),
    re_path(
        r'^admin/users/(?P<id>\d+)/obtain_jwt_token/$',
        AdminObtainUserTokenView.as_view(),
        name='users-obtain-user-jwt-token',
    ),
    re_path(
        r'^users/register/password/$',
        UserRegistrationView.as_view(),
        name='users-register-password',
    ),
    re_path(
        r'^users/check/password/$',
        CheckPasswordStrengthView.as_view(),
        name='users-check-strength-password',
    ),
    re_path(
        r'^users/check/username/$',
        CheckUsernameAvailabilityView.as_view(),
        name='users-check-username-availability',
    ),
    re_path(
        r'^users/recovery/password/send_email/$',
        RequestPasswordRecoveryEmailView.as_view(),
        name='users-request-password-recovery-email',
    ),
    re_path(
        r'^users/recovery/password/$',
        RecoveryPasswordView.as_view(),
        name='users-recovery-password',
    ),
]
api_urlpatterns.extend(admin_user_router.urls)
api_urlpatterns.extend(user_router.urls)
