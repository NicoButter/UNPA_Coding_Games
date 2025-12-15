from django.urls import path
from . import views

app_name = 'judge'

urlpatterns = [
    # Enviar solución
    path('submit/<int:reto_id>/', views.submit_solution, name='submit_solution'),
    
    # Ver detalles de una submission
    path('submission/<int:submission_id>/', views.submission_detail, name='submission_detail'),
    
    # Historial de submissions para un reto
    path('history/<int:reto_id>/', views.submission_history, name='submission_history'),
]
