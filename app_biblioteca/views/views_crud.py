from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from app_biblioteca.models import Book, Reader, Lending, Language, Editorial, Genre
from app_biblioteca.forms import BookForm, ReaderForm, LendingForm, LanguageForm, EditorialForm, GenreForm, UsuarioEditarForm
from django.contrib.auth.models import User
from app_biblioteca.views.views_utils import is_admin
from app_biblioteca.models import Book, Reader, Lending, Language, Editorial, Genre
from django.contrib.auth.models import User

def handle_form(request, form_class, template_name, instance=None, redirect_url=None, context_name='form'):
    form = form_class(request.POST or None, instance=instance)
    
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)

        # Si es un préstamo, asignar el usuario actual si no tiene uno
        if isinstance(obj, Lending) and not obj.user:
            obj.user = request.user

        obj.save()
        return redirect(redirect_url)

    context = {
        context_name: form,
        'object': instance,
    }

    # Agrega el nombre específico de objeto según el tipo de instancia
    if isinstance(instance, Lending):
        context['lending'] = instance
    elif isinstance(instance, Book):
        context['book'] = instance
    elif isinstance(instance, Reader):
        context['reader'] = instance
    elif isinstance(instance, Language):
        context['language'] = instance
    elif isinstance(instance, Editorial):
        context['editorial'] = instance
    elif isinstance(instance, Genre):
        context['genre'] = instance
    elif isinstance(instance, User):
        context['usuario'] = instance

    return render(request, template_name, context)

@login_required
def createBook(request):
    return handle_form(request, BookForm, 'books/modals/createBook.html', redirect_url='books', context_name='book_form')

@login_required
def editBook(request, id):
    book = get_object_or_404(Book, id=id)
    return handle_form(request, BookForm, 'books/modals/editBook.html', instance=book, redirect_url='books', context_name='book_form')

@login_required
def createReader(request):
    return handle_form(request, ReaderForm, 'readers/modals/createReader.html', redirect_url='readers', context_name='reader_form')

@login_required
def editReader(request, id):
    reader = get_object_or_404(Reader, id=id)
    return handle_form(request, ReaderForm, 'readers/modals/editReader.html', instance=reader, redirect_url='readers', context_name='reader_form')

@login_required
def createLending(request):
    form = LendingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        lending = form.save(commit=False)
        lending.user = request.user
        lending.save()
        return redirect('main')
    return render(request, 'lendings/modals/createLending.html', {'lending_form': form})

@login_required
def editLending(request, id):
    lending = get_object_or_404(Lending, id=id)
    return handle_form(request, LendingForm, 'lendings/modals/editLending.html', instance=lending, redirect_url='main', context_name='lending_form')

@login_required
def createLanguage(request):
    if not is_admin(request.user):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Necesitas permisos de administrador'}, status=403)
        return redirect('languages')
    return handle_form(request, LanguageForm, 'languages/modals/createLanguage.html', redirect_url='languages', context_name='language_form')

@login_required
def editLanguage(request, id):
    if not is_admin(request.user):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Necesitas permisos de administrador'}, status=403)
        return redirect('languages')
    language = get_object_or_404(Language, id=id)
    return handle_form(request, LanguageForm, 'languages/modals/editLanguage.html', instance=language, redirect_url='languages', context_name='language_form')

@login_required
def createEditorial(request):
    if not is_admin(request.user):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Necesitas permisos de administrador'}, status=403)
        return redirect('editorials')
    return handle_form(request, EditorialForm, 'editorials/modals/createEditorial.html', redirect_url='editorials', context_name='editorial_form')

@login_required
def editEditorial(request, id):
    if not is_admin(request.user):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Necesitas permisos de administrador'}, status=403)
        return redirect('editorials')
    editorial = get_object_or_404(Editorial, id=id)
    return handle_form(request, EditorialForm, 'editorials/modals/editEditorial.html', instance=editorial, redirect_url='editorials', context_name='editorial_form')

@login_required
def createGenre(request):
    if not is_admin(request.user):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Necesitas permisos de administrador'}, status=403)
        return redirect('genres')
    return handle_form(request, GenreForm, 'genres/modals/createGenre.html', redirect_url='genres', context_name='genre_form')

@login_required
def editGenre(request, id):
    if not is_admin(request.user):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Necesitas permisos de administrador'}, status=403)
        return redirect('genres')
    genre = get_object_or_404(Genre, id=id)
    return handle_form(request, GenreForm, 'genres/modals/editGenre.html', instance=genre, redirect_url='genres', context_name='genre_form')

@login_required
def edit_user(request, id):
    usuario = get_object_or_404(User, id=id)
    is_self = (request.user.id == usuario.id)
    if request.method == 'POST':
        form = UsuarioEditarForm(request.POST, instance=usuario, is_self=is_self)
        if form.is_valid():
            form.save()
            nuevo_rol = form.cleaned_data.get('rol')
            if nuevo_rol:
                usuario.groups.clear()
                usuario.groups.add(nuevo_rol)
                if nuevo_rol.name == 'Admin':
                    usuario.is_staff = True
                    usuario.is_superuser = True
                elif nuevo_rol.name == 'Encargado':
                    usuario.is_staff = False
                    usuario.is_superuser = False
            usuario.save()
            return JsonResponse({'success': True, 'redirect_url': reverse('users')})
        return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = UsuarioEditarForm(instance=usuario, is_self=is_self)
        return render(request, 'users/modals/edit_user_modal.html', {
            'form': form,
            'usuario': usuario,
            'is_self': is_self
        })

@login_required(login_url='/app_biblioteca/login/')
def delete_object(request, model, object_id_name):
    if request.method == "POST":
        if not is_admin(request.user):
            return JsonResponse({"success": False, "error": "Necesitas permisos de administrador"})

        object_id = request.POST.get(object_id_name, None)
        if object_id:
            obj = get_object_or_404(model, id=object_id)

            if model == User:
                if not request.user.is_superuser:
                    return JsonResponse({"success": False, "error": "No tienes permiso para eliminar usuarios"})
                if obj.is_superuser:
                    return JsonResponse({"success": False, "error": "No se puede eliminar otro Administrador"})

            obj.is_active = False
            obj.save()
            return JsonResponse({"success": True})

        return JsonResponse({"success": False, "error": "No se proporcionó un ID válido"})

    return JsonResponse({"success": False, "error": "Método no permitido"})

@login_required(login_url='/app_biblioteca/login/')
def delete_lending(request):
    return delete_object(request, Lending, "lendingid")

@login_required(login_url='/app_biblioteca/login/')
def delete_reader(request):
    return delete_object(request, Reader, "readerid")

@login_required(login_url='/app_biblioteca/login/')
def delete_book(request):
    return delete_object(request, Book, "bookid")

@login_required(login_url='/app_biblioteca/login/')
def delete_editorial(request):
    return delete_object(request, Editorial, "editorialid")

@login_required(login_url='/app_biblioteca/login/')
def delete_genre(request):
    return delete_object(request, Genre, "genreid")

@login_required(login_url='/app_biblioteca/login/')
def delete_language(request):
    return delete_object(request, Language, "languageid")

@login_required(login_url='/app_biblioteca/login/')
def delete_user(request):
    return delete_object(request, User, "userid")