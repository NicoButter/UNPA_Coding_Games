# Guía para el Jefe del Capitolio - Crear Retos con Juez Automático

## Acceso al Sistema

Como **Jefe del Capitolio**, tienes acceso completo para crear torneos y retos desde el **Admin de Django**.

### URL de Acceso
```
http://localhost:8000/admin/
```

## Flujo Completo: Crear Torneo y Retos

### 1️⃣ Crear un Torneo

1. En el admin, ir a **Arena → Torneos**
2. Click en **"Añadir Torneo"**
3. Completar los campos:

**Información Básica:**
- **Nombre**: Ej: "75th Hunger Games"
- **Edición**: Ej: 75
- **Descripción**: Descripción del torneo
- **Imagen**: (Opcional) Logo del torneo

**Fechas:**
- **Fecha de inicio**: Cuándo comienza el torneo
- **Fecha de fin**: Cuándo termina
- **Inicio inscripciones**: Cuándo pueden inscribirse
- **Fin inscripciones**: Fecha límite de inscripción

**Estado y Configuración:**
- **Estado**: "En Configuración" (cambiar a "Inscripción Abierta" cuando esté listo)
- **Torneo Activo**: ☑️ (activar)
- **Puntos mínimos ganar**: 0 (o definir mínimo)
- **Permite equipos**: ☐ (según preferencia)
- **Puntuación por distrito**: ☑️ (si quieres ranking por distrito)

**Personal Asignado:**
- **Creado por**: (Se auto-asigna)
- **Vigilantes asignados**: Seleccionar vigilantes (Peacekeepers)

4. Click en **"Guardar"**

### 2️⃣ Crear un Reto con Juez Automático

Una vez creado el torneo:

1. Ir a **Arena → Retos**
2. Click en **"Añadir Reto"**
3. Completar los campos:

#### Información Básica
- **Torneo**: Seleccionar el torneo creado
- **Título**: Ej: "Suma de Dos Números"
- **Descripción**: Breve descripción
- **Enunciado**: Descripción completa del problema (puede incluir Markdown)

Ejemplo de enunciado:
```markdown
# Suma de Dos Números

Implementa una función que sume dos números enteros.

## Entrada
Dos números enteros `a` y `b`

## Salida
La suma de `a + b`

## Ejemplo
**Entrada:** a=2, b=3
**Salida:** 5

## Restricciones
- -10^6 ≤ a, b ≤ 10^6
```

#### Clasificación
- **Dificultad**: Novato / Intermedio / Avanzado / Experto
- **Tipo**: Individual / Por Equipo / Por Distrito
- **Categoría**: Ej: "Algoritmos", "Estructuras de Datos"

#### Puntuación
- **Puntos base**: Ej: 100
- **Puntos bonus**: Ej: 20 (por velocidad)

#### Fechas
- **Fecha de publicación**: Cuándo se hace visible
- **Fecha límite**: (Opcional) Hasta cuándo se puede enviar

#### Configuración Básica
- **Reto Activo**: ☑️
- **Visible para Tributos**: ☑️
- **Archivo de datos**: (Opcional) Archivos de ejemplo

#### ⚙️ Sistema de Juez Automático

**Este es el apartado clave para el juez:**

1. **Tiene validación automática**: ☑️ **MARCAR ESTO**

2. **Lenguajes permitidos**: `python,javascript,java`
   - Separar por comas
   - Solo los lenguajes que quieres permitir

