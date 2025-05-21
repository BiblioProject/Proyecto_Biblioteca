from app_biblioteca import views
from django.urls import path, include
from . import views

urlpatterns = [
    path(r'', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('valida_user/', views.valida_user, name='valida_user'),
    path('delete_lending/', views.delete_lending, name='delete_lending'),
    path('books/', views.books_view, name='books'),
    path('delete_book/', views.delete_book, name='delete_book'),
    path('readers/', views.readers_view, name='readers'),
<<<<<<< HEAD
    path('createBook/', views.createBook, name = 'create_book'),
    path('editBook/<int:id>', views.editBook, name = 'edit_book'),
    path('createReader/', views.createReader, name = 'create_reader'),
    path('editReader/<int:id>', views.editReader, name = 'edit_reader'),
    path('createLending/', views.createLending, name = 'create_lending'),
    path('editLending/<int:id>', views.editLending, name = 'edit_lending')
=======
    path('delete_reader/', views.delete_reader, name='delete_reader'),
    path('editorials/', views.editorials_view, name='editorials'),
    path('delete_editorial/', views.delete_editorial, name='delete_editorial'),
    path('genres/', views.genres_view, name='genres'),
    path('delete_genre/', views.delete_genre, name='delete_genre'),
    path('languages/', views.languages_view, name='languages'),
    path('delete_language/', views.delete_language, name='delete_language'),
>>>>>>> 205892282ee1e232723eff01ed201c0728804e50
]