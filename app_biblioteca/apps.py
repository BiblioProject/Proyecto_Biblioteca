from django.apps import AppConfig
from django.db.models.signals import post_migrate

def crear_roles(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from app_biblioteca.models import Book, Reader, Lending

    # Crear grupos
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    encargado_group, _ = Group.objects.get_or_create(name='Encargado')

    # Permisos del encargado: agregar y cambiar libros, lectores y préstamos
    content_types = [
        ContentType.objects.get_for_model(Book),
        ContentType.objects.get_for_model(Reader),
        ContentType.objects.get_for_model(Lending),
    ]

    perms = Permission.objects.filter(
        content_type__in=content_types,
        codename__in=[
            'add_book', 'change_book',
            'add_reader', 'change_reader',
            'add_lending', 'change_lending',
        ]
    )

    encargado_group.permissions.set(perms)  # Asignar permisos
    admin_group.permissions.set(Permission.objects.all())  # Admin tiene todos

class AppBibliotecaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_biblioteca'

    def ready(self):
        from . import signals
        post_migrate.connect(crear_roles, sender=self)
        
