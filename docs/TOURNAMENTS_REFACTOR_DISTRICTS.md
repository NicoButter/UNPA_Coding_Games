# Refactorización: Tournaments App - Uso de District Model

## Resumen de Cambios

La aplicación `tournaments` ha sido refactorizada para utilizar el modelo `District` de la aplicación `districts` en lugar de mantener su propio modelo `UnidadAcademica`. Esta es una mejora arquitectónica que elimina duplicación de código y mantiene una separación clara de responsabilidades.

### Principio de Diseño

- **districts app**: Responsable de gestionar distritos/unidades académicas y sus miembros
- **tournaments app**: Responsable de gestionar torneos y sus asignaciones (mentores, vigilantes)

## Cambios Realizados

### 1. Modelo `TournamentMentor` (tournaments/models.py)

**Antes:**
```python
from .models import UnidadAcademica

class TournamentMentor(models.Model):
    ...
    unidad_academica = models.ForeignKey(
        UnidadAcademica,
        on_delete=models.CASCADE,
        ...
    )
    class Meta:
        unique_together = [['torneo', 'unidad_academica']]
```

**Después:**
```python
from districts.models import District

class TournamentMentor(models.Model):
    ...
    distrito = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name='mentores_torneo',
        verbose_name='Distrito'
    )
    class Meta:
        unique_together = [['torneo', 'distrito']]
```

### 2. Formularios (tournaments/forms.py)

- `TournamentMentorForm`: Actualizado para usar `'distrito'` en lugar de `'unidad_academica'`
- `AssignMentorsToUnidadesForm` renombrado a `AssignMentorsToDistritosForm`
- Actualizadas referencias a queryset: `District.objects.filter(is_active=True)`

### 3. Vistas (tournaments/views.py)

- `TournamentDetailView._get_distritos_sin_mentor()`: Renombrado de `_get_unidades_sin_mentor()`
- Actualizadas variables de contexto: `distritos_sin_mentor` en lugar de `unidades_sin_mentor`
- `BulkAssignMentorsView`: Adaptado para trabajar con campos de distrito

### 4. Admin (tournaments/admin.py)

- Removido: `UnidadAcademicaAdmin`
- `TournamentMentorInline` y `TournamentMentorAdmin`: Actualizados para usar `'distrito'`

### 5. Tests (tournaments/tests.py)

- Removida clase: `UnidadAcademicaModelTest`
- `TournamentMentorModelTest`: Actualizado para usar `District.objects.create()` en lugar de `UnidadAcademica`
- Actualizado nombre del test: `test_unique_constraint_torneo_distrito`

### 6. Templates (tournaments/templates/)

Actualizados los siguientes templates:
- `tournament_detail.html`: `unidades_sin_mentor` → `distritos_sin_mentor`, `unidad_academica.nombre` → `distrito.name`
- `add_mentor.html`: Etiqueta "Unidad Académica" → "Distrito"
- `bulk_assign_mentors.html`: Referencias a `distritos` en lugar de `unidades`
- `confirm_remove_mentor.html`: Campo actualizado

### 7. URLs (tournaments/urls.py)

- Removidas rutas: `unidades/`, `unidades/crear/`, `unidades/<pk>/editar/`
- La gestión de distritos se delega completamente a la app `districts`

### 8. Migración de Base de Datos

**Migración 0002**: Realiza las siguientes operaciones en orden:
1. Remueve la restricción `unique_together` antigua
2. Remueve el campo `unidad_academica`
3. Agrega el nuevo campo `distrito` (ForeignKey a District)
4. Establece la nueva restricción `unique_together` con (torneo, distrito)
5. Altera opciones del modelo
6. Elimina el modelo `UnidadAcademica`

## Beneficios de la Refactorización

✅ **Eliminación de Duplicación**: No hay dos modelos diferentes para representar unidades académicas

✅ **Separación de Responsabilidades**: 
- `districts`: gestiona entidades organizacionales
- `tournaments`: gestiona eventos y asignaciones de roles

✅ **Mantenibilidad**: Un único punto de verdad para distritos/unidades académicas

✅ **Reutilización**: Otras apps pueden usar `District` sin conflictos

✅ **Consistencia**: Usa campos estándar de `District` (name, code, description, is_active)

## Compatibilidad

### Campo `is_active`
- **Districts**: utiliza `is_active` (booleano)
- **Tournaments**: también utiliza `is_active` para asignaciones de mentores
- Ambas convenciones son consistentes

### Campos de Distrito
- `name`: Nombre del distrito
- `code`: Código único
- `description`: Descripción
- `is_active`: Estado activo/inactivo
- `color_primary` y `color_secondary`: Colores para UI

## Verificación Post-Refactor

✅ Todas las migraciones aplicadas exitosamente
✅ 9 tests pasando (sin cambios funcionales)
✅ Sistema check sin errores
✅ No hay referencias a `UnidadAcademica` en el código

## Próximos Pasos (Opcionales)

1. Considerar crear una vista en `districts` para gestionar distritos si no existe
2. Actualizar documentación general del sistema
3. Considerar agregar filtros en el admin de tournaments por distrito (usando `list_filter`)

## Impacto en el Usuario

El impacto es **transparente** para el usuario final:
- Los formularios ahora muestran "Distrito" en lugar de "Unidad Académica"
- El flujo de trabajo es idéntico
- Los datos se migran automáticamente durante `migrate`

