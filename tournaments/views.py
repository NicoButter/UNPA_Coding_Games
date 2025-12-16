from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import transaction
from django.http import JsonResponse
from .models import Tournament, TournamentMentor, TournamentVigilante, TournamentStatus
from .forms import (
    TournamentForm, TournamentMentorForm, TournamentVigilanteForm,
    AssignMentorsToDistritosForm, AssignVigilantesToTournamentForm
)
from districts.models import District
from capitol.models import Personaje


class IsJefeCapitolioMixin(UserPassesTestMixin):
    """Mixin para verificar que el usuario es Jefe del Capitolio"""
    def test_func(self):
        return self.request.user.rol == 'jefe_capitolio'
    
    def handle_no_permission(self):
        messages.error(self.request, 'Solo los Jefes del Capitolio pueden acceder a esta sección.')
        return redirect('dashboard')


class TournamentListView(LoginRequiredMixin, IsJefeCapitolioMixin, ListView):
    """Lista todos los torneos"""
    model = Tournament
    template_name = 'tournaments/tournament_list.html'
    context_object_name = 'torneos'
    paginate_by = 10
    
    def get_queryset(self):
        return Tournament.objects.all().order_by('-fecha_creacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_torneos'] = Tournament.objects.count()
        context['torneos_activos'] = Tournament.objects.filter(es_activo=True).count()
        return context


class TournamentDetailView(LoginRequiredMixin, IsJefeCapitolioMixin, DetailView):
    """Detalle de un torneo específico"""
    model = Tournament
    template_name = 'tournaments/tournament_detail.html'
    context_object_name = 'torneo'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        torneo = self.get_object()
        
        context['mentores'] = TournamentMentor.objects.filter(
            torneo=torneo,
            es_activa=True
        )
        context['vigilantes'] = TournamentVigilante.objects.filter(
            torneo=torneo,
            es_activa=True
        )
        context['historial'] = TournamentStatus.objects.filter(torneo=torneo)[:5]
        context['distritos_sin_mentor'] = self._get_distritos_sin_mentor(torneo)
        
        return context
    
    def _get_distritos_sin_mentor(self, torneo):
        """Obtiene distritos sin mentor asignado en este torneo"""
        distritos_con_mentor = TournamentMentor.objects.filter(
            torneo=torneo,
            es_activa=True
        ).values_list('distrito_id', flat=True)
        
        return District.objects.filter(
            is_active=True
        ).exclude(id__in=distritos_con_mentor)


