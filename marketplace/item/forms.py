from django import forms

from .models import Item

#INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('genre', 'title', 'author', 'description', 'format', 'language', 'number_of_pages',
                  'cover_color', 'price', 'image')
        widgets = {
            'genre': forms.Select(attrs={
                'class': 'w-half py-4 px-6 rounded-xl border'   # basta poco spazio
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'author': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'  # lascio più spazio
            }),
            'format': forms.Select(attrs={
                'class': 'w-half py-4 px-6 rounded-xl border'  # basta poco spazio
            }),
            'language': forms.Select(attrs={
                'class': 'w-half py-4 px-6 rounded-xl border'
            }),
            'number_of_pages': forms.TextInput(attrs={
                'class': 'w-half py-4 px-6 rounded-xl border'
            }),
            'cover_color': forms.Select(attrs={
                'class': 'w-half py-4 px-6 rounded-xl border'
            }),
            'price': forms.TextInput(attrs={
                'class': 'w-half py-4 px-6 rounded-xl border'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-half py-4 px-6 rounded-xl border'
            })
    }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('genre', 'title', 'author', 'description', 'format', 'language', 'number_of_pages',
                  'cover_color', 'price', 'image')
        widgets = {
            'genre': forms.Select(attrs={
                'class': 'w-half py-2 px-6 rounded-xl border'  # basta poco spazio
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-1/2 py-2 px-6 rounded-xl border'
            }),
            'author': forms.TextInput(attrs={
                'class': 'w-1/2 py-2 px-6 rounded-xl border'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-1/2 py-2 px-6 rounded-xl border flex items-start'  # lascio più spazio
            }),
            'format': forms.Select(attrs={
                'class': 'w-half py-2 px-6 rounded-xl border'  # basta poco spazio
            }),
            'language': forms.Select(attrs={
                'class': 'w-half py-2 px-6 rounded-xl border'
            }),
            'number_of_pages': forms.TextInput(attrs={
                'class': 'w-half py-2 px-6 rounded-xl border'
            }),
            'cover_color': forms.Select(attrs={
                'class': 'w-half py-2 px-6 rounded-xl border'
            }),
            'price': forms.TextInput(attrs={
                'class': 'w-half py-2 px-6 rounded-xl border'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-half py-2 px-6 rounded-xl border'
            })
        }