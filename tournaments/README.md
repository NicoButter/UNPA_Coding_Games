# App Tournaments - Gestión de Torneos

## Descripción

La app `tournaments` es responsable de gestionar completamente el ciclo de vida de los torneos de programación en UNPA Coding Games. Proporciona una interfaz integral para:

- **Crear y configurar torneos** con flexibilidad en fechas (acreditación, competencia, premios)
- **Gestionar unidades académicas** que participan en los torneos
- **Asignar mentores** a cada unidad académica
- **Asignar vigilantes** al torneo con roles específicos
- **Registrar historial** de cambios de estado

## Modelos

### 1. **UnidadAcademica**
Representa una unidad académica de la UNPA (sede, carrera, etc).

**Campos:**
- `nombre`: Nombre único de la unidad
- `codigo`: Código identificador único
- `descripcion`: Descripción detallada
- `ubicacion`: Ubicación física
- `es_activa`: Estado de la unidad

### 2. **Tournament**
Modelo principal que representa un torneo con todas sus configuraciones.

**Campos principales:**
- `nombre`: Nombre del torneo
- `numero_edicion`: Número de edición (ej: 75)
- `descripcion`: Descripción del torneo
- `imagen`: Imagen representativa

**Fechas (flexibles):**
- `fecha_acreditacion_inicio` - `fecha_acreditacion_fin`: Período de acreditación
- `fecha_competencia_inicio` - `fecha_competencia_fin`: Período de competencia
- `fecha_premios`: Fecha de entrega de premios

> **Nota**: Las fechas pueden ser el mismo día (ej: acreditación 08:00-10:00, competencia 10:30-15:00, premios 16:00)

**Configuración:**
- `estado`: Estado actual del torneo (planificación, acreditación, competencia, entrega_premios, finalizado, cancelado)
- `es_activo`: Indica si el torneo está activo
- `permite_equipos`: Si permite competencia por equipos
- `puntuacion_por_unidad`: Si la puntuación se suma por unidad académica
- `puntos_minimos_ganar`: Puntos mínimos requeridos para ganar

**Relaciones:**
- `creado_por`: ForeignKey a Personaje (Jefe del Capitolio)
- `mentores_asignados`: ManyToMany a través de TournamentMentor
- `vigilantes_asignados`: ManyToMany a través de TournamentVigilante

**Métodos útiles:**
- `esta_en_acreditacion`: Verifica si está en período de acreditación
- `esta_en_competencia`: Verifica si está en período de competencia
- `esta_en_entrega_premios`: Verifica si está en período de premios

### 3. **TournamentMentor**
Asignación de un mentor a una unidad académica específica en un torneo.

**Campos:**
- `torneo`: ForeignKey a Tournament
- `mentor`: ForeignKey a Personaje (rol='mentor')
- `unidad_academica`: ForeignKey a UnidadAcademica
- `es_activa`: Si la asignación está activa
- `observaciones`: Notas sobre la asignación

**Restricciones:**
- `unique_together`: (torneo, unidad_academica) - Solo un mentor por unidad en cada torneo
- Las validaciones previenen asignaciones duplicadas activas

### 4. **TournamentVigilante**
Asignación de un vigilante a un torneo con un rol específico.

**Campos:**
- `torneo`: ForeignKey a Tournament
- `vigilante`: ForeignKey a Personaje (rol='vigilante')
- `rol_en_torneo`: Rol del vigilante (general, acreditacion, competencia, premios)
- `es_activa`: Si la asignación está activa
- `observaciones`: Notas sobre la asignación

**Restricciones:**
- `unique_together`: (torneo, vigilante) - Cada vigilante solo una vez por torneo

### 5. **TournamentStatus**
Registra el historial de cambios de estado del torneo.

**Campos:**
- `torneo`: ForeignKey a Tournament
- `estado_anterior`: Estado anterior
- `estado_nuevo`: Nuevo estado
- `cambio_por`: Personaje que realizó el cambio
- `fecha_cambio`: Cuándo ocurrió el cambio
- `razon`: Razón del cambio

## URLs

