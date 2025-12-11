# Especificación de Requerimientos de Software (ERS)
## UNPA Coding Games - Plataforma de Competencias de Programación

---

### **Información del Documento**

| Campo | Detalle |
|-------|---------|
| **Proyecto** | UNPA Coding Games |
| **Versión** | 1.0 |
| **Fecha** | 10 de Diciembre de 2025 |
| **Autores** | Equipo de Desarrollo UNPA |
| **Estado** | En Desarrollo |

---

## **1. INTRODUCCIÓN**

### 1.1 Propósito

Este documento especifica los requerimientos funcionales y no funcionales para el sistema **UNPA Coding Games**, una plataforma web de competencias de programación inspirada en la temática de "Los Juegos del Hambre". El sistema está diseñado para facilitar torneos de programación entre estudiantes universitarios y participantes externos.

### 1.2 Alcance

El sistema **UNPA Coding Games** permite:

- Gestión jerárquica de roles (Jefe del Capitolio, Mentores, Vigilantes, Tributos)
- Creación y gestión de torneos de programación
- Sistema de acreditación mediante códigos QR
- Resolución y validación automática de retos de programación
- Sistema de patrocinio (ayudas de mentores a tributos)
- Monitoreo en tiempo real de competencias
- Notificaciones y comunicación entre roles

### 1.3 Definiciones, Acrónimos y Abreviaturas

| Término | Definición |
|---------|------------|
| **Tributo** | Estudiante o participante que compite en los torneos |
| **Mentor** | Docente que representa una unidad académica y guía a sus tributos |
| **Vigilante** | Personal que acredita tributos y supervisa las competencias |
| **Jefe del Capitolio** | Administrador principal del sistema |
| **Arena** | Espacio virtual donde se desarrollan las competencias |
| **Reto** | Desafío de programación dentro de un torneo |
| **Patrocinio** | Sistema de ayudas que los mentores envían a sus tributos |
| **QR** | Código QR único para cada tributo usado en acreditación |
| **UNPA** | Universidad Nacional de la Patagonia Austral |

### 1.4 Referencias

- Django 5.0.14 - Framework web
- Python 3.14 - Lenguaje de programación
- SQLite3 - Sistema de base de datos
- ReportLab 4.4.5 - Generación de PDFs
- QRCode + Pillow - Generación de códigos QR

---

## **2. DESCRIPCIÓN GENERAL**

### 2.1 Perspectiva del Producto

UNPA Coding Games es una aplicación web independiente desarrollada con Django que simula un sistema de competencias de programación con una estructura jerárquica inspirada en "Los Juegos del Hambre". Integra sistemas de autenticación, gestión de usuarios, validación automática de código, y comunicación en tiempo real.

### 2.2 Funciones del Producto

**Principales funcionalidades:**

1. **Gestión de Usuarios y Roles**
   - Sistema de autenticación personalizado
   - 4 roles con permisos específicos
   - Gestión de perfiles por rol

2. **Sistema de Acreditación**
   - Generación automática de credenciales con QR
   - Acreditación mediante escaneo QR (webcam)
   - Envío automático de credenciales por email

3. **Gestión de Torneos**
   - Creación y configuración de torneos
   - Asignación de retos a torneos
   - Sistema de puntuación configurable

4. **Arena de Competencia**
   - Resolución de retos de programación
   - Validación automática con casos de prueba
   - Ejecución segura de código

5. **Sistema de Patrocinio**
   - Presupuesto de puntos para mentores
   - Envío de ayudas con costos diferenciados
   - Límites diarios de ayudas

6. **Monitoreo en Tiempo Real**
   - Panel de vigilancia en vivo
   - Estadísticas actualizadas automáticamente
   - Notificaciones push

### 2.3 Características de Usuario

| Rol | Perfil | Conocimientos Requeridos |
|-----|--------|-------------------------|
| **Jefe del Capitolio** | Docente/Coordinador principal | Gestión académica, conocimientos de programación |
| **Mentor** | Docente de unidad académica | Conocimientos de programación, pedagogía |
| **Vigilante** | Auxiliar/Ayudante | Conocimientos básicos de informática |
| **Tributo** | Estudiante/Participante | Programación en al menos un lenguaje |

