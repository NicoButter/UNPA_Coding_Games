"""
Middleware para validar acreditación de tributos antes de acceder al arena
"""
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


class AccreditationMiddleware:
    """
    Middleware que verifica que los tributos estén acreditados antes de acceder al arena
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Rutas del arena que requieren acreditación
        arena_paths = ['/arena/torneo/', '/arena/reto/']
        
        # Verificar si la ruta actual es del arena
        is_arena_path = any(request.path.startswith(path) for path in arena_paths)
        
        if is_arena_path and request.user.is_authenticated:
            # Solo aplicar a tributos
            if request.user.rol == 'tributo':
                try:
                    tributo_info = request.user.tributoinfo
                    
                    # Verificar estado de acreditación
                    if tributo_info.estado not in ['acreditado', 'activo', 'ganador']:
                        messages.warning(
                            request,
                            f'Debes estar acreditado para acceder al arena. '
                            f'Estado actual: {tributo_info.get_estado_display()}'
                        )
                        return redirect('dashboards:dashboard')
                        
                except AttributeError:
                    messages.error(request, 'No se encontró información de tributo')
                    return redirect('dashboards:dashboard')
        
        response = self.get_response(request)
        return response
