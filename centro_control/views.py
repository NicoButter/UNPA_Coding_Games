from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AcreditacionForm
from django.http import HttpResponseForbidden
from capitol.models import TributoInfo

@login_required
def dashboard(request):
    """Dashboard principal del centro de control"""
    if request.user.rol not in ['vigilante', 'jefe_capitolio']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    # Obtener estadísticas
    tributos = TributoInfo.objects.all()
    total_tributos = tributos.count()
    pendientes = tributos.filter(estado='pendiente').count()
    acreditados = tributos.filter(estado='acreditado').count()
    activos = tributos.filter(estado='activo').count()
    
    context = {
        'tributos': tributos.order_by('-fecha_registro')[:10],  # Últimos 10
        'total_tributos': total_tributos,
        'pendientes': pendientes,
        'acreditados': acreditados,
        'activos': activos,
    }
    return render(request, 'centro_control/dashboard.html', context)

@login_required
def acreditar_tributo(request, tributo_id):
    """Acreditar un tributo específico"""
    if request.user.rol not in ['vigilante', 'jefe_capitolio']:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    tributo_info = get_object_or_404(TributoInfo, id=tributo_id)
    
    if request.method == 'POST':
        form = AcreditacionForm(request.POST, instance=tributo_info)
        if form.is_valid():
            tributo = form.save(commit=False)
            tributo.acreditar()  # Usar el método del modelo
            messages.success(request, f'Tributo {tributo.codigo_tributo} acreditado exitosamente.')
            return redirect('centro_control:dashboard')  
    else:
        form = AcreditacionForm(instance=tributo_info)
    
    context = {
        'form': form,
        'tributo_info': tributo_info,
    }
    return render(request, 'centro_control/acreditar_tributo.html', context)
