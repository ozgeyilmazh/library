
from django.contrib import admin
from django.urls import path, include
from books.views import *

urlpatterns = [
    path('', index, name='index'),
    path('home/', homepage, name='home'),
    path('books/', bookList, name='books'),
    path('my-library/', myLibrary, name='my_library'),
    path('user-card/', count_books, name='count_books'),
    path('my-library/i-will/', book_ill_read, name='book_ill_read'),
    path('my-library/i-am-reading/', book_iam_reading, name='book_iam_reading'),
    path('my-library/i-read/', book_i_read, name='book_i_read'),
    path('addto-my-library/<int:id>', add_to_my_library, name='add_to_my_library'),
    path('addto-i-will/<int:id>', add_to_i_will, name='add_to_i_will'),
    path('addto-iam-reading-now/<int:id>', add_to_iam_reading_now, name='add_to_iam_reading_now'),
    path('addto-i-read/<int:id>', add_to_i_read, name='add_to_i_read'),
    path('add-note/<int:pid>', add_note, name='add_note'),
    path('create-note/<int:pid>', create_note, name='create_note'),
    path('notes/<int:id>', list_notes, name='list_notes'),
    # path('now-notes/<int:id>', now_list_notes, name='now_list_notes'),
    path('note-search/', note_search, name="note_search"),
    path('book-search/', book_search, name="book_search"),
    path('personal-book-search/', personal_book_search, name="personal_book_search"),
    path('book-search-i-read/', book_search_i_read, name="book_search_i_read"),
    path('book-search-i-ll-read/', book_search_i_ll_read, name="book_search_i_ll_read"),
    path('book-search-i-am-reading/', book_search_i_am_reading, name="book_search_i_am_reading"),
    path('my-library/getBookCount/', getBookCount, name="getBookCount"),
]
