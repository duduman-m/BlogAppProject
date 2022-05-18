from django.contrib.auth.models import AbstractUser, Permission
from django.db import models


class Writer(AbstractUser):
    """Extended user model using the AbstractUser model"""
    is_editor = models.BooleanField(verbose_name="Is Editor", default=False)

    @property
    def name(self):
        return self.get_full_name()

    def __str__(self):
        return self.get_full_name()
