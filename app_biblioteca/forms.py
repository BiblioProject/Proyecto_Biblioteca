from django import forms
from .models import Book, Reader, Lending, Language, Genre, Editorial
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UsuarioEditarForm(forms.ModelForm):
    rol = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=["Admin", "Encargado"]),
        required=False,
        empty_label="Selecciona un rol"
    )

    def __init__(self, *args, **kwargs):
        self.is_self = kwargs.pop('is_self', False)
        super(UsuarioEditarForm, self).__init__(*args, **kwargs)

        if not self.is_self:
            # Si no se está editando a sí mismo, deshabilitar todos los campos excepto el rol
            for field in self.fields:
                if field != 'rol':
                    self.fields[field].disabled = True
        else:
            # Si se está editando a sí mismo, el campo de rol también debe ser editable
            self.fields['rol'].required = False

        # Establece el valor inicial del rol actual
        if self.instance and self.instance.groups.exists():
            self.fields['rol'].initial = self.instance.groups.first()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'rol']
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'rol': 'Rol',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'pages', 'description', 'available',
                    'editorial', 'language', 'genre', 'stock']
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
                    'placeholder':'Año de edición',
                    'id':'id_publication_year',
                    'type': 'number'
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
        fields = ['reader', 'book', 'date', 'estimated_return_date', 'real_return_date']
        exclude = ['user']
        labels = {
            'reader': 'Lector',
            'book': 'Libro',
            'date': 'Fecha',
            'estimated_return_date':'Retorno estimado',
            'real_return_date':'Retorno Real',
        }
        widgets = {
            'date': forms.DateInput(
                attrs={'class': 'form-control', 'id': 'id_date', 'type': 'date', 'readonly':'readonly'}
            ),
            'estimated_return_date': forms.DateInput(
                attrs={'class': 'form-control', 'id':'id_estimated_return_date', 'type': 'date', 'readonly':'readonly'}
            ),
            'real_return_date': forms.DateInput(
                attrs={'class': 'form-control', 'id': 'id_real_return_date', 'type': 'date'}
            ),
        }
    #Muestra solo los lectores y libros activos en LendingForm
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reader'].queryset = Reader.objects.filter(is_active=True)
        self.fields['book'].queryset = Book.objects.filter(is_active=True)

        # Si es un préstamo nuevo, establecer valores por defecto
        if not self.instance.pk:
            today = now().date()
            self.initial['date'] = today
            self.initial['estimated_return_date'] = today + timedelta(days=7)

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name']
        labels = {'name':'Idioma'}
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el Idioma',
                    'id':'name'
                }
            ),
        }

class EditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = ['name']
        labels = {'name':'Editorial'}
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese la Editorial',
                    'id':'name'
                }
            ),
        }

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        labels = {'name':'Género'}
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el género',
                    'id':'name'
                }
            ),
        }

