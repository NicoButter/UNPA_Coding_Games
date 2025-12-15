# 🎪 Guía de Extensión de Estilos a Otros Dashboards

## 📋 Introducción

Los estilos base creados para el dashboard del Jefe del Capitolio pueden extenderse fácilmente a otros dashboards (Mentor, Tributo, Vigilante, etc.). Esta guía explica cómo hacerlo.

## 🔄 Estructura Base Reutilizable

Ya existe una estructura base compartida que todos los dashboards usan:

```
dashboards/templates/dashboards/base_dashboard.html
    ├── Header (usuario, rol)
    ├── Stats Container (tarjetas de estadísticas)
    ├── Dashboard Content (contenido principal)
    └── Quick Actions (acciones rápidas)
```

Y los estilos base:

```
dashboards/static/dashboards/css/
    ├── dashboard_styles.css (base compartida)
    └── jefe_capitolio_dashboard.css (específico del jefe)
```

## 📚 Pasos para Extender a Otros Dashboards

### 1. Crear Archivo CSS Específico

Crea un nuevo archivo CSS para cada dashboard:

```bash
dashboards/static/dashboards/css/mentor_dashboard.css
dashboards/static/dashboards/css/tributo_dashboard.css
dashboards/static/dashboards/css/vigilante_dashboard.css
```

### 2. Estructura Recomendada del CSS

Copia esta estructura base y personalízala:

```css
/* ============================================
   Estilos del Dashboard [NOMBRE]
   Temática: The Hunger Games
   ============================================ */

:root {
    /* Hereda variables del Capitolio pero puedes personalizarlas */
    --capitol-gold: #d4af37;
    --dashboard-primary: #color-para-este-dashboard;
    --dashboard-secondary: #color-secundario;
    /* Agregar colores específicos si es necesario */
}

/* Aquí van tus estilos específicos */
```

### 3. Vincular el CSS en el Template

En el template específico del dashboard:

```django
{% block dashboard_extra_styles %}
    <link rel="stylesheet" href="{% static 'dashboards/css/mentor_dashboard.css' %}">
{% endblock %}
```

### 4. Componentes Reutilizables

Ya existen componentes reutilizables en:

```
dashboards/templates/dashboards/components/
    ├── stats_card.html (tarjeta de estadística)
    ├── quick_actions.html (acciones rápidas)
    ├── recent_activity.html (actividad reciente)
    └── (otros componentes)
```

## 🎨 Variantes de Temática por Rol

### Para Mentores 🎓
```css
:root {
    --dashboard-primary: #7b68ee;  /* Púrpura - Educación */
    --dashboard-secondary: #dda0dd;
}
```

### Para Tributos ⚔️
```css
:root {
    --dashboard-primary: #ff6b6b;  /* Rojo - Acción/Competencia */
    --dashboard-secondary: #ffa07a;
}
```

### Para Vigilantes 👁️
```css
:root {
    --dashboard-primary: #20b2aa;  /* Verde-azulado - Vigilancia */
    --dashboard-secondary: #48d1cc;
}
```

## 🔐 Mejores Prácticas

### 1. **Mantener Consistencia Visual**

Siempre usa las variables de color del Capitolio como base:

```css
/* ✅ BIEN */
border-color: rgba(var(--capitol-gold), 0.3);

/* ❌ EVITAR */
border-color: #d4af37;  /* Hardcodear colores */
```

### 2. **Reutilizar Clases Base**

```html
<!-- ✅ Usar clases existentes -->
<div class="dashboard-card">
    <h3>Título</h3>
</div>

<!-- ❌ Crear nuevas clases innecesarias -->
<div class="mentor-card special-style">
    <h3>Título</h3>
</div>
```

### 3. **Usar Animaciones Existentes**

```css
/* ✅ Reutilizar animaciones definidas */
.mi-elemento {
    animation: fadeInUp 0.6s ease-out;
}

/* Animaciones disponibles:
   - fadeInUp
   - glow
   - slideIn (definida en base_styles.css)
*/
```

### 4. **Mantener Orden en el CSS**

Estructura recomendada:

```css
/* 1. Variables globales */
:root { ... }

/* 2. Sobrescrituras de clases base */
.dashboard-card { ... }

/* 3. Clases específicas del dashboard */
.mentor-specific-class { ... }

/* 4. Estados (hover, active, etc.) */
.something:hover { ... }

/* 5. Animaciones */
@keyframes { ... }

/* 6. Media queries */
@media { ... }
```

## 📝 Ejemplo Completo: Dashboard de Mentor

### Archivo: `dashboards/static/dashboards/css/mentor_dashboard.css`

