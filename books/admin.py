from django.contrib import admin
from .models import Book, BookUserList, BookNotes
from .resources import BookResources
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class BookAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'author',
        'title',
        'image',
        'content',
    )
    resource_class = BookResources

admin.site.register(Book, BookAdmin)

class BookUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'status2',
        'booksList'
    )

admin.site.register(BookUserList, BookUserAdmin)

class BookNoteUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'booksList',
        'notes',
        'timestamp'
    )

admin.site.register(BookNotes, BookNoteUserAdmin)
