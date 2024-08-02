from django.urls import path
from . import views

urlpatterns = [
    path('acreditar_tributo/', views.acreditar_tributo, name='acreditar_tributo'),
    # otras URLs...
]
