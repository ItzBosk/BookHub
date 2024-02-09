from django import forms
from .models import UserQuery

class NewQueryForm(forms.ModelForm):
    min_price = forms.FloatField(required=False, widget=forms.NumberInput(attrs={
        'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]',
        'step': 'any',  # permette valori decinali
    }))
    max_price = forms.FloatField(required=False, widget=forms.NumberInput(attrs={
        'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]',
        'step': 'any',
    }))

    class Meta:
        model = UserQuery
        fields = ['name', 'genre', 'title', 'author', 'description', 'format', 'language', 'number_of_pages', 'cover_color',
                  'min_price', 'max_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-1/2 py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'}),
            'genre': forms.Select(attrs={'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'}),
            'title': forms.TextInput(attrs={'class': 'w-1/2 py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'}),
            'author': forms.TextInput(attrs={'class': 'w-1/2 py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'}),
            'description': forms.Textarea(attrs={'class': 'w-1/2 py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'}),
            'format': forms.Select(attrs={'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'}),
            'language': forms.Select(attrs={'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'}),
            'number_of_pages': forms.NumberInput(attrs={'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'}),
            'cover_color': forms.Select(attrs={'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'}),
            'min_price': forms.NumberInput(attrs={'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'}),
            'max_price': forms.NumberInput(attrs={'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'}),
        }

class EditQueryForm(forms.ModelForm):
    min_price = forms.FloatField(required=False, widget=forms.NumberInput(attrs={
        'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]',
        'step': 'any',  # permette valori decimali
    }))
    max_price = forms.FloatField(required=False, widget=forms.NumberInput(attrs={
        'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]',
        'step': 'any',
    }))

    class Meta:
        model = UserQuery
        fields = ['name', 'genre', 'title', 'author', 'description', 'format', 'language', 'number_of_pages', 'cover_color',
                  'min_price', 'max_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-1/2 py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'}),
            'genre': forms.Select(attrs={'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'}),
            'title': forms.TextInput(attrs={'class': 'w-1/2 py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'}),
            'author': forms.TextInput(attrs={'class': 'w-1/2 py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'}),
            'description': forms.Textarea(attrs={'class': 'w-1/2 py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'}),
            'format': forms.Select(attrs={'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'}),
            'language': forms.Select(attrs={'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'}),
            'number_of_pages': forms.NumberInput(attrs={'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'}),
            'cover_color': forms.Select(attrs={'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'}),
            'min_price': forms.NumberInput(attrs={'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'}),
            'max_price': forms.NumberInput(attrs={'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'}),
        }