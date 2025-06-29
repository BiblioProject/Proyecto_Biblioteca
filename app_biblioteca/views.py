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
from .forms import BookForm, ReaderForm, LendingForm, LanguageForm, EditorialForm, GenreForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import Count, Q, CharField, TextField, IntegerField, FloatField, DecimalField, DateField, DateTimeField, ForeignKey
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.db.models.functions import Cast
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

class CustomLoginView(LoginView):
   template_name = "auth/login.html"

class CustomPasswordResetView(PasswordResetView):
   template_name = "auth/password_reset_form.html"

class CustomPasswordResetDoneView(PasswordResetDoneView):
   template_name = "auth/password_reset_done.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
   template_name = "auth/password_reset_confirm.html"

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
   template_name = "auth/password_reset_complete.html"

def logout(request):
   auth_logout(request)
   return redirect('login')

def registro_usuario(request):
   if request.method == 'POST':
      form = RegistroUsuarioForm(request.POST)
      if form.is_valid():
         form.save()
         return redirect('login')
   else:
      form = RegistroUsuarioForm()
   return render(request, 'auth/registro.html', {'form': form})

def login(request):
   args = {}
   return TemplateResponse(request, 'auth/login.html', args)

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

   search_term = request.GET.get("q")
   if search_term:
      search_filters = Q()
      for field in model._meta.get_fields():
         if hasattr(field, 'attname') and not field.auto_created:
            field_name = field.name
            # Campos de texto
            if isinstance(field, (CharField, TextField)):
               search_filters |= Q(**{f"{field.name}__icontains": search_term})
            # Campos numéricos convertidos a texto para icontains
            elif isinstance(field, (IntegerField, FloatField, DecimalField, DateField, DateTimeField)):
               # Convertimos a texto para comparar como string
               queryset = queryset.annotate(**{
                  f"{field_name}_str": Cast(field_name, CharField())
               })
               search_filters |= Q(**{f"{field_name}_str__icontains": search_term})
            # Relaciones ForeignKey con nombre legible
            elif isinstance(field, ForeignKey):
               related_model = field.related_model
               # Busca en campos de texto de la tabla relacionada
               for rel_field in related_model._meta.get_fields():
                  if isinstance(rel_field, (CharField, TextField)) and not rel_field.auto_created:
                     search_filters |= Q(**{f"{field.name}__{rel_field.name}__icontains": search_term})
      queryset = queryset.filter(search_filters)

   paginator = Paginator(queryset, per_page)
   page_number = request.GET.get("page")
   page_obj = paginator.get_page(page_number)

   return render(request, template, {'page_obj': page_obj, 'search_term': search_term})

@login_required(login_url='/app_biblioteca/login/')
def books_view(request):
   return list_objects(request, Book, 'books/books.html', per_page=5)

@login_required(login_url='/app_biblioteca/login/')
def main(request):
   return list_objects(request, Lending, 'lendings/lendings.html')

@login_required(login_url='/app_biblioteca/login/')
def readers_view(request):
   return list_objects(request, Reader, 'readers/readers.html')

@login_required(login_url='/app_biblioteca/login/')
def editorials_view(request):
   return list_objects(request, Editorial, 'editorials/editorials.html')

@login_required(login_url='/app_biblioteca/login/')
def genres_view(request):
   return list_objects(request, Genre, 'genres/genres.html')

@login_required(login_url='/app_biblioteca/login/')
def languages_view(request):
   return list_objects(request, Language, 'languages/languages.html')

@login_required(login_url='/app_biblioteca/login/')
def users_view(request):
   return list_objects(request, User, 'users/users.html', per_page=5)

# Función para listar préstamos según libro
@login_required(login_url='/app_biblioteca/login/')
def lendings_book(request, bookid):
   return list_objects(request, Lending, 'lendings/lendings.html', filter_field="book_id", filter_value=bookid)

# Función para listar préstamos según lector
@login_required(login_url='/app_biblioteca/login/')
def lendings_reader(request, readerid):
   return list_objects(request, Lending, 'lendings/lendings.html', filter_field="reader_id", filter_value=readerid)

# Función para listar libros según editorial
@login_required(login_url='/app_biblioteca/login/')
def books_editorial(request, editorialid):
   return list_objects(request, Book, 'books/books.html', filter_field="editorial_id", filter_value=editorialid)