```css
/* ============================================
   Estilos del Dashboard de Mentor
   Temática: The Hunger Games - Educación
   ============================================ */

:root {
    /* Hereda del Capitolio */
    --capitol-gold: #d4af37;
    --capitol-silver: #c0c0c0;
    
    /* Colores específicos para mentores */
    --mentor-primary: #7b68ee;      /* Púrpura educación */
    --mentor-secondary: #dda0dd;    /* Orquídea */
    --mentor-accent: #ba55d3;       /* Violet medio */
}

/* Personalización de cards para mentores */
.dashboard-card {
    border-color: rgba(123, 104, 238, 0.3);
}

.dashboard-card:hover {
    border-color: var(--mentor-primary);
    box-shadow: 0 12px 40px rgba(123, 104, 238, 0.25);
}

.dashboard-card h3 {
    color: var(--mentor-primary);
}

/* Stats específicas de mentor */
.stat-card.mentor-stat {
    border-color: rgba(123, 104, 238, 0.3);
}

.stat-card.mentor-stat .stat-value {
    color: var(--mentor-primary);
}

/* Tarjeta de tributos */
.tributo-card {
    background: rgba(123, 104, 238, 0.05);
    border: 1px solid rgba(123, 104, 238, 0.2);
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 10px;
    transition: all 0.3s ease;
}

.tributo-card:hover {
    background: rgba(123, 104, 238, 0.1);
    border-color: var(--mentor-primary);
    transform: translateX(4px);
}

/* Lista de tareas */
.task-item {
    padding: 10px 15px;
    border-left: 3px solid var(--mentor-primary);
    background: rgba(123, 104, 238, 0.05);
    margin-bottom: 8px;
    border-radius: 4px;
}

.task-item.completed {
    opacity: 0.6;
    text-decoration: line-through;
    border-left-color: #2ecc71;
}

/* Responsive */
@media (max-width: 768px) {
    .tributo-card {
        margin-bottom: 8px;
    }
}
```

### Archivo: `dashboards/templates/dashboards/mentor_dashboard.html`

```django
{% extends 'dashboards/base_dashboard.html' %}
{% load static %}

{% block dashboard_title %}Mi Panel de Mentor{% endblock %}

{% block dashboard_extra_styles %}
    <link rel="stylesheet" href="{% static 'dashboards/css/mentor_dashboard.css' %}">
{% endblock %}

{% block dashboard_stats %}
    {% include 'dashboards/components/stats_card.html' with title="Mis Tributos" value=stats.mis_tributos icon="👥" %}
    {% include 'dashboards/components/stats_card.html' with title="Competencias" value=stats.competencias_asignadas icon="📚" %}
    {% include 'dashboards/components/stats_card.html' with title="Calificaciones" value=stats.promedio_calificacion icon="⭐" %}
{% endblock %}

{% block dashboard_content %}
    <!-- Contenido específico del mentor -->
{% endblock %}
```

## 🧪 Testear Nueva Extensión

1. **Verificar CSS es válido**:
```bash
# Revisar que no hay errores de sintaxis
grep -c "^@keyframes\|^:root\|^/" dashboards/static/dashboards/css/new_dashboard.css
```

2. **Verificar en navegador**:
   - Abrir el dashboard en el navegador
   - Inspeccionar elementos (F12)
   - Verificar que los estilos se están aplicando

3. **Checkeo de responsividad**:
   - Probar en dispositivos móviles
   - Verificar que los media queries funcionan

## 🔗 Referencias

- Archivo base: `dashboards/static/dashboards/css/dashboard_styles.css`
- Ejemplo principal: `dashboards/static/dashboards/css/jefe_capitolio_dashboard.css`
- Documentación completa: `docs/ESTILOS_DASHBOARD_CAPITOLIO.md`

## ✅ Checklist para Nueva Extensión

- [ ] Crear archivo CSS nuevo
- [ ] Definir variables :root específicas
- [ ] Personalizar clases base si es necesario
- [ ] Crear componentes CSS específicos
- [ ] Enlazar CSS en el template
- [ ] Probar en navegador
- [ ] Verificar responsividad
- [ ] Documentar cambios

## 💡 Tips

- **Mantén la paleta dorada del Capitolio**: Es la identidad visual del proyecto
- **Usa CSS variables**: Facilita cambios futuros
- **Evita !important**: Usa cascada CSS correctamente
- **Comenta el código**: Especialmente secciones complejas
- **Reutiliza animaciones**: No duplices código

---

**Versión**: 1.0  
**Última actualización**: 15 de Diciembre de 2025
