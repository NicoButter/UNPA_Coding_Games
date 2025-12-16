from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .forms import PersonajeRegistroForm, TributoInfoForm, CustomAuthenticationForm
from .models import TributoInfo, Personaje
from .utils import generar_gafete_pdf, generar_gafete_html
from django.utils import timezone


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

def login_docente_view(request):
    if request.user.is_authenticated:
        return redirect('dashboards:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Verificar que el usuario sea docente o jefe
            if user.rol not in ['docente', 'jefe_capitolio', 'mentor']:
                messages.error(request, 'Solo docentes pueden ingresar por aquí.')
                return render(request, 'capitol/login_docente.html', {'form': form})
            
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.get_full_name()}!')
            return redirect('dashboards:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'capitol/login_docente.html', {'form': form})

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
        tributo_info = request.user.tributoinfo
    except TributoInfo.DoesNotExist:
        tributo_info = None
    
    context = {
        'tributo_info': tributo_info,
    }
    return render(request, 'capitol/perfil.html', context)


@login_required
def descargar_gafete(request):
    """Descarga el gafete del tributo en PDF"""
    try:
        tributo_info = request.user.tributoinfo
    except TributoInfo.DoesNotExist:
        messages.error(request, "No tienes información de tributo registrada")
        return redirect('dashboards:dashboard')
    
    # Generar PDF
    pdf_buffer = generar_gafete_pdf(tributo_info)
    
    # Preparar respuesta
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    filename = f'gafete_{tributo_info.codigo_tributo}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@login_required
def ver_gafete(request):
    """Muestra el gafete del tributo en HTML para visualizar"""
    try:
        tributo_info = request.user.tributoinfo
    except TributoInfo.DoesNotExist:
        messages.error(request, "No tienes información de tributo registrada")
        return redirect('dashboards:dashboard')
    
    html = generar_gafete_html(tributo_info)
    return HttpResponse(html)


def enviar_gafete_email(tributo_info):
    """
    Envía el gafete por email al tributo
    
    Args:
        tributo_info: Instancia de TributoInfo
    
    Returns:
        Boolean indicando si se envió exitosamente
    """
    try:
        # Generar PDF
        pdf_buffer = generar_gafete_pdf(tributo_info)
        
        # Preparar email
        subject = f'Tu Gafete para UNPA Coding Games - {tributo_info.codigo_tributo}'
        
        context = {
            'tributo': tributo_info,
            'nombre': tributo_info.personaje.get_full_name(),
            'codigo': tributo_info.codigo_tributo,
            'distrito': tributo_info.distrito,
        }
        
        # Mensaje en texto plano
        message = f"""
¡Bienvenido a UNPA Coding Games!

Hola {tributo_info.personaje.get_full_name()},

Tu registro ha sido completado exitosamente. En este correo encontrarás tu gafete de participante adjunto como PDF.

INFORMACIÓN DE TU GAFETE:
- Código de Tributo: {tributo_info.codigo_tributo}
- Distrito: {tributo_info.distrito}
- Nivel: {tributo_info.get_nivel_display()}

INSTRUCCIONES:
1. Imprime el gafete adjunto o guárdalo en tu teléfono
2. El día del torneo, presenta tu gafete al vigilante en la entrada
3. El vigilante escaneará tu código QR para acreditarte
4. Una vez acreditado, accede a la sala de computadoras
5. Siéntate en cualquier terminal disponible
6. La webcam escaneará automáticamente tu QR y accederás a tu dashboard

¡Que los juegos comiencen! 🔥

Contacto: nicobutter@gmail.com
UNPA - Universidad Nacional de la Patagonia Austral
        """
        
        # Crear email
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@unpa.edu.ar',
            to=[tributo_info.personaje.email],
        )
        
        # Adjuntar PDF
        pdf_buffer.seek(0)
        email.attach(
            f'gafete_{tributo_info.codigo_tributo}.pdf',
            pdf_buffer.read(),
            'application/pdf'
        )
        
        # Enviar
        email.send(fail_silently=False)
        
        # Marcar como generada
        tributo_info.credencial_generada = True
        tributo_info.fecha_generacion_credencial = timezone.now()
        tributo_info.save()
        
        return True
        
    except Exception as e:
        print(f"Error al enviar email: {e}")
        return False


