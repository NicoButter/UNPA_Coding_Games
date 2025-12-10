// Sistema de notificaciones en tiempo real para dashboards
// Actualiza el contador de ayudas pendientes automáticamente

class NotificationSystem {
    constructor() {
        this.checkInterval = 30000; // 30 segundos
        this.init();
    }
    
    init() {
        // Solo ejecutar si hay un elemento de notificaciones
        if (document.querySelector('[data-notifications-badge]')) {
            this.startPolling();
        }
    }
    
    startPolling() {
        // Verificar notificaciones cada 30 segundos
        setInterval(() => {
            this.checkNotifications();
        }, this.checkInterval);
        
        // Verificar inmediatamente al cargar
        this.checkNotifications();
    }
    
    async checkNotifications() {
        try {
            const response = await fetch('/api/notifications/check/');
            const data = await response.json();
            
            this.updateBadges(data);
            this.showToastIfNew(data);
        } catch (error) {
            console.error('Error checking notifications:', error);
        }
    }
    
    updateBadges(data) {
        // Actualizar badges de ayudas pendientes
        const badges = document.querySelectorAll('[data-notifications-badge="ayudas"]');
        badges.forEach(badge => {
            if (data.ayudas_pendientes > 0) {
                badge.textContent = data.ayudas_pendientes;
                badge.style.display = 'inline-block';
                badge.classList.add('pulse');
            } else {
                badge.style.display = 'none';
            }
        });
        
        // Actualizar contador en el título de la página
        const currentTitle = document.title;
        if (data.ayudas_pendientes > 0) {
            if (!currentTitle.startsWith('(')) {
                document.title = `(${data.ayudas_pendientes}) ${currentTitle}`;
            }
        } else {
            document.title = currentTitle.replace(/^\(\d+\)\s/, '');
        }
    }
    
    showToastIfNew(data) {
        // Si hay ayudas nuevas desde la última verificación, mostrar notificación
        const lastCount = parseInt(localStorage.getItem('last_ayudas_count') || '0');
        
        if (data.ayudas_pendientes > lastCount) {
            const diff = data.ayudas_pendientes - lastCount;
            this.showToast(`✨ Tienes ${diff} nueva(s) ayuda(s) de tu mentor`);
            
            // Reproducir sonido si está habilitado
            if (localStorage.getItem('notifications_sound') !== 'false') {
                this.playNotificationSound();
            }
        }
        
        localStorage.setItem('last_ayudas_count', data.ayudas_pendientes.toString());
    }
    
    showToast(message) {
        // Crear elemento de toast si no existe
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10000;
            `;
            document.body.appendChild(toastContainer);
        }
        
        // Crear toast
        const toast = document.createElement('div');
        toast.className = 'notification-toast';
        toast.style.cssText = `
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            margin-bottom: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            animation: slideInRight 0.3s ease-out;
            cursor: pointer;
            max-width: 300px;
        `;
        toast.textContent = message;
        
        // Click para ir a ayudas
        toast.onclick = () => {
            window.location.href = '/tributo/ayudas/';
        };
        
        toastContainer.appendChild(toast);
        
        // Auto-eliminar después de 5 segundos
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }
    
    playNotificationSound() {
        // Crear un beep simple usando Web Audio API
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.2);
    }
}

// Agregar estilos de animación
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
        }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    [data-notifications-badge] {
        display: inline-block;
        background: #FF0000;
        color: white;
        border-radius: 50%;
        padding: 2px 6px;
        font-size: 0.75em;
        font-weight: bold;
        margin-left: 5px;
        min-width: 20px;
        text-align: center;
    }
`;
document.head.appendChild(style);

// Inicializar el sistema cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new NotificationSystem();
    });
} else {
    new NotificationSystem();
}
