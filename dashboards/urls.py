from django.urls import path
from . import views

app_name = 'dashboards'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    
    # URLs para Jefe del Capitolio
    path('jefe/asignar-mentores/', views.asignar_mentores_view, name='asignar_mentores'),
    path('jefe/asignar-vigilantes/', views.asignar_vigilantes_view, name='asignar_vigilantes'),
    
    # URLs para Mentores
    path('mentor/enviar-ayuda/', views.enviar_ayuda_view, name='enviar_ayuda'),
    path('mentor/tributos/', views.mis_tributos_view, name='mis_tributos'),
    
    # URLs para Tributos
    path('tributo/ayudas/', views.ver_ayudas_view, name='ver_ayudas'),
    
    # URLs para Vigilantes
    path('vigilante/monitoreo/', views.panel_monitoreo_view, name='panel_monitoreo'),
    
    # Administración personalizada
    path('jefe/admin/', views.admin_jefe_view, name='admin_jefe'),
    path('jefe/crear-torneo/', views.crear_torneo_view, name='crear_torneo'),
    path('jefe/crear-retos/', views.crear_retos_view, name='crear_retos'),
    path('jefe/asignar-mentores-admin/', views.asignar_mentores_admin_view, name='asignar_mentores_admin'),
    path('jefe/asignar-vigilantes-admin/', views.asignar_vigilantes_admin_view, name='asignar_vigilantes_admin'),
    
    # API
    path('api/notifications/check/', views.check_notifications_api, name='check_notifications'),
    path('api/monitor/tributos/', views.monitor_tributos_api, name='monitor_tributos'),
]
