# Instrucciones de Migración - Sistema de Juez

## Pasos para activar el sistema de juez automático

### 1. Verificar instalación de dependencias

```bash
cd /home/lordcommander/proyectos_2024/UNPA_Coding_Games
pip install -r requirements.txt
```

Esto instalará:
- `docker==7.0.0` - Cliente Python para Docker

### 2. Verificar Docker

Asegurarse de que Docker esté instalado y corriendo:

```bash
# Ver versión de Docker
docker --version

# Si no está instalado en Fedora:
sudo dnf install docker

# Iniciar Docker
sudo systemctl start docker
sudo systemctl enable docker

# Agregar usuario al grupo docker (para no usar sudo)
sudo usermod -aG docker $USER

# Cerrar sesión y volver a iniciar, o ejecutar:
newgrp docker

# Verificar que funciona
docker ps
```

### 3. Crear migraciones

```bash
python manage.py makemigrations arena
python manage.py makemigrations judge
```

Esto creará las migraciones para:
- Los nuevos campos en el modelo `Reto` (arena)
- El modelo `Submission` (judge)

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Descargar imágenes Docker

Opción A - Usando el script de utilidades:

```bash
python manage.py shell
>>> from judge.management_utils import setup_docker_images
>>> setup_docker_images()
>>> exit()
```

Opción B - Manualmente:

```bash
docker pull python:3.11-slim
docker pull openjdk:17-slim
docker pull node:18-slim
```

### 6. Verificar instalación

```bash
python manage.py shell
>>> from judge.management_utils import check_docker_status
>>> check_docker_status()
>>> exit()
```

Deberías ver:
```
✓ Conexión a Docker exitosa

Imágenes necesarias:
  ✓ python: python:3.11-slim
  ✓ java: openjdk:17-slim
  ✓ javascript: node:18-slim

Contenedores activos: 0
```

### 7. Crear reto de ejemplo (opcional)

```bash
python manage.py shell
>>> from judge.management_utils import create_sample_challenge
>>> create_sample_challenge()
>>> exit()
```

### 8. Probar el sistema (opcional)

```bash
python manage.py shell
>>> from judge.management_utils import test_judge_system
>>> test_judge_system()
>>> exit()
```

Deberías ver:
```
=== Prueba del Sistema de Juez ===

Evaluando código Python...

Resultados:
  Veredicto: AC
  Puntos: 100
  Tests pasados: 2/2
  Tiempo: 0.156s

✓ Sistema funcionando correctamente
```

## Configuración de un reto con el juez

### Desde el Admin de Django

1. Acceder a `http://localhost:8000/admin/`
2. Ir a **Arena → Retos**
3. Crear o editar un reto
4. Configurar los siguientes campos:

**Campos existentes:**
- Título, descripción, enunciado (como antes)
- **Tiene validación automática**: ☑ Marcar
- **Lenguajes permitidos**: `python,java,javascript`

**Nuevos campos:**
- **Tests ocultos**: Agregar JSON con los tests (ver ejemplo abajo)
- **Límite tiempo**: `5.0` (segundos)
- **Límite memoria**: `256` (MB)

### Ejemplo de tests_ocultos

```json
{
    "python": [
        {
            "name": "Test Básico 1",
            "function_call": {
                "name": "suma",
                "args": [2, 3]
            },
            "expected": "5"
        },
        {
            "name": "Test Básico 2",
            "function_call": {
                "name": "suma",
                "args": [10, 20]
            },
            "expected": "30"
        },
        {
            "name": "Test con Negativos",
            "function_call": {
                "name": "suma",
                "args": [-5, 5]
            },
            "expected": "0"
        }
    ],
    "javascript": [
        {
            "name": "Test Básico 1",
            "function_call": {
                "name": "suma",
                "args": [2, 3]
            },
            "expected": "5"
        }
    ]
}
```

### Formato de tests

Cada test debe tener:
- `name`: Nombre descriptivo del test
- `function_call`: Objeto con:
  - `name`: Nombre de la función a llamar
  - `args`: Array de argumentos
- `expected`: Salida esperada (como string)

