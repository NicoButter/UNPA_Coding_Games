# Sistema de Juez Automático - UNPA Coding Games

## Descripción General

El módulo `judge` implementa un sistema de evaluación automática de código que permite:

- Que tributos envíen soluciones desde su dashboard
- Ejecutar código en contenedores Docker aislados
- Evaluar contra tests ocultos definidos por el Jefe del Capitolio
- Retornar veredictos (PASS/FAIL), stdout, stderr y tiempo de ejecución
- Persistir resultados en base de datos

## Componentes

### 1. Modelos (`judge/models.py`)

#### Submission
Almacena cada entrega de código:
- Código fuente del tributo
- Lenguaje utilizado
- Veredicto de evaluación
- Puntos obtenidos
- Casos pasados/totales
- Métricas de ejecución (tiempo, memoria)
- Salidas stdout/stderr
- Detalles completos (solo para staff)

#### Extensión al modelo Reto
Se agregaron campos al modelo `Reto` en `arena/models.py`:
- `tests_ocultos`: JSONField con tests por lenguaje
- `limite_tiempo`: Límite de tiempo en segundos
- `limite_memoria`: Límite de memoria en MB

### 2. Plantillas de Ejecución (`judge/templates/`)

Plantillas que combinan el código del usuario con tests:

- **python.py**: Para código Python
- **java.java**: Para código Java  
- **js.js**: Para código JavaScript (Node.js)

Cada plantilla:
1. Inyecta el código del usuario
2. Agrega los tests ocultos
3. Ejecuta los tests
4. Retorna resultados en formato JSON

### 3. Ejecutor Docker (`judge/docker_executor.py`)

**Clase: `DockerExecutor`**

Ejecuta código en contenedores aislados con:
- **Sin acceso a red** (`network_disabled=True`)
- **Límites de CPU** (cpu_quota, cpu_period)
- **Límites de memoria** (mem_limit)
- **Límite de procesos** (pids_limit)
- **Timeout** configurable

Imágenes Docker utilizadas:
- Python: `python:3.11-slim`
- Java: `openjdk:17-slim`
- JavaScript: `node:18-slim`

### 4. Runner del Juez (`judge/runner.py`)

**Clase: `JudgeRunner`**

Orquesta el proceso de evaluación:

```python
runner = JudgeRunner()
resultado = runner.evaluate_submission(
    user_code="def suma(a, b): return a + b",
    language="python",
    tests=[
        {"name": "Test 1", "function_call": {"name": "suma", "args": [2, 3]}, "expected": "5"},
        {"name": "Test 2", "function_call": {"name": "suma", "args": [10, 20]}, "expected": "30"}
    ],
    time_limit=5.0,
    memory_limit=256
)
```

Retorna:
```python
{
    'veredicto': 'AC',  # AC, WA, TLE, MLE, RE, CE, SE, PE
    'puntos': 100,
    'casos_pasados': 2,
    'casos_totales': 2,
    'tiempo_ejecucion': 0.123,
    'stdout': '...',
    'stderr': '',
    'detalles': {...}
}
```

### 5. Vistas (`judge/views.py`)

#### `submit_solution(request, reto_id)`
- **Método:** POST
- **Permisos:** Login requerido, solo tributos
- **Parámetros POST:**
  - `codigo`: Código fuente
  - `lenguaje`: python, java o javascript

**Flujo:**
1. Valida que el tributo puede enviar solución
2. Crea Submission en estado PE (Pending)
3. Ejecuta JudgeRunner
4. Actualiza Submission con resultados
5. Retorna veredicto (sin detalles de tests)

#### `submission_detail(request, submission_id)`
- **Método:** GET
- **Permisos:** Solo el tributo dueño o staff

Retorna detalles de una submission específica.

#### `submission_history(request, reto_id)`
- **Método:** GET
- **Permisos:** Solo el tributo

Retorna historial de submissions del tributo para un reto.

## Uso

### 1. Configurar un Reto con Tests Ocultos

Como Jefe del Capitolio, en el admin de Django:

```python
# Ejemplo de tests_ocultos para un reto "Suma de dos números"
{
    "python": [
        {
            "name": "Test Básico",
            "function_call": {
                "name": "suma",
                "args": [2, 3]
            },
            "expected": "5"
        },
        {
            "name": "Test con Negativos",
            "function_call": {
                "name": "suma",
                "args": [-5, 10]
            },
            "expected": "5"
        }
    ],
    "java": [
        {
            "name": "Test Básico",
            "input": "2 3",
            "expected": "5"
        }
    ],
    "javascript": [
        {
            "name": "Test Básico",
            "function_call": {
                "name": "suma",
                "args": [2, 3]
            },
            "expected": "5"
        }
    ]
}
```

### 2. Enviar Solución desde el Frontend

```javascript
// Ejemplo con fetch API
fetch('/judge/submit/1/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: new URLSearchParams({
        'codigo': 'def suma(a, b):\n    return a + b',
        'lenguaje': 'python'
    })
})
.then(response => response.json())
.then(data => {
    console.log('Veredicto:', data.veredicto);
    console.log('Puntos:', data.puntos_obtenidos);
    console.log('Tests pasados:', data.casos_pasados, '/', data.casos_totales);
});
```

