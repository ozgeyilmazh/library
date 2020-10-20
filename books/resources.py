from import_export import resources

from .models import Book
class BookResources(resources.ModelResource):
    class Meta:
        model = Book
        fields = (
                'id',
                'author',
                'title',
                'content'
        )