Para tests que usan stdin/stdout en lugar de funciones:
```json
{
    "name": "Test con Input",
    "input": "10 20",
    "expected": "30"
}
```

## Integrar en el frontend

### 1. Agregar formulario al dashboard del tributo

Copiar el código de `judge/example_frontend.html` al template del dashboard de tributos.

Ubicación sugerida: `dashboards/templates/dashboards/tributo_dashboard.html`

### 2. Modificar template de arena

En `arena/templates/arena/resolver_reto.html`, agregar el formulario de envío.

### 3. Agregar estilos (opcional)

Agregar los estilos de `judge/example_frontend.html` a los archivos CSS del proyecto.

## Testing manual completo

### 1. Crear un reto desde el admin

```
Título: Suma de Dos Números
Descripción: Implementa una función suma(a, b)
Lenguajes permitidos: python,javascript
Tiene validación automática: ☑
Tests ocultos: [ver JSON arriba]
Límite tiempo: 5.0
Límite memoria: 256
```

### 2. Desde el navegador

1. Login como tributo
2. Ir al dashboard
3. Seleccionar el reto
4. Escribir código:

**Python:**
```python
def suma(a, b):
    return a + b
```

**JavaScript:**
```javascript
function suma(a, b) {
    return a + b;
}
```

5. Click en "Enviar Solución"
6. Verificar resultado: Debería mostrar **AC (Accepted)** con 100 puntos

### 3. Probar caso fallido

Enviar código incorrecto:

```python
def suma(a, b):
    return a * b  # Multiplicación en vez de suma
```

Resultado esperado: **WA (Wrong Answer)**

### 4. Ver historial

Click en "Ver Historial" para ver todas las submissions anteriores.

## Troubleshooting

### Error: "No se pudo conectar a Docker"

```bash
sudo systemctl status docker
sudo systemctl start docker
```

### Error: "permission denied while trying to connect"

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Error: "Image not found"

```bash
docker pull python:3.11-slim
docker pull openjdk:17-slim
docker pull node:18-slim
```

### Submissions quedan en PE (Pending)

- Verificar logs del servidor Django
- Ejecutar `python manage.py runserver` y ver errores en consola
- Verificar que Docker está corriendo
- Verificar formato JSON de tests_ocultos

### TLE en todos los tests

- Aumentar `limite_tiempo` en el reto
- Verificar que el código no tiene loops infinitos
- Verificar que Docker no está sobrecargado

## Verificar que todo funciona

```bash
# 1. Verificar migración
python manage.py showmigrations arena judge

# 2. Verificar Docker
docker ps

# 3. Verificar imágenes
docker images | grep -E "python|openjdk|node"

# 4. Probar evaluación
python manage.py shell
>>> from judge.management_utils import test_judge_system
>>> test_judge_system()

# 5. Ver estadísticas (si hay submissions)
>>> from judge.management_utils import show_statistics
>>> show_statistics()
```

## Comandos útiles

### Ver todas las submissions
```bash
python manage.py shell
>>> from judge.models import Submission
>>> Submission.objects.all()
```

### Limpiar submissions de prueba
```bash
python manage.py shell
>>> from judge.models import Submission
>>> Submission.objects.filter(veredicto='PE').delete()
```

### Limpiar contenedores Docker
```bash
docker ps -a | grep "python\|openjdk\|node" | awk '{print $1}' | xargs docker rm -f
```

### Ver logs de evaluación en tiempo real
```bash
python manage.py runserver
# En otra terminal:
tail -f logs/judge.log  # Si configuras logging
```

## Próximos pasos

1. ✅ Sistema de juez implementado
2. ✅ Modelos creados
3. ✅ Vistas y URLs configuradas
4. ⏳ Integrar formulario en dashboard de tributos
5. ⏳ Agregar feedback visual mejorado
6. ⏳ Implementar sistema de cola para múltiples submissions
7. ⏳ Agregar soporte para más lenguajes (C++, Rust)

## Soporte

Para más información, ver:
- [judge/README.md](../judge/README.md) - Documentación del módulo
- [docs/JUDGE_SYSTEM.md](JUDGE_SYSTEM.md) - Documentación completa del sistema
