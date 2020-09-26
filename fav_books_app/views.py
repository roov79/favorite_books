from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

### Login and Refistration

def index(request):
    request.session.flush()
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors =  Users.objects.reg_val(request.POST)
        if  len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/')
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = Users.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_pw)
        request.session['u_id'] = new_user.id
        return redirect('/books')
    return redirect('/')

def login(request):
    if request.method == "POST":
        errors = Users.objects.log_val(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        user = Users.objects.get(email=request.POST['email'])
        request.session['u_id'] = user.id
        return redirect('/books')
    return redirect('/')

def books(request):
    if 'u_id' not in request.session:
        return redirect('/')
    context = {
        'user': Users.objects.get(id=request.session['u_id']),
        'books_list': Books.objects.all(),
    }
    return render(request, 'books.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

### Books Actions

def add_book(request):
    if request.method == "POST":
        errors = Books.objects.book_val(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        user = Users.objects.get(id=request.session['u_id'])
        book = Books.objects.create(title=request.POST['title'], description=request.POST['desc'], uploaded_by=user)
        user.liked_books.add(book)
        return redirect('/books')
    return redirect('/books')

def book_info(request, id):
    if 'u_id' not in request.session:
        return redirect('/')
    context = {
        'user': Users.objects.get(id=request.session['u_id']),
        'book': Books.objects.get(id=id),
    }
    return render(request, 'book_info.html', context)

def edit_book(request, id):
    if request.method == 'POST':
        errors = Books.objects.book_val(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/book_info/{id}')
        book = Books.objects.get(id=id)
        book.title = request.POST['title']
        book.description = request.POST['desc']
        book.save()
        return redirect('/books')
    return redirect('/books')

def delete_book(request, id):
    del_book = Books.objects.get(id=id)
    del_book.delete()
    return redirect('/books')

def favorite(request, id):
    user = Users.objects.get(id=request.session["u_id"])
    book = Books.objects.get(id=id)
    user.liked_books.add(book)
    return redirect(f'/books')

def unfavorite(request, id):
    user = Users.objects.get(id=request.session["u_id"])
    book = Books.objects.get(id=id)
    user.liked_books.remove(book)
    return redirect(f'/books')