### 2.4 Restricciones

- Sistema multi-usuario con acceso concurrente
- Compatible con navegadores modernos (Chrome, Firefox, Edge)
- Requiere cámara web para acreditación por QR
- Ejecución de código limitada a entornos seguros
- Conexión a internet requerida

### 2.5 Suposiciones y Dependencias

- Los usuarios tienen acceso a computadoras con navegador web
- Disponibilidad de servidor SMTP para envío de emails
- Los tributos tienen direcciones de email válidas
- Ambiente de ejecución Python disponible para validar código

---

## **3. REQUERIMIENTOS ESPECÍFICOS**

### 3.1 Requerimientos Funcionales

#### **RF-01: Gestión de Usuarios**

| ID | RF-01 |
|----|-------|
| **Nombre** | Sistema de Autenticación y Roles |
| **Prioridad** | Alta |
| **Descripción** | El sistema debe permitir la gestión completa de usuarios con 4 roles diferenciados |

**Casos de uso:**
- **RF-01.1** Registro de usuarios por rol
- **RF-01.2** Login/Logout con credenciales
- **RF-01.3** Gestión de perfiles según rol
- **RF-01.4** Asignación de mentores a unidades académicas
- **RF-01.5** Asignación de vigilantes a torneos
- **RF-01.6** Asignación de tributos a mentores

#### **RF-02: Sistema de Acreditación**

| ID | RF-02 |
|----|-------|
| **Nombre** | Acreditación de Tributos con QR |
| **Prioridad** | Alta |
| **Descripción** | Sistema completo de generación, envío y validación de credenciales |

**Casos de uso:**
- **RF-02.1** Generación automática de código QR único por tributo
- **RF-02.2** Generación de credencial PDF con QR
- **RF-02.3** Envío automático de credencial por email al registrarse
- **RF-02.4** Acreditación mediante escaneo QR por vigilante
- **RF-02.5** Login automático mediante webcam y QR
- **RF-02.6** Re-envío de credencial si se solicita

#### **RF-03: Gestión de Torneos**

| ID | RF-03 |
|----|-------|
| **Nombre** | Administración de Torneos |
| **Prioridad** | Alta |
| **Descripción** | Creación, configuración y gestión de torneos de programación |

**Casos de uso:**
- **RF-03.1** Crear torneo con fechas y configuración
- **RF-03.2** Asignar vigilantes a torneos
- **RF-03.3** Configurar puntos mínimos para ganar
- **RF-03.4** Gestionar estados del torneo (configuración, inscripción, en curso, finalizado)
- **RF-03.5** Listar torneos disponibles para tributos acreditados

#### **RF-04: Arena de Competencia**

| ID | RF-04 |
|----|-------|
| **Nombre** | Sistema de Retos y Validación |
| **Prioridad** | Alta |
| **Descripción** | Plataforma para resolver retos de programación con validación automática |

**Casos de uso:**
- **RF-04.1** Crear retos con diferentes dificultades
- **RF-04.2** Definir casos de prueba (visibles y ocultos)
- **RF-04.3** Enviar solución en lenguajes soportados (Python, JavaScript, etc.)
- **RF-04.4** Validar automáticamente contra casos de prueba
- **RF-04.5** Calcular puntuación según casos pasados y bonificaciones
- **RF-04.6** Permitir múltiples intentos
- **RF-04.7** Mostrar resultados de validación

#### **RF-05: Sistema de Patrocinio**

| ID | RF-05 |
|----|-------|
| **Nombre** | Ayudas de Mentores a Tributos |
| **Prioridad** | Media |
| **Descripción** | Sistema de puntos para que mentores envíen ayudas a sus tributos |

