from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from capitol.models import TributoInfo, Personaje
from arena.models import AyudaMentor, Torneo
from .forms import AsignarMentorForm, AsignarVigilantesForm, AsignarTributoMentorForm, EnviarAyudaForm


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
    
    # Ayudas recibidas del mentor (no leídas)
    ayudas_pendientes = []
    ayudas_recientes = []
    if tributo_info:
        ayudas_pendientes = AyudaMentor.objects.filter(
            tributo=tributo_info,
            leida=False
        ).order_by('-fecha_envio')[:5]
        
        ayudas_recientes = AyudaMentor.objects.filter(
            tributo=tributo_info,
            leida=True
        ).order_by('-fecha_lectura')[:3]
    
    tributo_actions = [
        {'title': 'Mi Gafete', 'url': '/gafete/ver/', 'icon': '🎫'},
        {'title': 'Torneos Disponibles', 'url': '/arena/torneos/', 'icon': '🏆'},
        {'title': 'Mensajes de mi Mentor', 'url': '/tributo/ayudas/', 'icon': '💬'},
        {'title': 'Descargar Gafete PDF', 'url': '/gafete/descargar/', 'icon': '📄'},
    ]
    
    context = {
        'tributo_info': tributo_info,
        'tributo_actions': tributo_actions,
        'ayudas_pendientes': ayudas_pendientes,
        'ayudas_recientes': ayudas_recientes,
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
        {'title': 'Escanear QR para Acreditar', 'url': '/acreditar/qr/', 'icon': '📷'},
        {'title': 'Panel de Monitoreo en Vivo', 'url': '/vigilante/monitoreo/', 'icon': '📺'},
        {'title': 'Ver Todos los Tributos', 'url': '/admin/capitol/tributoinfo/', 'icon': '👥'},
        {'title': 'Terminal de Login (Webcam)', 'url': '/login/webcam/', 'icon': '🎮'},
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
    # Tributos asignados a este mentor
    mis_tributos = TributoInfo.objects.filter(
        mentor=request.user
    ).select_related('personaje').order_by('-fecha_registro')
    
    # Obtener o crear presupuesto
    from arena.models import PresupuestoMentor
    presupuesto, created = PresupuestoMentor.objects.get_or_create(
        mentor=request.user,
        defaults={
            'puntos_totales': 1000,
            'max_ayudas_por_dia': 10,
        }
    )
    
    # Estadísticas del mentor
    stats = {
        'mis_tributos': mis_tributos.count(),
        'acreditados': mis_tributos.filter(estado='acreditado').count(),
        'en_competencia': mis_tributos.filter(estado='activo').count(),
        'ganadores': mis_tributos.filter(estado='ganador').count(),
        'unidad_academica': request.user.unidad_academica or 'No asignada',
        'distrito': request.user.distrito_asignado or 'No asignado',
        'puntos_patrocinio': presupuesto.puntos_disponibles,
    }
    
    # Ayudas enviadas recientemente
    ayudas_enviadas = AyudaMentor.objects.filter(
        mentor=request.user
    ).select_related('tributo__personaje').order_by('-fecha_envio')[:10]
    
    mentor_actions = [
        {'title': 'Mis Tributos', 'url': '/mentor/tributos/', 'icon': '👥'},
        {'title': 'Enviar Ayuda/Pista', 'url': '/mentor/enviar-ayuda/', 'icon': '💡'},
        {'title': 'Revisar Progresos', 'url': '/mentor/progresos/', 'icon': '📊'},
        {'title': 'Historial de Ayudas', 'url': '/mentor/historial-ayudas/', 'icon': '📜'},
    ]
    
    context = {
        'mis_tributos': mis_tributos,
        'stats': stats,
        'mentor_actions': mentor_actions,
        'ayudas_enviadas': ayudas_enviadas,
        'presupuesto': presupuesto,
    }
    return render(request, 'dashboards/mentor_dashboard.html', context)


def jefe_capitolio_dashboard(request):
    """Dashboard para el jefe del Capitolio"""
    tributos = TributoInfo.objects.all()
    torneos = Torneo.objects.all()
    
    stats = {
        'total_tributos': tributos.count(),
        'torneos_activos': torneos.filter(estado__in=['inscripcion', 'en_curso']).count(),
        'total_mentores': Personaje.objects.filter(rol='mentor').count(),
        'total_vigilantes': Personaje.objects.filter(rol='vigilante').count(),
        'mentores_sin_asignar': Personaje.objects.filter(rol='mentor', unidad_academica__isnull=True).count(),
        'tributos_sin_mentor': tributos.filter(mentor__isnull=True).count(),
        'nuevos_registros': tributos.filter(fecha_registro__gte='2025-12-01').count(),
    }
    
    # Detalles por distrito
    distritos_detalle = []
    for i in range(1, 14):
        distrito_tributos = tributos.filter(distrito=i)
        mentor_distrito = Personaje.objects.filter(rol='mentor', distrito_asignado=i).first()
        distritos_detalle.append({
            'numero': i,
            'total': distrito_tributos.count(),
            'mentor': mentor_distrito.get_full_name() if mentor_distrito else 'Sin asignar',
            'unpa': distrito_tributos.filter(tipo='alumno_unpa').count(),
            'externos': distrito_tributos.filter(tipo='externo').count(),
            'acreditados': distrito_tributos.filter(estado='acreditado').count(),
            'activos': distrito_tributos.filter(estado='activo').count(),
        })
    
    # Torneos recientes
    torneos_recientes = torneos.order_by('-fecha_creacion')[:5]
    
    jefe_actions = [
        {'title': 'Asignar Mentores', 'url': '/jefe/asignar-mentores/', 'icon': '🎯'},
        {'title': 'Asignar Vigilantes', 'url': '/jefe/asignar-vigilantes/', 'icon': '👮'},
        {'title': 'Crear Torneo', 'url': '/admin/arena/torneo/add/', 'icon': '➕'},
        {'title': 'Panel Admin Completo', 'url': '/admin/', 'icon': '⚙️'},
        {'title': 'Gestionar Usuarios', 'url': '/admin/capitol/personaje/', 'icon': '👥'},
        {'title': 'Reportes Completos', 'url': '/jefe/reportes/', 'icon': '📊'},
    ]
    
    context = {
        'stats': stats,
        'distritos_detalle': distritos_detalle,
        'jefe_actions': jefe_actions,
        'torneos_recientes': torneos_recientes,
    }
    return render(request, 'dashboards/jefe_capitolio_dashboard.html', context)


# ============= VISTAS PARA JEFE DEL CAPITOLIO =============

@login_required
def asignar_mentores_view(request):
    """Vista para que el Jefe del Capitolio asigne mentores a distritos"""
    if request.user.rol != 'jefe_capitolio':
        return HttpResponseForbidden("Solo el Jefe del Capitolio puede asignar mentores")
    
    mentores = Personaje.objects.filter(rol='mentor').order_by('distrito_asignado', 'username')
    
    if request.method == 'POST':
        mentor_id = request.POST.get('mentor_id')
        mentor = get_object_or_404(Personaje, id=mentor_id, rol='mentor')
        form = AsignarMentorForm(request.POST, instance=mentor)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'Mentor {mentor.get_full_name()} asignado exitosamente')
            return redirect('dashboards:asignar_mentores')
    
    context = {
        'mentores': mentores,
        'form': AsignarMentorForm(),
    }
    return render(request, 'dashboards/asignar_mentores.html', context)


