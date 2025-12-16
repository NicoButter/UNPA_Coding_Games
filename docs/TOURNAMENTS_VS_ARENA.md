# Compatibilidad: Tournaments vs Arena

## Resumen de la Situación

Existen **dos modelos de torneos** en el sistema:

1. **`arena.Torneo`**: Modelo existente en la app arena
2. **`tournaments.Tournament`**: Nuevo modelo especializado

## Comparación

### arena.Torneo (Existente)

**Características**:
- Enfocado en la ejecución de desafíos
- Tiene relación con distritos (1-13)
- Gestiona vigilantes directamente
- Vinculado a puntuación por distrito

**Campos Principales**:
```python
nombre
descripcion
edicion
fecha_inicio / fecha_fin
fecha_inscripcion_inicio / fecha_inscripcion_fin
estado (configuracion, inscripcion, en_curso, finalizado, cancelado)
es_activo
puntos_minimos_ganar
permite_equipos
puntuacion_por_distrito
vigilantes_asignados (M2M)
```

### tournaments.Tournament (Nuevo)

**Características**:
- Enfocado en la gestión administrativa
- Período de acreditación específico
- Asignación de mentores a unidades académicas
- Flexible con fechas (mismo día posible)
- Auditoría completa de cambios

**Campos Principales**:
```python
nombre
numero_edicion
fecha_acreditacion_inicio / fecha_acreditacion_fin
fecha_competencia_inicio / fecha_competencia_fin
fecha_premios
estado (planificacion, acreditacion, competencia, etc)
creado_por
mentores_asignados (M2M)
vigilantes_asignados (M2M)
```

## ¿Cuál Usar?

### Usar `tournaments.Tournament` si:

- ✅ Necesitas gestionar múltiples unidades académicas
- ✅ Quieres asignar mentores específicos a cada unidad
- ✅ Necesitas período de acreditación separado
- ✅ Quieres auditoría completa de cambios
- ✅ Los eventos pueden ocurrir el mismo día

### Usar `arena.Torneo` si:

- ✅ Ya tienes competencias basadas en distritos
- ✅ Necesitas gestión de desafíos específicos
- ✅ Tienes inscripciones abiertas/cerradas
- ✅ La puntuación se basa en distritos

## Opción 1: Coexistencia (Recomendado)

**Ambos sistemas funcionan independientemente:**

```
┌──────────────────────────┐
│   tournaments.Tournament  │
├──────────────────────────┤
│ - Gestión administrativa │
│ - Asignación de mentores │
│ - Período de acreditación│
└──────────────────────────┘

┌──────────────────────────┐
│     arena.Torneo         │
├──────────────────────────┤
│ - Gestión de desafíos    │
│ - Puntuación por distrito│
│ - Inscripciones          │
└──────────────────────────┘
```

### Ventajas:
- No hay conflictos
- Cada uno maneja su dominio
- Fácil de mantener

### Desventajas:
- Datos duplicados potencialmente
- Difícil sincronizar estados

## Opción 2: Migración Gradual

**Migrar lentamente data de arena.Torneo a tournaments.Tournament:**

### Paso 1: Crear un manager customizado

```python
# tournaments/managers.py
from django.db import models

class TournamentManager(models.Manager):
    @classmethod
    def from_arena(cls, arena_torneo):
        """Crear Tournament desde un arena.Torneo existente"""
        tournament = cls.create(
            nombre=arena_torneo.nombre,
            numero_edicion=arena_torneo.edicion,
            descripcion=arena_torneo.descripcion,
            fecha_acreditacion_inicio=arena_torneo.fecha_inscripcion_inicio,
            fecha_acreditacion_fin=arena_torneo.fecha_inscripcion_fin,
            fecha_competencia_inicio=arena_torneo.fecha_inicio,
            fecha_competencia_fin=arena_torneo.fecha_fin,
            fecha_premios=arena_torneo.fecha_fin + timedelta(days=1),
            creado_por=arena_torneo.creado_por,
            estado='competencia' if arena_torneo.estado == 'en_curso' else 'planificacion'
        )
        return tournament
```

### Paso 2: Script de migración

```bash
python manage.py shell
```

```python
from arena.models import Torneo
from tournaments.models import Tournament

for arena_torneo in Torneo.objects.all():
    # Verificar si no existe ya
    exists = Tournament.objects.filter(
        nombre=arena_torneo.nombre,
        numero_edicion=arena_torneo.edicion
    ).exists()
    
    if not exists:
        tournament = Tournament.from_arena(arena_torneo)
        print(f"✓ Migrado: {tournament.nombre}")
    else:
        print(f"✗ Ya existe: {arena_torneo.nombre}")
```

## Opción 3: Integración Profunda (Avanzada)

**Crear una relación entre ambos modelos:**

```python
# tournaments/models.py
from arena.models import Torneo as ArenaTorneo

class Tournament(models.Model):
    # ... campos existentes ...
    
    # Referencia opcional al torneo de arena
    arena_torneo = models.OneToOneField(
        ArenaTorneo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tournament_config'
    )
    
    def sync_to_arena(self):
        """Sincronizar cambios a arena.Torneo"""
        if self.arena_torneo:
            self.arena_torneo.nombre = self.nombre
            self.arena_torneo.descripcion = self.descripcion
            self.arena_torneo.edicion = self.numero_edicion
            self.arena_torneo.save()
```

### Ventajas:
- Datos conectados
- Sincronización posible
- Vista unificada potencial

### Desventajas:
- Complejidad aumentada
- Múltiples fuentes de verdad
- Difícil de mantener

## Recomendación

**→ Usar Opción 1: Coexistencia**

Razones:
1. Cada sistema tiene propósitos distintos
2. No hay conflictos técnicos
3. Fácil de mantener y extender
4. Permite decisiones independientes

## Cómo Diferenciar en Uso

### Para el Jefe del Capitolio:

```
Dashboard
├── Gestión de Torneos (tournaments)
│   ├── Crear torneo
│   ├── Asignar mentores
│   ├── Asignar vigilantes
│   └── Ver auditoría
│
├── Competencias (arena)
│   ├── Ver desafíos
│   ├── Ver participantes
│   ├── Ver puntuaciones
│   └── Gestionar inscripciones
```

### URLs Claramente Separadas:

```
# Para gestión administrativa
/tournaments/        # Nueva app

# Para gestión de desafíos
/arena/              # App existente
```

## Migraciones Futuras Posibles

Después de estabilizar ambos sistemas:

1. **Fusión Opcional**: Si se decide combinar
2. **Sincronización**: Sincronizar datos cuando sea necesario
3. **API Unificada**: Crear API REST que combine ambos

## Conclusión

**Ambas apps pueden coexistir pacíficamente** mientras cumplan propósitos distintos:

- **tournaments**: Gestión administrativa de torneos
- **arena**: Gestión de desafíos y competencias

Esta separación permite:
- Especialización clara
- Independencia técnica
- Facilidad de mantenimiento
- Escalabilidad futura
