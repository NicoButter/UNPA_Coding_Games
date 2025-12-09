from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Count, Q
from capitol.models import TributoInfo, Personaje


@login_required
def dashboard_view(request):
    """
    Vista principal del dashboard que redirige según el rol del usuario
    """
    user = request.user
    
    # Detectar rol y preparar contexto
    if user.rol == 'tributo':
        return tributo_dashboard(request)
    elif user.rol == 'vigilante':
        return vigilante_dashboard(request)
    elif user.rol == 'mentor':
        return mentor_dashboard(request)
    elif user.rol == 'jefe_capitolio':
        return jefe_capitolio_dashboard(request)
    else:
        return HttpResponseForbidden("Rol no reconocido")


def tributo_dashboard(request):
    """Dashboard para tributos"""
    try:
        tributo_info = request.user.tributo_info
    except TributoInfo.DoesNotExist:
        tributo_info = None
    
    tributo_actions = [
        {'title': 'Mi Perfil', 'url': '/perfil/', 'icon': '👤'},
        {'title': 'Arena de Entrenamiento', 'url': '#', 'icon': '🎮'},
        {'title': 'Ver Competencias', 'url': '#', 'icon': '🏆'},
        {'title': 'Mis Estadísticas', 'url': '#', 'icon': '📊'},
    ]
    
    context = {
        'tributo_info': tributo_info,
        'tributo_actions': tributo_actions,
    }
    return render(request, 'dashboards/tributo_dashboard.html', context)


def vigilante_dashboard(request):
    """Dashboard para vigilantes"""
    tributos = TributoInfo.objects.select_related('personaje').all()
    
    stats = {
        'total_tributos': tributos.count(),
        'pendientes': tributos.filter(estado='pendiente').count(),
        'acreditados': tributos.filter(estado='acreditado').count(),
        'activos': tributos.filter(estado='activo').count(),
    }
    
    tributos_recientes = tributos.order_by('-fecha_registro')[:10]
    
    # Estadísticas por distrito
    distritos_stats = []
    for i in range(1, 14):
        count = tributos.filter(distrito=i).count()
        if stats['total_tributos'] > 0:
            percentage = (count / stats['total_tributos']) * 100
        else:
            percentage = 0
        distritos_stats.append({
            'numero': i,
            'count': count,
            'percentage': percentage
        })
    
    vigilante_actions = [
        {'title': 'Acreditar Tributo', 'url': '/admin/capitol/tributoinfo/', 'icon': '✓'},
        {'title': 'Ver Todos los Tributos', 'url': '/admin/capitol/tributoinfo/', 'icon': '👥'},
        {'title': 'Escanear QR', 'url': '#', 'icon': '📷'},
        {'title': 'Generar Reporte', 'url': '#', 'icon': '📄'},
    ]
    
    recent_activities = [
        {'user': 'Juan Pérez', 'action': 'se registró como tributo', 'time': 'Hace 5 minutos'},
        {'user': 'María García', 'action': 'fue acreditada', 'time': 'Hace 15 minutos'},
        {'user': 'Sistema', 'action': 'generó credenciales masivas', 'time': 'Hace 1 hora'},
    ]
    
    context = {
        'stats': stats,
        'tributos_recientes': tributos_recientes,
        'distritos_stats': distritos_stats,
        'vigilante_actions': vigilante_actions,
        'recent_activities': recent_activities,
    }
    return render(request, 'dashboards/vigilante_dashboard.html', context)


def mentor_dashboard(request):
    """Dashboard para mentores"""
    # Por ahora, datos de ejemplo. Luego se conectará con el sistema de asignación
    mis_tributos = TributoInfo.objects.filter(
        estado__in=['acreditado', 'activo']
    ).select_related('personaje')[:6]
    
    stats = {
        'mis_tributos': mis_tributos.count(),
        'en_competencia': TributoInfo.objects.filter(estado='activo').count(),
        'victorias': 0,  # Implementar cuando exista sistema de competencias
        'distrito': request.user.tributo_info.distrito if hasattr(request.user, 'tributo_info') else 12,
    }
    
    mentor_actions = [
        {'title': 'Mis Tributos', 'url': '#', 'icon': '👥'},
        {'title': 'Crear Entrenamiento', 'url': '#', 'icon': '📝'},
        {'title': 'Revisar Progresos', 'url': '#', 'icon': '📊'},
        {'title': 'Mensajes', 'url': '#', 'icon': '💬'},
    ]
    
    context = {
        'mis_tributos': mis_tributos,
        'stats': stats,
        'mentor_actions': mentor_actions,
    }
    return render(request, 'dashboards/mentor_dashboard.html', context)


def jefe_capitolio_dashboard(request):
    """Dashboard para el jefe del Capitolio"""
    tributos = TributoInfo.objects.all()
    
    stats = {
        'total_tributos': tributos.count(),
        'competencias_activas': 0,  # Implementar cuando exista modelo de competencias
        'total_mentores': Personaje.objects.filter(rol='mentor').count(),
        'total_vigilantes': Personaje.objects.filter(rol='vigilante').count(),
        'nuevos_registros': tributos.filter(fecha_registro__gte='2025-12-01').count(),
        'tasa_participacion': 85,  # Calcularlo dinámicamente
        'competencias_completadas': 0,
    }
    
    # Detalles por distrito
    distritos_detalle = []
    for i in range(1, 14):
        distrito_tributos = tributos.filter(distrito=i)
        distritos_detalle.append({
            'numero': i,
            'total': distrito_tributos.count(),
            'unpa': distrito_tributos.filter(tipo='alumno_unpa').count(),
            'externos': distrito_tributos.filter(tipo='externo').count(),
            'acreditados': distrito_tributos.filter(estado='acreditado').count(),
            'activos': distrito_tributos.filter(estado='activo').count(),
        })
    
    jefe_actions = [
        {'title': 'Panel Admin', 'url': '/admin/', 'icon': '⚙️'},
        {'title': 'Nueva Competencia', 'url': '#', 'icon': '➕'},
        {'title': 'Gestionar Usuarios', 'url': '/admin/capitol/personaje/', 'icon': '👥'},
        {'title': 'Reportes Completos', 'url': '#', 'icon': '📊'},
    ]
    
    context = {
        'stats': stats,
        'distritos_detalle': distritos_detalle,
        'jefe_actions': jefe_actions,
    }
    return render(request, 'dashboards/jefe_capitolio_dashboard.html', context)