@login_required
def asignar_vigilantes_view(request):
    """Vista para que el Jefe del Capitolio asigne vigilantes a torneos"""
    if request.user.rol != 'jefe_capitolio':
        return HttpResponseForbidden("Solo el Jefe del Capitolio puede asignar vigilantes")
    
    torneos = Torneo.objects.all().prefetch_related('vigilantes_asignados').order_by('-fecha_inicio')
    vigilantes = Personaje.objects.filter(rol='vigilante').order_by('username')
    
    if request.method == 'POST':
        torneo_id = request.POST.get('torneo_id')
        torneo = get_object_or_404(Torneo, id=torneo_id)
        vigilantes_ids = request.POST.getlist('vigilantes')
        
        torneo.vigilantes_asignados.set(vigilantes_ids)
        messages.success(request, f'Vigilantes asignados al torneo {torneo.nombre}')
        return redirect('dashboards:asignar_vigilantes')
    
    context = {
        'torneos': torneos,
        'vigilantes': vigilantes,
    }
    return render(request, 'dashboards/asignar_vigilantes.html', context)


# ============= VISTAS PARA MENTORES =============

@login_required
def enviar_ayuda_view(request):
    """Vista para que el mentor envíe ayudas a sus tributos"""
    if request.user.rol != 'mentor':
        return HttpResponseForbidden("Solo los mentores pueden enviar ayudas")
    
    # Obtener o crear presupuesto del mentor
    from arena.models import PresupuestoMentor, obtener_costo_ayuda
    presupuesto, created = PresupuestoMentor.objects.get_or_create(
        mentor=request.user,
        defaults={
            'puntos_totales': 1000,
            'max_ayudas_por_dia': 10,
        }
    )
    
    if request.method == 'POST':
        form = EnviarAyudaForm(request.POST, mentor=request.user)
        
        if form.is_valid():
            tipo_ayuda = form.cleaned_data['tipo']
            costo = obtener_costo_ayuda(tipo_ayuda)
            
            # Verificar si puede enviar la ayuda
            puede_enviar, mensaje = presupuesto.puede_enviar_ayuda(costo)
            
            if not puede_enviar:
                messages.error(request, mensaje)
            else:
                ayuda = form.save(commit=False)
                ayuda.mentor = request.user
                ayuda.costo_puntos = costo
                ayuda.save()
                
                # Gastar puntos
                presupuesto.gastar_puntos(costo)
                
                messages.success(
                    request, 
                    f'Ayuda enviada a {ayuda.tributo.personaje.get_full_name()}. '
                    f'Costo: {costo} pts. Puntos restantes: {presupuesto.puntos_disponibles}'
                )
                return redirect('dashboards:dashboard')
    else:
        form = EnviarAyudaForm(mentor=request.user)
    
    # Estadísticas de ayudas de hoy
    hoy = timezone.now().date()
    ayudas_hoy = AyudaMentor.objects.filter(
        mentor=request.user,
        fecha_envio__date=hoy
    ).count()
    
    from arena.models import COSTOS_AYUDAS
    
    context = {
        'form': form,
        'mis_tributos': TributoInfo.objects.filter(mentor=request.user),
        'presupuesto': presupuesto,
        'ayudas_hoy': ayudas_hoy,
        'costos_ayudas': COSTOS_AYUDAS,
    }
    return render(request, 'dashboards/enviar_ayuda.html', context)