**Casos de uso:**
- **RF-05.1** Asignar presupuesto inicial de 1000 puntos a mentores
- **RF-05.2** Enviar ayudas de 5 tipos (pista, ejemplo, recurso, motivación, advertencia)
- **RF-05.3** Descontar puntos según tipo de ayuda
- **RF-05.4** Limitar ayudas por día (10 máximo)
- **RF-05.5** Notificar a tributo cuando recibe ayuda
- **RF-05.6** Marcar ayudas como leídas
- **RF-05.7** Recargar puntos (solo Jefe del Capitolio)

#### **RF-06: Dashboards por Rol**

| ID | RF-06 |
|----|-------|
| **Nombre** | Interfaces Personalizadas por Rol |
| **Prioridad** | Alta |
| **Descripción** | Cada rol tiene un dashboard específico con funcionalidades propias |

**Casos de uso:**
- **RF-06.1** Dashboard Jefe del Capitolio: asignaciones, estadísticas generales
- **RF-06.2** Dashboard Mentor: tributos asignados, presupuesto, enviar ayudas
- **RF-06.3** Dashboard Vigilante: acreditación, monitoreo en vivo
- **RF-06.4** Dashboard Tributo: torneos, ayudas recibidas, credencial

#### **RF-07: Monitoreo en Tiempo Real**

| ID | RF-07 |
|----|-------|
| **Nombre** | Panel de Monitoreo para Vigilantes |
| **Prioridad** | Media |
| **Descripción** | Panel en vivo que muestra tributos compitiendo |

**Casos de uso:**
- **RF-07.1** Visualizar tributos activos en tiempo real
- **RF-07.2** Ver progreso de retos por tributo
- **RF-07.3** Filtrar por estado (activo, acreditado, pendiente)
- **RF-07.4** Auto-actualización cada 5 segundos
- **RF-07.5** Estadísticas globales (activos, acreditados, completados)

#### **RF-08: Sistema de Notificaciones**

| ID | RF-08 |
|----|-------|
| **Nombre** | Notificaciones en Tiempo Real |
| **Prioridad** | Media |
| **Descripción** | Sistema de notificaciones para tributos |

**Casos de uso:**
- **RF-08.1** Notificar cuando llega ayuda del mentor
- **RF-08.2** Mostrar badge con contador de ayudas sin leer
- **RF-08.3** Toast notification al recibir ayuda
- **RF-08.4** Actualizar título de página con contador
- **RF-08.5** Polling cada 30 segundos

#### **RF-09: Middleware de Acceso**

| ID | RF-09 |
|----|-------|
| **Nombre** | Control de Acceso a Arena |
| **Prioridad** | Alta |
| **Descripción** | Solo tributos acreditados pueden acceder a la arena |

**Casos de uso:**
- **RF-09.1** Interceptar accesos a `/arena/torneo/` y `/arena/reto/`
- **RF-09.2** Verificar estado del tributo (acreditado, activo, ganador)
- **RF-09.3** Redirigir con mensaje si no está acreditado

#### **RF-10: Reportes y Estadísticas**

| ID | RF-10 |
|----|-------|
| **Nombre** | Generación de Reportes |
| **Prioridad** | Baja |
| **Descripción** | Sistema de reportes para análisis |

**Casos de uso:**
- **RF-10.1** Ranking de tributos por puntos
- **RF-10.2** Ranking de distritos
- **RF-10.3** Estadísticas por torneo
- **RF-10.4** Historial de participaciones

---

### 3.2 Requerimientos No Funcionales

#### **RNF-01: Rendimiento**

- El sistema debe soportar al menos 100 usuarios concurrentes
- Tiempo de respuesta < 2 segundos para operaciones normales
- Validación de código < 10 segundos por intento
- Actualización del panel de monitoreo < 5 segundos

#### **RNF-02: Seguridad**

- Contraseñas hasheadas con algoritmo bcrypt
- Autenticación requerida para todas las operaciones
- Validación de permisos por rol
- Ejecución de código en entorno aislado (subprocess)
- Tokens QR únicos e irrepetibles (UUID)
- Middleware de seguridad de Django activado

#### **RNF-03: Usabilidad**

