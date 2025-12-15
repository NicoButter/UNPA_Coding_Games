"""
Management command para crear usuarios de prueba para cada rol
Ejecutar: python manage.py crear_usuarios_prueba
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from capitol.models import TributoInfo
from django.utils import timezone
from datetime import timedelta

Personaje = get_user_model()


class Command(BaseCommand):
    help = 'Crea usuarios de prueba para cada rol del sistema'

    def handle(self, *args, **kwargs):
        usuarios = [
            {
                'username': 'tributo',
                'password': 'tributo010203',
                'email': 'tributo@test.com',
                'first_name': 'Katniss',
                'last_name': 'Everdeen',
                'rol': 'tributo',
                'distrito': 12
            },
            {
                'username': 'mentor',
                'password': 'mentor010203',
                'email': 'mentor@test.com',
                'first_name': 'Haymitch',
                'last_name': 'Abernathy',
                'rol': 'mentor',
                'unidad_academica': 'UNPA Sede Caleta Olivia',
                'distrito_asignado': 12
            },
            {
                'username': 'vigilante',
                'password': 'vigilante010203',
                'email': 'vigilante@test.com',
                'first_name': 'Cato',
                'last_name': 'Peacekeeper',
                'rol': 'vigilante'
            },
            {
                'username': 'jefe_capitolio',
                'password': 'jefe_capitolio010203',
                'email': 'jefe@test.com',
                'first_name': 'President',
                'last_name': 'Snow',
                'rol': 'jefe_capitolio'
            }
        ]

        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('Creando usuarios de prueba...'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('')

        for user_data in usuarios:
            username = user_data['username']
            password = user_data['password']
            rol = user_data['rol']
            distrito = user_data.pop('distrito', None)
            
            # Verificar si el usuario ya existe
            if Personaje.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'✓ Usuario "{username}" ya existe, omitiendo...')
                )
                continue
            
            # Crear usuario
            user = Personaje.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=password,
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                rol=rol,
                is_staff=(rol == 'jefe_capitolio'),
                is_superuser=(rol == 'jefe_capitolio')
            )
            
            # Configurar campos adicionales según el rol
            if rol == 'mentor':
                user.unidad_academica = user_data.get('unidad_academica', '')
                user.distrito_asignado = user_data.get('distrito_asignado')
                user.save()
            
            # Si es tributo, crear TributoInfo
            if rol == 'tributo' and distrito:
                TributoInfo.objects.create(
                    personaje=user,
                    distrito=distrito,
                    tipo='alumno_unpa',
                    nivel='novato',
                    fecha_registro=timezone.now()
                )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Usuario creado: {username:<20} | Rol: {rol:<20} | Password: {password}'
                )
            )
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('Usuarios de prueba creados exitosamente'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('')
        self.stdout.write('Credenciales de acceso:')
        self.stdout.write('')
        
        for user_data in usuarios:
            self.stdout.write(
                f'  • {user_data["rol"]:<20} → username: {user_data["username"]:<20} password: {user_data["password"]}'
            )
        
        self.stdout.write('')
        self.stdout.write('Acceso al sistema:')
        self.stdout.write('  • Login: http://localhost:8000/login/')
        self.stdout.write('  • Admin: http://localhost:8000/admin/ (jefe_capitolio)')
        self.stdout.write('')
