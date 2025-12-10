# Sistema de Resolución de Retos - UNPA Coding Games

## ✅ Implementación Completada

### Características Implementadas

#### 1. **Lista de Torneos Disponibles** (`/arena/torneos/`)
- Muestra todos los torneos activos (estado: inscripción o en curso)
- Vista de tarjetas con información del torneo
- Filtrado automático por fechas
- Solo accesible para tributos

#### 2. **Arena del Torneo** (`/arena/torneo/<id>/`)
- Vista principal con los 5 retos del torneo
- Grid responsive con tarjetas de cada reto
- Estados visuales por reto:
  - ✅ Completado (verde)
  - ⏳ En Progreso (amarillo)
  - ❌ Fallido (rojo)
  - ● Sin Iniciar (gris)
- **Timer en tiempo real** que cuenta regresivamente
- Auto-finalización al acabar el tiempo
- Estadísticas en tiempo real:
  - Retos completados
  - Puntos totales
  - Tiempo restante
- **Navegación libre** entre retos
- Botón de "Finalizar Participación"

#### 3. **Editor de Código** (`/arena/reto/<id>/`)
- **Panel dividido** (enunciado | editor)
- **CodeMirror** integrado con:
  - Resaltado de sintaxis
  - Numeración de líneas
  - Tema Monokai
  - Auto-cierre de brackets
- **Casos de ejemplo** visibles
- Selección de lenguaje de programación
- **Validación AJAX** en tiempo real
- **Intentos ilimitados**
- Botón para limpiar código
- **Feedback inmediato**:
  - Casos pasados vs totales
  - Puntos obtenidos
  - Detalle por cada caso de prueba
  - Entrada, salida esperada, tu salida
  - Casos privados (ocultos)

#### 4. **Sistema de Validación Automática**
```python
def ejecutar_codigo(codigo, lenguaje, entrada):
    # Ejecuta código con subprocess
    # Timeout de 5 segundos
    # Captura stdout/stderr
    # Compara con salida esperada
    # Calcula puntos
```

**Características**:
- Ejecución segura con timeout
- Comparación exacta de salidas
- Manejo de errores
- Puntuación automática:
  - Puntos base por caso correcto
  - Bonus por primer intento exitoso
- Casos de prueba visibles y ocultos
- Actualización de ranking del distrito

#### 5. **Resultados Finales** (`/arena/torneo/<id>/resultados/`)
- Resumen completo de participación
- Tabla con detalle por reto
- Ranking del distrito
- Estadísticas personales
- Mensajes motivacionales según rendimiento

### Flujo de Uso

```
1. Tributo accede → Dashboard
2. Click en "Torneos Disponibles"
3. Selecciona un torneo → Vista Arena
4. Ve 5 retos con estado y puntos
5. Click en "Resolver" → Editor de código
6. Escribe solución
7. Click "Enviar Solución" → Validación automática
8. Ve resultados caso por caso
9. Si completó → Siguiente reto
   Si falló → Puede reintentar
10. Puede cambiar de reto en cualquier momento
11. Cuando termina → "Finalizar Participación"
12. Ve resultados finales y ranking
```

### Archivos Creados

#### Vistas (`arena/views.py`)
- `torneos_disponibles()` - Lista de torneos
- `arena_torneo()` - Vista principal del arena
- `resolver_reto()` - Editor de código
- `validar_solucion()` - Validación AJAX
- `ejecutar_codigo()` - Ejecución segura de código
- `actualizar_ranking_distrito()` - Actualiza rankings
- `finalizar_participacion()` - Finaliza torneo
- `resultado_torneo()` - Resultados finales

#### URLs (`arena/urls.py`)
```python
'torneos/' - Lista de torneos
'torneo/<id>/' - Arena del torneo
'reto/<id>/' - Editor de código
'reto/<id>/validar/' - Validación AJAX
'torneo/<id>/finalizar/' - Finalizar
'torneo/<id>/resultados/' - Resultados
```

#### Templates
- `torneos_disponibles.html` - Grid de torneos
- `arena_torneo.html` - Vista principal con retos
- `resolver_reto.html` - Editor CodeMirror
- `resultado_torneo.html` - Resultados finales

