from django.core.mail import send_mail

send_mail(
    "Confirmación de donación",
    f"Has realizado una donación de ${amount} para la solicitud {help_obj.title}.",
    "volunet@system.com",
    [request.user.email],
    fail_silently=False,
)
