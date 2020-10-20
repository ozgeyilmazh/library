from django.forms import ModelForm, TextInput
from django import forms
from .models import BookNotes

class BookNoteForm(ModelForm):
    class Meta:
        model = BookNotes
        fields = ['notes',]
        widgets = {
            'notes': TextInput(attrs={
                'class': 'input',
            }),

        }

class SearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length = 100)