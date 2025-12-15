"""
Vistas para el sistema de juez automático
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction

from arena.models import Reto
from capitol.models import TributoInfo
from .models import Submission
from .runner import JudgeRunner


@login_required
@require_http_methods(["POST"])
def submit_solution(request, reto_id):
    """
    Procesa el envío de una solución por parte de un tributo
    
    Flujo:
    1. Recibe código y lenguaje desde el POST
    2. Valida que el tributo puede enviar solución
    3. Crea registro de Submission
    4. Ejecuta el código usando JudgeRunner
    5. Actualiza Submission con resultados
    6. Retorna veredicto al frontend (sin detalles de tests)
    """
    # Obtener el reto
    reto = get_object_or_404(Reto, id=reto_id)
    
    # Verificar que el usuario es un tributo
    try:
        tributo = TributoInfo.objects.get(personaje__usuario=request.user)
    except TributoInfo.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Solo los tributos pueden enviar soluciones'
        }, status=403)
    
    # Verificar que el reto está disponible
    if not reto.esta_disponible:
        return JsonResponse({
            'success': False,
            'error': 'Este reto no está disponible actualmente'
        }, status=400)
    
    # Obtener datos del POST
    codigo = request.POST.get('codigo', '').strip()
    lenguaje = request.POST.get('lenguaje', '').lower()
    
    # Validaciones básicas
    if not codigo:
        return JsonResponse({
            'success': False,
            'error': 'El código no puede estar vacío'
        }, status=400)
    
    if lenguaje not in ['python', 'java', 'javascript']:
        return JsonResponse({
            'success': False,
            'error': f'Lenguaje no soportado: {lenguaje}'
        }, status=400)
    
    # Verificar que el reto permite este lenguaje
    lenguajes_permitidos = [l.strip().lower() for l in reto.lenguajes_permitidos.split(',')]
    if lenguaje not in lenguajes_permitidos:
        return JsonResponse({
            'success': False,
            'error': f'Este reto no permite código en {lenguaje}'
        }, status=400)
    
    # Verificar que el reto tiene validación automática
    if not reto.tiene_validacion_automatica:
        return JsonResponse({
            'success': False,
            'error': 'Este reto no tiene validación automática configurada'
        }, status=400)
    
    # Obtener tests ocultos del reto
    tests = reto.tests_ocultos.get(lenguaje, [])
    if not tests:
        return JsonResponse({
            'success': False,
            'error': f'No hay tests configurados para {lenguaje} en este reto'
        }, status=400)
    
    # Crear submission en estado pendiente
    with transaction.atomic():
        submission = Submission.objects.create(
            tributo=tributo,
            reto=reto,
            lenguaje=lenguaje,
            codigo=codigo,
            veredicto='PE',  # Pending
            casos_totales=len(tests)
        )
        
        try:
            # Ejecutar el juez
            runner = JudgeRunner()
            resultado = runner.evaluate_submission(
                user_code=codigo,
                language=lenguaje,
                tests=tests,
                time_limit=reto.limite_tiempo,
                memory_limit=reto.limite_memoria
            )
            
            # Actualizar submission con resultados
            submission.veredicto = resultado['veredicto']
            submission.puntos_obtenidos = resultado['puntos']
            submission.casos_pasados = resultado['casos_pasados']
            submission.tiempo_ejecucion = resultado.get('tiempo_ejecucion', 0)
            submission.stdout = resultado.get('stdout', '')
            submission.stderr = resultado.get('stderr', '')
            submission.detalles_ejecucion = resultado.get('detalles', {})
            submission.fecha_evaluacion = timezone.now()
            submission.save()
            
            # Preparar respuesta para el frontend (SIN detalles de tests ocultos)
            response_data = {
                'success': True,
                'submission_id': submission.id,
                'veredicto': submission.get_veredicto_display(),
                'veredicto_code': submission.veredicto,
                'puntos_obtenidos': submission.puntos_obtenidos,
                'casos_pasados': submission.casos_pasados,
                'casos_totales': submission.casos_totales,
                'porcentaje_exito': submission.porcentaje_exito,
                'tiempo_ejecucion': submission.tiempo_ejecucion,
                'es_aceptado': submission.es_aceptado
            }
            
            # Solo incluir stderr si hubo error (sin revelar detalles internos)
            if submission.veredicto in ['RE', 'CE', 'SE']:
                # Filtrar información sensible del stderr
                stderr_filtered = _filter_sensitive_info(submission.stderr)
                response_data['error_message'] = stderr_filtered
            
            return JsonResponse(response_data)
            
        except Exception as e:
            # Error durante la evaluación
            submission.veredicto = 'SE'
            submission.stderr = f'Error del sistema: {str(e)}'
            submission.fecha_evaluacion = timezone.now()
            submission.save()
            
            return JsonResponse({
                'success': False,
                'error': 'Error al evaluar la solución. Intenta nuevamente.',
                'submission_id': submission.id
            }, status=500)


@login_required
def submission_detail(request, submission_id):
    """
    Muestra los detalles de una submission
    Solo visible para el tributo que la envió o mentores/vigilantes
    """
    submission = get_object_or_404(Submission, id=submission_id)
    
    # Verificar permisos
    user_personaje = request.user.personaje
    es_dueno = submission.tributo.personaje == user_personaje
    es_staff = user_personaje.rol in ['jefe_capitolio', 'mentor', 'vigilante']
    
    if not (es_dueno or es_staff):
        return JsonResponse({
            'success': False,
            'error': 'No tienes permiso para ver esta submission'
        }, status=403)
    
    # Preparar datos (sin tests ocultos para tributos)
    data = {
        'id': submission.id,
        'reto': submission.reto.titulo,
        'lenguaje': submission.get_lenguaje_display(),
        'veredicto': submission.get_veredicto_display(),
        'veredicto_code': submission.veredicto,
        'puntos_obtenidos': submission.puntos_obtenidos,
        'casos_pasados': submission.casos_pasados,
        'casos_totales': submission.casos_totales,
        'tiempo_ejecucion': submission.tiempo_ejecucion,
        'fecha_envio': submission.fecha_envio.isoformat(),
        'es_aceptado': submission.es_aceptado
    }
    
    # Solo staff puede ver el código y detalles completos
    if es_staff:
        data['codigo'] = submission.codigo
        data['stdout'] = submission.stdout
        data['stderr'] = submission.stderr
        data['detalles'] = submission.detalles_ejecucion
    elif es_dueno:
        # El tributo puede ver su código pero no todos los detalles internos
        data['codigo'] = submission.codigo
        if submission.veredicto in ['RE', 'CE']:
            data['error_message'] = _filter_sensitive_info(submission.stderr)
    
    return JsonResponse(data)


@login_required
def submission_history(request, reto_id):
    """
    Retorna el historial de submissions de un tributo para un reto específico
    """
    reto = get_object_or_404(Reto, id=reto_id)
    
    try:
        tributo = TributoInfo.objects.get(personaje__usuario=request.user)
    except TributoInfo.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Solo los tributos pueden ver su historial'
        }, status=403)
    
    submissions = Submission.objects.filter(
        tributo=tributo,
        reto=reto
    ).order_by('-fecha_envio')[:10]  # Últimas 10 submissions
    
    data = {
        'submissions': [
            {
                'id': sub.id,
                'veredicto': sub.get_veredicto_display(),
                'veredicto_code': sub.veredicto,
                'puntos': sub.puntos_obtenidos,
                'casos_pasados': sub.casos_pasados,
                'casos_totales': sub.casos_totales,
                'tiempo': sub.tiempo_ejecucion,
                'fecha': sub.fecha_envio.isoformat(),
                'lenguaje': sub.get_lenguaje_display()
            }
            for sub in submissions
        ]
    }
    
    return JsonResponse(data)


def _filter_sensitive_info(stderr: str) -> str:
    """
    Filtra información sensible del stderr antes de mostrarla al tributo
    Remueve paths internos, detalles del sistema, etc.
    """
    if not stderr:
        return ''
    
    # Líneas a filtrar
    filtered_lines = []
    sensitive_keywords = ['/code/', '/tmp/', 'Docker', 'container']
    
    for line in stderr.split('\n'):
        # Omitir líneas con información sensible
        if any(keyword in line for keyword in sensitive_keywords):
            continue
        filtered_lines.append(line)
    
    return '\n'.join(filtered_lines[:20])  # Máximo 20 líneas
