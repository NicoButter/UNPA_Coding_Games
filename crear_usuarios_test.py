#!/usr/bin/env python
"""
Script para crear usuarios de prueba
Ejecutar: python crear_usuarios_test.py
O desde Django shell: exec(open('crear_usuarios_test.py').read())
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unpa_code_games.settings')
django.setup()

from django.contrib.auth import get_user_model
from capitol.models import TributoInfo
from django.utils import timezone

Personaje = get_user_model()

# Definir usuarios
usuarios = [
    {
        'username': 'tributo',
        'password': 'tributo010203',
        'email': 'tributo@test.com',
        'first_name': 'Katniss',
        'last_name': 'Everdeen',
        'rol': 'tributo',
        'distrito': 12,
        'descripcion': 'Tributo del Distrito 12 - Alumno de prueba'
    },
    {
        'username': 'mentor',
        'password': 'mentor010203',
        'email': 'mentor@test.com',
        'first_name': 'Haymitch',
        'last_name': 'Abernathy',
        'rol': 'mentor',
        'unidad_academica': 'UNPA Sede Caleta Olivia',
        'distrito_asignado': 12,
        'descripcion': 'Mentor del Distrito 12 - Profesor de prueba'
    },
    {
        'username': 'vigilante',
        'password': 'vigilante010203',
        'email': 'vigilante@test.com',
        'first_name': 'Cato',
        'last_name': 'Peacekeeper',
        'rol': 'vigilante',
        'descripcion': 'Vigilante (Peacekeeper) - Supervisor de prueba'
    },
    {
        'username': 'jefe_capitolio',
        'password': 'jefe_capitolio010203',
        'email': 'jefe@test.com',
        'first_name': 'President',
        'last_name': 'Snow',
        'rol': 'jefe_capitolio',
        'descripcion': 'Jefe del Capitolio - Administrador principal'
    }
]

print('='*70)
print('CREANDO USUARIOS DE PRUEBA PARA UNPA CODING GAMES')
print('='*70)
print()

usuarios_creados = 0
usuarios_existentes = 0

for user_data in usuarios:
    username = user_data['username']
    password = user_data['password']
    rol = user_data['rol']
    distrito = user_data.pop('distrito', None)
    descripcion = user_data.pop('descripcion', '')
    
    # Verificar si existe
    if Personaje.objects.filter(username=username).exists():
        print(f'⚠️  Usuario "{username}" ya existe, omitiendo...')
        usuarios_existentes += 1
        continue
    
    try:
        # Crear usuario
        user = Personaje.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=password,
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            rol=rol,
            is_staff=(rol in ['jefe_capitolio', 'vigilante']),
            is_superuser=(rol == 'jefe_capitolio')
        )
        
        # Configurar campos adicionales
        if rol == 'mentor':
            user.unidad_academica = user_data.get('unidad_academica', '')
            user.distrito_asignado = user_data.get('distrito_asignado')
            user.save()
        
        # Crear TributoInfo si es tributo
        if rol == 'tributo' and distrito:
            TributoInfo.objects.create(
                personaje=user,
                distrito=distrito,
                tipo='alumno_unpa',
                nivel='novato',
                fecha_registro=timezone.now()
            )
        
        print(f'✓ Creado: {username:<20} | {rol:<20} | {descripcion}')
        usuarios_creados += 1
        
    except Exception as e:
        print(f'✗ Error al crear {username}: {e}')

print()
print('='*70)
print(f'RESUMEN: {usuarios_creados} usuarios creados, {usuarios_existentes} ya existían')
print('='*70)
print()
print('CREDENCIALES DE ACCESO:')
print('-'*70)

for user_data in usuarios:
    print(f'  {user_data["rol"].upper():<20}')
    print(f'    Username: {user_data["username"]}')
    print(f'    Password: {user_data["password"]}')
    print()

print('-'*70)
print('URLs DEL SISTEMA:')
print('  • Login:  http://localhost:8000/login/')
print('  • Admin:  http://localhost:8000/admin/ (usar: jefe_capitolio)')
print('='*70)
