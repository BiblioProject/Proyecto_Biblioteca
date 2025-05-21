from app_biblioteca import views
from django.urls import path, include
from . import views

urlpatterns = [
    path(r'', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('valida_user/', views.valida_user, name='valida_user'),
    path('books/', views.books_view, name='books'),
    path('readers/', views.readers_view, name='readers'),
    path('createBook/', views.createBook, name = 'create_book'),
    path('editBook/<int:id>', views.editBook, name = 'edit_book'),
    path('createReader/', views.createReader, name = 'create_reader'),
    path('editReader/<int:id>', views.editReader, name = 'edit_reader'),
    path('createLending/', views.createLending, name = 'create_lending'),
    path('editLending/<int:id>', views.editLending, name = 'edit_lending')
]