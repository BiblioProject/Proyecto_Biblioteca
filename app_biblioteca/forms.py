from django import forms
from .models import Book, Reader, Lending

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'pages', 'description', 'stock', 'available',
                    'editorial', 'language', 'genre']
        labels = {
            'title': 'Título',
            'author': 'Autor',
            'publication_year': 'Año',
            'pages': 'Páginas',
            'description': 'Descripción',
            'stock': 'Stock',
            'available': 'Disponibles',
            'editorial': 'Editorial',
            'language': 'Idioma',
            'genre': 'Género',
        }
        widgets = {
            'title': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el título del libro',
                    'id':'title'
                }
            ),
            'author': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el autor del libro',
                    'id':'author'
                }
            ),
            'publication_year': forms.NumberInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Año de publicación',
                    'id':'publication_year'
                }
            ),
            'pages': forms.NumberInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Número de páginas',
                    'id':'pages'
                }
            ),
            'description': forms.Textarea(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Breve descripción',
                    'id':'description'
                }
            ),
            'stock': forms.NumberInput(
                attrs={'class': 'form-control', 'id': 'id_stock', 'type': 'number'}
            ),
            'available': forms.NumberInput(
                attrs={'class': 'form-control', 'id': 'id_available', 'type': 'number'}
            ),
        }

class PinLoginForm(forms.Form):
    reader_id = forms.IntegerField(label="ID de lector")
    pin = forms.CharField(label="PIN", widget=forms.PasswordInput, max_length=6)
        
class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ['name', 'first_surname', 'second_surname', 'address', 'phone',]
        labels = {
            'name': 'Nombre',
            'first_surname': 'Primer Apellido',
            'second_surname': 'Segundo Apellido',
            'address': 'Dirección',
            'phone': 'Número',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nombre del lector',
                    'id':'name'
                }
            ),
            'first_surname': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Primer Apellido',
                    'id':'first_surname'
                }
            ),
            'second_surname': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Segundo Apellido',
                    'id':'second_surname'
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Dirección',
                    'id':'address'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Número de teléfono',
                    'id':'phone'
                }
            ),
        }

class LendingForm(forms.ModelForm):
    class Meta:
        model = Lending
        fields = ['reader', 'book', 'date', 'real_return_date']
        labels = {
            'reader': 'Lector',
            'book': 'Libro',
            'date': 'Fecha',
            'real_return_date':'Retorno Real',
        }
        widgets = {
            'date': forms.DateInput(
                attrs={'class': 'form-control', 'id': 'id_date', 'type': 'date'}
            ),
            'real_return_date': forms.DateInput(
                attrs={'class': 'form-control', 'id': 'id_real_return_date', 'type': 'date'}
            ),
        }