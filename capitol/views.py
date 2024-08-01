from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import PersonajeCreationForm
from .forms import CustomAuthenticationForm


def home_view(request):
    return render(request, 'capitol/index.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirige a una página después del inicio de sesión
    else:
        form = CustomAuthenticationForm()

    return render(request, 'capitol/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = PersonajeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PersonajeCreationForm()
    return render(request, 'capitol/register.html', {'form': form})
