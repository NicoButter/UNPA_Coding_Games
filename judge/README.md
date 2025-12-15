# Judge - Sistema de Juez Automático

Módulo de evaluación automática de código para UNPA Coding Games.

## Estructura

```
judge/
├── __init__.py
├── apps.py                 # Configuración de la app Django
├── models.py              # Modelo Submission
├── admin.py               # Admin de Django
├── views.py               # Vistas para enviar/ver submissions
├── urls.py                # URLs de la app
├── runner.py              # Orquestador del juez
├── docker_executor.py     # Ejecutor de código en Docker
├── management_utils.py    # Utilidades de gestión
├── templates/             # Plantillas de ejecución
│   ├── python.py
│   ├── java.java
│   └── js.js
└── migrations/
```

## Características

✅ Ejecución de código en contenedores Docker aislados  
✅ Soporte para Python, Java y JavaScript  
✅ Límites de tiempo, memoria y CPU configurables  
✅ Sin acceso a red en contenedores  
✅ Tests ocultos (nunca visibles en frontend)  
✅ Veredictos: AC, WA, TLE, MLE, RE, CE, SE, PE  
✅ Persistencia de resultados en BD  
✅ API REST para integración  

## Quick Start

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar Docker

```bash
# Verificar Docker
docker --version

# Iniciar Docker
sudo systemctl start docker

# Agregar usuario a grupo docker (opcional)
sudo usermod -aG docker $USER
```

### 3. Migrar base de datos

```bash
python manage.py makemigrations arena judge
python manage.py migrate
```

### 4. Descargar imágenes Docker

```bash
python manage.py shell
>>> from judge.management_utils import setup_docker_images
>>> setup_docker_images()
```

O manualmente:

```bash
docker pull python:3.11-slim
docker pull openjdk:17-slim
docker pull node:18-slim
```

### 5. Crear reto de ejemplo

```bash
python manage.py shell
>>> from judge.management_utils import create_sample_challenge
>>> create_sample_challenge()
```

### 6. Probar el sistema

```bash
python manage.py shell
>>> from judge.management_utils import test_judge_system
>>> test_judge_system()
```

## Uso desde el Frontend

### Enviar solución

```javascript
const submitSolution = async (retoId, codigo, lenguaje) => {
    const formData = new FormData();
    formData.append('codigo', codigo);
    formData.append('lenguaje', lenguaje);
    
    const response = await fetch(`/judge/submit/${retoId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    });
    
    return await response.json();
};

// Uso
const resultado = await submitSolution(1, 'def suma(a, b): return a + b', 'python');
console.log(resultado.veredicto); // "Accepted"
console.log(resultado.puntos_obtenidos); // 100
```

### Ver historial

```javascript
const response = await fetch('/judge/history/1/');
const data = await response.json();
console.log(data.submissions); // Array de submissions
```

## Configurar Tests Ocultos

Como Jefe del Capitolio, en el admin:

1. Ir a **Arena > Retos**
2. Seleccionar o crear un reto
3. Marcar **Tiene validación automática**
4. Configurar **Lenguajes permitidos**: `python,java,javascript`
5. En **Tests ocultos**, agregar JSON:

```json
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
            "name": "Test Negativo",
            "function_call": {
                "name": "suma",
                "args": [-5, 10]
            },
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

6. Configurar **Límite tiempo**: `5.0` segundos
7. Configurar **Límite memoria**: `256` MB
8. Guardar

## API Endpoints

### POST `/judge/submit/<reto_id>/`
Envía una solución para evaluación.

**Parámetros:**
- `codigo`: Código fuente (string)
- `lenguaje`: `python`, `java` o `javascript`

**Respuesta:**
```json
{
    "success": true,
    "submission_id": 42,
    "veredicto": "Accepted",
    "veredicto_code": "AC",
    "puntos_obtenidos": 100,
    "casos_pasados": 5,
    "casos_totales": 5,
    "porcentaje_exito": 100.0,
    "tiempo_ejecucion": 0.234,
    "es_aceptado": true
}
```

### GET `/judge/submission/<submission_id>/`
Obtiene detalles de una submission.

### GET `/judge/history/<reto_id>/`
Obtiene historial de submissions del tributo para un reto.

## Veredictos

| Código | Nombre | Descripción |
|--------|--------|-------------|
| AC | Accepted | ✓ Todos los tests pasaron |
| WA | Wrong Answer | ✗ Output incorrecto |
| TLE | Time Limit Exceeded | ⏱ Excedió tiempo límite |
| MLE | Memory Limit Exceeded | 💾 Excedió memoria |
| RE | Runtime Error | ⚠ Error de ejecución |
| CE | Compilation Error | 🔨 Error de compilación |
| SE | System Error | 🔧 Error del sistema |
| PE | Pending | ⏳ En evaluación |

## Seguridad

- ✅ Código ejecutado en Docker aislado
- ✅ Sin acceso a red
- ✅ Límites de CPU, memoria y tiempo
- ✅ Tests ocultos nunca enviados al frontend
- ✅ stderr filtrado antes de mostrar
- ✅ Contenedores efímeros (se destruyen tras uso)

## Mantenimiento

### Ver estadísticas

```bash
python manage.py shell
>>> from judge.management_utils import show_statistics
>>> show_statistics()
```

### Limpiar contenedores antiguos

```python
from judge.docker_executor import DockerExecutor
executor = DockerExecutor()
executor.cleanup_old_containers()
```

### Verificar estado de Docker

```bash
python manage.py shell
>>> from judge.management_utils import check_docker_status
>>> check_docker_status()
```

## Troubleshooting

### Docker no está disponible
```bash
sudo systemctl start docker
sudo usermod -aG docker $USER
# Cerrar sesión y volver a iniciar
```

### Imágenes no descargadas
```bash
python manage.py shell
>>> from judge.management_utils import setup_docker_images
>>> setup_docker_images()
```

### TLE en todos los tests
- Aumentar `limite_tiempo` en el reto
- Verificar que el código del tributo no tiene loops infinitos

### Submission en estado PE
- Revisar logs del servidor
- Verificar formato JSON de `tests_ocultos`

## Documentación Completa

Ver [docs/JUDGE_SYSTEM.md](../docs/JUDGE_SYSTEM.md) para documentación completa.

## Licencia

Parte del proyecto UNPA Coding Games.
