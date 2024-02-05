from django.test import TestCase, Client
from django.contrib.auth.models import User
from config.models import UserQuery
from item.models import Item, Genre, Format, Language, CoverColor
from config.tasks import run_user_queries
from django.core.files.images import ImageFile
from django.urls import reverse
from config.models import UserQuery
from .forms import NewQueryForm, EditQueryForm


"""Test background thread"""
class RunUserQueriesTestCase(TestCase):

    def setUp(self):

        # crea un utente per associare il libro di test
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

        # crea un libro di test
        self.genre = Genre.objects.create(name='Fantasy')
        self.format = Format.objects.create(name='Print Book')
        self.language = Language.objects.create(name='English')
        self.cover_color = CoverColor.objects.create(name='Blue')

        self.item = Item.objects.create(
            genre=self.genre,
            title="Test Book",
            author="Test Author",
            description="A test description",
            format=self.format,
            language=self.language,
            number_of_pages=100,
            cover_color=self.cover_color,
            price=20.00,
            image = ImageFile(open('media/item_images/test.jpg', 'rb'), name='test.jpg'),
            is_sold=False,
            created_by=self.user
        )

    def tearDown(self):
        # Elimina le immagini dopo il test
        self.item.image.delete(save=False)
        super().tearDown()

    """Verifica l'esecuzione del task senza UserQuery"""
    def test_run_with_no_user_queries(self):
        # non devono esserci UserQuery già presenti
        self.assertEqual(UserQuery.objects.count(), 0)

        # esegui il task e verifica che non ci siano errori
        try:
            run_user_queries()
            no_errors = True
        except Exception:
            no_errors = False
        self.assertTrue(no_errors)

    """Test che verifica la corretta identificazione dei nuovi risultati"""
    def test_identifies_new_results_correctly(self):
        # nuova query utente che corrisponde al libro di test
        query = UserQuery.objects.create(user=self.user, title="Test Book", genre=self.genre)

        run_user_queries()  # esecuzione del task

        # check che il task abbia identificato correttamente i nuovi risultati
        self.assertTrue(query.results.filter(id=self.item.id).exists())

    """Test che verifica che gli Item già presenti non vengano aggiunti nuovamente"""
    def test_does_not_add_existing_results(self):
        # nuova query utente che corrisponde al libro di test
        query = UserQuery.objects.create(user=self.user, title="Test Book", genre=self.genre)

        # aggiunta del libro di test ai risultati della per simulare un risultato preesistente
        query.results.add(self.item)

        run_user_queries()  # 1° esecuzione

        initial_count = query.results.count()       # conteggio risultati

        run_user_queries()  # 2° esecuzione

        self.assertEqual(query.results.count(), initial_count)

    """Test che verifica il corretto funzionamento dei filtri per campi specifici"""
    def test_filters_by_specific_fields(self):
        # nuova query utente
        query = UserQuery.objects.create(user=self.user, genre=self.genre)

        # nuovo libro che corrisponde ai criteri della query (libro di test)
        matching_item = self.item

        # nuovo libro che non soddisfa la query
        non_matching_genre = Genre.objects.create(name="Sci-Fi")
        non_matching_item = Item.objects.create(
            title="Another Book",
            author="Different Author",
            genre=non_matching_genre,
            format=self.format,
            language=self.language,
            number_of_pages=200,
            cover_color=self.cover_color,
            price=25.00,
            is_sold=False,
            created_by=self.user
        )

        run_user_queries()

        # check che la query includa matching_item nei suoi risultati
        self.assertTrue(query.results.filter(id=matching_item.id).exists())

        # check che la query non includa non_matching_item nei suoi risultati
        self.assertFalse(query.results.filter(id=non_matching_item.id).exists())

    """Test che verifica il corretto funzionamento del filtro di range di prezzo"""
    def test_price_range_filtering(self):
        # creazione di una query con limiti di prezzo
        query = UserQuery.objects.create(user=self.user, min_price=10.00, max_price=20.00)

        # creazione di un libro con il prezzo che rientra nel range specificato
        in_range_item = Item.objects.create(
            title="In Range Book",
            price=15.00,
            genre=self.genre,
            format=self.format,
            language=self.language,
            number_of_pages=100,
            cover_color=self.cover_color,
            is_sold=False,
            created_by=self.user
        )

        # creazione di un libro con il prezzo che non rientra nel range specificato
        out_of_range_item = Item.objects.create(
            title="Out of Range Book",
            price=25.00,
            genre=self.genre,
            format=self.format,
            language=self.language,
            number_of_pages=100,
            cover_color=self.cover_color,
            is_sold=False,
            created_by=self.user
        )

        # esecuzione del task per filtrare i risultati basandosi sui criteri di prezzo della query
        run_user_queries()

        # check che in_range_item sia nei risultati, e che invece out_of_range_item non sia nei risultati
        self.assertTrue(query.results.filter(id=in_range_item.id).exists(),
                        "L'item nel range di prezzo dovrebbe essere incluso nei risultati.")
        self.assertFalse(query.results.filter(id=out_of_range_item.id).exists(),
                         "L'item fuori dal range di prezzo non dovrebbe essere incluso nei risultati.")

    """Test che verifica il corretto funzionamento del filtraggio basato su più campi"""
    def test_filters_by_multiple_fields(self):
        # creazione di una query che filtra per genere, prezzo e lingua
        query = UserQuery.objects.create(
            user=self.user,
            genre=self.genre,
            min_price=10.00,
            max_price=50.00,
            language=self.language
        )

        # creazione di due libri, uno che corrisponde a tutti i criteri della query, e uno che non corrisponde
        matching_item = Item.objects.create(
            title="Matching Book",
            price=15.00,
            genre=self.genre,
            format=self.format,
            language=self.language,
            number_of_pages=100,
            cover_color=self.cover_color,
            is_sold=False,
            created_by=self.user
        )
        non_matching_item = Item.objects.create(
            title="Matching Book",
            price=60.00,  # prezzo fuori dal range specificato
            genre=self.genre,
            format=self.format,
            language=self.language,
            number_of_pages=100,
            cover_color=self.cover_color,
            is_sold=False,
            created_by=self.user
        )

        # esecuzione del task per verificare che solo matching_item venga aggiunto ai risultati
        run_user_queries()

        # check che matching_item sia nei risultati, e che invece non_matching_item non sia nei risultati
        self.assertTrue(query.results.filter(id=matching_item.id).exists())
        self.assertFalse(query.results.filter(id=non_matching_item.id).exists())


