""" Common fields mixin """

from django.db import models


class CommonFieldsMixin(models.Model):
    """Add created_at and updated_at fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        """Define metadata options."""

        abstract = True
