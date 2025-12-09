from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PersonajeRegistroForm, TributoInfoForm, CustomAuthenticationForm
from .models import TributoInfo


def home_view(request):
    return render(request, 'capitol/index.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboards:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido de vuelta, {user.get_full_name()}!')
            
            # Redirigir al dashboard
            return redirect('dashboards:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'capitol/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('home')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        user_form = PersonajeRegistroForm(request.POST, request.FILES)
        tributo_form = TributoInfoForm(request.POST)
        
        if user_form.is_valid() and tributo_form.is_valid():
            # Crear el usuario
            user = user_form.save(commit=False)
            user.rol = 'tributo'  # Por defecto todos los registros son tributos
            user.save()
            
            # Crear la información del tributo
            tributo = tributo_form.save(commit=False)
            tributo.personaje = user
            tributo.save()
            
            messages.success(request, 
                f'¡Registro exitoso! Tu código de tributo es: {tributo.codigo_tributo}. '
                'Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        user_form = PersonajeRegistroForm()
        tributo_form = TributoInfoForm()
    
    context = {
        'user_form': user_form,
        'tributo_form': tributo_form,
    }
    return render(request, 'capitol/register.html', context)

@login_required
def perfil_view(request):
    """Vista del perfil del tributo"""
    try:
        tributo_info = request.user.tributo_info
    except TributoInfo.DoesNotExist:
        tributo_info = None
    
    context = {
        'tributo_info': tributo_info,
    }
    return render(request, 'capitol/perfil.html', context)

