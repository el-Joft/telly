""" Create user model """

import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from api_v1.models.base import CommonFieldsMixin
from api_v1.models.role import Role
from api_v1.models.user_manager import UsersManager


class User(AbstractBaseUser, CommonFieldsMixin):
    """Users model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=30, null=False)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=False)
    mobile_number = models.CharField(
        max_length=100, null=False, unique=True)
    password = models.CharField(max_length=128, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateTimeField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.CharField(max_length=500, null=False)
    active = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    role = models.ForeignKey(Role,  on_delete=models.CASCADE)
    objects = UsersManager()

    USERNAME_FIELD = 'email'
    # required fields besides password and email
    REQUIRED_FIELDS = []

    class Meta:
        """Define metadata options."""

        ordering = ('pk',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        """Return object's string representation."""
        return f'{self.first_name} {self.last_name}'

    @property
    def is_active(self):
        """Check if user is active."""
        return self.active

    @property
    def is_staff(self):
        """Check whether user is staff."""
        return self.staff

    @property
    def is_superuser(self):
        """Check whether user is super admin."""
        return self.admin
