from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.images import ImageFile
from item.models import Genre, Item, Format, Language, CoverColor
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

"""Test index view"""
class IndexViewTest(TestCase):
    # creazione libro di test
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.genre = Genre.objects.create(name='Fantasy')
        self.format = Format.objects.create(name='Print Book')
        self.language = Language.objects.create(name='English')
        self.cover_color = CoverColor.objects.create(name='Blue')

        self.item = Item.objects.create(
            title="Test Book",
            author="Test Author",
            description="A test description",
            genre=self.genre,
            format=self.format,
            language=self.language,
            number_of_pages=100,
            cover_color=self.cover_color,
            price=20.00,
            image=ImageFile(open('media/item_images/test.jpg', 'rb'), name='test.jpg'),
            is_sold=False,
            created_by=self.user
        )

    def tearDown(self):
        # pulizia immagini di test
        self.item.image.delete(save=False)
        super().tearDown()

    """Verifica che la pagina index carichi correttamente"""
    def test_index_view_status_code(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)

    """Verifica che il contesto della pagina index contenga gli articoli"""
    def test_index_view_context_contains_items(self):
        response = self.client.get(reverse('core:index'))
        self.assertIn('items', response.context)
        self.assertIn(self.item, response.context['items'])

    """Verifica che il contesto della pagina index contenga i generi"""
    def test_index_view_genre_in_context(self):
        response = self.client.get(reverse('core:index'))
        self.assertIn('genres', response.context)
        self.assertIn(self.genre, response.context['genres'])

"""Test signup view"""
class SignupViewTest(TestCase):

    def setUp(self):
        # Setup iniziale per creare un client e definire l'url della view di registrazione
        self.client = Client()
        self.url = reverse('core:signup')

    """Verifica che la pagina di registrazione sia accessibile"""
    def test_signup_page_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    """Controlla se il form di registrazione viene visualizzato correttamente"""
    def test_signup_form_displayed(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<form')
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password1"')
        self.assertContains(response, 'name="password2"')

    """Verifica che un form di registrazione valido reindirizzi l'utente alla pagina di login"""
    def test_successful_signup_redirect(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, '/login/')

    """Verifica che il form di registrazione con dati non validi non crei un nuovo utente e riporti errori"""
    def test_signup_with_invalid_data(self):
        self.client.login(username='testuser', password='password')
        data = {
            'username': '',  # username mancante
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())
        self.assertTrue('form' in response.context)     # assicura che la form sia presente nel contesto della risposta
        form_errors = response.context['form'].errors   # verifica che la form contenga errori
        self.assertTrue('username' in form_errors)

"""Test signout view"""
class SignoutViewTest(TestCase):

    def setUp(self):
        # Creazione di un client di test e di un utente di test
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.signout_url = reverse('core:signout')
        self.index_url = reverse('core:index')

    """Verifica il reindirizzamento alla home page dopo il logout"""
    def test_signout_redirect(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.signout_url)    # fai il logout
        self.assertRedirects(response, self.index_url)  # verifica reindirizzamento

    """Controlla la terminazione della sessione dopo il logout"""
    def test_session_terminated_after_signout(self):
        self.client.login(username='testuser', password='password')     # login
        self.client.get(self.signout_url)   # logout
        user_id = self.client.session.get('_auth_user_id')  # verifica che la sessione sia terminata
        self.assertIsNone(user_id)

    """Assicura che l'utente sia anonimo dopo il logout"""
    def test_user_is_anonymous_after_signout(self):
        self.client.login(username='testuser', password='password')
        self.client.get(self.signout_url)
        response = self.client.get(self.index_url)      # verifica che l'utente sia anonimo dopo il logout
        self.assertTrue(response.context['user'].is_anonymous)