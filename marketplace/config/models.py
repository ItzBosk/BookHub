from django.db import models
from django.contrib.auth.models import User
from item.models import Genre, Format, Language, CoverColor, Item

class UserQuery(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, related_name='user_queries', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    format = models.ForeignKey(Format, related_name='user_queries', on_delete=models.CASCADE, blank=True, null=True)
    language = models.ForeignKey(Language, related_name='user_queries', on_delete=models.CASCADE, blank=True, null=True)
    number_of_pages = models.FloatField(default=0.0, blank=True, null=True)
    cover_color = models.ForeignKey(CoverColor, related_name='user_queries', on_delete=models.CASCADE, blank=True,
                                    null=True)
    min_price = models.FloatField(blank=True, null=True)
    max_price = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    results = models.ManyToManyField(Item, blank=True)  # store query results

    class Meta:
        app_label = 'config'

    def __str__(self):
        return f"Research: {self.name} made by: {self.user.username}"