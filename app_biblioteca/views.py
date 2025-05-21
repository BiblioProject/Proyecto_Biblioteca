from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.contrib import auth
from django.contrib import messages
from django.shortcuts import redirect
from .models import Lending, Book, Reader
from .forms import BookForm, ReaderForm, LendingForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError
=======
from django.contrib import auth, messages
from .models import Lending, Book, Reader, Editorial, Genre, Language
from django.conf import settings
import glob,os, json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
>>>>>>> 205892282ee1e232723eff01ed201c0728804e50

@login_required(login_url='/app_biblioteca/login/')
def main(request):
   lendings=Lending.objects.filter(is_active=True)
   paginator = Paginator(lendings, 7)  # 7 elementos por página
   page_number = request.GET.get("page")
   page_obj = paginator.get_page(page_number)

   return render(request, 'lendings.html', {'page_obj': page_obj})  # Pasamos page_obj correctamente

@login_required(login_url='/app_biblioteca/login/')
def books_view(request):
   books = Book.objects.filter(is_active=True)
   paginator = Paginator(books, 5)  # 5 elementos por página
   page_number = request.GET.get("page")
   page_obj = paginator.get_page(page_number)

   return render(request, 'books.html', {'page_obj': page_obj})  # Pasamos page_obj correctamente

@login_required(login_url='/app_biblioteca/login/')
def readers_view(request):
   readers = Reader.objects.filter(is_active=True)
   paginator = Paginator(readers, 7)  # 7 elementos por página
   page_number = request.GET.get("page")
   page_obj = paginator.get_page(page_number)

   return render(request, 'readers.html', {'page_obj': page_obj})  # Pasamos page_obj correctamente

@login_required(login_url='/app_biblioteca/login/')
def editorials_view(request):
   editorials = Editorial.objects.filter(is_active=True)
   paginator = Paginator(editorials, 7)  # 7 elementos por página
   page_number = request.GET.get("page")
   page_obj = paginator.get_page(page_number)

   return render(request, 'editorials.html', {'page_obj': page_obj})  # Pasamos page_obj correctamente

@login_required(login_url='/app_biblioteca/login/')
def genres_view(request):
   genres = Genre.objects.filter(is_active=True)
   paginator = Paginator(genres, 7)  # 7 elementos por página
   page_number = request.GET.get("page")
   page_obj = paginator.get_page(page_number)

   return render(request, 'genres.html', {'page_obj': page_obj})  # Pasamos page_obj correctamente

@login_required(login_url='/app_biblioteca/login/')
def languages_view(request):
   language = Language.objects.filter(is_active=True)
   paginator = Paginator(language, 7)  # 7 elementos por página
   page_number = request.GET.get("page")
   page_obj = paginator.get_page(page_number)

   return render(request, 'languages.html', {'page_obj': page_obj})  # Pasamos page_obj correctamente

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

<<<<<<< HEAD
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
=======
@login_required(login_url='/app_biblioteca/login/')
def delete_lending(request):
    if request.method == "POST":
        lendingid = request.POST.get("lendingid", None)
        if lendingid:
            lending = get_object_or_404(Lending, id=lendingid)
            lending.is_active = False
            lending.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "No se proporcionó un ID válido"})
    
    return JsonResponse({"success": False, "error": "Método no permitido"})

@login_required(login_url='/app_biblioteca/login/')
def delete_reader(request):
    if request.method == "POST":
        readerid = request.POST.get("readerid", None)
        if readerid:
            reader = get_object_or_404(Reader, id=readerid)
            reader.is_active = False
            reader.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "No se proporcionó un ID válido"})
    
    return JsonResponse({"success": False, "error": "Método no permitido"})

@login_required(login_url='/app_biblioteca/login/')
def delete_book(request):
    if request.method == "POST":
        bookid = request.POST.get("bookid", None)
        if bookid:
            book = get_object_or_404(Book, id=bookid)
            book.is_active = False
            book.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "No se proporcionó un ID válido"})
    
    return JsonResponse({"success": False, "error": "Método no permitido"})

@login_required(login_url='/app_biblioteca/login/')
def delete_editorial(request):
    if request.method == "POST":
        editorialid = request.POST.get("editorialid", None)
        if editorialid:
            editorial = get_object_or_404(Editorial, id=editorialid)
            editorial.is_active = False
            editorial.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "No se proporcionó un ID válido"})
    
    return JsonResponse({"success": False, "error": "Método no permitido"})

@login_required(login_url='/app_biblioteca/login/')
def delete_genre(request):
    if request.method == "POST":
        genreid = request.POST.get("genreid", None)
        if genreid:
            genre = get_object_or_404(Genre, id=genreid)
            genre.is_active = False
            genre.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "No se proporcionó un ID válido"})
    
    return JsonResponse({"success": False, "error": "Método no permitido"})

@login_required(login_url='/app_biblioteca/login/')
def delete_language(request):
    if request.method == "POST":
        languageid = request.POST.get("languageid", None)
        if languageid:
            language = get_object_or_404(Language, id=languageid)
            language.is_active = False
            language.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "No se proporcionó un ID válido"})
    
    return JsonResponse({"success": False, "error": "Método no permitido"})
>>>>>>> 205892282ee1e232723eff01ed201c0728804e50
