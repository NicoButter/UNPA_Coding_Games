# Integración de Tournaments con Dashboard del Jefe del Capitolio

## Descripción General

La app `tournaments` proporciona un sistema completo para gestionar torneos de programación. Esta guía detalla cómo integrar la gestión de torneos en el dashboard del Jefe del Capitolio.

## Paso 1: Acceso a Tournaments desde el Dashboard

El Jefe del Capitolio debe poder acceder a la gestión de torneos desde su dashboard principal. Se recomienda agregar un widget o menú directo.

### URL Base
```
/tournaments/
```

### Rutas Principales
- **Lista de Torneos**: `/tournaments/`
- **Crear Torneo**: `/tournaments/crear/`
- **Detalle del Torneo**: `/tournaments/<id>/`

## Paso 2: Flujo Completo de Creación de Torneo

### 2.1 Crear el Torneo

1. Ir a `/tournaments/crear/`
2. Completar el formulario con:
   - **Nombre**: Ej: "Hunger Games 2025"
   - **Edición**: Ej: 75
   - **Descripción**: Detalles del torneo
   - **Fechas de Acreditación**: Período en que se acreditan participantes
   - **Fechas de Competencia**: Período de programación
   - **Fecha de Premios**: Cuándo se entregan
   - **Configuración**: Equipos, puntuación por unidad, puntos mínimos

3. Guardar el torneo

### 2.2 Asignar Mentores

#### Opción A: Asignación Individual

1. Ir a detalle del torneo
2. Sección "Mentores Asignados"
3. Click "Agregar Mentor"
4. Seleccionar:
   - Mentor disponible
   - Unidad académica
5. Guardar

#### Opción B: Asignación Masiva

1. Ir a `/tournaments/asignar-mentores-multiples/`
2. Seleccionar torneo
3. Marcar mentores a asignar
4. Marcar unidades académicas destino
5. Guardar

El sistema distribuirá automáticamente los mentores entre las unidades.

### 2.3 Asignar Vigilantes

1. En detalle del torneo
2. Sección "Vigilantes Asignados"
3. Click "Agregar Vigilante"
4. Seleccionar:
   - Vigilante disponible
   - Rol en el torneo:
     - **General**: Responsabilidades generales
     - **Acreditación**: Supervisa acreditación
     - **Competencia**: Supervisa competencia
     - **Premios**: Supervisa entrega de premios
5. Guardar

O usar asignación masiva en `/tournaments/asignar-vigilantes-multiples/`

## Paso 3: Gestión de Unidades Académicas

### Crear Unidades Académicas

1. Ir a `/tournaments/unidades/`
2. Click "Crear Unidad"
3. Completar:
   - Nombre (ej: "Ingeniería en Sistemas")
   - Código único (ej: "SIS-001")
   - Descripción
   - Ubicación
   - Activa (checkbox)
4. Guardar

### Editar Unidades

1. Ir a `/tournaments/unidades/`
2. Click en editar junto a la unidad
3. Modificar campos necesarios
4. Guardar

## Paso 4: Vistas y Reportes

### Dashboard del Torneo

Cada torneo tiene un detalle que muestra:

- **Estado del torneo**: En qué fase se encuentra
- **Cronograma**: Fechas de cada período
- **Mentores asignados**: Lista con unidades académicas
- **Vigilantes asignados**: Lista con roles
- **Historial de cambios**: Auditoría de estados anteriores

### Validaciones Automáticas

El sistema valida automáticamente:

1. **Coherencia de fechas**: Acreditación → Competencia → Premios
2. **Asignaciones duplicadas**: Impide dos mentores en misma unidad
3. **Unicidad de vigilantes**: Cada vigilante solo una vez por torneo

## Integración en Templates

### Widget para Dashboard Principal

Para agregar un widget de Torneos en el dashboard, incluir:

```html
<!-- En dashboards/templates/dashboard_jefe.html -->

<div class="card">
    <div class="card-header bg-primary text-white">
        <h5 class="mb-0">
            <i class="fas fa-trophy"></i> Torneos Activos
        </h5>
    </div>
    <div class="card-body">
        <a href="{% url 'tournaments:tournament_list' %}" class="btn btn-primary">
            <i class="fas fa-arrow-right"></i> Gestionar Torneos
        </a>
        {% if torneos_activos %}
            <div class="mt-3">
                <h6>Torneos en Ejecución:</h6>
                <ul>
                {% for torneo in torneos_activos %}
                    <li>
                        <a href="{% url 'tournaments:tournament_detail' torneo.pk %}">
                            {{ torneo.nombre }} - Edición #{{ torneo.numero_edicion }}
                        </a>
                    </li>
                {% endfor %}
                </ul>
            </div>
        {% endif %}
    </div>
</div>
```

### Contexto Necesario en Vista del Dashboard

```python
# En dashboards/views.py

from tournaments.models import Tournament

def dashboard_jefe(request):
    context = {
        'torneos_activos': Tournament.objects.filter(es_activo=True),
        'total_torneos': Tournament.objects.count(),
        # ... otros datos del dashboard
    }
    return render(request, 'dashboard_jefe.html', context)
```

## Validaciones de Seguridad

Todas las vistas están protegidas:

```python
# Solo usuarios con rol 'jefe_capitolio' pueden acceder
class IsJefeCapitolioMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.rol == 'jefe_capitolio'
```

## Estados del Torneo

El sistema maneja 6 estados posibles:

| Estado | Descripción |
|--------|-------------|
| **planificacion** | Torneo en configuración inicial |
| **acreditacion** | Período para acreditar participantes |
| **competencia** | Competencia en curso |
| **entrega_premios** | Fase de entrega de premios |
| **finalizado** | Torneo completado |
| **cancelado** | Torneo cancelado |

### Cambios de Estado

Los cambios de estado se registran automáticamente en `TournamentStatus` con:
- Usuario que realizó el cambio
- Fecha y hora del cambio
- Razón (opcional)

## Datos Requeridos

Para crear un torneo funcional:

1. **Jefe del Capitolio**: Usuario con rol 'jefe_capitolio'
2. **Mentores**: Usuarios con rol 'mentor'
3. **Vigilantes**: Usuarios con rol 'vigilante'
4. **Unidades Académicas**: Creadas previamente en `/tournaments/unidades/`

## Ejemplo de Uso Completo

```python
from tournaments.models import Tournament, TournamentMentor, TournamentVigilante, UnidadAcademica
from capitol.models import Personaje
from django.utils import timezone
from datetime import timedelta

# 1. Crear Unidad Académica
unidad = UnidadAcademica.objects.create(
    nombre="Ingeniería en Sistemas",
    codigo="SIS-001",
    ubicacion="Campus Principal"
)

# 2. Crear Torneo
jefe = Personaje.objects.get(username='jefe_admin')
now = timezone.now()

torneo = Tournament.objects.create(
    nombre="Hunger Games 2025",
    numero_edicion=75,
    fecha_acreditacion_inicio=now,
    fecha_acreditacion_fin=now + timedelta(hours=2),
    fecha_competencia_inicio=now + timedelta(hours=3),
    fecha_competencia_fin=now + timedelta(hours=8),
    fecha_premios=now + timedelta(hours=9),
    creado_por=jefe
)

# 3. Asignar Mentor
mentor = Personaje.objects.get(username='mentor1', rol='mentor')
TournamentMentor.objects.create(
    torneo=torneo,
    mentor=mentor,
    unidad_academica=unidad,
    asignado_por=jefe
)

# 4. Asignar Vigilantes
vigilante1 = Personaje.objects.get(username='vigilante1', rol='vigilante')
TournamentVigilante.objects.create(
    torneo=torneo,
    vigilante=vigilante1,
    rol_en_torneo='general',
    asignado_por=jefe
)
```

## Próximas Mejoras

1. **Notificaciones por Email**: Notificar mentores y vigilantes cuando son asignados
2. **Reportes PDF**: Generar reportes de torneos
3. **API REST**: Endpoints para aplicaciones móviles
4. **Integraciones**: Conectar automáticamente con challenges y arena
5. **Dashboard Avanzado**: Gráficas de participación y puntuaciones

## Soporte

Para más información sobre la app tournaments, consultar:
- [tournaments/README.md](tournaments/README.md)
- Documentación de modelos en [tournaments/models.py](tournaments/models.py)
- Documentación de vistas en [tournaments/views.py](tournaments/views.py)
