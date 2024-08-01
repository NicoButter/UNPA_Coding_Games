from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import PersonajeCreationForm

def home_view(request):
    return render(request, 'capitol/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'capitol/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'capitol/login.html')

def register(request):
    if request.method == 'POST':
        form = PersonajeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PersonajeCreationForm()
    return render(request, 'capitol/register.html', {'form': form})
