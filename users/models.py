from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El correo electrónico es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    SEX_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    username = None
    email = models.EmailField("Correo Electrónico", unique=True)

    name = models.CharField("Nombres", max_length=100)
    last_name = models.CharField("Apellidos", max_length=100)
    sex = models.CharField("Género", max_length=1, choices=SEX_CHOICES)

    is_admin = models.BooleanField("Administrador del Sistema", default=False)


    date = models.DateField("Fecha de nacimiento", null=True, blank=True)
    phone_number = models.CharField("Número de teléfono", max_length=10, null=True, blank=True)
    dni = models.CharField("DNI", max_length=10, null=True, blank=True)

    profile_image = models.ImageField("Foto de perfil", upload_to="profiles/", null=True, blank=True)

    id_document_pdf = models.FileField(
        "Documento PDF validado",
        upload_to="documents/pdf/",
        null=True,
        blank=True
    )

    id_document_image = models.FileField(
        "Foto de cédula o selfie",
        upload_to="documents/images/",
        null=True,
        blank=True
    )

    bank_account = models.CharField(
        "Cuenta Bancaria",
        max_length=20,
        null=True,
        blank=True
    )

    is_verified = models.BooleanField("Cuenta verificada", default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def total_points(self):
        # Evitar importación circular
        from volunteers.models import Help, Participation
        completed_count = self.helps.filter(status='closed').count()
        participations_count = self.participations.count()
        return (completed_count * 10) + (participations_count * 5)
