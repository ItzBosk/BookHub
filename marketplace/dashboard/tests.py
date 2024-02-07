from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from item.models import Genre, Format, Language, CoverColor, Item
from django.core.files.images import ImageFile

"""Test della vista della dashboard"""
class DashboardViewTests(TestCase):
    
    def setUp(self):
        # Preparazione del client di test e dell'URL della vista
        self.client = Client()
        self.url = reverse('dashboard:index')

    """Verifica che l'utente venga reindirizzato alla pagina di login se non autenticato"""
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/login/?next={self.url}', msg_prefix="L'utente non autenticato non viene reindirizzato alla pagina di login.")


"""Test per la visualizzazione dei libri nella dashboard dell'utente"""
class DashboardItemsTest(TestCase):

    def setUp(self):
        # Creazione dell'utente di test
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # creazione libro di test
        self.genre = Genre.objects.create(name="Fantasy")
        self.format = Format.objects.create(name="Hardcover")
        self.language = Language.objects.create(name="English")
        self.cover_color = CoverColor.objects.create(name="Red")
        image = ImageFile(open('static/test.jpg', 'rb'), name='test.jpg')

        self.item = Item.objects.create(
            title="Test Book",
            created_by=self.user,
            price=9.99,
            genre=self.genre,
            format=self.format,
            language=self.language,
            cover_color=self.cover_color,
            number_of_pages=100,
            image=image,
        )
        self.client = Client()

    def tearDown(self):
        # Elimina le immagini dopo il test
        self.item.image.delete(save=False)
        super().tearDown()

    """Verifica che l'utente visualizzi solo i propri libri nella dashboard"""
    def test_user_sees_own_items(self):
        # effettua il login prima della richiesta GET
        login_successful = self.client.login(username='testuser', password='12345')
        self.assertTrue(login_successful, "Il login dell'utente non è riuscito.")
        
        # esegue una richiesta GET alla vista della dashboard e verifica il contenuto della risposta
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200, "Stato errato della risposta")
        self.assertTrue('items' in response.context, "La risposta non contiene 'items'")
        self.assertEqual(len(response.context['items']), 1, "Il numero di 'items' nella risposta non è 1")
        self.assertEqual(response.context['items'][0], self.item, "Il libro nella risposta non corrisponde al libro di test")


"""Test del template e del contesto della rispsota"""
class DashboardTemplateAndContextTest(TestCase):

    def setUp(self):
        # creazione di un utente di test e login
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # creazione libro di test associato all'utente
        self.genre = Genre.objects.create(name="Fantasy")
        self.format = Format.objects.create(name="Hardcover")
        self.language = Language.objects.create(name="English")
        self.cover_color = CoverColor.objects.create(name="Red")
        image = ImageFile(open('static/test.jpg', 'rb'), name='test.jpg')

        self.item = Item.objects.create(
            title="Test Book",
            author="Author Test",
            description="Test description",
            genre=self.genre,
            format=self.format,
            language=self.language,
            number_of_pages=123,
            cover_color=self.cover_color,
            price=29.99,
            image=image,
            created_by=self.user
        )

    def tearDown(self):
        # Elimina le immagini dopo il test
        self.item.image.delete(save=False)
        super().tearDown()

    """Test utilizzo del template corretto"""
    def test_uses_correct_template(self):
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')

    """Test contentuto del contesto della risposta"""
    def test_context_contains_user_items(self):
        response = self.client.get(reverse('dashboard:index'))
        self.assertIn('items', response.context)
        self.assertIn(self.item, response.context['items'])