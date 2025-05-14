from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta

class Category(models.Model):
    name = models.CharField(max_length=100, blank=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Editorial(models.Model):
    name = models.CharField(max_length=100, blank=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=50, blank=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255, blank=False)
    author = models.CharField(max_length=255, blank=False)
    publication_year = models.IntegerField(blank=False)

    pages = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    stock = models.IntegerField(default=1)
    available = models.IntegerField(default=1)

    is_active = models.BooleanField(default=True)

    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def clean(self):
        # Validaciones de publicación
        if self.publication_year < 0:
            raise ValidationError("El año de publicación no puede ser negativo.")
        
        current_year = now().year

        if self.publication_year < 1000 or self.publication_year > current_year:
            raise ValidationError(f"El año de publicación debe estar entre 1000 y {current_year}.")

        # Validación de páginas
        if self.pages is not None and self.pages < 0:
            raise ValidationError("La cantidad de páginas no puede ser negativa.")
        
        # Validaciones de stock y disponibilidad
        if self.available > self.stock:
            raise ValidationError("La cantidad disponible no puede ser mayor que el stock.")
        if self.available < 0:
            raise ValidationError("No puede haber disponibilidad negativa.")
        if self.stock < 0:
            raise ValidationError("El stock no puede ser negativo.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.author}"

class Reader(models.Model):
    name = models.CharField(max_length=30, blank=False)
    first_surname = models.CharField(max_length=30, blank=False)
    second_surname = models.CharField(max_length=30, blank=True, null=True)
    
    address = models.CharField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    sanctions = models.IntegerField(default=0)
    sanction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.sanctions < 0:
            raise ValidationError("El número de sanciones no puede ser negativo.")
        if self.sanction_amount < 0:
            raise ValidationError("El monto total de sanciones no puede ser negativo.")

    def __str__(self):
        return f"{self.name} {self.first_surname}"

class Lending(models.Model):
    _states = (
        (0, 'Prestado'),
        (1, 'Devuelto'),
        (2, 'Atrasado'),
    )
    state = models.SmallIntegerField(choices=_states, default=0)

    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    loan_term_days = models.IntegerField(default=7)
    daily_rate=models.DecimalField(max_digits=10, decimal_places=2, default=1.50)

    date = models.DateField(default=now)
    estimated_return_date = models.DateField(null=False)
    real_return_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    @property
    def days_late(self):
        if not self.real_return_date:
            return 0
        if self.real_return_date > self.estimated_return_date:
            return (self.real_return_date - self.estimated_return_date).days
        return 0

    @property
    def calculated_sanction_amount(self):
        return self.days_late * self.daily_rate

    def clean(self):
        if self.loan_term_days <= 0:
            raise ValidationError("El plazo del préstamo debe ser mayor que 0 días.")
    
        if self.daily_rate < 0:
            raise ValidationError("La tarifa diaria no puede ser negativa.")
        
        if not self.estimated_return_date:
            self.estimated_return_date = self.date + timedelta(days=self.loan_term_days)
        
        if self.real_return_date and self.real_return_date < self.date:
            raise ValidationError("La fecha de devolución no puede ser anterior a la fecha del préstamo.")

    def save(self, *args, **kwargs):
        self.full_clean()

        if not self.pk:  # Préstamo nuevo
            if self.book.available <= 0:
                raise ValidationError("No hay ejemplares disponibles.")
            self.book.available -= 1
            self.book.save()
        else:  # Actualización (devolución)
            if self.real_return_date and self.state == 0:  # Prestado
                if self.real_return_date > self.estimated_return_date:
                    self.state = 2  # Atrasado
                    self.reader.sanctions += 1
                    self.reader.sanction_amount += self.calculated_sanction_amount
                    self.reader.save()
                else:
                    self.state = 1  # Devuelto

                self.book.available += 1
                self.book.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reader.name} - {self.book.title}"