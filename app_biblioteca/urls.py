from app_biblioteca import views
from django.urls import path, include

urlpatterns = [
    path(r'', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('valida_user/', views.valida_user, name='valida_user'),
]