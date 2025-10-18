from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout 
from .forms import UserForm

def home(request):
    return render(request, 'home.html')

def principal(request):
    return render(request, 'principal.html')

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Credenciales inválidas")
    return render(request, 'login.html')
def user_logout(request):
    logout(request)  # 🧹 elimina la sesión actual del usuario
    return redirect('login')  
