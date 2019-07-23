"""Create the Roles Model"""
import uuid

from django.db import models

from api_v1.models.base import CommonFieldsMixin


class Role(CommonFieldsMixin):
    """Create role model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
