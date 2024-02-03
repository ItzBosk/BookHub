from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from item.models import Item, Genre, Format, Language, CoverColor
from django.core.files.images import ImageFile
from item.forms import EditItemForm, NewItemForm


"""Test detail view"""
class ItemDetailViewTest(TestCase):

    def setUp(self):
        # Creazione di un libro di test
        self.genre = Genre.objects.create(name='Fantasy')
        self.format = Format.objects.create(name='Audiobook')
        self.language = Language.objects.create(name='English')
        self.cover_color = CoverColor.objects.create(name='Blue')
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        image = ImageFile(open('media/item_images/test.jpg', 'rb'), name='test.jpg')

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

    def tearDown(self):
        # Check if the image file exists before attempting to delete
        if self.item.image and hasattr(self.item.image, 'path'):
            try:
                self.item.image.delete(save=False)
            except Exception as e:
                print(f"Error deleting test image: {e}")
        super().tearDown()

    """Verifica la corretta creazione del libro di test nel database"""
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

    """verifica la risposta HTTP 200 per un ID libro valido"""
    def test_response_status(self):
        response = self.client.get(reverse('item:detail', args=[self.item.id]))
        self.assertEqual(response.status_code, 200, "La vista non restituisce un codice di stato 200 per un ID di libro valido")

    """controlla che l'oggetto item nel contesto contenga le informazioni corrette"""
    def test_context_object(self):
        response = self.client.get(reverse('item:detail', args=[self.item.id]))
        self.assertEqual(response.context['item'].id, self.item.id, "L'oggetto 'item' nel contesto non ha l'ID atteso.")

    """verifica la redirezione per un ID libro non valido"""
    def test_template_used(self):
        response = self.client.get(reverse('item:detail', args=[self.item.id]))
        self.assertTemplateUsed(response, 'item/detail.html', "Non viene utilizzato il template 'item/detail.html' come atteso.")

    """controlla che venga utilizzato il template corretto"""
    def test_invalid_item(self):
        response = self.client.get(reverse('item:detail', args=[9999]))
        self.assertEqual(response.status_code, 404, "La vista non restituisce un codice di stato 404 per un ID di libro non valido.")


"""Test delete view"""
class ItemDeleteViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', email='other@example.com',
                                                   password='testpassword')

        self.genre = Genre.objects.create(name='Fantasy')
        self.format = Format.objects.create(name='Ebook')
        self.language = Language.objects.create(name='Italian')
        self.cover_color = CoverColor.objects.create(name='Green')
        image = ImageFile(open('media/item_images/test.jpg', 'rb'), name='test.jpg')

        self.item = Item.objects.create(
            genre=self.genre,
            format=self.format,
            language=self.language,
            cover_color=self.cover_color,
            title="Owned Item",
            author="Author Owner",
            price=20.0,
            created_by=self.user,
            image=image
        )

    def tearDown(self):
        # Elimina le immagini dopo il test
        self.item.image.delete(save=False)
        super().tearDown()

    """Verifica che l'utente che ha creato l'articolo possa eliminarlo"""
    def test_delete_item_by_owner(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('item:delete', args=[self.item.pk]))
        self.assertRedirects(response, reverse('dashboard:index'),
                             msg_prefix="L'utente proprietario non viene reindirizzato correttamente dopo l'eliminazione.")
        with self.assertRaises(Item.DoesNotExist):
            Item.objects.get(pk=self.item.pk)

    """Verifica che un utente che non ha creato l'articolo non possa eliminarlo"""
    def test_delete_attempt_by_non_owner(self):
        self.client.login(username='otheruser', password='testpassword')
        response = self.client.post(reverse('item:delete', args=[self.item.pk]))
        self.assertEqual(response.status_code, 404,
                         "Un utente non proprietario riesce ad accedere alla vista di eliminazione dell'articolo.")

    """Verifica che gli utenti non autenticati vengano reindirizzati alla pagina di login"""
    def test_delete_unauthenticated_access(self):
        response = self.client.get(reverse('item:delete', args=[self.item.pk]))
        login_url = reverse('core:login')
        expected_url = f'{login_url}?next={reverse("item:delete", args=[self.item.pk])}'
        self.assertRedirects(response, expected_url,
                             msg_prefix="Gli utenti non autenticati non vengono reindirizzati correttamente alla pagina di login.")


