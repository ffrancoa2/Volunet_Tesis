from django.shortcuts import render, redirect, get_object_or_404
from .models import Help
from .forms import HelpForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def volunteer_dashboard(request):
    own_helps = Help.objects.filter(volunteer=request.user).values_list('id', flat=True)
    accepted_helps = Help.objects.filter(accepted_by=request.user, status='accepted').values_list('id', flat=True)
    combined_ids = list(own_helps) + list(accepted_helps)
    my_activities = Help.objects.filter(id__in=combined_ids).order_by('-created_at')

    active_requests = Help.objects.filter(status='active').exclude(volunteer=request.user)

    return render(request, 'volunteers/volunteer.html', {
        'helps': my_activities,
        'requests_volunteer': active_requests,
    })

@login_required
def request_detail(request, pk):
    help_request = get_object_or_404(Help, pk=pk)
    return render(request, 'volunteers/request_detail.html', {'solicitud': help_request})


@login_required
def create_help_request(request):
    helps = Help.objects.filter(volunteer=request.user)
    if request.method == "POST":
        form = HelpForm(request.POST)
        if form.is_valid():
            help_request = form.save(commit=False)
            help_request.volunteer = request.user
            help_request.save()
            messages.success(request, "Solicitud publicada correctamente.")
            return redirect("volunteers:help")
        else:
            messages.error(request, "Corrige los errores antes de enviar el formulario.")
    else:
        form = HelpForm()
    return render(request, "volunteers/help.html", {
        "form": form,
        "requests": helps
    })


@login_required
def edit_request(request, pk):
    help_request = get_object_or_404(Help, pk=pk, volunteer=request.user)
    if request.method == "POST":
        form = HelpForm(request.POST, instance=help_request)
        if form.is_valid():
            form.save()
            return redirect("volunteers:help")
    else:
        form = HelpForm(instance=help_request)
    return render(request, "volunteers/help_edit.html", {"form": form})


@login_required
def delete_request(request, pk):
    help_request = get_object_or_404(Help, pk=pk, volunteer=request.user)
    if request.method == "POST":
        help_request.delete()
        return redirect("volunteers:help")
    return render(request, "volunteers/help_delete.html", {"help_request": help_request})


@login_required
def accept_request(request, pk):
    help_request = get_object_or_404(Help, pk=pk)
    if help_request.status == 'active':
        help_request.status = 'accepted'
        help_request.accepted_by = request.user
        help_request.save()
        messages.success(request, f"La solicitud '{help_request.title}' fue aceptada correctamente.")
    else:
        messages.warning(request, "Esta solicitud ya no está disponible.")
    return redirect('volunteers:volunteer_dashboard')


@login_required
def reject_request(request, pk):
    help_request = get_object_or_404(Help, pk=pk)
    help_request.status = 'closed'
    help_request.save()
    messages.warning(request, f"La solicitud '{help_request.title}' fue rechazada.")
    return redirect('volunteers:volunteer_dashboard')
