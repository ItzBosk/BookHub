from django import forms
from django.db import models
from item.models import Item
from .models import UserQuery

class QueryForm(forms.Form):
    min_price = forms.FloatField(required=False)
    max_price = forms.FloatField(required=False)

    class Meta:
        model = UserQuery
        fields = ['genre', 'title', 'author', 'description', 'format', 'language', 'number_of_pages', 'cover_color',
                  'min_price', 'max_price']
        widgets = {
            'genre': forms.Select(attrs={'class': 'w-half py-4 px-6 rounded-xl border'}),
            'title': forms.TextInput(attrs={'class': 'w-full py-4 px-6 rounded-xl border'}),
            'author': forms.TextInput(attrs={'class': 'w-full py-4 px-6 rounded-xl border'}),
            'description': forms.Textarea(attrs={'class': 'w-full py-4 px-6 rounded-xl border'}),
            'format': forms.Select(attrs={'class': 'w-half py-4 px-6 rounded-xl border'}),
            'language': forms.Select(attrs={'class': 'w-half py-4 px-6 rounded-xl border'}),
            'number_of_pages': forms.NumberInput(attrs={'class': 'w-half py-4 px-6 rounded-xl border'}),
            'cover_color': forms.Select(attrs={'class': 'w-half py-4 px-6 rounded-xl border'}),
            'min_price': forms.NumberInput(attrs={'class': 'w-half py-4 px-6 rounded-xl border'}),
            'max_price': forms.NumberInput(attrs={'class': 'w-half py-4 px-6 rounded-xl border'}),
        }