```
tournaments/                                  # Lista de torneos
tournaments/crear/                           # Crear torneo
tournaments/<id>/                            # Detalle del torneo
tournaments/<id>/editar/                     # Editar torneo
tournaments/<id>/eliminar/                   # Eliminar torneo
tournaments/<id>/agregar-mentor/             # Agregar mentor a torneo
tournaments/mentor/<id>/remover/             # Remover mentor
tournaments/<id>/agregar-vigilante/          # Agregar vigilante
tournaments/vigilante/<id>/remover/          # Remover vigilante
tournaments/unidades/                        # Lista de unidades académicas
tournaments/unidades/crear/                  # Crear unidad académica
tournaments/unidades/<id>/editar/            # Editar unidad académica
```

## Flujo de Creación de Torneo

### Paso 1: Crear el Torneo
1. Ir a "Crear Nuevo Torneo"
2. Completar información básica (nombre, edición, descripción)
3. Definir fechas:
   - **Acreditación**: Período en que se acreditan los participantes
   - **Competencia**: Período de la competencia
   - **Premios**: Cuándo se entregan los premios
4. Configurar opciones (equipos, puntuación, puntos mínimos)
5. Guardar

### Paso 2: Asignar Mentores
1. Ir al detalle del torneo creado
2. En la sección "Mentores Asignados", hacer clic en "Agregar Mentor"
3. Seleccionar el mentor y la unidad académica
4. Guardar
5. Repetir para cada unidad académica

**O Asignación Masiva:**
- Usar la vista de "Asignar Múltiples Mentores"
- Seleccionar mentores y unidades de una vez

### Paso 3: Asignar Vigilantes
1. En el detalle del torneo, sección "Vigilantes Asignados"
2. Hacer clic en "Agregar Vigilante"
3. Seleccionar vigilante y rol (general, acreditación, competencia, premios)
4. Guardar
5. Repetir según sea necesario

## Validaciones

### Tournament
- Las fechas deben ser coherentes (acreditación < competencia < premios)
- Inicio debe ser anterior al fin en cada período
- El modelo `clean()` realiza estas validaciones automáticamente

### TournamentMentor
- No se puede asignar dos mentores activos a la misma unidad en un torneo
- El sistema evita duplicados automáticamente

### TournamentVigilante
- Cada vigilante solo puede estar una vez por torneo
- Los roles permiten mejor organización de responsabilidades

## Vistas

### Listado
- **TournamentListView**: Lista todos los torneos con paginación

### CRUD Torneos
- **TournamentCreateView**: Crear nuevo torneo
- **TournamentDetailView**: Ver detalles del torneo
- **TournamentUpdateView**: Editar torneo
- **TournamentDeleteView**: Eliminar torneo

### Gestión de Mentores
- **AddMentorToTournamentView**: Agregar un mentor a un torneo
- **RemoveMentorFromTournamentView**: Remover un mentor
- **BulkAssignMentorsView**: Asignación masiva de mentores

### Gestión de Vigilantes
- **AddVigilanteToTournamentView**: Agregar un vigilante
- **RemoveVigilanteFromTournamentView**: Remover un vigilante
- **BulkAssignVigilantesView**: Asignación masiva de vigilantes

### Unidades Académicas
- **UnidadAcademicaListView**: Listar unidades
- **UnidadAcademicaCreateView**: Crear unidad
- **UnidadAcademicaUpdateView**: Editar unidad

## Admin

La app está completamente configurada en Django Admin con:

- Filtros por estado, fecha, etc.
- Búsqueda de torneos
- Inlines para mentores, vigilantes e historial
- Badges de colores para estados
- Auditoría automática de cambios

## Seguridad

- Todas las vistas requieren autenticación
- Solo usuarios con rol `jefe_capitolio` pueden acceder
- Las asignaciones de estado se registran automáticamente

## Integración con otras apps

### capitol
- Usa modelo `Personaje` para mentores, vigilantes y creadores

### dashboards
- Se integrará para mostrar resumen de torneos en el dashboard del jefe

### arena
- Los datos de tourneys pueden ser usados por la app arena si existe

## Testing

La app incluye pruebas unitarias para:
- Creación y validación de modelos
- Restricciones de unicidad
- Validaciones de fechas
- Búsquedas y filtros

Ejecutar tests:
```bash
python manage.py test tournaments
```

## Pendientes de Integración

1. **Dashboard del Jefe**: Integrar widget en dashboards
2. **Notificaciones**: Notificar a mentores y vigilantes cuando son asignados
3. **Reportes**: Generar reportes de torneos
4. **API REST**: Crear endpoints REST para móvil/externa
5. **Sincronización con Arena**: Vincular automáticamente desafíos con torneos
