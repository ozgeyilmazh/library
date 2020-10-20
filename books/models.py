from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Book(models.Model):
    title = models.CharField(
        max_length=200,
        default="",
        null=True,
        blank=True,
    )
    author = models.CharField(
        max_length=200,
        default="",
        null=True,
        blank=True,
    )
    image = models.ImageField(null=True, blank=True,upload_to="images/books")
    content = models.TextField()
    def __str__(self):
        return f" {self.author} - {self.title} "
    @property
    def photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

STATUS = (
     ('kutuphane','Kütüphanem'),
)
STATUS2 = (
    ('bitenler', 'Bitenler'),
    ('okunacaklar', 'Okunacaklar'),
    ('simdi_okuduklarım', 'Şimdi Okuduklarım'),
)
DEFAULT_STATUS = "kutuphane"
class BookUserList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )
    booksList = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
    )
    status = models.CharField(
        default=DEFAULT_STATUS,
        choices=STATUS,
        max_length=10
    )
    status2 = models.CharField(
        choices=STATUS2,
        max_length=30,
    )

class BookNotes(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
    )

    booksList = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    notes = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

