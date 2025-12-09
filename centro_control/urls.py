from django.urls import path
from . import views

app_name = 'centro_control'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('acreditar/<int:tributo_id>/', views.acreditar_tributo, name='acreditar_tributo'),
]
