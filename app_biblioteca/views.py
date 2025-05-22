from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from .models import Lending, Book, Reader, Editorial, Genre, Language
from django.conf import settings
import glob,os, json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .forms import BookForm, ReaderForm, LendingForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .forms import PinLoginForm

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

def pin_login(request):
    if request.method == 'POST':
        form = PinLoginForm(request.POST)
        if form.is_valid():
            reader_id = form.cleaned_data['reader_id']
            pin = form.cleaned_data['pin']
            try:
                reader = Reader.objects.get(id=reader_id, pin=pin, is_active=True)
                request.session['reader_id'] = reader.id
                return redirect('main')  # O la vista principal de lectores
            except Reader.DoesNotExist:
                messages.error(request, "ID o PIN incorrecto.")
    else:
        form = PinLoginForm()
    return render(request, 'pin_login.html', {'form': form})

def vista_para_lectores(request):
    if not request.session.get('reader_id'):
        return redirect('pin_login')
    


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

def createBook(request):
   if request.method == 'POST':
      book_form = BookForm(request.POST)
      if book_form.is_valid():
         book_form.save()
         return redirect('books')
   else:
      book_form = BookForm()
   return render(request, 'createBook.html',{'book_form':book_form} )

def editBook(request, id):
   book_form = None
   error = None
   try:
      book = Book.objects.get(id = id)
      if request.method == 'GET':
         book_form = BookForm(instance = book)
      else:
         book_form = BookForm(request.POST, instance = book)
         if book_form.is_valid():
               book_form.save()
         return redirect('books')
   except ObjectDoesNotExist as e: 
      error = e
      book = None
   return render(request, 'editBook.html', {'book_form': book_form, 'error':error, 'book': book})

def createReader(request):
   if request.method == 'POST':
      reader_form = ReaderForm(request.POST)
      if reader_form.is_valid():
         reader_form.save()
         return redirect('readers')
   else:
      reader_form = ReaderForm()
   return render(request, 'createReader.html',{'reader_form':reader_form})

def editReader(request, id):
   reader_form = None
   error = None
   try:
      reader = Reader.objects.get(id = id)
      if request.method == 'GET':
         reader_form = ReaderForm(instance = reader)
      else:
         reader_form = ReaderForm(request.POST, instance = reader)
         if reader_form.is_valid():
               reader_form.save()
         return redirect('readers')
   except ObjectDoesNotExist as e: 
      error = e
      reader = None
   return render(request, 'editReader.html', {'reader_form': reader_form, 'error':error, 'reader': reader})

def createLending(request):
   if request.method == 'POST':
      lending_form = LendingForm(request.POST)
      if lending_form.is_valid():
         lending_form.save()
         return redirect('main')
   else:
      lending_form = LendingForm()
   return render(request, 'createLending.html',{'lending_form':lending_form})

def editLending(request, id):
   lending_form = None
   error = None
   try:
      lending = Lending.objects.get(id = id)
      if request.method == 'GET':
         lending_form = LendingForm(instance = lending)
      else:
         lending_form = LendingForm(request.POST, instance = lending)
         if lending_form.is_valid():
               lending_form.save()
         return redirect('main')
   except ObjectDoesNotExist as e: 
      error = e
      lending = None
   return render(request, 'editLending.html', {'lending_form': lending_form, 'error':error, 'lending': lending})