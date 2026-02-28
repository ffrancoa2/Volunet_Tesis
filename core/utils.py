from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

def send_volunet_email(subject, template_name, context, recipient_list, from_email=None):
    """
    Helper universal para enviar correos con soporte HTML y texto plano.
    """
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL
    
    # Intentar cargar la versión HTML
    try:
        html_content = render_to_string(f'emails/{template_name}.html', context)
    except:
        html_content = None

    # Intentar cargar la versión de texto (o usar un backup)
    try:
        text_content = render_to_string(f'emails/{template_name}.txt', context)
    except:
        # Fallback si no hay .txt: remover tags HTML rudimentariamente si existe html_content
        if html_content:
            from django.utils.html import strip_tags
            text_content = strip_tags(html_content)
        else:
            text_content = context.get('message', '')

    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    if html_content:
        msg.attach_alternative(html_content, "text/html")
    
    return msg.send(fail_silently=True)

def notify_admin(subject, message):
    """
    Notifica al administrador del sistema usando los settings configurados.
    """
    admin_email = getattr(settings, 'ADMIN_EMAIL', 'ffrancoa2@unemi.edu.ec') # Mantiene compatible el actual por si no está en settings
    return send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[admin_email],
        fail_silently=True
    )
