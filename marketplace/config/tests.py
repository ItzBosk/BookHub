from django.test import TestCase
from django.contrib.auth.models import User
from config.models import UserQuery
from item.models import Item, Genre, Format, Language, CoverColor
from config.tasks import run_user_queries
from django.core.files.images import ImageFile


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