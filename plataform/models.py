from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    SEX_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    name = models.CharField("Nombres", max_length=100)
    last_name = models.CharField("Apellidos", max_length=100)
    sex = models.CharField("Género", max_length=1, choices=SEX_CHOICES)
    date = models.DateField("Fecha de nacimiento", null=True, blank=True)
    
    def __str__(self):
        return self.username