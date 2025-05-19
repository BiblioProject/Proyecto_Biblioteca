from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from django.shortcuts import redirect
from .models import Lending, Book, Reader

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