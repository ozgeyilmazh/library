from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Book, BookUserList, BookNotes
from .forms import BookNoteForm, SearchForm
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from account.models import Profile
def index(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, 'index.html')

@login_required(login_url="login")   
def homepage(request):
    context = dict() 
    current_user = request.user.id
    data = Profile(user_id=current_user)
    try:
        q1 = Profile.objects.get(user_id=current_user)
    except Profile.DoesNotExist:
        q1 = None
    if q1 != None:
        print("kayıt edilmiş") 
    else:
        data.save()
    context['kutuphanem'] = BookUserList.objects.filter(user_id=current_user, status='kutuphane').count()
    context['bitenler'] = BookUserList.objects.filter(user_id=current_user, status2='bitenler').count()
    context['suan'] = BookUserList.objects.filter(user_id=current_user, status2='simdi_okuduklarım').count()
    context['okunacaklar'] = BookUserList.objects.filter(user_id=current_user, status2='okunacaklar').count()
    note = BookNotes.objects.filter(user_id=current_user).order_by('-timestamp')
    context['note'] = BookNotes.objects.filter(user_id=current_user).order_by('-timestamp')
    count_books(request)
    page = request.GET.get('page', 1)
    paginator = Paginator(note, 20)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    return render(request, 'homepage.html', context)

@login_required(login_url="login")  
def bookList(request):
    numbers_list = Book.objects.all().order_by('title')
    page = request.GET.get('page', 1)
    paginator = Paginator(numbers_list, 15)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    return render(request, 'books.html', {'books': numbers})

@login_required(login_url="login")  
def myLibrary(request):
    context = dict()
    current_user = request.user.id
    my_books = BookUserList.objects.filter(user_id=current_user).order_by('booksList__title')
    page = request.GET.get('page', 1)

    paginator = Paginator(my_books, 15)
    try:
        context['my_books'] = paginator.page(page)
    except PageNotAnInteger:
        context['my_books'] = paginator.page(1)
    except EmptyPage:
        context['my_books'] = paginator.page(paginator.num_pages)
    count_books(request)
    return render(request, 'library/my-library.html', context)

@login_required(login_url="login")  
def count_books(request):
    context = dict()
    current_user = request.user.id
    request.session['kutuphanem']=BookUserList.objects.filter(user_id=current_user, status='kutuphane').count()
    request.session['bitenler']=BookUserList.objects.filter(user_id=current_user, status2='bitenler').count()
    request.session['suan']=BookUserList.objects.filter(user_id=current_user, status2='simdi_okuduklarım').count()
    request.session['okunacaklar']=BookUserList.objects.filter(user_id=current_user, status2='okunacaklar').count()
    return render(request, 'user/user-card.html', context)

@login_required(login_url="login")  
def getBookCount(request):
    current_user = request.user.id
    queryset1= BookUserList.objects.filter(user_id=current_user, status='kutuphane').count()
    queryset2= BookUserList.objects.filter(user_id=current_user, status2='bitenler').count()
    queryset3= BookUserList.objects.filter(user_id=current_user, status2='simdi_okuduklarım').count()
    queryset4= BookUserList.objects.filter(user_id=current_user, status2='okunacaklar').count()
    return JsonResponse({"kutuphane":queryset1, "bitenler": queryset2, "simdi_okuduklarım":queryset3, "okunacaklar":queryset4 })


@login_required(login_url="login")  
def book_ill_read(request):
    context = dict()
    current_user = request.user.id
    my_books = BookUserList.objects.filter(user_id=current_user, status2='okunacaklar').order_by('booksList__title')
    page = request.GET.get('page', 1)

    paginator = Paginator(my_books, 15)
    try:
        context['my_books'] = paginator.page(page)
    except PageNotAnInteger:
        context['my_books'] = paginator.page(1)
    except EmptyPage:
        context['my_books'] = paginator.page(paginator.num_pages)
    return render(request, 'library/books-that-ill-read.html', context)


@login_required(login_url="login")  
def book_iam_reading(request):
    context = dict()
    current_user = request.user.id
    my_books = BookUserList.objects.filter(user_id=current_user, status2='simdi_okuduklarım').order_by('booksList__title')
    page = request.GET.get('page', 1)

    paginator = Paginator(my_books, 15)
    try:
        context['my_books'] = paginator.page(page)
    except PageNotAnInteger:
        context['my_books'] = paginator.page(1)
    except EmptyPage:
        context['my_books'] = paginator.page(paginator.num_pages)
    return render(request, 'library/books-that-i-read-now.html', context)


@login_required(login_url="login")  
def book_i_read(request):
    context = dict()
    current_user = request.user.id
    my_books = BookUserList.objects.filter(user_id=current_user, status2='bitenler').order_by('booksList__title')
    page = request.GET.get('page', 1)

    paginator = Paginator(my_books, 15)
    try:
        context['my_books'] = paginator.page(page)
    except PageNotAnInteger:
        context['my_books'] = paginator.page(1)
    except EmptyPage:
        context['my_books'] = paginator.page(paginator.num_pages)
    return render(request, 'library/books-that-i-already-read.html', context)

#Ekleme Kütüphane, Okunacaklar, Bitenler, Şuan Okuduklarım

