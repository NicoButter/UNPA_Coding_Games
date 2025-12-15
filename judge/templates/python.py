"""
Plantilla de ejecución para Python
Combina el código del usuario con los tests ocultos
"""
import sys
import json
import time

# CÓDIGO DEL USUARIO
{user_code}

# FUNCIÓN PRINCIPAL DE TESTING
def __run_tests():
    """Ejecuta los tests ocultos y retorna resultados"""
    tests = {tests_json}
    results = []
    total_time = 0
    
    for i, test in enumerate(tests):
        test_input = test.get('input', '')
        expected_output = test.get('expected', '')
        test_name = test.get('name', f'Test {i+1}')
        
        try:
            # Preparar entrada
            if test_input:
                sys.stdin = __import__('io').StringIO(test_input)
            
            # Capturar salida
            import io
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            # Medir tiempo
            start_time = time.time()
            
            # Ejecutar función del usuario
            if 'function_call' in test:
                # Si el test especifica una función a llamar
                func_name = test['function_call']['name']
                func_args = test['function_call'].get('args', [])
                func_kwargs = test['function_call'].get('kwargs', {})
                
                result = globals()[func_name](*func_args, **func_kwargs)
                actual_output = str(result).strip()
            else:
                # Si se espera que el código imprima directamente
                exec(test.get('code', ''), globals())
                actual_output = captured_output.getvalue().strip()
            
            elapsed_time = time.time() - start_time
            total_time += elapsed_time
            
            # Restaurar stdout
            sys.stdout = sys.__stdout__
            
            # Comparar salidas
            expected_clean = str(expected_output).strip()
            passed = actual_output == expected_clean
            
            results.append({
                'name': test_name,
                'passed': passed,
                'time': elapsed_time,
                'expected': expected_clean,
                'actual': actual_output
            })
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            total_time += elapsed_time
            sys.stdout = sys.__stdout__
            
            results.append({
                'name': test_name,
                'passed': False,
                'time': elapsed_time,
                'error': str(e),
                'error_type': type(e).__name__
            })
    
    # Imprimir resultados en JSON
    print(json.dumps({
        'tests': results,
        'total_time': total_time,
        'passed': sum(1 for r in results if r['passed']),
        'total': len(results)
    }))

if __name__ == '__main__':
    __run_tests()
