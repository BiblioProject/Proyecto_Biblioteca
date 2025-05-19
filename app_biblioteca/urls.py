from app_biblioteca import views
from django.urls import path, include

urlpatterns = [
    path(r'', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('valida_user/', views.valida_user, name='valida_user'),
    path('delete_lending/', views.delete_lending, name='delete_lending'),
    path('books/', views.books_view, name='books'),
    path('delete_book/', views.delete_book, name='delete_book'),
    path('readers/', views.readers_view, name='readers'),
    path('delete_reader/', views.delete_reader, name='delete_reader'),
    path('editorials/', views.editorials_view, name='editorials'),
    path('delete_editorial/', views.delete_editorial, name='delete_editorial'),
    path('genres/', views.genres_view, name='genres'),
    path('delete_genre/', views.delete_genre, name='delete_genre'),
    path('languages/', views.languages_view, name='languages'),
    path('delete_language/', views.delete_language, name='delete_language'),
]