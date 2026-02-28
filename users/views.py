from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserForm, CustomAuthenticationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import rotate_token


def principal(request):
    return render(request, 'users/principal.html')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Registro exitoso! Bienvenido a Voluntariado Digital.")
            return redirect('principal')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = UserForm()

    return render(request, 'users/register.html', {'form': form})


from django.middleware.csrf import rotate_token

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            rotate_token(request)
            messages.success(request, f"¡Bienvenido {user.name}!")

            if user.is_superuser or user.is_admin:
                return redirect('adminpanel:admin_dashboard')

            return redirect('principal')

        else:
            messages.error(request, "Correo o contraseña incorrectos.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'users/login.html', {'form': form})



def user_logout(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')


@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('principal')
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = ProfileForm(instance=user)

    return render(request, 'users/profile.html', {'form': form})


    return render(request, 'users/profile.html', {'form': form})

@login_required
def update_profile_image(request):
    if request.method == "POST":
        user = request.user
        image = request.FILES.get("profile_image")
        if image:
            user.profile_image = image
            user.save()
    return redirect("users:profile") 

@login_required
def verify_account(request):
    user = request.user

    if request.method == "POST":
        pdf = request.FILES.get("doc_pdf")
        photo = request.FILES.get("doc_id")

        if pdf:
            user.id_document_pdf = pdf

        if photo:
            user.id_document_image = photo

        # El usuario envió para revisión → is_verified sigue en False
        user.save()

        messages.success(request, "Tus documentos fueron enviados. El administrador revisará tu solicitud.")
        return redirect("users:profile")

    return redirect("users:profile")

