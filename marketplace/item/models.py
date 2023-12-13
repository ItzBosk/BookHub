from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    # fix nome app
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    # nomi categorie (override string representation)
    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # può anche non esserci
    price = models.FloatField()
    image = models.ImageField(upload_to="item_images", blank=True,
                              null=True)  # specifica posizione image, se non esiste django crea la cartella
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items',
                                   on_delete=models.CASCADE)  # link tra due db (users e items)
    created_at = models.DateTimeField(auto_now_add=True)  # django salva in automatico la data alla creazione

    # nomi prodotti (override string representation)
    def __str__(self):
        return self.name
