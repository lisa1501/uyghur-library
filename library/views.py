import os
import PyPDF2
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from .forms import BookForm, CommentForm
from .models import Book, Category, Comment
from django.contrib import messages
from datetime import datetime
from django.core.mail import send_mail
from django.db.models import Avg

def home(request):
    trans = translate(language='ko')
    return render(request, 'library/home.html', {'trans': trans})

def translate(language):
    current_language = get_language()
    try:
        activate(language)
        text=gettext('Library')
    finally:
        activate(current_language)
    return text

def faq(request):
    return render(request, 'library/faq.html')

def searchbar(request):
    if request.method=="GET":
        search = request.GET.get('q')
        if search:
            book = Book.objects.all().filter(title__icontains=search)
            if book:
                category = request.GET.get('category')
                if category == None:
                    books = Book.objects.all()
                else:
                    books = Book.objects.filter(category__name=category)
                categories = Category.objects.all()
                return render(request, 'library/search.html', {'book':book, 'books': books, 'categories': categories})
            else:
                messages.warning(request, 'Book not found.')
                return render(request, 'library/book_list.html')
        else:
            return render(request, 'library/home.html')

def book_list(request):
    category = request.GET.get('category')
    if category == None:
        books = Book.objects.all()
    else:
        books = Book.objects.filter(category__name=category)
    categories = Category.objects.all()
    
    return render(request, 'library/book_list.html', {
        'books': books,
        'categories':categories,
    })

def book_info(request, isbn):
    book = get_object_or_404(Book, ISBN=isbn)
    file=str(book.pdf)
    pdf_file=(file.split('/'))[-1]
    num_comments = Comment.objects.filter(book=book).count()
    comments = Comment.objects.filter(book=book)
    average=comments.aggregate(Avg("rate"))["rate__avg"]

    is_favorite = False
    if book.favorite.filter(id=request.user.id).exists():
        is_favorite = True

    return render(request, 'library/book_info.html', 
                    {'book':book, 
                    'is_favorite': is_favorite,
                    'num_comments': num_comments, 
                    'comments': comments,
                    'average':average,
                    'pdf_file':pdf_file})

def add_favorite(request, isbn):
    book = get_object_or_404(Book, ISBN=isbn)
    if book.favorite.filter(id=request.user.id).exists():
        book.favorite.remove(request.user)
    else:
        book.favorite.add(request.user)

    return redirect(reverse('book_info', args=[isbn])) 

def add_comment(request, isbn):
    book = get_object_or_404(Book, ISBN=isbn)
    form = CommentForm(instance=book)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data['comment_body']
            rate = form.cleaned_data['rate']
            c = Comment(book=book, commenter_name=name, comment_body=body, date_added=datetime.now(), rate=rate)
            c.save()
            return redirect(reverse('book_info', args=[isbn]))  
        else:
            return redirect(reverse('book_info', args=[isbn]))    
    else:
        form = CommentForm()    

    context = {
        'form': form
    }
    return render(request, 'library/book_info.html', context)

def delete_comment(request, isbn, comment_pk):
    comment = Comment.objects.filter(id=comment_pk)
    comment.delete()
    return redirect(reverse('book_info', args=[isbn]))

def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            check_book = Book.objects.filter(ISBN=request.POST['ISBN'])
            if not check_book:
                new_book = form.save(commit=False)
                pdf = request.FILES['pdf']
                reader = PyPDF2.PdfReader(pdf)
                pages=len(reader.pages)
                new_book.pages = int(float(pages))
                new_book.save()
                messages.success(request, 'Book has been successfully uploaded.')
                return redirect('book_list')
            else:
                messages.warning(request, 'Book already exists.')
                return render(request, 'library/upload_book.html', {'form': BookForm()})
    else:
        form = BookForm()
    return render(request, 'library/upload_book.html', {
        'form': form
    })

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        }
        message = '''
        New message: {}
        From: {}
        '''.format(data['message'], data['email'])
        send_mail(data['subject'], message, '', ['capstoneprojectadac15@gmail.com'])
        messages.success(request, 'Message sent! You should receive a response within 24-48 hours.')
    return render(request, 'library/contact_us.html', {})