- Interfaz responsive (desktop, tablet, mobile)
- Diseño intuitivo con temática "Hunger Games"
- Notificaciones claras y no intrusivas
- Feedback visual inmediato en operaciones
- Accesibilidad básica (contraste, tamaño de texto)

#### **RNF-04: Confiabilidad**

- Disponibilidad del sistema > 95%
- Backup automático de base de datos
- Manejo de errores con mensajes claros
- Logs de operaciones críticas
- Recuperación ante fallos

#### **RNF-05: Mantenibilidad**

- Código documentado siguiendo PEP 8
- Arquitectura MVC de Django
- Separación de responsabilidades
- Tests unitarios para funciones críticas
- Migraciones versionadas de BD

#### **RNF-06: Portabilidad**

- Compatible con Linux, Windows, macOS
- Base de datos SQLite (desarrollo), PostgreSQL/MySQL (producción)
- Python 3.10+
- Navegadores: Chrome 90+, Firefox 88+, Edge 90+

#### **RNF-07: Escalabilidad**

- Diseño modular por aplicaciones Django
- Base de datos normalizada
- Posibilidad de migrar a microservicios
- Cache de consultas frecuentes
- Optimización de queries con select_related/prefetch_related

---

## **4. CASOS DE USO PRINCIPALES**

### CU-01: Registrar Tributo

**Actor Principal:** Tributo  
**Precondiciones:** Ninguna  
**Flujo Principal:**
1. Usuario accede a página de registro
2. Completa formulario con datos personales
3. Selecciona tipo (Alumno UNPA / Externo)
4. Sistema genera código único de tributo
5. Sistema genera QR único
6. Sistema crea credencial PDF
7. Sistema envía email con credencial adjunta
8. Usuario recibe confirmación

**Postcondiciones:** Tributo registrado con estado "pendiente"

---

### CU-02: Acreditar Tributo

**Actor Principal:** Vigilante  
**Precondiciones:** Tributo registrado, Vigilante autenticado  
**Flujo Principal:**
1. Vigilante accede a panel de acreditación QR
2. Sistema activa webcam
3. Tributo muestra su QR (impreso o en pantalla)
4. Vigilante escanea QR con webcam
5. Sistema valida token QR
6. Sistema cambia estado a "acreditado"
7. Sistema registra fecha de acreditación
8. Sistema muestra datos del tributo

**Postcondiciones:** Tributo puede acceder a la arena

---

### CU-03: Resolver Reto

**Actor Principal:** Tributo  
**Precondiciones:** Tributo acreditado, Torneo activo  
**Flujo Principal:**
1. Tributo accede a arena del torneo
2. Selecciona reto disponible
3. Lee descripción y casos de ejemplo
4. Escribe código en editor
5. Selecciona lenguaje de programación
6. Envía solución
7. Sistema ejecuta código contra casos de prueba
8. Sistema calcula puntos según casos pasados
9. Sistema muestra resultados
10. Sistema actualiza ranking

**Postcondiciones:** Participación registrada con puntos

---

### CU-04: Enviar Ayuda

**Actor Principal:** Mentor  
**Precondiciones:** Mentor tiene tributos asignados, Presupuesto suficiente  
**Flujo Principal:**
1. Mentor accede a "Enviar Ayuda"
2. Selecciona tributo destinatario
3. Elige tipo de ayuda (determina costo)
4. Escribe título y contenido
5. Opcionalmente relaciona con reto específico
6. Sistema verifica puntos disponibles
7. Sistema verifica límite diario
8. Sistema descuenta puntos
9. Sistema envía ayuda
10. Sistema notifica a tributo

**Postcondiciones:** Ayuda enviada, puntos descontados

---

### CU-05: Monitorear Competencia

**Actor Principal:** Vigilante  
**Precondiciones:** Vigilante autenticado, Torneo en curso  
**Flujo Principal:**
1. Vigilante accede a Panel de Monitoreo
2. Sistema muestra tributos en tiempo real
3. Sistema actualiza cada 5 segundos
4. Vigilante filtra por estado si desea
5. Vigilante observa progreso de retos
6. Sistema muestra última actividad