@login_required
def mis_tributos_view(request):
    """Vista para que el mentor vea sus tributos asignados"""
    if request.user.rol != 'mentor':
        return HttpResponseForbidden("Solo los mentores pueden ver esta página")
    
    tributos = TributoInfo.objects.filter(
        mentor=request.user
    ).select_related('personaje').order_by('-fecha_registro')
    
    context = {
        'tributos': tributos,
    }
    return render(request, 'dashboards/mis_tributos.html', context)


# ============= VISTAS PARA TRIBUTOS =============

@login_required
def ver_ayudas_view(request):
    """Vista para que el tributo vea las ayudas de su mentor"""
    try:
        tributo_info = request.user.tributo_info
    except TributoInfo.DoesNotExist:
        messages.error(request, 'No tienes información de tributo')
        return redirect('dashboards:dashboard')
    
    # Marcar ayudas como leídas si se accede con parámetro
    ayuda_id = request.GET.get('marcar_leida')
    if ayuda_id:
        ayuda = get_object_or_404(AyudaMentor, id=ayuda_id, tributo=tributo_info)
        ayuda.marcar_como_leida()
    
    ayudas = AyudaMentor.objects.filter(
        tributo=tributo_info
    ).select_related('mentor', 'reto').order_by('-fecha_envio')
    
    context = {
        'ayudas': ayudas,
        'ayudas_pendientes': ayudas.filter(leida=False).count(),
    }
    return render(request, 'dashboards/ver_ayudas.html', context)


