from django.contrib import admin

from .models import Genre, Item, Format, Language, CoverColor

admin.site.register(Genre)
admin.site.register(Item)
admin.site.register(Format)
admin.site.register(Language)
admin.site.register(CoverColor)