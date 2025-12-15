# Guía de Estilos - Dashboard del Jefe del Capitolio

## 📋 Resumen

Se han implementado estilos elegantes y sofisticados acordes a la temática de **The Hunger Games - Trilogía del Capitolio** para el dashboard del Jefe del Capitolio.

## 🎨 Paleta de Colores del Capitolio

La paleta se basa en los colores característicos del Capitolio:

| Variable CSS | Color | Uso |
|---|---|---|
| `--capitol-gold` | #d4af37 | Títulos, acentos, bordes |
| `--capitol-dark` | #0a0a0a | Fondo principal oscuro |
| `--capitol-silver` | #c0c0c0 | Textos secundarios |
| `--capitol-light` | #e8e4d9 | Textos claros |
| `--capitol-purple` | #6b3b6b | Acentos secundarios |
| `--capitol-accent` | #f0e68c | Acentos brillantes |

### Colores Funcionales

- **Success**: #2ecc71 (Verde)
- **Warning**: #f39c12 (Naranja)
- **Danger**: #e74c3c (Rojo)
- **Info**: #3498db (Azul)
- **Neutral**: #95a5a6 (Gris)

## 🏗️ Componentes Principales

### 1. **Dashboard Card** (`.dashboard-card`)

Card base para todos los contenedores del dashboard.

**Características:**
- Bordes dorados con efecto vidrio (backdrop-filter)
- Efecto hover con brillo dorado
- Sombra elegante
- Transiciones suaves

```html
<div class="dashboard-card">
    <h3>Título</h3>
    <!-- Contenido -->
</div>
```

### 2. **Stats Card** (`.stat-card`)

Tarjetas de estadísticas en la parte superior.

**Variantes de color:**
- Por defecto: Dorado
- `.info`: Azul
- `.success`: Verde
- `.warning`: Naranja

```html
<div class="stat-card">
    <div class="stat-icon">👥</div>
    <div class="stat-label">Total Tributos</div>
    <p class="stat-value">2847</p>
</div>
```

### 3. **Datos en Tablas** (`.data-table`)

Tablas con estilos acordes al Capitolio.

**Características:**
- Encabezados con fondo degradado dorado
- Filas con hover elegante
- Texto resaltado en dorado

### 4. **Notificaciones** (`.notification-item`)

Elementos de notificación con indicador de estado.

**Estados:**
- `.unread`: Con brillo dorado y animación
- Default: Estilo normal
- `.notification-item.unread`: Efecto glow animado

```html
<div class="notification-item unread">
    <div class="notification-icon">👤</div>
    <div class="notification-content">
        <p><strong>5 nuevos tributos</strong> esperan acreditación</p>
        <span class="time">Hace 2 horas</span>
    </div>
</div>
```

### 5. **Acciones Rápidas** (`.action-btn`)

Botones para acciones rápidas.

```html
<div class="action-btn">
    <span class="action-icon">➕</span>
    <span>Nueva Competencia</span>
</div>
```

### 6. **Badges** (`.badge`)

Etiquetas para estados y categorías.

**Variantes:**
- `.badge-success`: Verde
- `.badge-info`: Azul
- `.badge-warning`: Naranja
- `.badge-danger`: Rojo

## 📱 Diseño Responsivo

El dashboard se adapta automáticamente a diferentes tamaños de pantalla:

- **Desktop (> 1024px)**: Grid de 2 columnas (8/4)
- **Tablet (768px - 1024px)**: Reajuste automático
- **Móvil (< 768px)**: Column simple, ajustes de tamaño de fuente

## ✨ Efectos y Animaciones

### 1. **Efecto Brillo en Cards**
```css
.dashboard-card::before { /* Línea de luz horizontal */
    animation: left 100% (izquierda a derecha)
}
```

### 2. **Entrada Suave (fadeInUp)**
Todas las cards entran con una animación suave desde abajo.

### 3. **Brillo en Notificaciones No Leídas**
```css
@keyframes glow {
    box-shadow varía entre 0 0 10px y 0 0 20px
}
```

### 4. **Efecto Hover**
- Transform translateY(-4px): Efecto de levantamiento
- Cambio de color dorado
- Aumento de sombra

## 🎯 Clases Principales

| Clase | Descripción |
|---|---|
| `.dashboard-container` | Contenedor principal con gradiente |
| `.dashboard-card` | Card base elegante |
| `.stat-card` | Tarjeta de estadística |
| `.data-table` | Tabla de datos |
| `.notification-item` | Elemento de notificación |
| `.action-btn` | Botón de acción |
| `.badge` | Etiqueta de estado |
| `.filter-select` | Selector de filtro elegante |
| `.settings-list` | Lista de configuración |

## 🔧 Personalización

### Cambiar Colores Principales

Edita las variables CSS en la parte superior del archivo:

```css
:root {
    --capitol-gold: #d4af37;      /* Cambiar color principal */
    --capitol-silver: #c0c0c0;    /* Color secundario */
    /* ... */
}
```

### Ajustar Bordes y Sombras

```css
.dashboard-card {
    border: 2px solid rgba(212, 175, 55, 0.3);  /* Ajustar opacidad del borde */
    box-shadow: 0 8px 32px rgba(212, 175, 55, 0.15);  /* Ajustar sombra */
}
```

## 📂 Archivos de Estilos

- **`jefe_capitolio_dashboard.css`**: Estilos específicos del dashboard del jefe
- **`dashboard_styles.css`**: Estilos base para todos los dashboards

## 🚀 Próximas Mejoras

- [ ] Integración con Chart.js para gráficos
- [ ] Temas oscuro/claro intercambiables
- [ ] Modo "Juegos" con animaciones más dramáticas
- [ ] Exportación de reportes con estilos
- [ ] Integración con sistemas de notificaciones en tiempo real

## 💡 Tips de Uso

1. **Para agregar nuevas tarjetas**: Usa la clase `.dashboard-card`
2. **Para estadísticas**: Usa `.stat-card` con las variantes de color
3. **Para tablas**: Envuelve con `.data-table`
4. **Para notificaciones urgentes**: Agrega la clase `.unread`
5. **Para botones de acción**: Usa `.action-btn`

---

**Tema**: The Hunger Games - Elegancia y Sofisticación del Capitolio
**Versión**: 1.0
**Última actualización**: Diciembre 2025
