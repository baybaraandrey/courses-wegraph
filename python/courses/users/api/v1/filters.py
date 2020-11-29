from django.contrib.auth import get_user_model

from django_filters import rest_framework as filters
from django_filters.rest_framework import (
    BooleanFilter,
)


User = get_user_model()


class UserFilter(filters.FilterSet):
    is_staff = BooleanFilter(
        field_name='is_staff',
    )
    is_active = BooleanFilter(
        field_name='is_active',
    )
    is_superuser = BooleanFilter(
        field_name='is_superuser',
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
