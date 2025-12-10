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
]
