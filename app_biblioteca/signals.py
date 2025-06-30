from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def asignar_rol_superusuario(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        instance.groups.add(admin_group)
