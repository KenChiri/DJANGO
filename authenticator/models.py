from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Officer(AbstractUser):
    police_number = models.CharField(max_length=10, unique=True)
    national_id = models.CharField(max_length=100, unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name='officer_groups',  # Custom reverse accessor name
        blank=True,
        help_text='The groups this user belongs to. A user can belong to multiple groups. By default, users are assigned automatically to the "Registered users" group.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='officer_user_permissions',  # Custom reverse accessor name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    is_superuser = models.BooleanField(
        default = False,
        help_text = 'Designates wether this users should have all permissions without explicitly assigning them',
        verbose_name = 'superuser status'
    )

    class Meta:
        unique_together = (("police_number", "national_id"),)





class AccidentFiles(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    abstract = models.CharField(max_length=1000, blank=True)  # Optional abstract field

    def __str__(self):
        return self.name 



class AccidentDraft(models.Model):
    scene = models.TextField()  # Use TextField for large text content
    created_date = models.DateTimeField(auto_now_add=True)  # Automatically record creation date

    def __str__(self):
        return f"Accident Draft - {self.created_date}"