# Función para listar libros según género
@login_required(login_url='/app_biblioteca/login/')
def books_genre(request, genreid):
   return list_objects(request, Book, 'books/books.html', filter_field="genre_id", filter_value=genreid)

# Función para listar libros según idioma
@login_required(login_url='/app_biblioteca/login/')
def books_language(request, languageid):
   return list_objects(request, Book, 'books/books.html', filter_field="language_id", filter_value=languageid)

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

@login_required(login_url='/app_biblioteca/login/')
def delete_user(request):
   return delete_object(request, User, "userid")

def createBook(request):
   if request.method == 'POST':
      book_form = BookForm(request.POST)
      if book_form.is_valid():
         book_form.save()
         return redirect('books')
   else:
      book_form = BookForm()
   return render(request, 'books/modals/createBook.html',{'book_form':book_form} )

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
   return render(request, 'books/modals/editBook.html', {'book_form': book_form, 'error':error, 'book': book})

def createReader(request):
   if request.method == 'POST':
      reader_form = ReaderForm(request.POST)
      if reader_form.is_valid():
         reader_form.save()
         return redirect('readers')
   else:
      reader_form = ReaderForm()
   return render(request, 'readers/modals/createReader.html',{'reader_form':reader_form})

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
   return render(request, 'readers/modals/editReader.html', {'reader_form': reader_form, 'error':error, 'reader': reader})

def createLending(request):
   if request.method == 'POST':
      lending_form = LendingForm(request.POST)
      if lending_form.is_valid():
         lending = lending_form.save(commit=False)
         lending.user = request.user
         lending_form.save()
         return redirect('main')
   else:
      lending_form = LendingForm()
   return render(request, 'lendings/modals/createLending.html',{'lending_form':lending_form})

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
   return render(request, 'lendings/modals/editLending.html', {'lending_form': lending_form, 'error':error, 'lending': lending})

def createLanguage(request):
   if request.method == 'POST':
      language_form = LanguageForm(request.POST)
      if language_form.is_valid():
         language_form.save()
         return redirect('languages')
   else:
      language_form = LanguageForm()
   return render(request, 'languages/modals/createLanguage.html',{'language_form':language_form})

def editLanguage(request, id):
   language_form = None
   error = None
   try:
      language = Language.objects.get(id = id)
      if request.method == 'GET':
         language_form = LanguageForm(instance = language)
      else:
         language_form = LanguageForm(request.POST, instance = language)
         if language_form.is_valid():
               language_form.save()
         return redirect('languages')
   except ObjectDoesNotExist as e: 
      error = e
      language = None
   return render(request, 'languages/modals/editLanguage.html', {'language_form': language_form, 'error':error, 'language': language})

def createEditorial(request):
   if request.method == 'POST':
      editorial_form = EditorialForm(request.POST)
      if editorial_form.is_valid():
         editorial_form.save()
         return redirect('editorials')
   else:
      editorial_form = EditorialForm()
   return render(request, 'editorials/modals/createEditorial.html',{'editorial_form':editorial_form})

def editEditorial(request, id):
   editorial_form = None
   error = None
   try:
      editorial = Editorial.objects.get(id = id)
      if request.method == 'GET':
         editorial_form = EditorialForm(instance = editorial)
      else:
         editorial_form = EditorialForm(request.POST, instance = editorial)
         if editorial_form.is_valid():
               editorial_form.save()
         return redirect('editorials')
   except ObjectDoesNotExist as e: 
      error = e
      editorial = None
   return render(request, 'editorials/modals/editEditorial.html', {'editorial_form': editorial_form, 'error':error, 'editorial': editorial})

def createGenre(request):
   if request.method == 'POST':
      genre_form = GenreForm(request.POST)
      if genre_form.is_valid():
         genre_form.save()
         return redirect('genres')
   else:
      genre_form = GenreForm()
   return render(request, 'genres/modals/createGenre.html',{'genre_form':genre_form})

