# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserForm, CustomAuthenticationForm
from django.forms.utils import ErrorDict

def principal(request):
    return render(request, 'users/principal.html')

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Registro exitoso!")
            return redirect('principal')
        else:
            request.session['form_errors'] = form.errors.get_json_data()
            request.session['form_data'] = request.POST.dict()
            return redirect('register')
    else:
        form = UserForm()
        if 'form_errors' in request.session:
            form._errors = ErrorDict(request.session.pop('form_errors'))
            form.data = request.session.pop('form_data')

    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "¡Bienvenido!")
            return redirect('principal')
        else:
            # Guardar errores y datos
            request.session['login_errors'] = form.errors.get_json_data()
            request.session['login_data'] = request.POST.dict()
            return redirect('login')  # REDIRECT → limpia POST
    else:
        form = CustomAuthenticationForm(request)
        # Cargar errores si existen
        if 'login_errors' in request.session:
            form._errors = ErrorDict(request.session.pop('login_errors'))
            form.data = request.session.pop('login_data', {})
              # Depuración
        else:
            form = CustomAuthenticationForm()  # Limpiar

    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('login')