"""Test past_researches view"""
class PastResearchesViewTest(TestCase):

    def setUp(self):
        # creazione di un utente di test e login
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')

        # creazione di una ricerca passata per l'utente
        self.genre = Genre.objects.create(name='Fantasy')
        self.format = Format.objects.create(name='Hardcover')
        self.language = Language.objects.create(name='English')
        self.cover_color = CoverColor.objects.create(name='Blue')
        self.user_query = UserQuery.objects.create(
            user=self.user,
            name="Test Query",
            genre=self.genre,
            title="Test Book",
            author="Test Author",
            description="Test Description",
            format=self.format,
            language=self.language,
            number_of_pages=100,
            cover_color=self.cover_color,
            min_price=10.00,
            max_price=50.00
        )
        self.url = reverse('past_researches')

    """Accesso alla view solo per utenti autenticati"""
    def test_access_by_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('past_queries' in response.context)
        self.assertIn(self.user_query, response.context['past_queries'])

    """Reindirizzamento utenti non autenticati"""
    def test_redirect_unauthenticated_user(self):
        self.client.logout()    # logout per testare il reindirizzamento
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{reverse("core:login")}?next={self.url}')


"""Test delete view"""
class DeleteViewTest(TestCase):

    def setUp(self):
        # Creazione dell'utente e login
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')

        # Creazione di una ricerca passata per l'utente
        self.genre = Genre.objects.create(name='Fantasy')
        self.format = Format.objects.create(name='Hardcover')
        self.language = Language.objects.create(name='English')
        self.cover_color = CoverColor.objects.create(name='Blue')
        self.query = UserQuery.objects.create(
            user=self.user,
            name="Fantasy Query",
            genre=self.genre,
            format=self.format,
            language=self.language,
            cover_color=self.cover_color,
        )
        self.url = reverse('delete', args=[self.query.pk])

    """Verifica che la ricerca possa essere eliminata dall'utente che l'ha creata"""
    def test_delete_by_owner(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('past_researches'))
        with self.assertRaises(UserQuery.DoesNotExist):
            UserQuery.objects.get(pk=self.query.pk)

    """Verifica che gli utenti non autenticati vengano reindirizzati alla pagina di login"""
    def test_redirect_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{reverse("core:login")}?next={self.url}')


