from django.urls import path
from . import views

app_name = 'arena'

urlpatterns = [
    # Torneos
    path('torneos/', views.torneos_disponibles, name='torneos_disponibles'),
    path('torneo/<int:torneo_id>/', views.arena_torneo, name='arena_torneo'),
    
    # Retos
    path('reto/<int:reto_id>/', views.resolver_reto, name='resolver_reto'),
    path('reto/<int:reto_id>/validar/', views.validar_solucion, name='validar_solucion'),
    
    # Finalización y resultados
    path('torneo/<int:torneo_id>/finalizar/', views.finalizar_participacion, name='finalizar_participacion'),
    path('torneo/<int:torneo_id>/resultados/', views.resultado_torneo, name='resultado_torneo'),
]