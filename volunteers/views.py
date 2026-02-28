from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction, models
from django.db.models import Sum
from .models import Help, Participation, Donation
from .forms import HelpForm
from core.utils import notify_admin


# ============================
#   CREAR SOLICITUD DE AYUDA
# ============================
@login_required
def create_help_request(request):
    """
    Permite crear nuevas solicitudes de ayuda y mostrar el historial y las activas.
    """
    if request.method == 'POST':
        form = HelpForm(request.POST, request.FILES)
        if form.is_valid():
            help_obj = form.save(commit=False)
            help_obj.volunteer = request.user
            help_obj.contact_number = request.user.phone_number
            help_obj.status = 'pending'  # por defecto pendiente
            help_obj.save()

            # ✅ Notificar al usuario
            send_mail(
                subject="📨 Tu solicitud ha sido enviada para revisión",
                message=f"Hola {request.user.name}, tu solicitud '{help_obj.title}' ha sido enviada correctamente y está en revisión.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
            )

            # ✅ Notificar al admin
            notify_admin(
                subject="🆕 Nueva solicitud enviada para revisión",
                message=f"El usuario {request.user.name} ha enviado la solicitud '{help_obj.title}'."
            )

            messages.success(request, "✅ Tu solicitud fue enviada correctamente y está en revisión.")
            return redirect('volunteers:help')
        else:
            messages.error(request, "⚠️ Corrige los errores del formulario.")
    else:
        form = HelpForm(initial={'contact_number': request.user.phone_number})

    # Mostrar solicitudes activas e historial
    active_requests = Help.objects.filter(
        volunteer=request.user,
        status__in=['pending', 'approved', 'active']
    ).order_by('-created_at')

    history_requests = Help.objects.filter(
        volunteer=request.user,
        status__in=['rejected', 'resubmit', 'closed']
    ).order_by('-created_at')

    return render(request, 'volunteers/help.html', {
        'form': form,
        'active_requests': active_requests,
        'history_requests': history_requests,
    })


# ============================
#   EDITAR SOLICITUD
# ============================
@login_required
def edit_request(request, pk):
    help_request = get_object_or_404(Help, pk=pk, volunteer=request.user)
    if request.method == "POST":
        form = HelpForm(request.POST, request.FILES, instance=help_request)
        if form.is_valid():
            form.save()
            help_request.status = "pending"
            help_request.save()

            # ✅ Notificar al usuario
            send_mail(
                subject="📩 Has actualizado tu solicitud",
                message=f"Hola {request.user.name}, tu solicitud '{help_request.title}' ha sido actualizada y enviada nuevamente para revisión.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
            )

            # ✅ Notificar al admin
            notify_admin(
                subject="🔄 Solicitud actualizada para revisión",
                message=f"El usuario {request.user.name} ha actualizado su solicitud '{help_request.title}' para revisión."
            )

            messages.success(request, "✅ Solicitud actualizada correctamente. Se notificó al administrador.")
            return redirect("volunteers:help")
        else:
            messages.error(request, "⚠️ Corrige los errores antes de guardar los cambios.")
    else:
        form = HelpForm(instance=help_request)

    return render(request, "volunteers/help_edit.html", {"form": form, "help_request": help_request})


# ============================
#   VOLUNTARIO DASHBOARD
# ============================
@login_required
def volunteer_dashboard(request):
    own_helps = Help.objects.filter(volunteer=request.user).values_list('id', flat=True)
    accepted_helps = Help.objects.filter(accepted_by=request.user, status='accepted').values_list('id', flat=True)
    combined_ids = list(own_helps) + list(accepted_helps)
    my_activities = Help.objects.filter(id__in=combined_ids).order_by('-created_at')

    active_requests = Help.objects.filter(status__in=['approved', 'active']).exclude(volunteer=request.user)
    participations = Participation.objects.filter(volunteer=request.user).values_list('help_id', flat=True)
    available_requests = active_requests.exclude(id__in=participations)

    return render(request, 'volunteers/volunteer.html', {
        'helps': my_activities,
        'volunteer_requests': available_requests,
        'participations': participations,
    })


# ============================
#   RECHAZAR / CERRAR SOLICITUD
# ============================
@login_required
def reject_request(request, pk):
    help_request = get_object_or_404(Help, pk=pk, volunteer=request.user)
    help_request.status = 'closed'
    help_request.save()
    messages.warning(request, f"La solicitud '{help_request.title}' fue cerrada correctamente.")
    return redirect('volunteers:volunteer_dashboard')


# ============================
#   ELIMINAR SOLICITUD
# ============================
@login_required
def delete_request(request, pk):
    help_request = get_object_or_404(Help, pk=pk, volunteer=request.user)
    if request.method == "POST":
        help_request.delete()
        return redirect("volunteers:help")
    return render(request, "volunteers/help_delete.html", {"help_request": help_request})


# ============================
#   DETALLE DE SOLICITUD
# ============================
@login_required
def request_detail(request, pk):
    help_request = get_object_or_404(Help, pk=pk)
    return render(request, 'volunteers/request_detail.html', {'solicitud': help_request})


# ============================
#   DONAR / PARTICIPAR
# ============================
@login_required
def donate_to_help(request, pk):
    help_obj = get_object_or_404(Help, pk=pk, status__in=['approved', 'active', 'accepted'])

    if request.method == "GET":
        return render(request, "volunteers/donate.html", {"help_obj": help_obj})

    elif request.method == "POST":
        amount = request.POST.get("amount")
        bank_name = request.POST.get("bank_name")
        account_type = request.POST.get("account_type")
        account_number = request.POST.get("account_number")

        if not amount or float(amount) <= 0:
            messages.error(request, "⚠️ Por favor ingresa un monto válido.")
            return render(request, "volunteers/donate.html", {"help_obj": help_obj})

        try:
            with transaction.atomic():
                donation = Donation.objects.create(
                    help=help_obj,
                    donor=request.user,
                    amount=amount,
                    payment_method=f"{bank_name} ({account_type}) - {account_number}",
                    status="completed"
                )

                help_obj.status = "accepted"
                help_obj.save()

            return redirect("volunteers:donation_success", pk=donation.pk)
        except Exception as e:
            messages.error(request, f"❌ Ocurrió un error al procesar la donación: {str(e)}")
            return render(request, "volunteers/donate.html", {"help_obj": help_obj})

    messages.error(request, "Método no permitido.")
    return redirect("volunteers:volunteer_dashboard")


# ============================
#   ÉXITO DE DONACIÓN
# ============================
@login_required
def donation_success(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    return render(request, "volunteers/donation_success.html", {"donation": donation})


# ============================
#   MIS SOLICITUDES
# ============================
@login_required
def my_requests(request):
    from django.db.models import Sum, Q
    requests = Help.objects.filter(volunteer=request.user).annotate(
        annotated_total_donations=Sum('donations__amount', filter=Q(donations__status='completed'))
    ).prefetch_related('donations__donor')
    
    for req in requests:
        current_donations = req.annotated_total_donations or 0
        req.donations_list = [d for d in req.donations.all() if d.status == 'completed']
        
        req.annotated_progress = 0
        if req.amount and req.amount > 0:
            req.annotated_progress = min((float(current_donations) / float(req.amount)) * 100, 100)

    return render(request, 'volunteers/my_requests.html', {'requests': requests})


# ============================
#   MIS DONACIONES
# ============================
@login_required
def my_donations(request):
    donations = Donation.objects.filter(donor=request.user).select_related('help')
    return render(request, 'volunteers/my_donations.html', {'donations': donations})
