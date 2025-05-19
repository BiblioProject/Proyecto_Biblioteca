from django.contrib import admin
from .models import Genre, Editorial, Language, Book, Reader, Lending

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
admin.site.register(Genre, GenreAdmin)

class EditorialAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
admin.site.register(Editorial, EditorialAdmin)

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
admin.site.register(Language, LanguageAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
admin.site.register(Book, BookAdmin)

class ReaderAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('sanctions', 'sanction_amount')
    
admin.site.register(Reader, ReaderAdmin)

class LendingAdmin(admin.ModelAdmin):
    list_display = ('reader','book')
    readonly_fields=('estimated_return_date','state')
    
admin.site.register(Lending, LendingAdmin)