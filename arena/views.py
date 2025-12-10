from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Count, Sum
from .models import Torneo, Reto, ParticipacionTributo, CasoDePrueba, RankingDistrito
from .forms import ParticipacionTributoForm
from capitol.models import TributoInfo
import json
import subprocess
import tempfile
import os


@login_required
def torneos_disponibles(request):
    """Vista para mostrar torneos activos donde el tributo puede participar"""
    if request.user.rol != 'tributo':
        messages.error(request, "Solo los tributos pueden acceder a esta sección")
        return redirect('dashboards:dashboard')
    
    # Obtener información del tributo
    try:
        tributo_info = request.user.tributoinfo
    except TributoInfo.DoesNotExist:
        messages.error(request, "Debes completar tu perfil de tributo primero")
        return redirect('dashboards:dashboard')
    
    # Torneos en estado de inscripción o en curso
    torneos_activos = Torneo.objects.filter(
        Q(estado='inscripcion') | Q(estado='en_curso'),
        is_activo=True,
        fecha_inicio__lte=timezone.now(),
    ).order_by('-fecha_inicio')
    
    context = {
        'torneos': torneos_activos,
        'tributo_info': tributo_info,
    }
    return render(request, 'arena/torneos_disponibles.html', context)


@login_required
def arena_torneo(request, torneo_id):
    """Vista principal del arena - muestra los 5 retos del torneo"""
    if request.user.rol != 'tributo':
        messages.error(request, "Solo los tributos pueden participar en torneos")
        return redirect('dashboards:dashboard')
    
    torneo = get_object_or_404(Torneo, id=torneo_id)
    tributo_info = get_object_or_404(TributoInfo, personaje=request.user)
    
    # Verificar que el torneo esté activo
    if torneo.estado not in ['inscripcion', 'en_curso']:
        messages.error(request, "Este torneo no está disponible actualmente")
        return redirect('arena:torneos_disponibles')
    
    # Obtener los retos del torneo (ordenados por dificultad)
    retos = Reto.objects.filter(
        torneo=torneo,
        is_activo=True,
        is_visible=True
    ).order_by('dificultad')
    
    # Obtener o crear participaciones del tributo para cada reto
    participaciones = {}
    for reto in retos:
        participacion, created = ParticipacionTributo.objects.get_or_create(
            tributo=tributo_info,
            reto=reto,
            defaults={'estado': 'no_iniciado'}
        )
        participaciones[reto.id] = participacion
    
    # Calcular estadísticas
    total_retos = retos.count()
    completados = sum(1 for p in participaciones.values() if p.estado == 'completado')
    puntos_totales = sum(p.puntos_obtenidos or 0 for p in participaciones.values())
    
    # Verificar tiempo límite (si existe)
    tiempo_restante = None
    if torneo.fecha_fin:
        tiempo_restante = (torneo.fecha_fin - timezone.now()).total_seconds()
        if tiempo_restante <= 0:
            messages.warning(request, "El tiempo del torneo ha finalizado")
    
    context = {
        'torneo': torneo,
        'retos': retos,
        'participaciones': participaciones,
        'total_retos': total_retos,
        'completados': completados,
        'puntos_totales': puntos_totales,
        'tiempo_restante': int(tiempo_restante) if tiempo_restante else None,
        'tributo_info': tributo_info,
    }
    return render(request, 'arena/arena_torneo.html', context)


@login_required
def resolver_reto(request, reto_id):
    """Vista para resolver un reto específico"""
    if request.user.rol != 'tributo':
        messages.error(request, "Solo los tributos pueden resolver retos")
        return redirect('dashboards:dashboard')
    
    reto = get_object_or_404(Reto, id=reto_id)
    tributo_info = get_object_or_404(TributoInfo, personaje=request.user)
    
    # Verificar que el torneo esté activo
    if reto.torneo.estado not in ['inscripcion', 'en_curso']:
        messages.error(request, "Este torneo no está disponible")
        return redirect('arena:torneos_disponibles')
    
    # Obtener o crear participación
    participacion, created = ParticipacionTributo.objects.get_or_create(
        tributo=tributo_info,
        reto=reto,
        defaults={'estado': 'no_iniciado'}
    )
    
    # Si es la primera vez, marcar como en progreso
    if participacion.estado == 'no_iniciado':
        participacion.estado = 'en_progreso'
        participacion.fecha_inicio = timezone.now()
        participacion.save()
    
    # Obtener casos de prueba visibles (ejemplos)
    casos_ejemplo = CasoDePrueba.objects.filter(
        reto=reto,
        es_ejemplo=True
    ).order_by('orden')
    
    # Obtener intentos previos
    intentos_previos = ParticipacionTributo.objects.filter(
        tributo=tributo_info,
        reto=reto
    ).order_by('-fecha_envio')[:5]
    
    context = {
        'reto': reto,
        'participacion': participacion,
        'casos_ejemplo': casos_ejemplo,
        'intentos_previos': intentos_previos,
        'torneo': reto.torneo,
        'form': ParticipacionTributoForm(instance=participacion, reto=reto),
    }
    return render(request, 'arena/resolver_reto.html', context)


