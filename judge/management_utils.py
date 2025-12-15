#!/usr/bin/env python
"""
Script de utilidad para el sistema de juez automático
Ejecutar con: python manage.py shell < judge/utils.py
O importar funciones individualmente
"""

def setup_docker_images():
    """
    Descarga todas las imágenes Docker necesarias para el juez
    """
    from judge.docker_executor import DockerExecutor
    
    print("=== Configuración de Imágenes Docker ===\n")
    
    executor = DockerExecutor()
    executor.pull_images()
    
    print("\n✓ Configuración completada")


def create_sample_challenge():
    """
    Crea un reto de ejemplo con tests configurados
    Útil para probar el sistema
    """
    from arena.models import Torneo, Reto
    from capitol.models import Personaje
    from django.utils import timezone
    from datetime import timedelta
    
    print("=== Creando Reto de Ejemplo ===\n")
    
    # Buscar o crear torneo
    torneo = Torneo.objects.first()
    if not torneo:
        print("Error: No hay torneos creados. Crea uno desde el admin primero.")
        return
    
    # Buscar jefe del capitolio
    jefe = Personaje.objects.filter(rol='jefe_capitolio').first()
    if not jefe:
        print("Warning: No hay Jefe del Capitolio. Crear reto sin creador.")
    
    # Tests ocultos de ejemplo
    tests_ocultos = {
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
            },
            {
                "name": "Test con Grandes Números",
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
    
    # Crear reto
    reto = Reto.objects.create(
        torneo=torneo,
        titulo="Suma de Dos Números [EJEMPLO]",
        descripcion="Implementa una función que sume dos números enteros",
        enunciado="""
# Suma de Dos Números

## Descripción
Debes implementar una función llamada `suma` que reciba dos números enteros 
y retorne su suma.

## Especificación

### Python
```python
def suma(a: int, b: int) -> int:
    # Tu código aquí
    pass
```

### JavaScript
```javascript
function suma(a, b) {
    // Tu código aquí
}
```

## Ejemplos

### Entrada
```
suma(2, 3)
```

### Salida
```
5
```

### Entrada
```
suma(-5, 10)
```

### Salida
```
5
```

## Restricciones
- -1,000,000 ≤ a, b ≤ 1,000,000
- El resultado siempre será un número entero válido

## Puntuación
- 100 puntos por pasar todos los tests
        """,
        dificultad='novato',
        tipo='individual',
        categoria='Fundamentos',
        puntos_base=100,
        fecha_publicacion=timezone.now(),
        fecha_limite=timezone.now() + timedelta(days=30),
        is_activo=True,
        is_visible=True,
        tiene_validacion_automatica=True,
        lenguajes_permitidos='python,javascript',
        tests_ocultos=tests_ocultos,
        limite_tiempo=2.0,
        limite_memoria=128,
        creado_por=jefe
    )
    
    print(f"✓ Reto creado: {reto.titulo}")
    print(f"  ID: {reto.id}")
    print(f"  Lenguajes: {reto.lenguajes_permitidos}")
    print(f"  Tests Python: {len(tests_ocultos['python'])}")
    print(f"  Tests JavaScript: {len(tests_ocultos['javascript'])}")
    print(f"\nPara probar, envía este código:")
    print("\nPython:")
    print("def suma(a, b):")
    print("    return a + b")
    print("\nJavaScript:")
    print("function suma(a, b) {")
    print("    return a + b;")
    print("}")


def test_judge_system():
    """
    Prueba el sistema de juez con un código de ejemplo
    """
    from judge.runner import JudgeRunner
    
    print("=== Prueba del Sistema de Juez ===\n")
    
    runner = JudgeRunner()
    
    # Código Python de prueba
    user_code = """
def suma(a, b):
    return a + b
"""
    
    tests = [
        {
            "name": "Test 1",
            "function_call": {
                "name": "suma",
                "args": [2, 3]
            },
            "expected": "5"
        },
        {
            "name": "Test 2",
            "function_call": {
                "name": "suma",
                "args": [10, 20]
            },
            "expected": "30"
        }
    ]
    
    print("Evaluando código Python...")
    resultado = runner.evaluate_submission(
        user_code=user_code,
        language="python",
        tests=tests,
        time_limit=5.0,
        memory_limit=256
    )
    
    print("\nResultados:")
    print(f"  Veredicto: {resultado['veredicto']}")
    print(f"  Puntos: {resultado['puntos']}")
    print(f"  Tests pasados: {resultado['casos_pasados']}/{resultado['casos_totales']}")
    print(f"  Tiempo: {resultado.get('tiempo_ejecucion', 0):.3f}s")
    
    if resultado['veredicto'] == 'AC':
        print("\n✓ Sistema funcionando correctamente")
    else:
        print(f"\n✗ Error: {resultado.get('error', 'Unknown')}")
        print(f"  stderr: {resultado.get('stderr', '')}")


def cleanup_submissions():
    """
    Limpia submissions antiguas de prueba
    """
    from judge.models import Submission
    
    print("=== Limpieza de Submissions ===\n")
    
    count = Submission.objects.filter(veredicto='PE').count()
    if count > 0:
        confirm = input(f"¿Eliminar {count} submissions pendientes? (s/n): ")
        if confirm.lower() == 's':
            Submission.objects.filter(veredicto='PE').delete()
            print(f"✓ {count} submissions eliminadas")
    else:
        print("No hay submissions pendientes para limpiar")


def show_statistics():
    """
    Muestra estadísticas del sistema de juez
    """
    from judge.models import Submission
    from django.db.models import Count, Avg
    
    print("=== Estadísticas del Sistema de Juez ===\n")
    
    total = Submission.objects.count()
    print(f"Total de submissions: {total}")
    
    if total > 0:
        # Por veredicto
        print("\nPor veredicto:")
        stats = Submission.objects.values('veredicto').annotate(
            count=Count('id')
        ).order_by('-count')
        
        for stat in stats:
            veredicto = stat['veredicto']
            count = stat['count']
            percentage = (count / total) * 100
            print(f"  {veredicto}: {count} ({percentage:.1f}%)")
        
        # Por lenguaje
        print("\nPor lenguaje:")
        lang_stats = Submission.objects.values('lenguaje').annotate(
            count=Count('id')
        ).order_by('-count')
        
        for stat in lang_stats:
            print(f"  {stat['lenguaje']}: {stat['count']}")
        
        # Tiempo promedio
        avg_time = Submission.objects.filter(
            tiempo_ejecucion__isnull=False
        ).aggregate(Avg('tiempo_ejecucion'))['tiempo_ejecucion__avg']
        
        if avg_time:
            print(f"\nTiempo promedio de ejecución: {avg_time:.3f}s")
        
        # Tasa de éxito
        accepted = Submission.objects.filter(veredicto='AC').count()
        success_rate = (accepted / total) * 100
        print(f"Tasa de éxito (AC): {success_rate:.1f}%")


def check_docker_status():
    """
    Verifica el estado de Docker y las imágenes
    """
    from judge.docker_executor import DockerExecutor
    
    print("=== Estado de Docker ===\n")
    
    try:
        executor = DockerExecutor()
        print("✓ Conexión a Docker exitosa")
        
        print("\nImágenes necesarias:")
        for lang, image in executor.IMAGES.items():
            try:
                executor.client.images.get(image)
                print(f"  ✓ {lang}: {image}")
            except:
                print(f"  ✗ {lang}: {image} (no descargada)")
        
        # Contenedores activos
        containers = executor.client.containers.list()
        print(f"\nContenedores activos: {len(containers)}")
        
    except Exception as e:
        print(f"✗ Error conectando a Docker: {e}")
        print("\nAsegúrate de que Docker esté instalado y corriendo:")
        print("  - systemctl start docker")
        print("  - sudo usermod -aG docker $USER")


# Menú interactivo
def menu():
    """
    Menú interactivo para utilidades del juez
    """
    while True:
        print("\n" + "="*50)
        print("Sistema de Juez Automático - Utilidades")
        print("="*50)
        print("\n1. Configurar imágenes Docker")
        print("2. Crear reto de ejemplo")
        print("3. Probar sistema de juez")
        print("4. Ver estadísticas")
        print("5. Verificar estado de Docker")
        print("6. Limpiar submissions")
        print("0. Salir")
        
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == '1':
            setup_docker_images()
        elif opcion == '2':
            create_sample_challenge()
        elif opcion == '3':
            test_judge_system()
        elif opcion == '4':
            show_statistics()
        elif opcion == '5':
            check_docker_status()
        elif opcion == '6':
            cleanup_submissions()
        elif opcion == '0':
            print("\n¡Hasta luego!")
            break
        else:
            print("\nOpción no válida")


if __name__ == '__main__':
    menu()
