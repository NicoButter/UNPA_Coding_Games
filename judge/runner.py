"""
Runner del juez automático
Orquesta el proceso de evaluación de código:
1. Combina código del usuario con tests ocultos
2. Ejecuta en Docker
3. Analiza resultados
4. Retorna veredicto y puntuación
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, List
from django.conf import settings

from .docker_executor import DockerExecutor


class JudgeRunner:
    """
    Orquestador principal del sistema de juez automático
    """
    
    def __init__(self):
        self.executor = DockerExecutor()
        self.templates_dir = Path(__file__).parent / 'templates'
    
    def evaluate_submission(
        self,
        user_code: str,
        language: str,
        tests: List[Dict[str, Any]],
        time_limit: float = 5.0,
        memory_limit: int = 256
    ) -> Dict[str, Any]:
        """
        Evalúa una solución enviada por un tributo
        
        Args:
            user_code: Código fuente del tributo
            language: Lenguaje de programación
            tests: Lista de tests ocultos a ejecutar
            time_limit: Límite de tiempo por ejecución
            memory_limit: Límite de memoria en MB
        
        Returns:
            Dict con veredicto, puntos, resultados detallados, stdout, stderr
        """
        # Validar lenguaje
        if language not in ['python', 'java', 'javascript']:
            return {
                'veredicto': 'SE',
                'error': f'Lenguaje no soportado: {language}',
                'puntos': 0,
                'casos_pasados': 0,
                'casos_totales': 0
            }
        
        # Validar que hay tests
        if not tests:
            return {
                'veredicto': 'SE',
                'error': 'No hay tests definidos para este reto',
                'puntos': 0,
                'casos_pasados': 0,
                'casos_totales': 0
            }
        
        try:
            # 1. Combinar código del usuario con plantilla de tests
            combined_code = self._combine_code_with_tests(
                user_code=user_code,
                language=language,
                tests=tests
            )
            
            # 2. Ejecutar en Docker
            execution_result = self.executor.execute(
                code=combined_code,
                language=language,
                time_limit=time_limit,
                memory_limit=memory_limit
            )
            
            # 3. Analizar resultados
            evaluation = self._analyze_results(
                execution_result=execution_result,
                total_tests=len(tests)
            )
            
            return evaluation
            
        except Exception as e:
            return {
                'veredicto': 'SE',
                'error': f'Error del sistema: {str(e)}',
                'puntos': 0,
                'casos_pasados': 0,
                'casos_totales': len(tests),
                'stdout': '',
                'stderr': str(e)
            }
    
    def _combine_code_with_tests(
        self,
        user_code: str,
        language: str,
        tests: List[Dict[str, Any]]
    ) -> str:
        """
        Combina el código del usuario con la plantilla de tests
        """
        # Cargar plantilla del lenguaje
        template_file = self.templates_dir / self._get_template_filename(language)
        
        if not template_file.exists():
            raise FileNotFoundError(f'Plantilla no encontrada: {template_file}')
        
        with open(template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Preparar tests en formato JSON
        tests_json = json.dumps(tests, ensure_ascii=False)
        
        # Para Java, necesitamos procesar diferente
        if language == 'java':
            # Asegurarse de que el código del usuario tiene la clase Solution
            if 'class Solution' not in user_code and 'public class Solution' not in user_code:
                user_code = f"class Solution {{\n{user_code}\n}}"
            
            # Reemplazar marcadores en la plantilla
            combined = template.replace('{user_code}', user_code)
            combined = combined.replace('{tests_json}', tests_json)
            
            # Dividir en dos archivos: Solution.java y __JudgeRunner.java
            # Retornamos solo __JudgeRunner.java que importa Solution
            return combined
        else:
            # Para Python y JavaScript, simplemente reemplazar marcadores
            combined = template.replace('{user_code}', user_code)
            combined = combined.replace('{tests_json}', tests_json)
            return combined
    
    def _get_template_filename(self, language: str) -> str:
        """Retorna el nombre del archivo de plantilla"""
        extensions = {
            'python': 'python.py',
            'java': 'java.java',
            'javascript': 'js.js'
        }
        return extensions.get(language, f'{language}.txt')
    
    def _analyze_results(
        self,
        execution_result: Dict[str, Any],
        total_tests: int
    ) -> Dict[str, Any]:
        """
        Analiza los resultados de la ejecución y determina el veredicto final
        """
        # Si hubo un error del sistema antes de ejecutar tests
        if not execution_result.get('success') and execution_result.get('veredicto') != 'OK':
            return {
                'veredicto': execution_result.get('veredicto', 'SE'),
                'error': execution_result.get('error', 'Error desconocido'),
                'puntos': 0,
                'casos_pasados': 0,
                'casos_totales': total_tests,
                'tiempo_ejecucion': execution_result.get('tiempo_ejecucion', 0),
                'stdout': execution_result.get('stdout', ''),
                'stderr': execution_result.get('stderr', ''),
                'detalles': {}
            }
        
        # Parsear salida JSON de los tests
        stdout = execution_result.get('stdout', '').strip()
        stderr = execution_result.get('stderr', '').strip()
        
        try:
            # La última línea del stdout debe ser el JSON con resultados
            lines = stdout.strip().split('\n')
            json_output = lines[-1] if lines else '{}'
            
            results = json.loads(json_output)
            
            casos_pasados = results.get('passed', 0)
            casos_totales = results.get('total', total_tests)
            tests_results = results.get('tests', [])
            total_time = results.get('total_time', 0)
            
            # Determinar veredicto final
            if casos_pasados == casos_totales:
                veredicto = 'AC'  # Accepted
            else:
                # Verificar si algún test tuvo error específico
                has_runtime_error = any(
                    'error' in test for test in tests_results
                )
                if has_runtime_error:
                    veredicto = 'RE'  # Runtime Error
                else:
                    veredicto = 'WA'  # Wrong Answer
            
            # Calcular puntos (proporcional a tests pasados)
            puntos = int((casos_pasados / casos_totales) * 100) if casos_totales > 0 else 0
            
            return {
                'veredicto': veredicto,
                'puntos': puntos,
                'casos_pasados': casos_pasados,
                'casos_totales': casos_totales,
                'tiempo_ejecucion': total_time,
                'stdout': stdout,
                'stderr': stderr,
                'detalles': {
                    'tests': tests_results
                }
            }
            
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            # Si no se puede parsear el JSON, probablemente hubo un error
            return {
                'veredicto': 'RE',
                'error': f'No se pudo parsear resultados: {str(e)}',
                'puntos': 0,
                'casos_pasados': 0,
                'casos_totales': total_tests,
                'tiempo_ejecucion': execution_result.get('tiempo_ejecucion', 0),
                'stdout': stdout,
                'stderr': stderr,
                'detalles': {}
            }
    
    def validate_code_syntax(self, code: str, language: str) -> Dict[str, Any]:
        """
        Valida la sintaxis del código sin ejecutarlo
        Útil para dar feedback rápido antes de enviar
        """
        if language == 'python':
            try:
                compile(code, '<string>', 'exec')
                return {'valid': True, 'error': None}
            except SyntaxError as e:
                return {
                    'valid': False,
                    'error': f'Error de sintaxis en línea {e.lineno}: {e.msg}'
                }
        
        # Para Java y JavaScript, podríamos usar herramientas externas
        # Por ahora solo retornamos válido
        return {'valid': True, 'error': None}
