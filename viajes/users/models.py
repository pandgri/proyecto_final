from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    birth_date = models.DateField(blank=True, null=True)
    country = CountryField(max_length=100, blank=True)

    def __str__(self):
        return self.username