"""Test new view"""
class NewQueryViewTest(TestCase):
    def setUp(self):
        # crea un utente di test
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

        # crea gli oggetti necessari per una nuova ricerca utente
        self.genre = Genre.objects.create(name='Fantasy')
        self.format = Format.objects.create(name='Print Book')
        self.language = Language.objects.create(name='English')
        self.cover_color = CoverColor.objects.create(name='Blue')

        self.url = reverse('new')

    """Verifica che la form per la creazione di nuove ricerche sia disponibile solo per utenti autenticati"""
    def test_access_by_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], NewQueryForm)

    """Verifica che utenti non autenticati vengano reindirizazti alla pagine di login"""
    def test_redirect_unauthenticated_user(self):
        response = self.client.get(self.url)
        login_url = reverse('core:login')
        self.assertRedirects(response, f'{reverse("core:login")}?next={self.url}')

    """Verifica che l'invio della form con dei dati validi crei una nuova ricerca per l'utente"""
    def test_form_submission_with_valid_data(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'name': 'My query',
            'genre': self.genre.id,
            'title': 'Epic Adventure',
            'author': 'Test author',
            'description': 'Test description',
            'format': self.format.id,
            'language': self.language.id,
            'number_of_pages': 350,
            'cover_color': self.cover_color.id,
            'min_price': 10.0,
            'max_price': 50.0,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(UserQuery.objects.count(), 1)
        self.assertEqual(UserQuery.objects.first().user, self.user)
        # verifica il reindirizzamento alla pagina con i risultati della ricerca
        self.assertRedirects(response, reverse('results', args=[UserQuery.objects.first().id]))
    
    """Verifica che l'invio della form con dati non validi non crei una nuova ricerca utente e mostri gli errori di validazione"""
    def test_form_submission_with_invalid_data(self):
        self.client.login(username='testuser', password='testpassword')
        invalid_data = {
            # errori intenzionali per verificare che la form li segnali
            'name': 'A' * 256,  # troppo lungo, oltre il limite consentito
            'author': 'Test author',
        }   
        response = self.client.post(self.url, invalid_data)

        # check che la nuova ricerca (errata) non sia stata creata
        self.assertEqual(UserQuery.objects.count(), 0)
        
        # recuperare la form dal contesto della risposta
        form = response.context.get('form')
        self.assertIsNotNone(form)      # check che la form sia nel contesto della risposta
        self.assertTrue(form.is_bound)  # verifica che la form sia stata riempita con dei dati
        self.assertTrue(form.errors)    # la form dovrebbe contenere degli errori

        # verifica la presenza di errori nel contesto della risposta, in questo caso di quello specifico
        if 'name' in form.errors:
            self.assertIn('Ensure this value has at most 255 characters (it has 256).', form.errors['name'])
        
        # indica che la form è stata renderizzata di nuovo e mostra gli errori nei dati inseriti
        self.assertEqual(response.status_code, 200)


"""Test edit view"""
class EditQueryViewTest(TestCase):

    def setUp(self):
        # Creazione dell'utente di test e login
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Creazione di una ricerca utente di test associata all'utente
        self.genre = Genre.objects.create(name='Fantasy')
        self.query = UserQuery.objects.create(user=self.user, name="My Query", genre=self.genre)

        # URL per la form di modifica
        self.url = reverse('edit', args=[self.query.id])

    """Verifica che l'utente autorizzato possa accedere alla form di modifica"""
    def test_edit_form_by_authorized_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], EditQueryForm)

    """Verifica che i dati validi inviati attraverso la form di modifica aggiornino correttamente la ricerca esistente"""
    def test_edit_query_with_valid_data(self):
        updated_data = {
            'name': 'Updated Query',
            'genre': self.genre.id,
        }
        response = self.client.post(self.url, updated_data)
        self.query.refresh_from_db()    # aggionra la ricerca dopo il salvataggio delle modifiche
        self.assertEqual(response.status_code, 302)  # check reindirizzamento
        self.assertEqual(self.query.name, 'Updated Query')


"""Test results view"""
class ResultsQueryViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # crea un utente per associare il libro di test
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        # crea un libro di test
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
            image = ImageFile(open('media/item_images/test.jpg', 'rb'), name='test.jpg'),
            is_sold=False,
            created_by=self.user
        )

        # crea una query di test
        self.query = UserQuery.objects.create(
        user=self.user,
        name="Test query",
        genre=self.genre,
        title="test book",
        author="test author",
        description="Test description",
        format=self.format,
        language=self.language,
        number_of_pages=100,
        cover_color=self.cover_color,
        min_price=10.00,
        max_price=50.00,
    )

    def tearDown(self):
        # Elimina le immagini dopo il test
        self.item.image.delete(save=False)
        super().tearDown()
    
    """Visualizzazione dei risultati: utente autenticato e autorizzato"""
    def test_results_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('results', args=[self.query.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.title)

    """Reindirizzamento degli utenti non autenticati alla pagina di login"""
    def test_results_view_redirects_unauthenticated_user(self):
        url = reverse('results', args=[self.query.id])
        response = self.client.get(url, follow=True)
        login_url = reverse('core:login')
        expected_redirect_url = f"{login_url}?next={url}"
        self.assertRedirects(response, expected_redirect_url)

    """Corretta visualizzazione dei risultati della query per l'utente"""
    def test_correct_display_of_query_results(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('results', args=[self.query.id]))
        # Assicurati che l'oggetto Item sia presente nei risultati
        self.assertIn(self.item, response.context['results'])