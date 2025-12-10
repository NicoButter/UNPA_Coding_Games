# UNPA Coding Games 🎮

Sistema de competencia de programación inspirado en Los Juegos del Hambre para la Universidad Nacional de la Patagonia Austral (UNPA).

## Descripción

Plataforma web que permite a estudiantes (tributos) participar en torneos y retos de programación, organizados por distritos con mentores asignados y supervisados por vigilantes, todo bajo la administración del Jefe del Capitolio.

## Características

- 🏆 **Gestión de Torneos**: Creación y administración de competencias
- 💻 **Retos de Programación**: Desafíos con validación automática
- 👥 **Sistema de Roles**: Tributo, Mentor, Vigilante, Jefe del Capitolio
- 🏅 **Rankings por Distrito**: Sistema de puntuación y leaderboards
- 📊 **Dashboards Personalizados**: Interfaces específicas para cada rol
- 🎫 **Credenciales QR**: Acreditación de tributos mediante códigos QR

## Tecnologías

- **Backend**: Django 5.0.14
- **Base de Datos**: SQLite3 (desarrollo) / PostgreSQL (producción)
- **Frontend**: HTML5, CSS3, JavaScript
- **Autenticación**: Django Custom User Model
- **QR Codes**: python-qrcode + Pillow

## Instalación

### Prerrequisitos

- Python 3.14+
- pip
- virtualenv

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/NicoButter/UNPA_Coding_Games.git
cd UNPA_Coding_Games
```

2. **Crear y activar entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus valores
```

5. **Ejecutar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

Acceder a http://127.0.0.1:8000/

## Estructura del Proyecto

```
UNPA_Coding_Games/
├── capitol/           # Autenticación y gestión de usuarios
├── centro_control/    # Monitoreo y acreditación
├── dashboards/        # Dashboards por rol
├── arena/            # Gestión de torneos y retos
├── templates/        # Templates globales
├── static/          # Archivos estáticos globales
├── media/           # Archivos subidos por usuarios
└── unpa_code_games/ # Configuración del proyecto
```

## Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Django Settings
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL - opcional)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=unpa_coding_games
# DB_USER=postgres
# DB_PASSWORD=tu_password
# DB_HOST=localhost
# DB_PORT=5432

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@example.com
EMAIL_HOST_PASSWORD=tu_password_email
```

## Roles del Sistema

### 👤 Tributo (Estudiante)
- Registrarse en torneos
- Resolver retos de programación
- Ver ranking personal y de distrito
- Obtener credencial QR

### 🎓 Mentor
- Gestionar tributos de su distrito
- Ver progreso de sus estudiantes
- Asignar y revisar retos
- Proporcionar retroalimentación

### 👁️ Vigilante (Staff)
- Acreditar tributos mediante QR
- Monitorear participación
- Supervisar torneos
- Reportes de actividad

### 👑 Jefe del Capitolio (Admin)
- Crear y gestionar torneos
- Asignar mentores a distritos
- Crear retos y casos de prueba
- Administración completa del sistema

## Uso

### Crear un Torneo

1. Ingresar como Jefe del Capitolio
2. Ir a `/admin/arena/torneo/`
3. Completar formulario de torneo
4. Asignar mentores a distritos
5. Activar inscripciones

### Crear un Reto

1. Acceder al panel de administración
2. Crear nuevo Reto en `/admin/arena/reto/`
3. Agregar casos de prueba
4. Configurar validación automática
5. Publicar reto

### Participar en un Reto (Tributo)

1. Ver torneos activos en el dashboard
2. Seleccionar reto disponible
3. Escribir solución en el editor
4. Enviar código
5. Ver resultados de validación

## Desarrollo

### Crear migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Ejecutar tests
```bash
python manage.py test
```

### Colectar archivos estáticos
```bash
python manage.py collectstatic
```

## Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Abrir Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## Contacto

**Nicolas Butterfield**  
📧 nicobutter@gmail.com

**Universidad Nacional de la Patagonia Austral (UNPA)**

Desarrollado para fomentar la práctica de programación entre estudiantes de la UNPA.

---

*Que los juegos comiencen* 🔥