**Postcondiciones:** Vigilante informado del estado actual

---

## **5. MODELOS DE DATOS**

### 5.1 Diagrama Entidad-Relación (Textual)

**Entidades Principales:**

```
Personaje (Usuario)
├─ id (PK)
├─ username
├─ email
├─ password (hash)
├─ rol: [tributo, vigilante, mentor, jefe_capitolio]
├─ unidad_academica (solo mentores)
├─ distrito_asignado (solo mentores)
└─ foto

TributoInfo
├─ id (PK)
├─ personaje_id (FK → Personaje)
├─ mentor_id (FK → Personaje) [mentor]
├─ codigo_tributo (unique)
├─ distrito
├─ nivel: [novato, experimentado, avanzado]
├─ estado: [pendiente, acreditado, activo, eliminado, ganador]
├─ qr_code (imagen)
├─ qr_token (UUID unique)
└─ fecha_acreditacion

Torneo
├─ id (PK)
├─ nombre
├─ edicion
├─ fecha_inicio
├─ fecha_fin
├─ estado: [configuracion, inscripcion, en_curso, finalizado]
├─ creado_por (FK → Personaje)
└─ vigilantes_asignados (M2M → Personaje)

Reto
├─ id (PK)
├─ torneo_id (FK → Torneo)
├─ titulo
├─ descripcion
├─ dificultad: [novato, intermedio, avanzado, experto]
├─ tipo: [algoritmo, estructura_datos, etc.]
├─ puntos_base
├─ puntos_bonus
└─ tiempo_limite

CasoDePrueba
├─ id (PK)
├─ reto_id (FK → Reto)
├─ nombre
├─ entrada
├─ salida_esperada
├─ is_visible (boolean)
└─ puntos

ParticipacionTributo
├─ id (PK)
├─ tributo_id (FK → TributoInfo)
├─ reto_id (FK → Reto)
├─ lenguaje
├─ codigo_solucion
├─ estado: [pendiente, en_progreso, completado, fallido]
├─ puntos_obtenidos
├─ casos_pasados
├─ casos_totales
├─ numero_intento
└─ fecha_envio

AyudaMentor
├─ id (PK)
├─ mentor_id (FK → Personaje)
├─ tributo_id (FK → TributoInfo)
├─ reto_id (FK → Reto) [opcional]
├─ tipo: [pista, ejemplo, recurso, motivacion, advertencia]
├─ titulo
├─ contenido
├─ leida (boolean)
├─ fecha_lectura
├─ costo_puntos
└─ fecha_envio

PresupuestoMentor
├─ id (PK)
├─ mentor_id (FK → Personaje) [OneToOne]
├─ puntos_totales
├─ puntos_usados
├─ max_ayudas_por_dia
├─ total_ayudas_enviadas
└─ ultima_ayuda_enviada
```

---

## **6. INTERFACES EXTERNAS**

### 6.1 Interfaces de Usuario

**Principales pantallas:**
- Login/Register
- Dashboard por rol (4 tipos)
- Arena de torneo
- Resolución de reto
- Panel de acreditación QR
- Panel de monitoreo en vivo
- Formulario de enviar ayuda
- Vista de ayudas recibidas
- Asignación de mentores/vigilantes

### 6.2 Interfaces de Hardware

- **Webcam:** Para escaneo de códigos QR
- **Impresora:** Para imprimir credenciales (opcional)

### 6.3 Interfaces de Software

- **Servidor SMTP:** Envío de emails con credenciales
- **Sistema de archivos:** Almacenamiento de QR y fotos
- **Python subprocess:** Ejecución de código de tributos

### 6.4 Interfaces de Comunicación

- **HTTP/HTTPS:** Protocolo principal
- **WebSockets:** (Futuro) Para notificaciones en tiempo real
- **REST API:** Endpoints para polling (notificaciones, monitoreo)

---

## **7. ATRIBUTOS DE CALIDAD**

