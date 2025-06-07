from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Viaje, Comentario, Actividad, Imagen
from datetime import date, time
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class ViajeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.viaje = Viaje.objects.create(
            usuario=self.user,
            titulo='Vacaciones en París',
            ciudad='París',
            fecha_inicio=date(2025, 6, 1),
            fecha_final=date(2025, 6, 10),
            descripcion='Un viaje soñado.',
            presupuesto=1500.50
        )

    def test_viaje_creacion(self):
        self.assertEqual(self.viaje.titulo, 'Vacaciones en París')
        self.assertEqual(str(self.viaje), 'Vacaciones en París - París')


class ComentarioModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user2', password='abc123')
        self.comentario = Comentario.objects.create(
            usuario=self.user,
            texto='Muy buen sitio',
            aprobado=True
        )

    def test_comentario_str(self):
        self.assertIn(self.user.username, str(self.comentario))


class ActividadModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user3', password='abc123')
        self.viaje = Viaje.objects.create(
            usuario=self.user,
            titulo='Ruta Maya',
            ciudad='Tulum',
            fecha_inicio=date(2025, 5, 10),
            fecha_final=date(2025, 5, 20),
            descripcion='Explorando ruinas.',
            presupuesto=1200.00
        )
        self.actividad = Actividad.objects.create(
            viaje=self.viaje,
            titulo='Visita Chichen Itzá',
            fecha=date(2025, 5, 12),
            tiempo=time(9, 0),
            localizacion='Yucatán',
            coste=30.00,
            informacion='Entrada general',
            completada=True
        )

    def test_actividad_str(self):
        self.assertEqual(str(self.actividad), 'Visita Chichen Itzá')


class ImagenModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user4', password='abc123')
        self.viaje = Viaje.objects.create(
            usuario=self.user,
            titulo='Montaña',
            ciudad='Andes',
            fecha_inicio=date(2025, 7, 1),
            fecha_final=date(2025, 7, 5),
            descripcion='Aventura en la montaña.',
            presupuesto=800.00
        )
        self.imagen = Imagen.objects.create(
            viaje=self.viaje,
            imagen=SimpleUploadedFile("foto.jpg", b"file_content", content_type="image/jpeg"),
            comentario='Foto en la cima'
        )

    def test_imagen_comentario(self):
        self.assertEqual(self.imagen.comentario, 'Foto en la cima')


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.comentario = Comentario.objects.create(usuario=self.user, texto='Buen viaje', aprobado=True)

    def test_home_status_code(self):
        response = self.client.get(reverse('info:home'))
        self.assertEqual(response.status_code, 200)

    def test_comentario_aprobado_visible(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('info:home'))
        self.assertContains(response, 'Buen viaje')

    def test_envio_comentario_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('info:home'), {'texto': 'Mi opinión'}, follow=True)
        self.assertContains(response, '¡Tu comentario fue enviado!. Está pendiente de aprobación.')
        self.assertTrue(Comentario.objects.filter(texto='Mi opinión').exists())
