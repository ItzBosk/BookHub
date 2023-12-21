from django.contrib.auth.models import User
from django.db import models

# generi letterari
class Genre(models.Model):
    name = models.CharField(max_length=255)

    # fix nome
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Genres'

    # nomi generi (override string representation)
    def __str__(self):
        return self.name

# formato del libro
class Format(models.Model):
    name = models.CharField(max_length=255)

    # fix nome
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Formats'

    def __str__(self):
        return self.name

# colori copertine
class CoverColor(models.Model):
    name = models.CharField(max_length=255)

    # fix nome
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Cover colors'

    def __str__(self):
        return self.name

# lingua
class Language(models.Model):
    name = models.CharField(max_length=255)

    # fix nome
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.name

class Item(models.Model):
    genre = models.ForeignKey(Genre, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # può anche non esserci
    format = models.ForeignKey(Format, related_name='items', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, related_name='items', on_delete=models.CASCADE,)
    number_of_pages = models.FloatField(default=0.0)
    cover_color = models.ForeignKey(CoverColor, related_name='items', on_delete=models.CASCADE)
    price = models.FloatField()
    image = models.ImageField(upload_to="item_images", blank=True,
                              null=True)  # specifica posizione image, se non esiste django crea la cartella
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items',
                                   on_delete=models.CASCADE)  # link tra due db (users e items)
    created_at = models.DateTimeField(auto_now_add=True)  # django salva in automatico la data alla creazione

    # nomi prodotti (override string representation)
    def __str__(self):
        return self.title
