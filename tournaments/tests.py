from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from capitol.models import Personaje
from districts.models import District
from .models import Tournament, TournamentMentor, TournamentVigilante


class TournamentModelTest(TestCase):
    """Tests para el modelo Tournament"""
    
    def setUp(self):
        self.jefe = Personaje.objects.create_user(
            username='jefe_test',
            password='pass123',
            rol='jefe_capitolio'
        )
        
        now = timezone.now()
        self.tournament = Tournament.objects.create(
            nombre='Hunger Games 2025',
            numero_edicion=75,
            fecha_acreditacion_inicio=now,
            fecha_acreditacion_fin=now + timedelta(hours=2),
            fecha_competencia_inicio=now + timedelta(hours=3),
            fecha_competencia_fin=now + timedelta(hours=8),
            fecha_premios=now + timedelta(hours=9),
            creado_por=self.jefe
        )
    
    def test_tournament_str(self):
        self.assertEqual(str(self.tournament), 'Hunger Games 2025 - Edición 75')
    
    def test_tournament_activo_por_defecto(self):
        self.assertTrue(self.tournament.es_activo)
    
    def test_tournament_estado_planificacion_defecto(self):
        self.assertEqual(self.tournament.estado, 'planificacion')
    
    def test_esta_en_acreditacion(self):
        now = timezone.now()
        tournament = Tournament.objects.create(
            nombre='Test Tournament',
            numero_edicion=1,
            fecha_acreditacion_inicio=now - timedelta(hours=1),
            fecha_acreditacion_fin=now + timedelta(hours=1),
            fecha_competencia_inicio=now + timedelta(hours=2),
            fecha_competencia_fin=now + timedelta(hours=7),
            fecha_premios=now + timedelta(hours=8),
            creado_por=self.jefe
        )
        self.assertTrue(tournament.esta_en_acreditacion)
    
    def test_clean_validation_fechas(self):
        """Verifica que las validaciones de fecha funcionen"""
        # Crear un torneo con fechas inválidas
        invalid_tournament = Tournament(
            nombre='Invalid',
            numero_edicion=1,
            fecha_acreditacion_inicio=timezone.now(),
            fecha_acreditacion_fin=timezone.now() - timedelta(hours=1),  # Fin antes que inicio
            fecha_competencia_inicio=timezone.now() + timedelta(hours=1),
            fecha_competencia_fin=timezone.now() + timedelta(hours=5),
            fecha_premios=timezone.now() + timedelta(hours=6),
            creado_por=self.jefe
        )
        
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            invalid_tournament.clean()


class TournamentMentorModelTest(TestCase):
    """Tests para el modelo TournamentMentor"""
    
    def setUp(self):
        self.jefe = Personaje.objects.create_user(
            username='jefe_test',
            password='pass123',
            rol='jefe_capitolio'
        )
        
        self.mentor = Personaje.objects.create_user(
            username='mentor_test',
            password='pass123',
            rol='mentor'
        )
        
        self.distrito = District.objects.create(
            name='Ingeniería en Sistemas',
            code='SIS-001',
            description='Carrera de Ingeniería en Sistemas'
        )
        
        now = timezone.now()
        self.tournament = Tournament.objects.create(
            nombre='Test Tournament',
            numero_edicion=1,
            fecha_acreditacion_inicio=now,
            fecha_acreditacion_fin=now + timedelta(hours=2),
            fecha_competencia_inicio=now + timedelta(hours=3),
            fecha_competencia_fin=now + timedelta(hours=8),
            fecha_premios=now + timedelta(hours=9),
            creado_por=self.jefe
        )
        
        self.mentor_assignment = TournamentMentor.objects.create(
            torneo=self.tournament,
            mentor=self.mentor,
            distrito=self.distrito,
            asignado_por=self.jefe
        )
    
    def test_mentor_assignment_str(self):
        expected = f"{self.mentor.get_full_name()} - {self.distrito.name} ({self.tournament.nombre})"
        self.assertEqual(str(self.mentor_assignment), expected)
    
    def test_unique_constraint_torneo_distrito(self):
        """Verifica que no se puede asignar dos mentores al mismo distrito en un torneo"""
        from django.db import IntegrityError
        
        otro_mentor = Personaje.objects.create_user(
            username='otro_mentor',
            password='pass123',
            rol='mentor'
        )
        
        with self.assertRaises(IntegrityError):
            TournamentMentor.objects.create(
                torneo=self.tournament,
                mentor=otro_mentor,
                distrito=self.distrito,
                asignado_por=self.jefe
            )


class TournamentVigilanteModelTest(TestCase):
    """Tests para el modelo TournamentVigilante"""
    
    def setUp(self):
        self.jefe = Personaje.objects.create_user(
            username='jefe_test',
            password='pass123',
            rol='jefe_capitolio'
        )
        
        self.vigilante = Personaje.objects.create_user(
            username='vigilante_test',
            password='pass123',
            rol='vigilante'
        )
        
        now = timezone.now()
        self.tournament = Tournament.objects.create(
            nombre='Test Tournament',
            numero_edicion=1,
            fecha_acreditacion_inicio=now,
            fecha_acreditacion_fin=now + timedelta(hours=2),
            fecha_competencia_inicio=now + timedelta(hours=3),
            fecha_competencia_fin=now + timedelta(hours=8),
            fecha_premios=now + timedelta(hours=9),
            creado_por=self.jefe
        )
        
        self.vigilante_assignment = TournamentVigilante.objects.create(
            torneo=self.tournament,
            vigilante=self.vigilante,
            rol_en_torneo='general',
            asignado_por=self.jefe
        )
    
    def test_vigilante_assignment_str(self):
        expected = f"{self.vigilante.get_full_name()} - Vigilante General ({self.tournament.nombre})"
        self.assertEqual(str(self.vigilante_assignment), expected)
    
    def test_vigilante_roles(self):
        """Verifica que los roles de vigilante se asignen correctamente"""
        roles = ['general', 'acreditacion', 'competencia', 'premios']
        for rol in roles:
            vigilante = Personaje.objects.create_user(
                username=f'vigilante_{rol}',
                password='pass123',
                rol='vigilante'
            )
            assignment = TournamentVigilante.objects.create(
                torneo=self.tournament,
                vigilante=vigilante,
                rol_en_torneo=rol,
                asignado_por=self.jefe
            )
            self.assertEqual(assignment.rol_en_torneo, rol)