@login_required
def reenviar_gafete(request):
    """Reenvía el gafete por email"""
    try:
        tributo_info = request.user.tributoinfo
    except TributoInfo.DoesNotExist:
        messages.error(request, "No tienes información de tributo registrada")
        return redirect('dashboards:dashboard')
    
    if enviar_gafete_email(tributo_info):
        messages.success(request, f"Gafete enviado a {request.user.email}")
    else:
        messages.error(request, "Hubo un error al enviar el email. Intenta nuevamente.")
    
    return redirect('dashboards:dashboard')


# Vista de acreditación para Vigilantes
@login_required
def acreditar_tributo_qr(request):
    """
    Vista para que vigilantes/mentores escaneen QR y acrediten tributos
    Solo accesible para vigilantes y mentores
    """
    if request.user.rol not in ['vigilante', 'mentor']:
        messages.error(request, "No tienes permiso para acceder a esta sección")
        return redirect('dashboards:dashboard')
    
    if request.method == 'POST':
        qr_token = request.POST.get('qr_token', '').strip()
        
        if not qr_token:
            return JsonResponse({'error': 'Token QR no proporcionado'}, status=400)
        
        try:
            tributo = TributoInfo.objects.get(qr_token=qr_token)
            
            # Acreditar tributo
            if tributo.estado == 'pendiente':
                tributo.acreditar()
                
                return JsonResponse({
                    'success': True,
                    'mensaje': f'Tributo {tributo.codigo_tributo} acreditado exitosamente',
                    'tributo': {
                        'codigo': tributo.codigo_tributo,
                        'nombre': tributo.personaje.get_full_name(),
                        'distrito': tributo.distrito,
                        'nivel': tributo.get_nivel_display(),
                        'estado': tributo.get_estado_display(),
                    }
                })
            elif tributo.estado == 'acreditado':
                return JsonResponse({
                    'warning': True,
                    'mensaje': f'El tributo {tributo.codigo_tributo} ya está acreditado',
                    'tributo': {
                        'codigo': tributo.codigo_tributo,
                        'nombre': tributo.personaje.get_full_name(),
                        'distrito': tributo.distrito,
                        'estado': tributo.get_estado_display(),
                    }
                })
            else:
                return JsonResponse({
                    'error': f'El tributo está en estado: {tributo.get_estado_display()}'
                }, status=400)
                
        except TributoInfo.DoesNotExist:
            return JsonResponse({'error': 'QR inválido o tributo no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Error al acreditar: {str(e)}'}, status=500)
    
    # GET: Mostrar interfaz de escaneo
    return render(request, 'centro_control/acreditar_tributo_qr.html')


# Vista de login con webcam para tributos
def login_webcam(request):
    """
    Vista de login alternativa con escaneo de QR por webcam
    Para usar en las terminales de la sala de competencia
    """
    if request.method == 'POST':
        qr_token = request.POST.get('qr_token', '').strip()
        
        if not qr_token:
            return JsonResponse({'error': 'Token QR no proporcionado'}, status=400)
        
        try:
            tributo = TributoInfo.objects.get(qr_token=qr_token)
            
            # Verificar que esté acreditado
            if tributo.estado != 'acreditado':
                return JsonResponse({
                    'error': 'Debes acreditarte primero con el vigilante',
                    'codigo': 'NOT_ACCREDITED'
                }, status=403)
            
            # Autenticar al usuario
            user = tributo.personaje
            
            # Login directo (sin contraseña, autenticación por QR)
            from django.contrib.auth import login as auth_login
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            return JsonResponse({
                'success': True,
                'mensaje': f'Bienvenido {user.get_full_name()}',
                'redirect_url': '/dashboard/'
            })
            
        except TributoInfo.DoesNotExist:
            return JsonResponse({'error': 'QR inválido'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Error: {str(e)}'}, status=500)
    
    # GET: Mostrar interfaz de login con webcam
    return render(request, 'capitol/login_webcam.html')

