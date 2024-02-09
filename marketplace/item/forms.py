from django import forms
from .models import Item

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('genre', 'title', 'author', 'description', 'format', 'language', 'number_of_pages',
                  'cover_color', 'price', 'image')
        widgets = {
            'genre': forms.Select(attrs={
                'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'   # basta poco spazio
            }), 
            'title': forms.TextInput(attrs={
                'class': 'w-1/2 py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
            }),
            'author': forms.TextInput(attrs={
                'class': 'w-1/2 py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-1/2 py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'  # lascio più spazio
            }),
            'format': forms.Select(attrs={
                'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'  # basta poco spazio
            }),
            'language': forms.Select(attrs={
                'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'
            }),
            'number_of_pages': forms.TextInput(attrs={
                'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
            }),
            'cover_color': forms.Select(attrs={
                'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'
            }),
            'price': forms.TextInput(attrs={
                'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
            })
    }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('genre', 'title', 'author', 'description', 'format', 'language', 'number_of_pages',
                  'cover_color', 'price', 'image')
        widgets = {
            'genre': forms.Select(attrs={
                'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'  # basta poco spazio
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-1/2 py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
            }),
            'author': forms.TextInput(attrs={
                'class': 'w-1/2 py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-1/2 py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
                # lascio più spazio
            }),
            'format': forms.Select(attrs={
                'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'  # basta poco spazio
            }),
            'language': forms.Select(attrs={
                'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'
            }),
            'number_of_pages': forms.TextInput(attrs={
                'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
            }),
            'cover_color': forms.Select(attrs={
                'class': 'w-half py-4 px-6 rounded-xl border bg-[#edf2f4]'
            }),
            'price': forms.TextInput(attrs={
                'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-half py-4 px-6 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-[#005662]'
            })
        }