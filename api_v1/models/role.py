"""Create the Roles Model"""

# pylint: disable=too-few-public-methods,
# undefined-variable, too-many-arguments

from django.db import models
from api_v1.models.base import CommonFieldsMixin


class Role(CommonFieldsMixin):
    """Create role model"""
    ROLE_TYPES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin'),
        ('user', 'User'),
        ('business', 'Business'),
    )
    role_type = models.CharField(
        max_length=30, unique=True,
        choices=ROLE_TYPES, db_index=True)

    class Meta:
        """Define metadata options."""

        ordering = ('pk',)
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        """Return object's string representation."""
        return self.role_type
