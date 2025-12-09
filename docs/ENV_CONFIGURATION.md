# Configuración de Variables de Entorno

Este documento explica las variables de entorno utilizadas en UNPA Coding Games.

## Archivo .env

El archivo `.env` debe estar ubicado en la raíz del proyecto y **nunca** debe ser incluido en el control de versiones (ya está en `.gitignore`).

## Variables Requeridas

### SECRET_KEY
- **Tipo**: String
- **Requerida**: Sí
- **Descripción**: Clave secreta de Django para firmar cookies y tokens
- **Ejemplo**: `SECRET_KEY=0@uo)@3n3p*=tfe)e40*y!=ojgihwdbu@a^p*9jpywr$m=3za0`
- **Generación**: 
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- **Seguridad**: 
  - Debe ser única para cada instalación
  - Cambiarla en producción
  - Mínimo 50 caracteres
  - No compartir públicamente

### DEBUG
- **Tipo**: Boolean
- **Requerida**: No (default: `True`)
- **Descripción**: Activa/desactiva el modo debug de Django
- **Valores**: `True` o `False`
- **Producción**: Debe ser `False` en producción
- **Desarrollo**: `True` para ver errores detallados

### ALLOWED_HOSTS
- **Tipo**: Lista separada por comas
- **Requerida**: Sí (en producción)
- **Descripción**: Dominios permitidos para servir la aplicación
- **Ejemplo**: `ALLOWED_HOSTS=localhost,127.0.0.1,midominio.com,www.midominio.com`
- **Desarrollo**: `localhost,127.0.0.1`
- **Producción**: Agregar todos los dominios donde se alojará la aplicación

## Variables de Base de Datos (Opcional)

Por defecto, el proyecto usa SQLite3. Para usar PostgreSQL, descomentar y configurar:

### DB_ENGINE
- **Valor**: `django.db.backends.postgresql`
- **Descripción**: Motor de base de datos

### DB_NAME
- **Ejemplo**: `DB_NAME=unpa_coding_games`
- **Descripción**: Nombre de la base de datos

### DB_USER
- **Ejemplo**: `DB_USER=postgres`
- **Descripción**: Usuario de PostgreSQL

### DB_PASSWORD
- **Ejemplo**: `DB_PASSWORD=mi_password_seguro`
- **Descripción**: Contraseña del usuario de PostgreSQL
- **Seguridad**: Usar contraseña fuerte en producción

### DB_HOST
- **Ejemplo**: `DB_HOST=localhost` o `DB_HOST=192.168.1.100`
- **Descripción**: Dirección del servidor de base de datos
- **Desarrollo**: `localhost`
- **Producción**: IP o dominio del servidor de BD

### DB_PORT
- **Ejemplo**: `DB_PORT=5432`
- **Descripción**: Puerto de PostgreSQL
- **Default**: `5432`

## Variables de Email (Opcional)

Para envío de correos electrónicos:

### EMAIL_BACKEND
- **Desarrollo**: `django.core.mail.backends.console.EmailBackend` (emails en consola)
- **Producción**: `django.core.mail.backends.smtp.EmailBackend` (envío real)

### EMAIL_HOST
- **Ejemplo Gmail**: `EMAIL_HOST=smtp.gmail.com`
- **Descripción**: Servidor SMTP

### EMAIL_PORT
- **Ejemplo TLS**: `EMAIL_PORT=587`
- **Ejemplo SSL**: `EMAIL_PORT=465`

### EMAIL_USE_TLS
- **Valores**: `True` o `False`
- **Descripción**: Usar TLS para conexión segura
- **Recomendado**: `True`

### EMAIL_HOST_USER
- **Ejemplo**: `EMAIL_HOST_USER=unpa.games@gmail.com`
- **Descripción**: Email desde el cual se envían correos

### EMAIL_HOST_PASSWORD
- **Descripción**: Contraseña o App Password
- **Gmail**: Requiere "App Password" si tienes 2FA activado
- **Seguridad**: No usar tu contraseña personal

## Variables de Archivos Estáticos

### STATIC_URL
- **Default**: `/static/`
- **Descripción**: URL base para archivos estáticos

### MEDIA_URL
- **Default**: `/media/`
- **Descripción**: URL base para archivos subidos por usuarios

## Variables de Seguridad (Producción)

Descomentar en `.env` para producción:

### SECURE_SSL_REDIRECT
- **Valor**: `True`
- **Descripción**: Redirigir todo el tráfico HTTP a HTTPS

### SESSION_COOKIE_SECURE
- **Valor**: `True`
- **Descripción**: Cookies de sesión solo por HTTPS

### CSRF_COOKIE_SECURE
- **Valor**: `True`
- **Descripción**: Cookies CSRF solo por HTTPS

### SECURE_HSTS_SECONDS
- **Valor**: `31536000` (1 año)
- **Descripción**: Tiempo de HSTS (HTTP Strict Transport Security)

### SECURE_HSTS_INCLUDE_SUBDOMAINS
- **Valor**: `True`
- **Descripción**: Aplicar HSTS a subdominios

### SECURE_HSTS_PRELOAD
- **Valor**: `True`
- **Descripción**: Permitir inclusión en listas de preload HSTS

## Ejemplo de .env para Desarrollo

```env
# Django Settings
SECRET_KEY=0@uo)@3n3p*=tfe)e40*y!=ojgihwdbu@a^p*9jpywr$m=3za0
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (Consola para desarrollo)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

## Ejemplo de .env para Producción

```env
# Django Settings
SECRET_KEY=tu_secret_key_super_segura_y_unica
DEBUG=False
ALLOWED_HOSTS=unpa-games.com,www.unpa-games.com

# Database PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=unpa_coding_games
DB_USER=unpa_user
DB_PASSWORD=password_super_seguro_123
DB_HOST=db.unpa-games.com
DB_PORT=5432

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@unpa-games.com
EMAIL_HOST_PASSWORD=app_password_generado

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

## Checklist de Seguridad

- [ ] `.env` en `.gitignore` (no subir a Git)
- [ ] `SECRET_KEY` única y compleja
- [ ] `DEBUG=False` en producción
- [ ] `ALLOWED_HOSTS` configurado correctamente
- [ ] Variables de seguridad SSL habilitadas en producción
- [ ] Contraseñas de BD fuertes
- [ ] Email con App Passwords (no contraseña personal)
- [ ] Archivo `.env.example` actualizado (sin valores sensibles)

## Solución de Problemas

### Error: "SECRET_KEY not found"
- Verificar que existe el archivo `.env` en la raíz
- Verificar que la variable `SECRET_KEY` está definida

### Error: "ALLOWED_HOSTS"
- En desarrollo: `ALLOWED_HOSTS=localhost,127.0.0.1`
- En producción: Agregar tu dominio

### Error de conexión a base de datos
- Verificar credenciales en `.env`
- Verificar que PostgreSQL está corriendo
- Verificar que la base de datos existe

### Emails no se envían
- En desarrollo: Verificar consola con `EMAIL_BACKEND=console`
- En producción: Verificar credenciales SMTP y firewall

## Referencias

- [Django Settings](https://docs.djangoproject.com/en/5.0/ref/settings/)
- [Django Security](https://docs.djangoproject.com/en/5.0/topics/security/)
- [python-decouple](https://github.com/HBNetwork/python-decouple)