3. **Tests ocultos**: **Aquí defines los tests que evalúan el código**

   Formato JSON por lenguaje:

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
                "args": [-5, 10]
            },
            "expected": "5"
        },
        {
            "name": "Test con Ceros",
            "function_call": {
                "name": "suma",
                "args": [0, 0]
            },
            "expected": "0"
        },
        {
            "name": "Test Números Grandes",
            "function_call": {
                "name": "suma",
                "args": [1000000, 2000000]
            },
            "expected": "3000000"
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
        },
        {
            "name": "Test Básico 2",
            "function_call": {
                "name": "suma",
                "args": [10, 20]
            },
            "expected": "30"
        }
    ]
}
```

4. **Límite de tiempo**: `5.0` (segundos)
   - Tiempo máximo que puede tardar cada test
   - Recomendado: 2.0 - 10.0 segundos

5. **Límite de memoria**: `256` (MB)
   - Memoria máxima permitida
   - Recomendado: 128 - 512 MB

6. Click en **"Guardar"**

## Formatos de Tests

### Formato 1: Llamada a Función (Recomendado)

```json
{
    "name": "Nombre descriptivo del test",
    "function_call": {
        "name": "nombre_de_la_funcion",
        "args": [arg1, arg2, arg3]
    },
    "expected": "resultado_esperado_como_string"
}
```

**Ejemplo para función que verifica si un número es par:**
```json
{
    "python": [
        {
            "name": "Test: 4 es par",
            "function_call": {
                "name": "es_par",
                "args": [4]
            },
            "expected": "True"
        },
        {
            "name": "Test: 5 no es par",
            "function_call": {
                "name": "es_par",
                "args": [5]
            },
            "expected": "False"
        }
    ]
}
```

### Formato 2: Input/Output (Para stdin/stdout)

```json
{
    "name": "Test con entrada estándar",
    "input": "10 20",
    "expected": "30"
}
```

**Ejemplo para programa que lee dos números y imprime su suma:**
```json
{
    "java": [
        {
            "name": "Test 1",
            "input": "2 3",
            "expected": "5"
        },
        {
            "name": "Test 2",
            "input": "100 200",
            "expected": "300"
        }
    ]
}
```

## Ejemplos Completos de Retos

### Ejemplo 1: Función Simple - Factorial

**Enunciado:**
```
Implementa una función factorial(n) que calcule el factorial de n.
```

**Tests ocultos:**
```json
{
    "python": [
        {
            "name": "Factorial de 0",
            "function_call": {"name": "factorial", "args": [0]},
            "expected": "1"
        },
        {
            "name": "Factorial de 1",
            "function_call": {"name": "factorial", "args": [1]},
            "expected": "1"
        },
        {
            "name": "Factorial de 5",
            "function_call": {"name": "factorial", "args": [5]},
            "expected": "120"
        },
        {
            "name": "Factorial de 10",
            "function_call": {"name": "factorial", "args": [10]},
            "expected": "3628800"
        }
    ],
    "javascript": [
        {
            "name": "Factorial de 5",
            "function_call": {"name": "factorial", "args": [5]},
            "expected": "120"
        }
    ]
}
```

### Ejemplo 2: Función con String - Invertir Texto

**Enunciado:**
```
Implementa una función invertir(texto) que invierta un string.
```

**Tests ocultos:**
```json
{
    "python": [
        {
            "name": "Test palabra simple",
            "function_call": {"name": "invertir", "args": ["hola"]},
            "expected": "aloh"
        },
        {
            "name": "Test string vacío",
            "function_call": {"name": "invertir", "args": [""]},
            "expected": ""
        },
        {
            "name": "Test con espacios",
            "function_call": {"name": "invertir", "args": ["hello world"]},
            "expected": "dlrow olleh"
        }
    ]
}
```

### Ejemplo 3: Función con Lista - Máximo

**Enunciado:**
```
Implementa una función maximo(lista) que retorne el número mayor de una lista.
```

**Tests ocultos:**
```json
{
    "python": [
        {
            "name": "Lista simple",
            "function_call": {"name": "maximo", "args": [[1, 5, 3, 2]]},
            "expected": "5"
        },
        {
            "name": "Con negativos",
            "function_call": {"name": "maximo", "args": [[-10, -5, -20]]},
            "expected": "-5"
        },
        {
            "name": "Un solo elemento",
            "function_call": {"name": "maximo", "args": [[42]]},
            "expected": "42"
        }
    ]
}
```

## ⚠️ Consideraciones Importantes

### Seguridad
- ✅ Los **tests_ocultos** NUNCA son visibles para los tributos
- ✅ Solo el Jefe del Capitolio puede verlos en el admin
- ✅ El tributo solo ve: veredicto (AC/WA/TLE/etc), puntos, tests pasados/totales

### Tests
- Crear al menos **5-10 tests** por lenguaje
- Incluir casos **normales, extremos y límite**
- Cubrir todos los escenarios posibles
- El orden no importa (se ejecutan todos)

### Límites
- **Tiempo**: Probar localmente y dar margen (2x-3x del tiempo real)
- **Memoria**: 256MB es suficiente para mayoría de problemas
- **Casos de prueba**: Puedes tener casos "ejemplo" visibles (en CasoDePrueba)

### Formato JSON
- Usar comillas dobles `"`, no simples `'`
- Los valores esperados siempre como string: `"5"` no `5`
- Verificar JSON válido: https://jsonlint.com/

## Verificar que Funciona

Después de crear el reto:

1. **Crear reto de prueba** con tests simples
2. **Probar desde terminal:**

```bash
python manage.py shell
>>> from judge.management_utils import test_judge_system
>>> test_judge_system()
```

3. **O probar con código específico:**

```python
from judge.runner import JudgeRunner
from arena.models import Reto

# Obtener el reto
reto = Reto.objects.get(id=1)

# Código de prueba
codigo = """
def suma(a, b):
    return a + b
"""

# Ejecutar
runner = JudgeRunner()
resultado = runner.evaluate_submission(
    user_code=codigo,
    language='python',
    tests=reto.tests_ocultos['python'],
    time_limit=reto.limite_tiempo,
    memory_limit=reto.limite_memoria
)

print(resultado)
```

## Flujo Completo en Resumen

```
1. Jefe del Capitolio crea Torneo
   ↓
2. Jefe crea Retos para ese Torneo
   ↓
3. Configura tests_ocultos en JSON
   ↓
4. Marca "tiene_validacion_automatica"
   ↓
5. Guarda el reto
   ↓
6. Tributos ven el reto en su dashboard
   ↓
7. Tributo envía código
   ↓
8. Sistema ejecuta en Docker con tests
   ↓
9. Tributo recibe veredicto (AC/WA/etc)
   ↓
10. Jefe puede ver todas las submissions en admin
```

## Recursos Adicionales

- **Documentación completa**: `docs/JUDGE_SYSTEM.md`
- **Ejemplos de tests**: `judge/management_utils.py` (función `create_sample_challenge`)
- **Formato JSON**: Ver archivo de documentación del juez

## Preguntas Frecuentes

**P: ¿Puedo tener diferentes tests para cada lenguaje?**
R: Sí, cada lenguaje tiene su propia lista de tests en el JSON.

**P: ¿Los tributos pueden ver los tests?**
R: NO. Los tests_ocultos NUNCA se envían al frontend. Solo ven el resultado.

**P: ¿Puedo modificar tests después de crear el reto?**
R: Sí, puedes editar el reto y cambiar los tests en cualquier momento.

**P: ¿Qué pasa si un test falla?**
R: El tributo recibe "WA" (Wrong Answer) y ve cuántos tests pasó del total, pero no ve cuál falló específicamente.

**P: ¿Puedo crear tests visibles de ejemplo?**
R: Sí, usa el modelo **CasoDePrueba** (en el inline del reto) para tests visibles. Los tests_ocultos son solo para el juez.

**P: ¿Necesito crear tests para todos los lenguajes permitidos?**
R: Es recomendable, pero si solo defines para Python, solo Python estará disponible para ese reto específicamente.