#### CSS
- `torneos.css` - Estilos para lista de torneos
- `arena.css` - Estilos del arena principal
- `resolver.css` - Estilos del editor
- `resultados.css` - Estilos de resultados

#### Otros
- `arena/templatetags/arena_filters.py` - Filtros personalizados
- `arena/forms.py` - Formularios completos

### Características Técnicas

#### Sistema de Estados
```python
ESTADOS = [
    ('no_iniciado', 'No Iniciado'),
    ('en_progreso', 'En Progreso'),
    ('enviado', 'Enviado'),
    ('validando', 'Validando'),
    ('completado', 'Completado'),
    ('fallido', 'Fallido'),
    ('tiempo_agotado', 'Tiempo Agotado'),
]
```

#### Sistema de Puntuación
- **Puntos base**: Definidos por el reto
- **Puntos por caso**: Cada caso de prueba tiene sus puntos
- **Bonus**: Solo en el primer intento exitoso
- **Ranking**: Suma de puntos de todos los tributos del distrito

#### Seguridad
- Login requerido (`@login_required`)
- Verificación de rol (solo tributos)
- Ejecución con timeout (5 segundos)
- Archivos temporales eliminados automáticamente
- CSRF protection
- Validación en backend

#### Tiempo Límite
- Configurado en el modelo Torneo
- Timer JavaScript en frontend
- Validación en backend
- Auto-finalización al acabar el tiempo
- Alerta visual cuando quedan < 5 minutos

### Dependencias Externas

#### CodeMirror (CDN)
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/theme/monokai.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/python/python.min.js"></script>
```

### Cómo Crear un Torneo con Retos

#### 1. Crear Torneo (Admin)
```python
torneo = Torneo.objects.create(
    nombre="Juegos del Hambre - Edición 2025",
    edicion=1,
    estado='inscripcion',
    fecha_inicio=datetime.now(),
    fecha_fin=datetime.now() + timedelta(hours=2),  # 2 horas
    puntos_minimos_ganar=100,
    creado_por=jefe_capitolio
)
```

#### 2. Crear Retos (5 retos con dificultad 1-5)
```python
# Reto 1 - Novato
reto1 = Reto.objects.create(
    torneo=torneo,
    titulo="Suma de dos números",
    dificultad='novato',
    puntos_base=10,
    puntos_bonus=5,
    tiene_validacion_automatica=True
)

# Casos de prueba
CasoDePrueba.objects.create(
    reto=reto1,
    nombre="Ejemplo 1",
    entrada="2 3",
    salida_esperada="5",
    es_ejemplo=True,
    is_visible=True,
    puntos=2
)
```

### Próximos Pasos Sugeridos

1. **Arena de Entrenamiento**: Retos de práctica sin tiempo límite
2. **Sistema de Teams**: Si `torneo.permite_equipos = True`
3. **Leaderboard Global**: Ranking de todos los tributos
4. **Historial de Participaciones**: Ver torneos anteriores
5. **Exportar Resultados**: CSV/PDF con resultados
6. **Notificaciones**: Alertas cuando hay nuevo torneo
7. **Chat/Comentarios**: Sistema de ayuda entre mentores y tributos
8. **Más Lenguajes**: Soporte para JavaScript, Java, C++

### Testing

Para probar el sistema:

```bash
# 1. Crear superusuario
python manage.py createsuperuser

# 2. Acceder al admin
http://127.0.0.1:8000/admin/

# 3. Crear:
- Un tributo (o registrarse)
- Un torneo
- 5 retos con casos de prueba
- Asignar mentor al distrito del tributo

# 4. Como tributo:
- Login
- Dashboard → "Torneos Disponibles"
- Seleccionar torneo
- Resolver retos
```

### Ejemplo de Código de Solución (Python)

```python
# Reto: Suma de dos números
# Entrada: Dos números separados por espacio
# Salida: La suma

entrada = input()
a, b = map(int, entrada.split())
print(a + b)
```

---

**Estado**: ✅ Sistema completamente funcional  
**Fecha**: 9 de diciembre de 2025  
**Desarrollador**: Nicolas Butterfield  
**Proyecto**: UNPA Coding Games
