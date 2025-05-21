from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from django.shortcuts import redirect
from .models import Lending, Book, Reader
from .forms import BookForm, ReaderForm, LendingForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError

@login_required(login_url='/app_biblioteca/login/')
def main(request):
   lendings=Lending.objects.all()
   for lending in lendings:
      print(lending.estimated_return_date)
   return render(request,'lendings.html',{'lendings':lendings})

@login_required(login_url='/app_biblioteca/login/')
def books_view(request):
   books = Book.objects.all()
   for book in books:
      print(book.title)
   return render(request, 'books.html', {'books': books})

@login_required(login_url='/app_biblioteca/login/')
def readers_view(request):
   readers = Reader.objects.all()
   for reader in readers:
      print(reader.name)
   return render(request, 'readers.html', {'readers': readers})

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