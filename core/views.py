from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from volunteers.models import Help, Participation



def home(request):
    return render(request, 'core/home.html')



@login_required
def principal(request):
    user = request.user

    # --- Estadísticas ---
    active_helps = Help.objects.filter(volunteer=user, status='active').count()
    completed_helps = Help.objects.filter(volunteer=user, status='closed').count()

    # --- Actividad reciente ---
    recent_activity = Help.objects.filter(volunteer=user).order_by('-created_at')[:3]

    context = {
        "active_helps": active_helps,
        "completed_helps": completed_helps,
        "total_points": user.total_points,  # Ahora centralizado en el modelo
        "recent_activity": recent_activity,
    }
    return render(request, "core/principal.html", context)