class TournamentCreateView(LoginRequiredMixin, IsJefeCapitolioMixin, CreateView):
    """Crear un nuevo torneo"""
    model = Tournament
    form_class = TournamentForm
    template_name = 'tournaments/tournament_form.html'
    success_url = reverse_lazy('tournament_list')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        messages.success(self.request, f'Torneo "{form.instance.nombre}" creado exitosamente.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Nuevo Torneo'
        context['button_text'] = 'Crear Torneo'
        return context


class TournamentUpdateView(LoginRequiredMixin, IsJefeCapitolioMixin, UpdateView):
    """Editar un torneo existente"""
    model = Tournament
    form_class = TournamentForm
    template_name = 'tournaments/tournament_form.html'
    success_url = reverse_lazy('tournament_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Torneo "{form.instance.nombre}" actualizado exitosamente.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editar Torneo: {self.object.nombre}'
        context['button_text'] = 'Actualizar Torneo'
        return context


class TournamentDeleteView(LoginRequiredMixin, IsJefeCapitolioMixin, DeleteView):
    """Eliminar un torneo"""
    model = Tournament
    template_name = 'tournaments/tournament_confirm_delete.html'
    success_url = reverse_lazy('tournament_list')
    
    def delete(self, request, *args, **kwargs):
        torneo = self.get_object()
        messages.success(request, f'Torneo "{torneo.nombre}" eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


class AssignMentorsView(LoginRequiredMixin, IsJefeCapitolioMixin, UpdateView):
    """Vista para asignar mentores a los distritos de un torneo"""
    model = Tournament
    form_class = TournamentMentorForm
    template_name = 'tournaments/assign_mentors.html'
    
    def get_success_url(self):
        return reverse_lazy('tournament_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        torneo = self.get_object()
        
        # Distritos sin mentor
        context['distritos'] = self._get_distritos_sin_mentor(torneo)
        
        # Mentores ya asignados
        context['mentores_asignados'] = TournamentMentor.objects.filter(
            torneo=torneo,
            es_activa=True
        )
        
        return context
    
    def _get_distritos_sin_mentor(self, torneo):
        """Obtiene distritos sin mentor asignado"""
        distritos_con_mentor = TournamentMentor.objects.filter(
            torneo=torneo,
            es_activa=True
        ).values_list('distrito_id', flat=True)
        
        return District.objects.filter(
            is_active=True
        ).exclude(id__in=distritos_con_mentor)


class AddMentorToTournamentView(LoginRequiredMixin, IsJefeCapitolioMixin, CreateView):
    """Agregar un mentor a una unidad académica en un torneo"""
    model = TournamentMentor
    form_class = TournamentMentorForm
    template_name = 'tournaments/add_mentor.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.torneo = get_object_or_404(Tournament, pk=kwargs['tournament_pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['torneo'] = self.torneo
        return kwargs
    
    def form_valid(self, form):
        form.instance.torneo = self.torneo
        form.instance.asignado_por = self.request.user
        messages.success(
            self.request,
            f'Mentor "{form.instance.mentor.get_full_name()}" asignado a '
            f'"{form.instance.unidad_academica.nombre}".'
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('tournament_detail', kwargs={'pk': self.torneo.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['torneo'] = self.torneo
        return context


class RemoveMentorFromTournamentView(LoginRequiredMixin, IsJefeCapitolioMixin, UpdateView):
    """Remover un mentor de un torneo"""
    model = TournamentMentor
    fields = ['es_activa']
    template_name = 'tournaments/confirm_remove_mentor.html'
    
    def form_valid(self, form):
        form.instance.es_activa = False
        messages.success(self.request, 'Mentor removido de este torneo.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('tournament_detail', kwargs={'pk': self.object.torneo.pk})


class AddVigilanteToTournamentView(LoginRequiredMixin, IsJefeCapitolioMixin, CreateView):
    """Agregar vigilantes a un torneo"""
    model = TournamentVigilante
    form_class = TournamentVigilanteForm
    template_name = 'tournaments/add_vigilante.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.torneo = get_object_or_404(Tournament, pk=kwargs['tournament_pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['torneo'] = self.torneo
        return kwargs
    
    def form_valid(self, form):
        form.instance.torneo = self.torneo
        form.instance.asignado_por = self.request.user
        messages.success(
            self.request,
            f'Vigilante "{form.instance.vigilante.get_full_name()}" asignado al torneo.'
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('tournament_detail', kwargs={'pk': self.torneo.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['torneo'] = self.torneo
        return context


class RemoveVigilanteFromTournamentView(LoginRequiredMixin, IsJefeCapitolioMixin, UpdateView):
    """Remover un vigilante de un torneo"""
    model = TournamentVigilante
    fields = ['es_activa']
    template_name = 'tournaments/confirm_remove_vigilante.html'
    
    def form_valid(self, form):
        form.instance.es_activa = False
        messages.success(self.request, 'Vigilante removido de este torneo.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('tournament_detail', kwargs={'pk': self.object.torneo.pk})


class BulkAssignMentorsView(LoginRequiredMixin, IsJefeCapitolioMixin, CreateView):
    """Vista para asignar múltiples mentores a múltiples distritos de un torneo"""
    model = TournamentMentor
    form_class = AssignMentorsToDistritosForm
    template_name = 'tournaments/bulk_assign_mentors.html'
    
    def form_valid(self, form):
        torneo = form.cleaned_data['torneo']
        mentores = form.cleaned_data['mentores']
        distritos = form.cleaned_data['distritos']
        
        asignaciones_creadas = 0
        asignaciones_duplicadas = 0
        
        with transaction.atomic():
            for mentor in mentores:
                # Distribuir mentores entre distritos (round-robin)
                for idx, distrito in enumerate(distritos):
                    mentor_asignado = mentores[idx % len(mentores)]
                    
                    # Verificar si ya existe la asignación
                    existe = TournamentMentor.objects.filter(
                        torneo=torneo,
                        distrito=distrito,
                        es_activa=True
                    ).exists()
                    
                    if not existe:
                        TournamentMentor.objects.create(
                            torneo=torneo,
                            mentor=mentor_asignado,
                            distrito=distrito,
                            asignado_por=self.request.user
                        )
                        asignaciones_creadas += 1
                    else:
                        asignaciones_duplicadas += 1
        
        messages.success(
            self.request,
            f'{asignaciones_creadas} asignaciones creadas. '
            f'({asignaciones_duplicadas} ya existían.)'
        )
        
        return redirect('tournament_detail', pk=torneo.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Asignar Múltiples Mentores'
        return context


class BulkAssignVigilantesView(LoginRequiredMixin, IsJefeCapitolioMixin, CreateView):
    """Vista para asignar múltiples vigilantes a un torneo"""
    model = TournamentVigilante
    form_class = AssignVigilantesToTournamentForm
    template_name = 'tournaments/bulk_assign_vigilantes.html'
    
    def form_valid(self, form):
        torneo = form.cleaned_data['torneo']
        vigilantes = form.cleaned_data['vigilantes']
        rol_defecto = form.cleaned_data['rol_por_defecto']
        
        asignaciones_creadas = 0
        asignaciones_duplicadas = 0
        
        with transaction.atomic():
            for vigilante in vigilantes:
                # Verificar si ya existe la asignación
                existe = TournamentVigilante.objects.filter(
                    torneo=torneo,
                    vigilante=vigilante,
                    es_activa=True
                ).exists()
                
                if not existe:
                    TournamentVigilante.objects.create(
                        torneo=torneo,
                        vigilante=vigilante,
                        rol_en_torneo=rol_defecto,
                        asignado_por=self.request.user
                    )
                    asignaciones_creadas += 1
                else:
                    asignaciones_duplicadas += 1
        
        messages.success(
            self.request,
            f'{asignaciones_creadas} vigilantes asignados. '
            f'({asignaciones_duplicadas} ya estaban asignados.)'
        )
        
        return redirect('tournament_detail', pk=torneo.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Asignar Múltiples Vigilantes'
        return context


class DistrictListView(LoginRequiredMixin, IsJefeCapitolioMixin, ListView):
    """Lista de distritos disponibles"""
    model = District
    template_name = 'tournaments/distrito_list.html'
    context_object_name = 'distritos'
    paginate_by = 20
    
    def get_queryset(self):
        return District.objects.all().order_by('name')


class DistrictCreateView(LoginRequiredMixin, IsJefeCapitolioMixin, CreateView):
    """Crear un nuevo distrito - Vista de referencia (usa districts app)"""
    model = District
    fields = ['name', 'code', 'description', 'is_active']
    template_name = 'tournaments/distrito_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Distrito creado exitosamente.')
        return reverse_lazy('distrito_list')


class DistrictUpdateView(LoginRequiredMixin, IsJefeCapitolioMixin, UpdateView):
    """Editar un distrito - Vista de referencia (usa districts app)"""
    model = District
    fields = ['name', 'code', 'description', 'is_active']
    template_name = 'tournaments/distrito_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Distrito actualizado exitosamente.')
        return reverse_lazy('distrito_list')
