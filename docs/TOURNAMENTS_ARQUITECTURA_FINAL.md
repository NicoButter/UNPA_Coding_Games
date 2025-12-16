# Arquitectura Final: Tournaments App

## Interacción entre Apps

```
┌─────────────────────┐
│   tournaments app   │
├─────────────────────┤
│ Models:             │
│ - Tournament        │
│ - TournamentMentor  │ ────ForeignKey───→ District (from districts)
│ - TournamentStatus  │ ────ForeignKey───→ Personaje (from capitol)
│ - TournamentVigilante
└─────────────────────┘
         ▲
         │
    depends on
         │
         ▼
┌─────────────────────┐
│   districts app     │
├─────────────────────┤
│ Models:             │
│ - District          │ ◄─── RESPONSABLE ÚNICA de gestión de distritos
│ - DistrictMembership│
└─────────────────────┘
```

## Responsabilidades por App

### districts app
- **Crea y gestiona**: Distritos/unidades académicas, códigos, descripciones, membresía
- **Proporciona**: El modelo `District` reutilizable para toda la plataforma
- **URL base**: `/districts/`

### tournaments app
- **Crea y gestiona**: Torneos, asignaciones de mentores a distritos, asignaciones de vigilantes, estado de torneos
- **Utiliza**: `District` como referencia (ForeignKey) - NO CREA NUEVOS DISTRITOS
- **URL base**: `/tournaments/`

## Modelo TournamentMentor (Arquitectura Final)

```python
class TournamentMentor(models.Model):
    torneo = ForeignKey(Tournament)           # ← Torneo
    mentor = ForeignKey(Personaje)            # ← Persona (rol: mentor)
    distrito = ForeignKey(District)           # ← Distrito (de districts app)
    
    # Metadatos
    fecha_asignacion = DateTimeField(auto_now_add=True)
    asignado_por = ForeignKey(Personaje)      # ← Persona (rol: jefe_capitolio)
    es_activa = BooleanField(default=True)
    
    # Restricciones
    unique_together = [['torneo', 'distrito']]  # Un mentor por distrito/torneo
```

## Flujo de Trabajo: Asignar Mentor a Torneo

```
1. Jefe del Capitolio entra a "Crear Torneo"
   └─ Define: nombre, fechas, edición

2. Sistema crea Tournament en BD
   └─ estado = 'planificacion'

3. Jefe selecciona "Asignar Mentores"
   └─ Elige mentores y distritos
   └─ Selecciona distritos de la lista EXISTENTE (desde districts)

4. Sistema crea TournamentMentor
   ├─ torneo = Tournament recién creado
   ├─ mentor = Personaje seleccionado
   ├─ distrito = District existente (de districts app)
   └─ asignado_por = Usuario actual

5. Si hay distritos sin mentor
   └─ Alerta en tournament_detail.html: "Distritos sin Mentor"
```

## Puntos Clave

### ✅ Separación de Responsabilidades
- Districts: "Qué es un distrito?"
- Tournaments: "Quién es mentor en este torneo?"

### ✅ NO Duplicación
```python
# ❌ ANTES (Duplicado)
tournaments.UnidadAcademica
districts.District  # ← Mismo concepto en dos places

# ✅ DESPUÉS (Único)
districts.District  # ← Una única fuente de verdad
```

### ✅ Reutilizable
Otras apps futuras pueden usar `District` sin problema:
```python
# En otra app
from districts.models import District

class Evento(models.Model):
    distrito = ForeignKey(District)
    # ← Reutiliza la misma definición
```

### ✅ Mantenible
Cambios en estructura de distritos se reflejan automáticamente en tournaments:
- Si districts agrega un nuevo campo → tournaments lo ve automáticamente
- Si se necesita actualizar definición → cambio único en `districts/models.py`

## Configuración Requerida

### En settings.py
```python
INSTALLED_APPS = [
    ...
    'districts',  # ← Debe estar antes que tournaments
    'tournaments',
    ...
]
```

### En urls.py
```python
urlpatterns = [
    path('districts/', include('districts.urls')),
    path('tournaments/', include('tournaments.urls')),
    ...
]
```

## Migraciones

### Historial de Migraciones de Tournaments
1. `0001_initial`: Crea modelos originales (incluyendo UnidadAcademica)
2. `0002_alter_tournamentmentor_options_and_more`: 
   - Remueve `UnidadAcademica` 
   - Renombra `TournamentMentor.unidad_academica` → `TournamentMentor.distrito`
   - Añade dependencia de `districts.0001_initial`

## Status: ✅ COMPLETO Y TESTADO

- ✅ Modelos refactorizados
- ✅ Formularios actualizados
- ✅ Vistas actualizadas
- ✅ Templates actualizados
- ✅ Admin actualizado
- ✅ Tests pasando (9/9)
- ✅ Migraciones aplicadas
- ✅ System check: Sin errores

