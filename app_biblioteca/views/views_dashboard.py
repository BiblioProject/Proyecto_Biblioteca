from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from app_biblioteca.models import Book, Lending, Reader, Editorial, Genre, Language
from django.contrib.auth.models import User
from .views_utils import is_admin

@login_required(login_url='/app_biblioteca/login/')
@user_passes_test(is_admin, login_url='/app_biblioteca/main/')
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

    libros_mas_prestados = Book.objects.filter(is_active=True).annotate(
        num_prestamos=Count('lending', filter=Q(lending__is_active=True))
    ).order_by('-num_prestamos')[:5]

    max_prestamos = libros_mas_prestados[0].num_prestamos if libros_mas_prestados else 1
    for libro in libros_mas_prestados:
        libro.porcentaje = round((libro.num_prestamos / max_prestamos) * 100, 2)

    return render(request, 'dashboard/dashboard.html', {
        'stats': stats,
        'ultimos_prestamos': ultimos_prestamos,
        'libros_mas_prestados': libros_mas_prestados
    })