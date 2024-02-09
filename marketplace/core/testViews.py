from django.test import TestCase, Client
from django.urls import reverse
from item.models import Genre, Item
from django.contrib.auth.models import User

class CoreViewsTestCase(TestCase):

    def setUp(self):
        # Imposta i dati di test
        self.client = Client()
        self.index_url = reverse('core:index')
        self.contact_url = reverse('core:contact')
        self.signup_url = reverse('core:signup')
        self.signout_url = reverse('core:signout')
        Genre.objects.create(name='GenreTest')
        Item.objects.create(name='ItemTest', is_sold=False)
        User.objects.create_user('testuser', 'testuser@example.com', 'testpassword')

    def test_index_view(self):
        # Testa la vista index
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertEqual(len(response.context['items']), 1)
        self.assertEqual(len(response.context['genres']), 1)

    def test_contact_view(self):
        # Testa la vista contact
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')

    def test_signup_view_GET(self):
        # Testa la vista signup con metodo GET
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/signup.html')
        self.assertIsInstance(response.context['form'], SignupForm)

    def test_signup_view_POST_valid(self):
        # Testa la vista signup con metodo POST e dati validi
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_signup_view_POST_invalid(self):
        # Testa la vista signup con metodo POST e dati non validi
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/signup.html')
        self.assertFalse(response.context['form'].is_valid())

    def test_signout_view(self):
        # Testa la vista signout
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.signout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:index'))
