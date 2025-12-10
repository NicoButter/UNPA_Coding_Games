from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('login/webcam/', views.login_webcam, name='login_webcam'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('perfil/', views.perfil_view, name='perfil'),
    
    # Gafetes
    path('gafete/descargar/', views.descargar_gafete, name='descargar_gafete'),
    path('gafete/ver/', views.ver_gafete, name='ver_gafete'),
    path('gafete/reenviar/', views.reenviar_gafete, name='reenviar_gafete'),
    
    # Acreditación
    path('acreditar/qr/', views.acreditar_tributo_qr, name='acreditar_tributo_qr'),
]
