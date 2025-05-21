from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from .models import Lending, Book, Reader, Editorial, Genre, Language
from django.conf import settings
import glob,os, json
from django.http import JsonResponse

def login(request):
   args = {}
   return TemplateResponse(request, 'login.html', args)

def valida_user(request):
  if 'username' in request.POST and "password" in request.POST:
     username = request.POST.get('username')
     password = request.POST.get('password')
     user = auth.authenticate(request, username=username, password=password)
     if user is not None:
        auth.login(request, user)       
     else:
        messages.info(request, 'Credenciales incorrectas')
  return redirect('/app_biblioteca/')

# Función genérica para listar objetos con paginación: Puede filtrar por un campo específico si se proporciona `filter_field` y `filter_value`.
@login_required(login_url='/app_biblioteca/login/')
def list_objects(request, model, template, filter_field=None, filter_value=None, per_page=7):
    query_params = {"is_active": True}
    if filter_field and filter_value:
        query_params[filter_field] = filter_value
    
    queryset = model.objects.filter(**query_params)
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, template, {'page_obj': page_obj})

@login_required(login_url='/app_biblioteca/login/')
def books_view(request):
    return list_objects(request, Book, 'books.html', per_page=5)

@login_required(login_url='/app_biblioteca/login/')
def main(request):
    return list_objects(request, Lending, 'lendings.html')

@login_required(login_url='/app_biblioteca/login/')
def readers_view(request):
    return list_objects(request, Reader, 'readers.html')

@login_required(login_url='/app_biblioteca/login/')
def editorials_view(request):
    return list_objects(request, Editorial, 'editorials.html')

@login_required(login_url='/app_biblioteca/login/')
def genres_view(request):
    return list_objects(request, Genre, 'genres.html')

@login_required(login_url='/app_biblioteca/login/')
def languages_view(request):
    return list_objects(request, Language, 'languages.html')

# Función para listar préstamos según libro
@login_required(login_url='/app_biblioteca/login/')
def lendings_book(request, bookid):
    return list_objects(request, Lending, 'lendings.html', filter_field="book_id", filter_value=bookid)

# Función para listar préstamos según lector
@login_required(login_url='/app_biblioteca/login/')
def lendings_reader(request, readerid):
    return list_objects(request, Lending, 'lendings.html', filter_field="reader_id", filter_value=readerid)

# Función para listar libros según editorial
@login_required(login_url='/app_biblioteca/login/')
def books_editorial(request, editorialid):
    return list_objects(request, Book, 'books.html', filter_field="editorial_id", filter_value=editorialid)

# Función para listar libros según género
@login_required(login_url='/app_biblioteca/login/')
def books_genre(request, genreid):
    return list_objects(request, Book, 'books.html', filter_field="genre_id", filter_value=genreid)

# Función para listar libros según idioma
@login_required(login_url='/app_biblioteca/login/')
def books_language(request, languageid):
    return list_objects(request, Book, 'books.html', filter_field="language_id", filter_value=languageid)

@login_required(login_url='/app_biblioteca/login/')
def delete_object(request, model, object_id_name):
    if request.method == "POST":
        object_id = request.POST.get(object_id_name, None)
        if object_id:
            obj = get_object_or_404(model, id=object_id)
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