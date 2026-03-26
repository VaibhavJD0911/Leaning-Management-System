from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )

    roles = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    def __str__(self):
        return self.username