@login_required
def validar_solucion(request, reto_id):
    """Valida la solución enviada por el tributo"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    if request.user.rol != 'tributo':
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    reto = get_object_or_404(Reto, id=reto_id)
    tributo_info = get_object_or_404(TributoInfo, personaje=request.user)
    
    # Obtener código y lenguaje
    codigo = request.POST.get('codigo_solucion', '')
    lenguaje = request.POST.get('lenguaje', 'python')
    
    if not codigo:
        return JsonResponse({'error': 'No se proporcionó código'}, status=400)
    
    # Crear o actualizar participación
    participacion, created = ParticipacionTributo.objects.get_or_create(
        tributo=tributo_info,
        reto=reto,
        defaults={'estado': 'en_progreso'}
    )
    
    participacion.codigo_solucion = codigo
    participacion.lenguaje = lenguaje
    participacion.estado = 'validando'
    participacion.numero_intento = (participacion.numero_intento or 0) + 1
    participacion.fecha_envio = timezone.now()
    participacion.save()
    
    # Obtener casos de prueba
    casos_prueba = CasoDePrueba.objects.filter(reto=reto).order_by('orden')
    
    if not casos_prueba.exists():
        return JsonResponse({
            'error': 'No hay casos de prueba configurados para este reto'
        }, status=400)
    
    # Ejecutar validación
    resultados = []
    casos_pasados = 0
    casos_totales = casos_prueba.count()
    puntos_obtenidos = 0
    
    for caso in casos_prueba:
        resultado = ejecutar_codigo(codigo, lenguaje, caso.entrada)
        
        es_correcto = resultado['salida'].strip() == caso.salida_esperada.strip()
        
        if es_correcto:
            casos_pasados += 1
            puntos_obtenidos += caso.puntos
        
        resultados.append({
            'caso': caso.nombre,
            'correcto': es_correcto,
            'entrada': caso.entrada if caso.is_visible else 'Oculto',
            'salida_esperada': caso.salida_esperada if caso.is_visible else 'Oculto',
            'salida_obtenida': resultado['salida'],
            'error': resultado.get('error'),
            'es_visible': caso.is_visible,
        })
    
    # Actualizar participación
    participacion.casos_pasados = casos_pasados
    participacion.casos_totales = casos_totales
    participacion.puntos_obtenidos = puntos_obtenidos
    
    if casos_pasados == casos_totales:
        participacion.estado = 'completado'
        participacion.fecha_completado = timezone.now()
        # Agregar puntos bonus si es la primera vez que lo completa
        if participacion.numero_intento == 1:
            participacion.puntos_obtenidos += reto.puntos_bonus
    else:
        participacion.estado = 'fallido'
    
    participacion.save()
    
    # Actualizar ranking del distrito
    actualizar_ranking_distrito(tributo_info, reto.torneo)
    
    return JsonResponse({
        'success': True,
        'casos_pasados': casos_pasados,
        'casos_totales': casos_totales,
        'puntos_obtenidos': participacion.puntos_obtenidos,
        'estado': participacion.estado,
        'resultados': resultados,
        'completado': participacion.estado == 'completado',
    })


def ejecutar_codigo(codigo, lenguaje, entrada):
    """Ejecuta el código del tributo con la entrada proporcionada"""
    try:
        if lenguaje == 'python':
            # Crear archivo temporal con el código
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(codigo)
                temp_file = f.name
            
            try:
                # Ejecutar código con timeout
                proceso = subprocess.run(
                    ['python3', temp_file],
                    input=entrada,
                    capture_output=True,
                    text=True,
                    timeout=5  # 5 segundos máximo
                )
                
                if proceso.returncode != 0:
                    return {
                        'salida': '',
                        'error': proceso.stderr
                    }
                
                return {
                    'salida': proceso.stdout,
                    'error': None
                }
            finally:
                # Eliminar archivo temporal
                os.unlink(temp_file)
        
        else:
            return {
                'salida': '',
                'error': f'Lenguaje {lenguaje} no soportado'
            }
    
    except subprocess.TimeoutExpired:
        return {
            'salida': '',
            'error': 'Tiempo de ejecución excedido (máximo 5 segundos)'
        }
    except Exception as e:
        return {
            'salida': '',
            'error': f'Error al ejecutar código: {str(e)}'
        }


def actualizar_ranking_distrito(tributo_info, torneo):
    """Actualiza el ranking del distrito del tributo"""
    distrito = tributo_info.distrito
    
    # Obtener o crear ranking
    ranking, created = RankingDistrito.objects.get_or_create(
        distrito=distrito,
        torneo=torneo
    )
    
    # Calcular puntos totales del distrito
    tributos_distrito = TributoInfo.objects.filter(distrito=distrito)
    
    puntos_totales = 0
    retos_completados = 0
    tributos_activos = 0
    
    for tributo in tributos_distrito:
        participaciones = ParticipacionTributo.objects.filter(
            tributo=tributo,
            reto__torneo=torneo
        )
        
        if participaciones.exists():
            tributos_activos += 1
            puntos_tributo = sum(p.puntos_obtenidos or 0 for p in participaciones)
            puntos_totales += puntos_tributo
            retos_completados += participaciones.filter(estado='completado').count()
    
    ranking.puntos_totales = puntos_totales
    ranking.retos_completados = retos_completados
    ranking.tributos_activos = tributos_activos
    ranking.save()


@login_required
def finalizar_participacion(request, torneo_id):
    """Finaliza la participación del tributo en el torneo"""
    if request.method != 'POST':
        messages.error(request, "Método no permitido")
        return redirect('arena:arena_torneo', torneo_id=torneo_id)
    
    if request.user.rol != 'tributo':
        messages.error(request, "No autorizado")
        return redirect('dashboards:dashboard')
    
    torneo = get_object_or_404(Torneo, id=torneo_id)
    tributo_info = get_object_or_404(TributoInfo, personaje=request.user)
    
    # Marcar todas las participaciones como finalizadas
    participaciones = ParticipacionTributo.objects.filter(
        tributo=tributo_info,
        reto__torneo=torneo,
        estado__in=['en_progreso', 'no_iniciado', 'enviado']
    )
    
    for participacion in participaciones:
        if participacion.estado == 'en_progreso':
            participacion.estado = 'fallido'
        participacion.save()
    
    messages.success(request, "Has finalizado tu participación en el torneo")
    return redirect('arena:resultado_torneo', torneo_id=torneo_id)


@login_required
def resultado_torneo(request, torneo_id):
    """Muestra los resultados del tributo en el torneo"""
    if request.user.rol != 'tributo':
        messages.error(request, "No autorizado")
        return redirect('dashboards:dashboard')
    
    torneo = get_object_or_404(Torneo, id=torneo_id)
    tributo_info = get_object_or_404(TributoInfo, personaje=request.user)
    
    # Obtener todas las participaciones
    participaciones = ParticipacionTributo.objects.filter(
        tributo=tributo_info,
        reto__torneo=torneo
    ).select_related('reto')
    
    # Calcular estadísticas
    total_puntos = sum(p.puntos_obtenidos or 0 for p in participaciones)
    retos_completados = participaciones.filter(estado='completado').count()
    total_retos = participaciones.count()
    
    # Obtener ranking del distrito
    ranking_distrito = RankingDistrito.objects.filter(
        torneo=torneo,
        distrito=tributo_info.distrito
    ).first()
    
    context = {
        'torneo': torneo,
        'participaciones': participaciones,
        'total_puntos': total_puntos,
        'retos_completados': retos_completados,
        'total_retos': total_retos,
        'ranking_distrito': ranking_distrito,
        'tributo_info': tributo_info,
    }
    return render(request, 'arena/resultado_torneo.html', context)