"""Test edit view"""
class ItemEditViewTest(TestCase):

    def setUp(self):
        # setup di base per i test di modifica dei libri
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.other_user = User.objects.create_user(username='otheruser', email='other@example.com', password='password')

        self.genre = Genre.objects.create(name='Fantasy')
        self.format = Format.objects.create(name='Print Book')
        self.language = Language.objects.create(name='English')
        self.cover_color = CoverColor.objects.create(name='Red')

        self.item = Item.objects.create(
            title="original iitle",
            author="original author",
            description="original description",
            price=10.0,
            genre=self.genre,
            format=self.format,
            language=self.language,
            cover_color=self.cover_color,
            created_by=self.user,
        )

    """Accesso alla pagina di modifica da parte del proprietario del libro"""
    def test_edit_page_access_by_owner(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('item:edit', args=[self.item.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], EditItemForm)

    """Tentativo di modifica da parte di un utente non proprietario del libro"""
    def test_edit_attempt_by_non_owner(self):
        self.client.login(username='otheruser', password='password')
        response = self.client.get(reverse('item:edit', args=[self.item.pk]))
        self.assertNotEqual(response.status_code, 200)

    """Modifica del libro completata con successo"""
    def test_successful_edit(self):
        self.client.login(username='testuser', password='password')
        data = {
            'title': "updated title",
            'author': "updated author",
            'description': "updated description",
            'price': 15.0,
            'genre': self.genre.id,
            'format': self.format.id,
            'language': self.language.id,
            'cover_color': self.cover_color.id,
            'number_of_pages': 350,
        }
        response = self.client.post(reverse('item:edit', args=[self.item.pk]), data)

        if response.status_code != 302:
            print("Form errors:", response.context['form'].errors)

        self.assertRedirects(response, reverse('item:detail', args=[self.item.pk]))

        updated_item = Item.objects.get(pk=self.item.pk)
        self.assertEqual(updated_item.title, "updated title")


"""Test new view"""
class ItemNewViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.url = reverse('item:new')

        self.genre = Genre.objects.create(name='Fantasy')
        self.format = Format.objects.create(name='Print Book')
        self.language = Language.objects.create(name='English')
        self.cover_color = CoverColor.objects.create(name='Red')

    """Accesso alla pagina di creazione nuovo libro da parte di un utente autenticato"""
    def test_new_page_access_by_authenticated_user(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], NewItemForm)

    """Tentativo di accesso alla pagina di creazione da parte di un utente non autenticato"""
    def test_new_page_access_by_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{reverse("core:login")}?next={self.url}')

    """Creazione di un nuovo libro con dati validi"""
    def test_new_book_creation_with_valid_data(self):
        self.client.login(username='testuser', password='password')
        data = {
            'title': "New Book",
            'author': "Author Name",
            'description': "Book Description",
            'price': 20.0,
            'genre': self.genre.id,
            'format': self.format.id,
            'language': self.language.id,
            'cover_color': self.cover_color.id,
            'number_of_pages': 100,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertRedirects(response, reverse('item:detail', args=[new_item.pk]))

    """Creazione di un nuovo libro con dati non validi"""
    def test_new_book_creation_with_invalid_data(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.url, {})  # Dati vuoti per testare la validazione del form
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)


"""Test items view"""
class ItemListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.genre_fantasy = Genre.objects.create(name='Fantasy')
        self.genre_scifi = Genre.objects.create(name='Sci-Fi')
        self.language = Language.objects.create(name='English')
        self.format = Format.objects.create(name='Ebook')
        self.cover_color = CoverColor.objects.create(name='Blue')
        image = ImageFile(open('media/item_images/test.jpg', 'rb'), name='test.jpg')

        self.item1 = Item.objects.create(
            title="Fantasy Book",
            author="Test Author",
            description="Test Description",
            genre=self.genre_fantasy,
            language=self.language,
            format=self.format,
            cover_color=self.cover_color,
            is_sold=False,
            number_of_pages=300,
            price=10.0,
            created_by=self.user,
            image=image
        )

        self.item2 = Item.objects.create(
            title="Sci-Fi Book",
            author="Test Author",
            description="Test Description",
            genre=self.genre_scifi,
            language=self.language,
            format=self.format,
            cover_color=self.cover_color,
            is_sold=False,
            number_of_pages=300,
            price=10.0,
            created_by=self.user,
            image=image
        )

    def tearDown(self):
        # pulizia delle immagini caricate dopo ogni test
        if self.item1.image:
            self.item1.image.delete(save=False)
        if self.item2.image:
            self.item2.image.delete(save=False)
        super().tearDown()

    """La vista degli articoli deve mostrare tutti gli articoli disponibili quando non vengono applicati filtri"""
    def test_view_all_items_without_filters(self):
        response = self.client.get(reverse('item:items'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.item1, response.context['items'])
        self.assertIn(self.item2, response.context['items'])

    """Solo gli articoli del genere specificato siano mostrati quando viene applicato un filtro per genere"""
    def test_filter_items_by_genre(self):
        response = self.client.get(reverse('item:items') + '?genre=' + str(self.genre_fantasy.id))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.item1, response.context['items'])
        self.assertNotIn(self.item2, response.context['items'])

    """Check che la ricerca funzioni correttamente, mostrando solo gli articoli che corrispondono alla parola chiave"""
    def test_search_items_by_keyword(self):
        response = self.client.get(reverse('item:items') + '?query=Fantasy')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.item1, response.context['items'])
        self.assertNotIn(self.item2, response.context['items'])

