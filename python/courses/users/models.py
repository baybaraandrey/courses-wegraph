from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """
    Default user for courses
    """

    phone = PhoneNumberField(blank=True, null=False)
    email = models.EmailField(
        _('email address'),
        blank=True,
        null=False,
        db_index=True,
        unique=True,
    )

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse('api:admin-users-detail', kwargs={'id': self.id})
