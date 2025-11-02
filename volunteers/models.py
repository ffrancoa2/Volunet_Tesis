from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Help(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activa'),
        ('pending', 'Pendiente'),
        ('accepted', 'Aceptada'),
        ('closed', 'Cerrada'),
    ]

    CATEGORY_CHOICES = [
        ('salud', 'Salud'),
        ('educacion', 'Educación'),
        ('donacion', 'Donación'),
        ('dinero', 'Dinero'),
        ('alimentos', 'Alimentos'),
        ('comunidad', 'Comunidad'),
        ('otro', 'Otro'),
    ]

    volunteer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='helps'
    )

    accepted_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='accepted_helps')
    title = models.CharField("Título de la ayuda", max_length=100)
    description = models.TextField("Descripción de la ayuda")
    category = models.CharField("Categoría", max_length=50, choices=CATEGORY_CHOICES, default='otro')
    location = models.CharField("Ubicación", max_length=100, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    date_start = models.DateField("Fecha de inicio", null=True, blank=True)
    date_end = models.DateField("Fecha de fin", null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)
    account_number = models.CharField("Número de cuenta", max_length=30, null=True, blank=True)
    amount = models.DecimalField("Monto solicitado", max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Solicitud de Ayuda"
        verbose_name_plural = "Solicitudes de Ayuda"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.volunteer.username}"

    def save(self, *args, **kwargs):
        if self.date_end and self.date_end < timezone.now().date():
            self.status = 'closed'
        super().save(*args, **kwargs)