@login_required(login_url="login")  
@csrf_exempt
def add_to_my_library(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user.id
    if request.is_ajax():
        data = BookUserList(user_id=current_user, booksList_id=id)
        try:
            q1 = BookUserList.objects.get(user_id=current_user, booksList_id=id)
        except BookUserList.DoesNotExist:
            q1 = None
        if q1 != None:
            message = "Kitap kütüphanenizde zaten mevcut"
            return HttpResponse(message)
        else:
            data.save()
            message = "Kütüphanenize eklendi"
            return HttpResponse(message)
    return HttpResponseRedirect(reverse('books', args=None))

@login_required(login_url="login")  
@csrf_exempt
def add_to_i_will(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user.id
    if request.is_ajax():
        count_books(request)
        obj = BookUserList.objects.get(user_id=current_user, id=id)
        data = BookUserList(user_id=current_user, pk=id, booksList=obj.booksList, status2='okunacaklar')
        try:
            q1 = BookUserList.objects.get(user_id=current_user, booksList=obj.booksList, status2='okunacaklar')
        except BookUserList.DoesNotExist:
            q1 = None
        if q1 != None:
            message = "Kitap zaten okunacaklar bölümünde"
            return HttpResponse(message)
        else:
            data.save()
            message = "Okunacaklara eklendi"
            return HttpResponse(message)
       
    return HttpResponseRedirect(url)

@login_required(login_url="login")  
@csrf_exempt
def add_to_iam_reading_now(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user.id
    if request.is_ajax():
        count_books(request)
        obj = BookUserList.objects.get(user_id=current_user, pk=id)
        data = BookUserList(user_id=current_user, pk=id, booksList=obj.booksList, status2='simdi_okuduklarım')
        try:
            q1 = BookUserList.objects.get(user_id=current_user,  booksList=obj.booksList,  status2='simdi_okuduklarım')
        except BookUserList.DoesNotExist:
            q1 = None
        if q1 != None:
            message = "Kitap zaten şu anda okunanlar bölümünde"
            return HttpResponse(message)
        else:
            data.save()
            message = "Şu an okunanlara eklendi"
            return HttpResponse(message)
    
    return HttpResponseRedirect(url)  

@login_required(login_url="login")  
@csrf_exempt
def add_to_i_read(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user.id
    if request.is_ajax():
        count_books(request)
        obj = BookUserList.objects.get(user_id=current_user, pk=id)
        data = BookUserList(user_id=current_user, pk=id, booksList=obj.booksList, status2='bitenler')
        try:
            q1 = BookUserList.objects.get(user_id=current_user, booksList=obj.booksList, status2='bitenler')
        except BookUserList.DoesNotExist:
            q1 = None
        if q1 != None:
            message = "Kitap zaten bitenler bölümünde"
            return HttpResponse(message)
        else:
            data.save()
            message =  "Bitenler bölümüne eklendi"
            return HttpResponse(message)
    
    return HttpResponseRedirect(url)      


@login_required(login_url="login")  
def create_note(request, pid):
    context = dict()
    context['book'] = get_object_or_404(Book, id=pid)

    return render(request, 'library/add-note.html', context)


@login_required(login_url="login")  
def add_note(request, pid):
    context = dict()
    current_user = request.user
    url = request.META.get('HTTP_REFERER')
    form2 = BookNoteForm(request.POST or None)
    if request.method == 'POST':
        if form2.is_valid():
            print(form2)
            data2=BookNotes()
            data2.user=current_user
            data2.notes=form2.cleaned_data['notes']
            data2.booksList_id = pid
            data2.save()
            print('Thank You')
        return HttpResponseRedirect('/home')

@login_required(login_url="login")  
def list_notes(request, id):
    context = dict()
    current_user = request.user
    context['note'] = BookNotes.objects.filter(user_id=current_user.id, booksList__id=id)
    return render(request, 'library/book-note-content.html', context)

# @login_required(login_url="login")  
# def now_list_notes(request, id):
    context = dict()
    current_user = request.user
    context['note'] = BookNotes.objects.filter(user_id=current_user.id, booksList__id=id)
    return render(request, 'library/now-book-note-content.html', context)


#Search işlemleri

def note_search(request):
    context=dict()
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query=form.cleaned_data['search_query']
            context['note']=BookNotes.objects.filter(notes__icontains=search_query, user_id=request.user.id)
            return render(request, 'search-results.html', context)

    return HttpResponseRedirect(url)

def book_search(request):
    context=dict()
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query=form.cleaned_data['search_query']
            context['books']=Book.objects.filter(Q(author__icontains=search_query) | Q(title__icontains=search_query))
            return render(request, 'book-search-results.html', context)

    return redirect('books')

def personal_book_search(request):
    context=dict()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query=form.cleaned_data['search_query']
            context['books']=BookUserList.objects.filter(Q(booksList__author__icontains=search_query) | Q(booksList__title__icontains=search_query), user=request.user.id)
            return render(request, 'personal-book-search-results.html', context)
    
    return redirect('my_library')

def book_search_i_read(request):
    context=dict()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query=form.cleaned_data['search_query']
            context['books']=BookUserList.objects.filter(Q(booksList__author__icontains=search_query) | Q(booksList__title__icontains=search_query), user=request.user.id, status2='bitenler')
            return render(request, 'personal-book-search-results.html', context)
    
    return redirect('book_i_read')

def book_search_i_ll_read(request):
    context=dict()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query=form.cleaned_data['search_query']
            context['books']=BookUserList.objects.filter(Q(booksList__author__icontains=search_query) | Q(booksList__title__icontains=search_query), user=request.user.id, status2='okunacaklar')
            return render(request, 'personal-book-search-results.html', context)
    
    return redirect('book_ill_read')

def book_search_i_am_reading(request):
    context=dict()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query=form.cleaned_data['search_query']
            context['books']=BookUserList.objects.filter(Q(booksList__author__icontains=search_query) | Q(booksList__title__icontains=search_query), user=request.user.id, status2='simdi_okuduklarım')
            return render(request, 'personal-book-search-results.html', context)
    
    return redirect('book_iam_reading')