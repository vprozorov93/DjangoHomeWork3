from django.shortcuts import render, redirect
from books.models import Book
from django.core.paginator import Paginator
from datetime import datetime, date


def index(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {'books': books}
    return render(request, template, context)


def books_on_date_view(request, slug):
    template = 'books/books_on_date.html'
    books = Book.objects.filter(pub_date=slug)
    pages = [s['pub_date'] for s in Book.objects.values('pub_date').distinct()]

    current_date = slug.split('-')
    current_date = date(int(current_date[0]), int(current_date[1]), int(current_date[2]))

    index_page = pages.index(current_date)

    neighbor_pages = dict()

    if 0 < index_page < len(pages)-1:
        neighbor_pages['<'] = str(pages[index_page-1])
        neighbor_pages['>'] = str(pages[index_page+1])
    elif index_page == 0:
        neighbor_pages['>'] = str(pages[index_page+1])
    elif index_page == len(pages)-1:
        neighbor_pages['<'] = str(pages[index_page-1])

    context = {'books': books,
               'pages': neighbor_pages,
               'date': slug}

    return render(request, template, context)