# ============= API PARA NOTIFICACIONES =============

@login_required
def check_notifications_api(request):
    """API endpoint para verificar notificaciones en tiempo real"""
    try:
        tributo_info = request.user.tributo_info
        ayudas_pendientes = AyudaMentor.objects.filter(
            tributo=tributo_info,
            leida=False
        ).count()
        
        return JsonResponse({
            'success': True,
            'ayudas_pendientes': ayudas_pendientes,
            'timestamp': timezone.now().isoformat()
        })
    except TributoInfo.DoesNotExist:
        return JsonResponse({
            'success': True,
            'ayudas_pendientes': 0,
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# ============= PANEL DE MONITOREO PARA VIGILANTES =============

@login_required
def panel_monitoreo_view(request):
    """Panel de monitoreo en vivo para vigilantes"""
    if request.user.rol != 'vigilante':
        return HttpResponseForbidden("Solo los vigilantes pueden acceder al panel de monitoreo")
    
    return render(request, 'dashboards/panel_monitoreo.html')


@login_required
def monitor_tributos_api(request):
    """API endpoint para obtener datos en tiempo real de tributos"""
    if request.user.rol != 'vigilante':
        return JsonResponse({'error': 'Acceso denegado'}, status=403)
    
    filter_type = request.GET.get('filter', 'all')
    
    # Obtener tributos según filtro
    tributos = TributoInfo.objects.select_related('personaje').all()
    
    if filter_type != 'all':
        tributos = tributos.filter(estado=filter_type)
    
    # Estadísticas generales
    hoy = timezone.now().date()
    from arena.models import ParticipacionTributo
    
    stats = {
        'total': TributoInfo.objects.count(),
        'activos': TributoInfo.objects.filter(estado='activo').count(),
        'acreditados': TributoInfo.objects.filter(estado='acreditado').count(),
        'completados_hoy': ParticipacionTributo.objects.filter(
            fecha_completado__date=hoy,
            estado='completado'
        ).count(),
    }
    
    # Datos de cada tributo
    tributos_data = []
    for tributo in tributos:
        # Obtener participaciones
        participaciones = ParticipacionTributo.objects.filter(tributo=tributo)
        total_participaciones = participaciones.count()
        completados = participaciones.filter(estado='completado').count()
        puntos_totales = sum([p.puntos_obtenidos for p in participaciones if p.puntos_obtenidos])
        
        # Última actividad
        ultima_participacion = participaciones.order_by('-fecha_envio').first()
        if ultima_participacion:
            tiempo_transcurrido = timezone.now() - ultima_participacion.fecha_envio
            if tiempo_transcurrido.seconds < 60:
                ultima_actividad = "Hace menos de 1 min"
            elif tiempo_transcurrido.seconds < 3600:
                ultima_actividad = f"Hace {tiempo_transcurrido.seconds // 60} min"
            else:
                ultima_actividad = f"Hace {tiempo_transcurrido.seconds // 3600}h"
        else:
            ultima_actividad = "Sin actividad"
        
        porcentaje = (completados / total_participaciones * 100) if total_participaciones > 0 else 0
        
        tributos_data.append({
            'nombre': tributo.personaje.get_full_name(),
            'codigo': tributo.codigo_tributo,
            'distrito': tributo.distrito,
            'estado': tributo.estado,
            'estado_display': tributo.get_estado_display(),
            'retos_completados': completados,
            'total_retos': total_participaciones,
            'porcentaje_completado': round(porcentaje, 1),
            'puntos': puntos_totales,
            'nivel': tributo.get_nivel_display(),
            'ultima_actividad': ultima_actividad,
        })
    
    return JsonResponse({
        'success': True,
        'stats': stats,
        'tributos': tributos_data,
        'timestamp': timezone.now().isoformat()
    })
