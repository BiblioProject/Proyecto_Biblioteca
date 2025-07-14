from django.db.models import Q, CharField, TextField, IntegerField, FloatField, DecimalField, DateField, DateTimeField, ForeignKey
from django.db.models.functions import Cast
from django.core.paginator import Paginator
from django.shortcuts import render

def is_admin(user):
    return user.groups.filter(name='admin').exists() or user.is_superuser

def list_objects(request, model, template, filter_field=None, filter_value=None, per_page=7):
    query_params = {"is_active": True}
    if filter_field and filter_value:
        query_params[filter_field] = filter_value

    queryset = model.objects.filter(**query_params)
    search_term = request.GET.get("q")

    if search_term:
        search_filters = Q()
        for field in model._meta.get_fields():
            if hasattr(field, 'attname') and not field.auto_created:
                field_name = field.name
                if isinstance(field, (CharField, TextField)):
                    search_filters |= Q(**{f"{field_name}__icontains": search_term})
                elif isinstance(field, (IntegerField, FloatField, DecimalField, DateField, DateTimeField)):
                    queryset = queryset.annotate(**{
                        f"{field_name}_str": Cast(field_name, CharField())
                    })
                    search_filters |= Q(**{f"{field_name}_str__icontains": search_term})
                elif isinstance(field, ForeignKey):
                    for rel_field in field.related_model._meta.get_fields():
                        if isinstance(rel_field, (CharField, TextField)) and not rel_field.auto_created:
                            search_filters |= Q(**{f"{field.name}__{rel_field.name}__icontains": search_term})
        queryset = queryset.filter(search_filters)

    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, template, {'page_obj': page_obj, 'search_term': search_term})