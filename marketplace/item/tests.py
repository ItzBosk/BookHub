from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import User
from item.models import Item, Genre, Format, Language, CoverColor

################################      test detail view     ################################

class ItemDetailViewTest(TestCase):

    # Creazione di un oggetto Item e oggetti correlati per il test
    def setUp(self):
        self.genre = Genre.objects.create(name='Fantasy')
        self.format = Format.objects.create(name='Audiobook')
        self.language = Language.objects.create(name='English')
        self.cover_color = CoverColor.objects.create(name='Blue')
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')

        image_path = 'media/item_images/test.jpg'
        image = SimpleUploadedFile(name='test.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')

        self.item = Item.objects.create(
            genre=self.genre,
            format=self.format,
            language=self.language,
            cover_color=self.cover_color,
            title="Test Book",
            author="Test Author",
            description="Test Description",
            number_of_pages=300,
            price=10.0,
            created_by=self.user,
            image = image
        )
        self.client = Client()

    # Verifica la creazione corretta di un nuovo libro nel database
    def test_new_item_creation(self):
        self.assertEqual(self.item.genre, self.genre)
        self.assertEqual(self.item.format, self.format)
        self.assertEqual(self.item.language, self.language)
        self.assertEqual(self.item.cover_color, self.cover_color)
        self.assertEqual(self.item.title, "Test Book")
        self.assertEqual(self.item.author, "Test Author")
        self.assertEqual(self.item.description, "Test Description")
        self.assertEqual(self.item.number_of_pages, 300)
        self.assertEqual(self.item.price, 10.0)
        self.assertEqual(self.item.created_by, self.user)

    # verifica la risposta HTTP 200 per un ID libro valido
    def test_response_status(self):
        response = self.client.get(reverse('item:detail', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)

    # controlla che l'oggetto item nel contesto contenga le informazioni corrette
    def test_context_object(self):
        response = self.client.get(reverse('item:detail', args=[self.item.id]))
        self.assertEqual(response.context['item'].id, self.item.id)

    # verifica la redirezione per un ID libro non valido
    def test_template_used(self):
        response = self.client.get(reverse('item:detail', args=[self.item.id]))
        self.assertTemplateUsed(response, 'item/detail.html')

    # controlla che venga utilizzato il template corretto
    def test_invalid_item(self):
        response = self.client.get(reverse('item:detail', args=[9999]))
        self.assertEqual(response.status_code, 404)
