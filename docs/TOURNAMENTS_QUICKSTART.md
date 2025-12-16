# Quick Start - App Tournaments

## Instalación Rápida

La app `tournaments` ya está configurada y lista para usar. Sigue estos pasos para comenzar:

### 1. Verificar que la app esté registrada

En `unpa_code_games/settings.py`:
```python
INSTALLED_APPS = [
    ...
    "tournaments",  # ✓ Ya está aquí
]
```

### 2. Ejecutar migraciones (si aún no lo hiciste)

```bash
python manage.py migrate tournaments
```

### 3. Crear Unidades Académicas (Datos Iniciales)

```bash
python manage.py shell
```

Luego en el shell:

```python
from tournaments.models import UnidadAcademica

# Crear unidades
unidades = [
    {"nombre": "Ingeniería en Sistemas", "codigo": "SIS-001", "ubicacion": "Campus Principal"},
    {"nombre": "Licenciatura en Informática", "codigo": "INF-001", "ubicacion": "Campus Principal"},
    {"nombre": "Tecnicatura en Programación", "codigo": "TEC-001", "ubicacion": "Campus Extensión"},
]

for unidad_data in unidades:
    UnidadAcademica.objects.create(**unidad_data)

print("✓ Unidades académicas creadas")
```

### 4. Acceder a la interfaz

1. Ir a `/tournaments/` como Jefe del Capitolio
2. Click en "Crear Nuevo Torneo"
3. Completar formulario y guardar
4. Asignar mentores y vigilantes

## Flujo Típico

```
┌─────────────────────────────────────────────────────────┐
│                   Crear Torneo                           │
├─────────────────────────────────────────────────────────┤
│ - Nombre y edición                                       │
│ - Fechas (acreditación, competencia, premios)          │
│ - Configuración                                          │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│           Asignar Mentores a Unidades                    │
├─────────────────────────────────────────────────────────┤
│ - Seleccionar mentor                                     │
│ - Seleccionar unidad académica                          │
│ - Repetir para cada unidad                              │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│        Asignar Vigilantes al Torneo                      │
├─────────────────────────────────────────────────────────┤
│ - Seleccionar vigilante                                  │
│ - Asignar rol (general, acreditación, etc)             │
│ - Repetir según necesite                                │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│         ¡Torneo listo para usar!                         │
└─────────────────────────────────────────────────────────┘
```

## URLs Principales

```
GET  /tournaments/                          # Lista de torneos
GET  /tournaments/crear/                    # Formulario crear
POST /tournaments/crear/                    # Guardar torneo
GET  /tournaments/<id>/                     # Detalle
GET  /tournaments/<id>/editar/              # Formulario editar
POST /tournaments/<id>/editar/              # Guardar cambios
GET  /tournaments/<id>/agregar-mentor/      # Agregar mentor
POST /tournaments/<id>/agregar-mentor/      # Guardar mentor
GET  /tournaments/<id>/agregar-vigilante/   # Agregar vigilante
POST /tournaments/<id>/agregar-vigilante/   # Guardar vigilante
GET  /tournaments/unidades/                 # Lista de unidades
```

## Admin

Acceder a Django Admin en `/admin/`:

- **Torneos**: Crear, editar, ver estado
- **Unidades Académicas**: Gestionar sedes/carreras
- **Mentores de Torneos**: Ver asignaciones
- **Vigilantes de Torneos**: Ver asignaciones
- **Historial de Estados**: Auditoría

## Datos de Prueba (Script)

Crear un script `crear_datos_tournaments.py`:

```python
#!/usr/bin/env python
import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unpa_code_games.settings')
django.setup()

from tournaments.models import Tournament, UnidadAcademica, TournamentMentor, TournamentVigilante
from capitol.models import Personaje

# Crear unidades
unidades = []
for i, nombre in enumerate(["Ingeniería en Sistemas", "Informática", "Programación"], 1):
    unidad, _ = UnidadAcademica.objects.get_or_create(
        codigo=f"UNI-{i:03d}",
        defaults={"nombre": nombre, "ubicacion": f"Campus {i}"}
    )
    unidades.append(unidad)
    print(f"✓ Unidad: {unidad.nombre}")

# Crear torneo
jefe = Personaje.objects.filter(rol='jefe_capitolio').first()
if jefe:
    now = timezone.now()
    torneo, created = Tournament.objects.get_or_create(
        nombre="Hunger Games 2025",
        defaults={
            "numero_edicion": 75,
            "fecha_acreditacion_inicio": now,
            "fecha_acreditacion_fin": now + timedelta(hours=2),
            "fecha_competencia_inicio": now + timedelta(hours=3),
            "fecha_competencia_fin": now + timedelta(hours=8),
            "fecha_premios": now + timedelta(hours=9),
            "creado_por": jefe
        }
    )
    if created:
        print(f"✓ Torneo: {torneo.nombre}")
    else:
        print(f"✓ Torneo ya existe: {torneo.nombre}")
else:
    print("✗ No hay Jefe del Capitolio disponible")

print("\n✓ Datos de prueba creados exitosamente")
```

Ejecutar con:
```bash
python crear_datos_tournaments.py
```

## Testing

Ejecutar tests de la app:

```bash
python manage.py test tournaments
```

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'tournaments'"

Solución: Asegurar que `tournaments` esté en `INSTALLED_APPS`

### Error: "Reverse accessor clash"

Solución: Ya corregido, usar `related_name='tournaments_creados'`

### Error: "No hay Jefe del Capitolio"

Solución: Crear usuario con rol 'jefe_capitolio' en admin

## Siguiente Paso

Integrar el widget de Torneos en el dashboard del Jefe del Capitolio. Ver:
- [TOURNAMENTS_INTEGRATION.md](TOURNAMENTS_INTEGRATION.md)

## Comandos Útiles

```bash
# Ver todas las migraciones
python manage.py showmigrations tournaments

# Crear superusuario
python manage.py createsuperuser

# Shell interactivo
python manage.py shell

# Ver todas las URLs
python manage.py show_urls

# Resetear datos (cuidado!)
python manage.py migrate tournaments zero
python manage.py migrate tournaments
```

¡Listo! La app tournaments está lista para ser usada.
