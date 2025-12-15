"""
Módulo para ejecutar código en contenedores Docker aislados
Garantiza seguridad mediante aislamiento, límites de recursos y sin acceso a red
"""
import docker
import tempfile
import os
import time
from pathlib import Path
from typing import Dict, Any, Optional


class DockerExecutor:
    """
    Ejecutor de código en Docker con restricciones de seguridad
    """
    
    # Imágenes Docker por lenguaje
    IMAGES = {
        'python': 'python:3.11-slim',
        'java': 'openjdk:17-slim',
        'javascript': 'node:18-slim'
    }
    
    # Comandos de ejecución por lenguaje
    COMMANDS = {
        'python': ['python', '/code/solution.py'],
        'java': [
            'sh', '-c',
            'cd /code && javac Solution.java __JudgeRunner.java && java __JudgeRunner'
        ],
        'javascript': ['node', '/code/solution.js']
    }
    
    # Extensiones de archivo
    EXTENSIONS = {
        'python': '.py',
        'java': '.java',
        'javascript': '.js'
    }
    
    def __init__(self):
        """Inicializa el cliente de Docker"""
        try:
            self.client = docker.from_env()
            # Verificar que Docker está disponible
            self.client.ping()
        except Exception as e:
            raise RuntimeError(f"No se pudo conectar a Docker: {e}")
    
    def execute(
        self,
        code: str,
        language: str,
        time_limit: float = 5.0,
        memory_limit: int = 256
    ) -> Dict[str, Any]:
        """
        Ejecuta código en un contenedor Docker aislado
        
        Args:
            code: Código fuente a ejecutar (ya combinado con tests)
            language: Lenguaje de programación ('python', 'java', 'javascript')
            time_limit: Límite de tiempo en segundos
            memory_limit: Límite de memoria en MB
        
        Returns:
            Dict con stdout, stderr, exit_code, tiempo_ejecucion, error
        """
        if language not in self.IMAGES:
            return {
                'success': False,
                'error': f'Lenguaje no soportado: {language}',
                'veredicto': 'SE'
            }
        
        # Crear directorio temporal para el código
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                # Escribir código en archivo
                filename = self._get_filename(language)
                code_path = os.path.join(tmpdir, filename)
                
                with open(code_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                
                # Configurar límites de recursos
                cpu_period = 100000  # 100ms
                cpu_quota = int(cpu_period * 1)  # 1 CPU core
                mem_limit = f"{memory_limit}m"
                
                # Ejecutar en Docker
                result = self._run_container(
                    tmpdir=tmpdir,
                    language=language,
                    time_limit=time_limit,
                    cpu_quota=cpu_quota,
                    cpu_period=cpu_period,
                    mem_limit=mem_limit
                )
                
                return result
                
            except Exception as e:
                return {
                    'success': False,
                    'stdout': '',
                    'stderr': str(e),
                    'exit_code': -1,
                    'tiempo_ejecucion': 0,
                    'error': str(e),
                    'veredicto': 'SE'
                }
    
    def _get_filename(self, language: str) -> str:
        """Retorna el nombre de archivo según el lenguaje"""
        if language == 'java':
            # Java requiere que el archivo se llame como la clase pública
            return 'Solution.java'
        elif language == 'python':
            return 'solution.py'
        elif language == 'javascript':
            return 'solution.js'
        return f'solution{self.EXTENSIONS[language]}'
    
    def _run_container(
        self,
        tmpdir: str,
        language: str,
        time_limit: float,
        cpu_quota: int,
        cpu_period: int,
        mem_limit: str
    ) -> Dict[str, Any]:
        """
        Ejecuta el contenedor Docker con las restricciones especificadas
        """
        image = self.IMAGES[language]
        command = self.COMMANDS[language]
        
        # Preparar configuración del contenedor
        container_config = {
            'image': image,
            'command': command,
            'volumes': {
                tmpdir: {'bind': '/code', 'mode': 'ro'}  # Solo lectura
            },
            'working_dir': '/code',
            'network_disabled': True,  # Sin acceso a red
            'mem_limit': mem_limit,
            'memswap_limit': mem_limit,  # Sin swap
            'cpu_quota': cpu_quota,
            'cpu_period': cpu_period,
            'pids_limit': 50,  # Límite de procesos
            'detach': True,
            'stdout': True,
            'stderr': True,
            'remove': False  # No remover automáticamente para inspeccionar
        }
        
        container = None
        try:
            # Crear y ejecutar contenedor
            container = self.client.containers.run(**container_config)
            
            # Esperar con timeout
            start_time = time.time()
            try:
                exit_code = container.wait(timeout=time_limit + 1)['StatusCode']
                execution_time = time.time() - start_time
                
                # Obtener salidas
                stdout = container.logs(stdout=True, stderr=False).decode('utf-8', errors='replace')
                stderr = container.logs(stdout=False, stderr=True).decode('utf-8', errors='replace')
                
                # Determinar veredicto
                veredicto = self._determine_verdict(
                    exit_code=exit_code,
                    execution_time=execution_time,
                    time_limit=time_limit,
                    stderr=stderr
                )
                
                return {
                    'success': exit_code == 0,
                    'stdout': stdout,
                    'stderr': stderr,
                    'exit_code': exit_code,
                    'tiempo_ejecucion': execution_time,
                    'veredicto': veredicto
                }
                
            except docker.errors.ContainerError as e:
                # Error durante la ejecución
                return {
                    'success': False,
                    'stdout': '',
                    'stderr': str(e),
                    'exit_code': e.exit_status,
                    'tiempo_ejecucion': time.time() - start_time,
                    'error': str(e),
                    'veredicto': 'RE'
                }
                
            except Exception as e:
                # Timeout u otro error
                execution_time = time.time() - start_time
                if execution_time >= time_limit:
                    veredicto = 'TLE'
                else:
                    veredicto = 'SE'
                
                return {
                    'success': False,
                    'stdout': '',
                    'stderr': str(e),
                    'exit_code': -1,
                    'tiempo_ejecucion': execution_time,
                    'error': str(e),
                    'veredicto': veredicto
                }
        
        finally:
            # Limpiar contenedor
            if container:
                try:
                    container.kill()
                except:
                    pass
                try:
                    container.remove(force=True)
                except:
                    pass
    
    def _determine_verdict(
        self,
        exit_code: int,
        execution_time: float,
        time_limit: float,
        stderr: str
    ) -> str:
        """
        Determina el veredicto basado en el resultado de la ejecución
        """
        if execution_time >= time_limit:
            return 'TLE'  # Time Limit Exceeded
        
        if exit_code != 0:
            if 'OutOfMemoryError' in stderr or 'MemoryError' in stderr:
                return 'MLE'  # Memory Limit Exceeded
            elif 'Compilation error' in stderr or 'SyntaxError' in stderr:
                return 'CE'  # Compilation Error
            else:
                return 'RE'  # Runtime Error
        
        # El veredicto AC/WA se determina después comparando outputs
        return 'OK'  # OK indica que se ejecutó correctamente
    
    def pull_images(self):
        """
        Descarga todas las imágenes Docker necesarias
        Útil para ejecutar en setup inicial
        """
        for language, image in self.IMAGES.items():
            try:
                print(f"Descargando imagen {image} para {language}...")
                self.client.images.pull(image)
                print(f"✓ Imagen {image} descargada")
            except Exception as e:
                print(f"✗ Error descargando {image}: {e}")
    
    def cleanup_old_containers(self):
        """
        Limpia contenedores antiguos que puedan haber quedado
        """
        try:
            filters = {'status': 'exited'}
            containers = self.client.containers.list(all=True, filters=filters)
            
            for container in containers:
                if any(image in str(container.image) for image in self.IMAGES.values()):
                    container.remove(force=True)
        except Exception as e:
            print(f"Error limpiando contenedores: {e}")
