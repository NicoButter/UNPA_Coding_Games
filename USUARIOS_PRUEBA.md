# Usuarios de Prueba - UNPA Coding Games

## 🎯 Usuarios Creados

Se han creado **4 usuarios de prueba**, uno para cada rol del sistema:

### 1. Tributo
```
Username: tributo
Password: tributo010203
Rol: Tributo del Distrito 12
```

### 2. Mentor
```
Username: mentor
Password: mentor010203
Rol: Mentor del Distrito 12
Unidad: UNPA Sede Caleta Olivia
```

### 3. Vigilante
```
Username: vigilante
Password: vigilante010203
Rol: Vigilante (Peacekeeper)
```

### 4. Jefe del Capitolio
```
Username: jefe_capitolio
Password: jefe_capitolio010203
Rol: Administrador Principal
Permisos: Superusuario (acceso total al admin)
```

## 🚀 Cómo Crear los Usuarios

### Opción 1: Management Command (Recomendado)

```bash
python manage.py crear_usuarios_prueba
```

### Opción 2: Script Directo

```bash
python crear_usuarios_test.py
```

### Opción 3: Django Shell

```bash
python manage.py shell
>>> exec(open('crear_usuarios_test.py').read())
```

## 📋 Permisos por Rol

### Tributo
- ✅ Ver torneos disponibles
- ✅ Participar en retos
- ✅ Enviar soluciones de código
- ✅ Ver su historial de submissions
- ✅ Ver resultados y puntos
- ❌ No acceso al admin

### Mentor
- ✅ Ver tributos de su distrito
- ✅ Enviar ayudas/patrocinio
- ✅ Ver soluciones de sus tributos
- ✅ Acceso limitado al admin
- ❌ No puede crear torneos/retos

### Vigilante
- ✅ Supervisar torneos asignados
- ✅ Monitorear participaciones
- ✅ Ver estadísticas
- ✅ Acceso limitado al admin
- ❌ No puede crear torneos/retos

### Jefe del Capitolio
- ✅ Acceso total al admin
- ✅ Crear y gestionar torneos
- ✅ Crear y gestionar retos
- ✅ Configurar tests automáticos
- ✅ Asignar mentores y vigilantes
- ✅ Ver todas las estadísticas

## 🌐 URLs de Acceso

### Login General
```
http://localhost:8000/login/
```

### Admin Django (Solo Jefe del Capitolio)
```
http://localhost:8000/admin/
Username: jefe_capitolio
Password: jefe_capitolio010203
```

### Dashboards
Después de login, cada usuario es redirigido a su dashboard correspondiente:

- **Tributo**: `/dashboard/tributo/`
- **Mentor**: `/dashboard/mentor/`
- **Vigilante**: `/dashboard/vigilante/`
- **Jefe del Capitolio**: `/dashboard/jefe-capitolio/`

## 🧪 Flujo de Pruebas Sugerido

### 1. Como Jefe del Capitolio
```
1. Login: http://localhost:8000/admin/
   User: jefe_capitolio
   Pass: jefe_capitolio010203

2. Crear un Torneo:
   Admin → Arena → Torneos → Añadir

3. Crear Retos con Juez:
   Admin → Arena → Retos → Añadir
   - Marcar "tiene_validacion_automatica"
   - Configurar tests_ocultos
   - Guardar

4. Cambiar estado del torneo a "Inscripción Abierta"
```

### 2. Como Tributo
```
1. Login: http://localhost:8000/login/
   User: tributo
   Pass: tributo010203

2. Ver torneos disponibles

3. Ingresar a un torneo

4. Seleccionar un reto

5. Escribir código y enviar solución

6. Ver resultado (AC, WA, TLE, etc.)
```

### 3. Como Mentor
```
1. Login: http://localhost:8000/login/
   User: mentor
   Pass: mentor010203

2. Ver tributos de su distrito

3. Enviar ayudas/patrocinio

4. Ver progreso de tributos
```

### 4. Como Vigilante
```
1. Login: http://localhost:8000/login/
   User: vigilante
   Pass: vigilante010203

2. Monitorear torneos asignados

3. Ver estadísticas y participaciones
```

## 🔄 Eliminar Usuarios de Prueba

Si necesitas eliminar los usuarios de prueba:

### Desde Django Shell
```python
python manage.py shell
>>> from capitol.models import Personaje
>>> Personaje.objects.filter(username__in=['tributo', 'mentor', 'vigilante', 'jefe_capitolio']).delete()
```

### Desde Admin
```
Admin → Capitol → Personajes → Seleccionar usuarios → Eliminar
```

## 📝 Notas Importantes

1. **Passwords**: Todos siguen el patrón `{rol}010203`
2. **Emails**: Son de prueba (@test.com), no funcionales
3. **Datos**: Son ficticios para testing
4. **Seguridad**: Cambiar passwords en producción
5. **Tributo**: Ya tiene TributoInfo creado automáticamente

## ⚙️ Personalización

Para crear usuarios adicionales, editar:
- `capitol/management/commands/crear_usuarios_prueba.py`
- `crear_usuarios_test.py`

Agregar nuevos usuarios a la lista `usuarios`.

## 🐛 Troubleshooting

### Error: "No module named 'django'"
Activar el entorno virtual primero:
```bash
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

### Error: "User already exists"
Los usuarios ya fueron creados. Para recrearlos, eliminarlos primero.

### Error: "UNIQUE constraint failed"
El username ya existe. Usar otro username o eliminar el existente.

## 📊 Verificar Usuarios Creados

```python
python manage.py shell
>>> from capitol.models import Personaje
>>> for user in Personaje.objects.filter(username__in=['tributo', 'mentor', 'vigilante', 'jefe_capitolio']):
...     print(f"{user.username} - {user.rol} - {user.is_staff}")
```

---

**Creado para**: UNPA Coding Games  
**Fecha**: 15 de diciembre de 2025  
**Versión**: 1.0