### 3. Respuesta del Sistema

```json
{
    "success": true,
    "submission_id": 42,
    "veredicto": "Accepted",
    "veredicto_code": "AC",
    "puntos_obtenidos": 100,
    "casos_pasados": 2,
    "casos_totales": 2,
    "porcentaje_exito": 100.0,
    "tiempo_ejecucion": 0.156,
    "es_aceptado": true
}
```

## Veredictos

| Código | Significado | Descripción |
|--------|------------|-------------|
| AC | Accepted | Todos los tests pasaron |
| WA | Wrong Answer | Output incorrecto |
| TLE | Time Limit Exceeded | Excedió el tiempo límite |
| MLE | Memory Limit Exceeded | Excedió el límite de memoria |
| RE | Runtime Error | Error durante la ejecución |
| CE | Compilation Error | Error de compilación (Java) |
| SE | System Error | Error del sistema de evaluación |
| PE | Pending | Aún no evaluado |

## Seguridad

### Restricciones Implementadas

1. **Aislamiento por Docker**
   - Cada ejecución en contenedor efímero
   - Sin acceso a red
   - Sin acceso al filesystem del host

2. **Límites de Recursos**
   - CPU limitado a 1 core
   - Memoria configurable (default 256MB)
   - Timeout configurable (default 5s)
   - Límite de procesos (50 max)

3. **Tests Ocultos**
   - Nunca se envían al frontend
   - Solo accesibles por Jefe del Capitolio
   - Almacenados en JSONField del Reto

4. **Filtrado de Información**
   - stderr filtrado antes de mostrar al tributo
   - Paths internos removidos
   - Información del sistema oculta

## Instalación y Setup

### 1. Requisitos

```bash
pip install django docker
```

### 2. Docker

Asegurarse de que Docker está instalado y corriendo:

```bash
docker --version
docker ps
```

### 3. Migrar Base de Datos

```bash
python manage.py makemigrations arena judge
python manage.py migrate
```

### 4. Descargar Imágenes Docker

```python
from judge.docker_executor import DockerExecutor

executor = DockerExecutor()
executor.pull_images()
```

O desde línea de comandos:

```bash
docker pull python:3.11-slim
docker pull openjdk:17-slim
docker pull node:18-slim
```

## Testing

### Test Manual

```python
# En el shell de Django
from judge.runner import JudgeRunner

runner = JudgeRunner()

# Test Python
code = """
def suma(a, b):
    return a + b
"""

tests = [
    {
        "name": "Test 1",
        "function_call": {"name": "suma", "args": [2, 3]},
        "expected": "5"
    }
]

resultado = runner.evaluate_submission(code, "python", tests)
print(resultado)
```

## Extensibilidad

### Agregar Nuevo Lenguaje (Ej: Rust)

1. **Agregar imagen Docker** en `docker_executor.py`:
```python
IMAGES = {
    ...
    'rust': 'rust:1.70-slim'
}
```

2. **Agregar comando de ejecución**:
```python
COMMANDS = {
    ...
    'rust': ['sh', '-c', 'cd /code && rustc solution.rs && ./solution']
}
```

3. **Crear plantilla** `judge/templates/rust.rs`

4. **Actualizar LENGUAJE_CHOICES** en `models.py`

## Mantenimiento

### Limpiar Contenedores Antiguos

```python
from judge.docker_executor import DockerExecutor

executor = DockerExecutor()
executor.cleanup_old_containers()
```

### Monitoreo

Ver submissions recientes:

```python
from judge.models import Submission

# Últimas 10 submissions
Submission.objects.all()[:10]

# Por veredicto
Submission.objects.filter(veredicto='AC').count()
Submission.objects.filter(veredicto='WA').count()
```

## Limitaciones Conocidas

1. Java requiere compilación, puede ser más lento
2. Tests ocultos deben definirse manualmente por el Jefe del Capitolio
3. Solo soporta I/O basado en funciones o stdin/stdout
4. No soporta tests interactivos

## Troubleshooting

### Error: "No se pudo conectar a Docker"
- Verificar que Docker esté corriendo: `systemctl start docker`
- Verificar permisos: agregar usuario a grupo docker

### Error: "Imagen no encontrada"
- Ejecutar `executor.pull_images()` para descargar imágenes

### TLE en todos los tests
- Aumentar `limite_tiempo` en el Reto
- Verificar que el código del tributo no tenga loops infinitos

### Submission queda en PE
- Ver logs del servidor para errores
- Verificar que tests_ocultos está bien formateado

## Roadmap Futuro

- [ ] Soporte para más lenguajes (Rust, C++, Go)
- [ ] Tests interactivos
- [ ] Análisis de complejidad temporal
- [ ] Sistema de cola para múltiples submissions
- [ ] Caché de resultados para código idéntico
- [ ] Métricas avanzadas (cobertura de código)