def editGenre(request, id):
   genre_form = None
   error = None
   try:
      genre = Genre.objects.get(id = id)
      if request.method == 'GET':
         genre_form = GenreForm(instance = genre)
      else:
         genre_form = GenreForm(request.POST, instance = genre)
         if genre_form.is_valid():
               genre_form.save()
         return redirect('genres')
   except ObjectDoesNotExist as e: 
      error = e
      genre = None
   return render(request, 'genres/modals/editGenre.html', {'genre_form': genre_form, 'error':error, 'genre': genre})

def createUser(request):
   if request.method == 'POST':
      user_form = UserForm(request.POST)
      if user_form.is_valid():
         user_form.save()
         return redirect('users')
   else:
      user_form = UserForm()
   return render(request, 'users/modals/createUser.html',{'user_form':user_form})

def editUser(request, id):
   user_form = None
   error = None
   try:
      user = User.objects.get(id = id)
      if request.method == 'GET':
         user_form = UserForm(instance = user)
      else:
         user_form = UserForm(request.POST, instance = user)
         if user_form.is_valid():
               user_form.save()
         return redirect('users')
   except ObjectDoesNotExist as e: 
      error = e
      user = None
   return render(request, 'users/modals/editUser.html', {'user_form': user_form, 'error':error, 'user': user})

def custom_password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = get_random_string(32)
            request.session['password_reset_token'] = token
            request.session['password_reset_user'] = user.pk
            # Crea el enlace de recuperación
            reset_link = request.build_absolute_uri(f'/app_biblioteca/reset_password/{token}/')
            # Envía el correo
            send_mail(
                'Recupera tu contraseña',
                f'Hola {user.username}, haz clic en el siguiente enlace para restablecer tu contraseña: {reset_link}',
                None,
                [email],
            )
            messages.success(request, 'Se ha enviado un enlace de recuperación a tu correo.')
            return redirect('custom_password_reset')
        except User.DoesNotExist:
            messages.error(request, 'No existe un usuario con ese correo.')
    return render(request, 'auth/custom_password_reset.html')

def custom_password_reset_confirm(request, token):
    session_token = request.session.get('password_reset_token')
    user_id = request.session.get('password_reset_user')
    if not session_token or session_token != token or not user_id:
        return render(request, 'auth/custom_password_reset_invalid.html')

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
        elif password1.isdigit():
            messages.error(request, 'La contraseña no puede ser completamente numérica.')
        else:
            user = User.objects.get(pk=user_id)
            user.password = make_password(password1)
            user.save()
            # Limpia la sesión
            del request.session['password_reset_token']
            del request.session['password_reset_user']
            messages.success(request, '¡Contraseña cambiada exitosamente! Ya puedes iniciar sesión.')
            return redirect('login')
    return render(request, 'auth/custom_password_reset_confirm.html')
   
@login_required(login_url='/app_biblioteca/login/')
def dashboard(request):
   stats = {
      'total_usuarios': User.objects.count(),
      'usuarios_activos': User.objects.filter(is_active=True).count(),
      'total_libros': Book.objects.filter(is_active=True).count(),
      'libros_prestados': Lending.objects.filter(is_active=True, real_return_date__isnull=True).count(),
      'total_lectores': Reader.objects.filter(is_active=True).count(),
      'total_editoriales': Editorial.objects.filter(is_active=True).count(),
      'total_generos': Genre.objects.filter(is_active=True).count(),
      'total_idiomas': Language.objects.filter(is_active=True).count(),
      'prestamos_activos': Lending.objects.filter(is_active=True, real_return_date__isnull=True).count(),
      'prestamos_completados': Lending.objects.filter(is_active=True, real_return_date__isnull=False).count(),
   }
    
   ultimos_prestamos = Lending.objects.filter(is_active=True).select_related('book', 'reader').order_by('-date')[:5]
   
   libros_mas_prestados = Book.objects.filter(
      is_active=True
   ).annotate(
      num_prestamos=Count('lending', filter=Q(lending__is_active=True))
   ).order_by('-num_prestamos')[:5]

   max_prestamos = libros_mas_prestados[0].num_prestamos if libros_mas_prestados else 1  
    
   for libro in libros_mas_prestados:
      libro.porcentaje = min((libro.num_prestamos / max_prestamos) * 100, 100)
    
   return render(request, 'dashboard/dashboard.html', {
      'stats': stats,
      'ultimos_prestamos': ultimos_prestamos,
      'libros_mas_prestados': libros_mas_prestados
   })