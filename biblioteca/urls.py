from django.contrib import admin
from django.urls import path, include
from app_biblioteca.views_list import main
from app_biblioteca.views_auth import logout_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app_biblioteca/', include('app_biblioteca.urls')),
    path('', main, name='main'),
    path('logout/', logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)