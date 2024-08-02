from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AcreditacionForm
from django.http import HttpResponseForbidden

@login_required
def acreditar_tributo(request):
    if request.user.rol != 'vigilante':
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    if request.method == 'POST':
        form = AcreditacionForm(request.POST)
        if form.is_valid():
            tributo_info = form.save(commit=False)
            tributo_info.personaje = request.user
            tributo_info.save()
            return redirect('success')  
    else:
        form = AcreditacionForm()
    return render(request, 'centro_control/acreditar_tributo.html', {'form': form})
