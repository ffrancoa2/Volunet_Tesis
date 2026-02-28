from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import User
from django.db.models import Count
from volunteers.models import Help, Participation
from users.forms import ProfileForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from core.utils import notify_admin


# -----------------------------
# Decorador de acceso admin
# -----------------------------
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.is_admin:
            return render(request, "adminpanel/access_denied.html")
        return view_func(request, *args, **kwargs)
    return wrapper


# -----------------------------
# Perfil del administrador
# -----------------------------
@login_required
@admin_required
def admin_profile(request):
    return render(request, "adminpanel/admin_profile.html")


@login_required
@admin_required
def admin_edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Tu perfil ha sido actualizado correctamente.")
            return redirect("adminpanel:admin_profile")
        else:
            messages.error(request, "⚠️ Corrige los errores del formulario.")
    else:
        form = ProfileForm(instance=user)
    return render(request, "adminpanel/admin_edit_profile.html", {"form": form})


# -----------------------------
# Gestión de usuarios
# -----------------------------
@login_required
@admin_required
def users_list(request):
    users = User.objects.all().order_by('-id')
    return render(request, "adminpanel/users_list.html", {"users": users})


@login_required
@admin_required
def user_detail(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    return render(request, "adminpanel/users_detail.html", {"user_obj": user_obj})


@login_required
@admin_required
def verify_user(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    user_obj.is_verified = True
    user_obj.save()
    messages.success(request, f"✅ El usuario {user_obj.name} fue verificado correctamente.")
    return redirect("adminpanel:users_list")


# -----------------------------
# Dashboard Principal
# -----------------------------
@login_required
@admin_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_volunteers = User.objects.filter(is_admin=False, is_superuser=False).count()
    pending_requests = Help.objects.filter(status='pending').count()
    approved_requests = Help.objects.filter(status='approved').count()
    rejected_requests = Help.objects.filter(status='rejected').count()
    active_requests = Help.objects.filter(status='active').count()
    closed_requests = Help.objects.filter(status='closed').count()
    recent_requests = Help.objects.all().order_by('-created_at')[:5]

    top_helpers = (
        Participation.objects
        .values('volunteer__name', 'volunteer__last_name')
        .annotate(total_helps=Count('help'))
        .order_by('-total_helps')[:5]
    )

    return render(request, 'adminpanel/dashboard.html', {
        'total_users': total_users,
        'total_volunteers': total_volunteers,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests,
        'active_requests': active_requests,
        'closed_requests': closed_requests,
        'recent_requests': recent_requests,
        'top_helpers': top_helpers,
    })


# -----------------------------
# Gestión de solicitudes de ayuda
# -----------------------------
@login_required
@admin_required
def helps_list(request):
    helps = Help.objects.all().order_by('-created_at')
    return render(request, "adminpanel/helps_list.html", {"helps": helps})


@login_required
@admin_required
def help_detail(request, help_id):
    help_obj = get_object_or_404(Help, id=help_id)
    return render(request, "adminpanel/help_detail.html", {"help_obj": help_obj})


# -----------------------------
# Acciones del administrador
# -----------------------------
@login_required
@admin_required
def approve_help(request, help_id):
    """Aprobar solicitud y notificar a usuarios y admin."""
    help_obj = get_object_or_404(Help, id=help_id)
    help_obj.status = 'approved'
    help_obj.save()

    current_site = get_current_site(request)
    help_url = f"http://{current_site.domain}/volunteers/help/detail/{help_obj.id}/"

    # Notificar solicitante
    send_mail(
        subject='✅ Tu solicitud ha sido aprobada',
        message=(
            f"Hola {help_obj.volunteer.name},\n\n"
            f"Tu solicitud '{help_obj.title}' ha sido aprobada.\n"
            f"Puedes verla aquí: {help_url}\n\n"
            f"Gracias por usar Volunet 💚"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[help_obj.volunteer.email],
    )

    # Notificar a otros usuarios
    other_users = User.objects.filter(is_active=True).exclude(id=help_obj.volunteer.id)
    emails = [u.email for u in other_users if u.email]
    if emails:
        send_mail(
            subject='💚 Nueva solicitud de ayuda disponible',
            message=(
                f"{help_obj.volunteer.name} necesita apoyo en '{help_obj.title}'.\n"
                f"Participa aquí: {help_url}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=emails,
            fail_silently=True,
        )

    # Notificar al administrador
    notify_admin(
        subject='📢 Nueva solicitud aprobada',
        message=(
            f"El usuario {help_obj.volunteer.name} publicó la solicitud '{help_obj.title}', "
            f"que ha sido aprobada correctamente."
        )
    )

    messages.success(request, f"La solicitud '{help_obj.title}' fue aprobada y notificada.")
    return redirect('adminpanel:helps_list')


@login_required
@admin_required
def reject_help(request, help_id):
    """Rechazar solicitud y notificar a usuario y admin."""
    help_obj = get_object_or_404(Help, id=help_id)
    help_obj.status = 'rejected'
    help_obj.save()

    send_mail(
        subject='❌ Tu solicitud fue rechazada',
        message=(
            f"Hola {help_obj.volunteer.name},\n\n"
            f"Lamentamos informarte que tu solicitud '{help_obj.title}' fue rechazada.\n"
            f"Puedes revisar los detalles en tu panel.\n\n"
            f"Equipo Volunet 💚"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[help_obj.volunteer.email],
    )

    notify_admin(
        subject='📢 Solicitud rechazada',
        message=(
            f"El usuario {help_obj.volunteer.name} envió la solicitud '{help_obj.title}', "
            f"que fue rechazada por el administrador."
        )
    )

    messages.error(request, f"La solicitud '{help_obj.title}' fue rechazada.")
    return redirect('adminpanel:helps_list')


@login_required
@admin_required
def request_resubmit_help(request, help_id):
    """Solicitar reenvío de documentos y notificar al usuario."""
    help_obj = get_object_or_404(Help, id=help_id)
    help_obj.status = 'resubmit'
    help_obj.save()

    current_site = get_current_site(request)
    action_url = f"http://{current_site.domain}/volunteers/help/edit/{help_obj.id}/?open_modal=true"

    html_content = render_to_string('emails/base_notification.html', {
        'name': help_obj.volunteer.name,
        'message': f"Tu solicitud <strong>{help_obj.title}</strong> necesita que vuelvas a subir los documentos o imágenes.",
        'action_url': action_url
    })

    text_content = (
        f"Hola {help_obj.volunteer.name}, tu solicitud '{help_obj.title}' "
        f"necesita que vuelvas a subir los documentos. Revisa aquí: {action_url}"
    )

    msg = EmailMultiAlternatives(
        subject='🔄 Reenvío de documentos solicitado',
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[help_obj.volunteer.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    # Notificar al admin
    notify_admin(
        subject='📢 Solicitud marcada como reenvío',
        message=f"La solicitud '{help_obj.title}' fue marcada como 'Pendiente de Reenvío'."
    )

    messages.warning(request, f"La solicitud '{help_obj.title}' fue marcada como 'Pendiente de Reenvío'.")
    return redirect('adminpanel:helps_list')
