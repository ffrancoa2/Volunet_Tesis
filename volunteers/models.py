from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Help(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobada'),
        ('rejected', 'Rechazada'),
        ('active', 'Activa'),
        ('accepted', 'Aceptada'), # Agregado para evitar estados huérfanos
        ('resubmit', 'Pendiente de Reenvío'),
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

    accepted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='accepted_helps'
    )

    title = models.CharField("Título de la ayuda", max_length=100)
    description = models.TextField("Descripción de la ayuda")
    category = models.CharField("Categoría", max_length=50, choices=CATEGORY_CHOICES, default='otro')
    location = models.CharField("Ubicación", max_length=100, null=True, blank=True)
    lat = models.FloatField("Latitud", null=True, blank=True)
    lng = models.FloatField("Longitud", null=True, blank=True)
    date_start = models.DateField("Fecha de inicio", null=True, blank=True)
    date_end = models.DateField("Fecha de fin", null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)

    # Campos adicionales
    contact_number = models.CharField("Número de contacto", max_length=10, null=True, blank=True)
    bank_account = models.CharField("Número de cuenta bancaria", max_length=30, null=True, blank=True)
    evidence_pdf = models.FileField("Documento de respaldo (PDF)", upload_to="helps/pdf/", null=True, blank=True)
    evidence_image = models.ImageField("Fotografía o evidencia", upload_to="helps/images/", null=True, blank=True)
    dni_copy = models.ImageField("Copia de cédula", upload_to="helps/dni/", null=True, blank=True)
    amount = models.DecimalField("Monto solicitado", max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Solicitud de Ayuda"
        verbose_name_plural = "Solicitudes de Ayuda"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.volunteer.email}"

    def save(self, *args, **kwargs):
        if self.date_end and self.date_end < timezone.now().date():
            self.status = 'closed'
        super().save(*args, **kwargs)

    @property
    def total_donations(self):
        return self.donations.filter(status='completed').aggregate(models.Sum('amount'))['amount__sum'] or 0

    @property
    def progress(self):
        if not self.amount or self.amount <= 0:
            return 0
        return min(float(self.total_donations / self.amount * 100), 100)


class Participation(models.Model):
    help = models.ForeignKey(Help, on_delete=models.CASCADE, related_name='participations')
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('help', 'volunteer')
        verbose_name = "Participación"
        verbose_name_plural = "Participaciones"

    def __str__(self):
        return f"{self.volunteer.email} en {self.help.title}"


class Donation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('completed', 'Completada'),
        ('failed', 'Fallida'),
    ]

    help = models.ForeignKey(
        Help,
        on_delete=models.CASCADE,
        related_name='donations',
        verbose_name='Solicitud de ayuda'
    )
    donor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='donations',
        verbose_name='Donante'
    )
    amount = models.DecimalField('Monto donado', max_digits=10, decimal_places=2)
    payment_method = models.CharField('Método de pago', max_length=30, default='manual')
    status = models.CharField('Estado', max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)

    class Meta:
        verbose_name = 'Donación'
        verbose_name_plural = 'Donaciones'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.donor.email} → {self.help.title} (${self.amount})"
