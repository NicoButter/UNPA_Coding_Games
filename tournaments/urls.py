from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    # Torneos - CRUD
    path('', views.TournamentListView.as_view(), name='tournament_list'),
    path('crear/', views.TournamentCreateView.as_view(), name='tournament_create'),
    path('<int:pk>/', views.TournamentDetailView.as_view(), name='tournament_detail'),
    path('<int:pk>/editar/', views.TournamentUpdateView.as_view(), name='tournament_update'),
    path('<int:pk>/eliminar/', views.TournamentDeleteView.as_view(), name='tournament_delete'),
    
    # Asignación de Mentores
    path('<int:tournament_pk>/agregar-mentor/', views.AddMentorToTournamentView.as_view(), name='add_mentor'),
    path('mentor/<int:pk>/remover/', views.RemoveMentorFromTournamentView.as_view(), name='remove_mentor'),
    path('<int:pk>/asignar-mentores/', views.AssignMentorsView.as_view(), name='assign_mentors'),
    path('asignar-mentores-multiples/', views.BulkAssignMentorsView.as_view(), name='bulk_assign_mentors'),
    
    # Asignación de Vigilantes
    path('<int:tournament_pk>/agregar-vigilante/', views.AddVigilanteToTournamentView.as_view(), name='add_vigilante'),
    path('vigilante/<int:pk>/remover/', views.RemoveVigilanteFromTournamentView.as_view(), name='remove_vigilante'),
    path('asignar-vigilantes-multiples/', views.BulkAssignVigilantesView.as_view(), name='bulk_assign_vigilantes'),
]
