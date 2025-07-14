from django.urls import path
from app_biblioteca.views.views_auth import (
    CustomLoginView, custom_password_reset, custom_password_reset_confirm,
    registro_usuario, valida_user
)
from app_biblioteca.views.views_list import (
    main, books_view, readers_view, editorials_view, genres_view, languages_view,
    users_view, lendings_book, lendings_reader,
    books_editorial, books_genre, books_language
)
from app_biblioteca.views.views_crud import (
    createBook, editBook, delete_book,
    createReader, editReader, delete_reader,
    createLending, editLending, delete_lending,
    createLanguage, editLanguage, delete_language,
    createEditorial, editEditorial, delete_editorial,
    createGenre, editGenre, delete_genre,
    edit_user, delete_user,
)
from app_biblioteca.views.views_dashboard import dashboard

urlpatterns = [
    path('', main, name='main'),  # préstamos

    # Libros
    path('books/', books_view, name='books'),
    path('delete_book/', delete_book, name='delete_book'),
    path('createBook/', createBook, name='create_book'),
    path('editBook/<int:id>/', editBook, name='edit_book'),
    path('books_editorial/<int:editorialid>/', books_editorial, name='books_editorial'),
    path('books_genre/<int:genreid>/', books_genre, name='books_genre'),
    path('books_language/<int:languageid>/', books_language, name='books_language'),

    # Lectores
    path('readers/', readers_view, name='readers'),
    path('delete_reader/', delete_reader, name='delete_reader'),
    path('createReader/', createReader, name='create_reader'),
    path('editReader/<int:id>/', editReader, name='edit_reader'),

    # Préstamos
    path('delete_lending/', delete_lending, name='delete_lending'),
    path('createLending/', createLending, name='create_lending'),
    path('editLending/<int:id>/', editLending, name='edit_lending'),
    path('lendings_book/<int:bookid>/', lendings_book, name='lendings_book'),
    path('lendings_reader/<int:readerid>/', lendings_reader, name='lendings_reader'),

    # Editoriales
    path('editorials/', editorials_view, name='editorials'),
    path('delete_editorial/', delete_editorial, name='delete_editorial'),
    path('createEditorial/', createEditorial, name='create_editorial'),
    path('editEditorial/<int:id>/', editEditorial, name='edit_editorial'),

    # Géneros
    path('genres/', genres_view, name='genres'),
    path('delete_genre/', delete_genre, name='delete_genre'),
    path('createGenre/', createGenre, name='create_genre'),
    path('editGenre/<int:id>/', editGenre, name='edit_genre'),

    # Idiomas
    path('languages/', languages_view, name='languages'),
    path('delete_language/', delete_language, name='delete_language'),
    path('createLanguage/', createLanguage, name='create_language'),
    path('editLanguage/<int:id>/', editLanguage, name='edit_language'),

    # Usuarios
    path('users/', users_view, name='users'),
    path('delete_user/', delete_user, name='delete_user'),
    path('edit_user/<int:id>/', edit_user, name='edit_user'),

    # Autenticación
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registro/', registro_usuario, name='registro'),
    path('valida_user/', valida_user, name='valida_user'),
    path('auth/', custom_password_reset, name='custom_password_reset'),
    path('reset_password/<str:token>/', custom_password_reset_confirm, name='custom_password_reset_confirm'),

    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),
]