### 7.1 Confiabilidad
- Manejo de excepciones en ejecución de código
- Validación de entrada en todos los formularios
- Rollback de transacciones en caso de error

### 7.2 Disponibilidad
- Sistema diseñado para estar operativo 24/7
- Mantenimiento programado en horarios de baja carga

### 7.3 Mantenibilidad
- Código modular y reutilizable
- Tests automatizados
- Documentación técnica y de usuario

### 7.4 Seguridad
- Protección CSRF activada
- Headers de seguridad configurados
- Validación de permisos en cada vista
- Sanitización de inputs

---

## **8. RESTRICCIONES DE DISEÑO**

- **Framework:** Django 5.0.14 (obligatorio)
- **Lenguaje:** Python 3.14
- **Base de datos:** SQLite (dev), PostgreSQL/MySQL (prod)
- **Frontend:** Templates Django + JavaScript vanilla
- **Arquitectura:** MVC (Model-View-Controller)

---

## **9. DEPENDENCIAS EXTERNAS**

### 9.1 Bibliotecas Python
```
Django==5.0.14
python-decouple==3.8
qrcode[pil]==8.0
Pillow==12.0.0
reportlab==4.4.5
```

### 9.2 Bibliotecas JavaScript
- **jsQR** (CDN): Lectura de códigos QR en navegador

---

## **10. APÉNDICES**

### 10.1 Glosario de Términos Técnicos

- **Middleware:** Componente que intercepta peticiones HTTP
- **Polling:** Técnica de consulta periódica al servidor
- **Subprocess:** Proceso hijo para ejecutar código aislado
- **UUID:** Identificador único universal
- **Canvas API:** API de navegador para manipular imágenes

### 10.2 Estructura de Directorios

```
UNPA_Coding_Games/
├── manage.py
├── .env
├── venv/
├── capitol/                    # App de autenticación
│   ├── models.py              # Personaje, TributoInfo
│   ├── views.py               # Login, registro, acreditación
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── middleware.py          # AccreditationMiddleware
│   ├── utils.py               # Generación de gafetes
│   ├── templates/capitol/
│   ├── static/capitol/
│   └── migrations/
├── arena/                     # App de competencias
│   ├── models.py              # Torneo, Reto, Participacion, AyudaMentor, PresupuestoMentor
│   ├── views.py               # Arena, resolver retos
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── patrocinio.py
│   ├── templates/arena/
│   ├── static/arena/
│   └── migrations/
├── dashboards/                # App de dashboards
│   ├── views.py               # Dashboards por rol, APIs
│   ├── forms.py               # Asignaciones, enviar ayuda
│   ├── urls.py
│   ├── templates/dashboards/
│   ├── static/dashboards/
│   │   └── js/
│   │       └── notifications.js
│   └── migrations/
├── centro_control/            # App auxiliar
│   └── templates/centro_control/
├── unpa_code_games/           # Configuración proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── PSI/                       # Documentación
│   └── Especificacion_Requerimientos.md
└── db.sqlite3
```

### 10.3 Variables de Entorno (.env)

```bash
SECRET_KEY=django-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_app
DEFAULT_FROM_EMAIL=UNPA Coding Games <tu_email@gmail.com>

# Security
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 10.4 Comandos de Gestión

```bash
# Desarrollo
python manage.py runserver

# Base de datos
python manage.py makemigrations
python manage.py migrate

# Superusuario
python manage.py createsuperuser

# Tests
python manage.py test

# Recolectar estáticos
python manage.py collectstatic
```

---

## **11. HISTORIAL DE REVISIONES**

| Versión | Fecha | Autor | Descripción |
|---------|-------|-------|-------------|
| 1.0 | 10/12/2025 | Equipo Dev | Versión inicial completa |

---

## **12. APROBACIONES**

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Jefe de Proyecto | | | |
| Líder Técnico | | | |
| Cliente/Sponsor | | | |

---

**Documento generado automáticamente basado en la implementación actual del sistema UNPA Coding Games.**
