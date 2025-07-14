from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from app_biblioteca.models import Book, Reader, Lending, Editorial, Genre, Language
from .views_utils import list_objects, is_admin

# Vista principal - préstamos
@login_required(login_url='/app_biblioteca/login/')
def main(request):
    return list_objects(request, Lending, 'lendings/lendings.html')

# Libros
@login_required(login_url='/app_biblioteca/login/')
def books_view(request):
    return list_objects(request, Book, 'books/books.html', per_page=5)

# Lectores
@login_required(login_url='/app_biblioteca/login/')
def readers_view(request):
    return list_objects(request, Reader, 'readers/readers.html')

# Editoriales
@login_required(login_url='/app_biblioteca/login/')
def editorials_view(request):
    return list_objects(request, Editorial, 'editorials/editorials.html')

# Géneros
@login_required(login_url='/app_biblioteca/login/')
def genres_view(request):
    return list_objects(request, Genre, 'genres/genres.html')

# Idiomas
@login_required(login_url='/app_biblioteca/login/')
def languages_view(request):
    return list_objects(request, Language, 'languages/languages.html')

# Usuarios (solo para administradores)
@login_required(login_url='/app_biblioteca/login/')
@user_passes_test(is_admin, login_url='/app_biblioteca/main/')
def users_view(request):
    return list_objects(request, User, 'users/users.html', per_page=5)

# Préstamos por libro
@login_required(login_url='/app_biblioteca/login/')
def lendings_book(request, bookid):
    return list_objects(request, Lending, 'lendings/lendings.html', filter_field="book_id", filter_value=bookid)

# Préstamos por lector
@login_required(login_url='/app_biblioteca/login/')
def lendings_reader(request, readerid):
    return list_objects(request, Lending, 'lendings/lendings.html', filter_field="reader_id", filter_value=readerid)

# Libros por editorial
@login_required(login_url='/app_biblioteca/login/')
def books_editorial(request, editorialid):
    return list_objects(request, Book, 'books/books.html', filter_field="editorial_id", filter_value=editorialid)

# Libros por género
@login_required(login_url='/app_biblioteca/login/')
def books_genre(request, genreid):
    return list_objects(request, Book, 'books/books.html', filter_field="genre_id", filter_value=genreid)

# Libros por idioma
@login_required(login_url='/app_biblioteca/login/')
def books_language(request, languageid):
    return list_objects(request, Book, 'books/books.html', filter_field="language_id", filter_value=languageid)