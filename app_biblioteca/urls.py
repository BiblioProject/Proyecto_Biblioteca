from app_biblioteca import views
from django.urls import path, include

urlpatterns = [
    path(r'', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('valida_user/', views.valida_user, name='valida_user'),
    path('books/', views.books_view, name='books'),
    path('readers/', views.readers_view, name='readers'),
]