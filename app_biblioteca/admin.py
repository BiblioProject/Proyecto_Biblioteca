from django.contrib import admin
from .models import Genre, Editorial, Language, Book, Reader, Lending

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name','is_active')
    
admin.site.register(Genre, GenreAdmin)

class EditorialAdmin(admin.ModelAdmin):
    list_display = ('name','is_active')
    
admin.site.register(Editorial, EditorialAdmin)

class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name','is_active')
    
admin.site.register(Language, LanguageAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','publication_year','stock','available','is_active')
    
admin.site.register(Book, BookAdmin)

class ReaderAdmin(admin.ModelAdmin):
    list_display = ('name','first_surname','sanctions','sanction_amount','is_active')
    readonly_fields = ('sanctions', 'sanction_amount')
    
admin.site.register(Reader, ReaderAdmin)

class LendingAdmin(admin.ModelAdmin):
    list_display = ('reader','book','date','state','is_active','user')
    readonly_fields=('estimated_return_date','state')
    
admin.site.register(Lending, LendingAdmin)