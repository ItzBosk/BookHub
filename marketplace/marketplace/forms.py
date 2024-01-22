from django import forms
from .models import UserQuery

class QueryForm(forms.ModelForm):
    min_price = forms.FloatField(required=False, widget=forms.NumberInput(attrs={
        'class': 'w-half py-4 px-6 rounded-xl border',
        'step': 'any',  # Allows decimal values
    }))
    max_price = forms.FloatField(required=False, widget=forms.NumberInput(attrs={
        'class': 'w-half py-4 px-6 rounded-xl border',
        'step': 'any',
    }))

    class Meta:
        model = UserQuery
        fields = ['name', 'genre', 'title', 'author', 'description', 'format', 'language', 'number_of_pages', 'cover_color',
                  'min_price', 'max_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full py-4 px-6 rounded-xl border'}),
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