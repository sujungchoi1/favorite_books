from django.shortcuts import render, redirect
from django.contrib import messages

import bcrypt
from .models import User, UserManager, Book, BookManager

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    # Validate the user input from the form
    # -- comparing the password with the pw confirm
    # Logic to check if email is already in database
    
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        password = request.POST['password_hash']
        pw_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()  # create
        print(pw_hash)

        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password_hash = pw_hash
        )
        print(request.POST)

        request.session['userid'] = User.objects.last().id
        print(request.session['userid'])
        return redirect("/books")


def login(request):
    # Are the user in the database? 
    # get will fail/error out if user is not in the database
    # get the user from the database -- if list is empty => no user with the matching data
    if request.method == 'POST':
        # filter reutnrs a list of user (query set is a list)
        user = User.objects.filter(email=request.POST['email']) 
        if user:
            logged_user = user[0] #only 1 user in the query set
        
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        # if bcrypt.checkpw(request.POST['password'].encode(), user[0].password_hash.encode()):
        request.session['userid'] = logged_user.id
        print("*****", logged_user.id)
        return redirect('/books')
        #else: when password doesn't match (line 46 on models.py)
            
def books(request):
    context = {
        'users': User.objects.all(),
        'this_user': User.objects.get(id=request.session['userid']),
        'books': Book.objects.all()
        
    }
    return render(request, "add.html", context)


def processNewBook(request):
    if request.method == 'POST':
        errors = Book.objects.book_validator(request.POST)
        print(errors)
    
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            # redirect the user back to the form to fix the errors
            return redirect('/books')
        
        new_book = Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['description'],
            uploaded_by = User.objects.get(id=request.session['userid']),
        )
        # from Sadie
        # new_book.users_who_like.add(User.objects.get(id=request.session['userid']))
        
        # user.liked_books is a list
        user = User.objects.get(id=request.session['userid'])
        user.liked_books.add(new_book.id)
        
        # save not needed - only for updating fields
        print(request.POST)
        print("**", user.liked_books.last().title)
        #doesn't work - printing 'None'
        
        # book9 = Book.objects.get(id=9)
        # liked_book_9 = book9.users_who_like.all()
        # for user in liked_book_9:
        #     user.first_name
        
    return redirect('/books')

def update(request, book_id):
    # each_book = Book.objects.get(id=book_id)
    context = {
        'users': User.objects.all(),
        'this_user': User.objects.get(id=request.session['userid']),
        'books': Book.objects.all(),
        'book': Book.objects.get(id=book_id)
        # 'this_book': Book.objects.get(id=request.session['bookid'])
    }
    return render(request, "update.html", context)

def processUpdate(request, book_id):
    update_book = Book.objects.get(id=book_id)
    update_book.title = request.POST['title']
    update_book.desc = request.POST['description']
    update_book.save()
    print("**updating book info")
    return redirect('/books/update/' +str(book_id))

def detail(request, book_id):
    context = {
        'users': User.objects.all(),
        'this_user': User.objects.get(id=request.session['userid']),
        'books': Book.objects.all(),
    }
    return render(request, "detail.html", context)

def delete(request, book_id):
    delete_book = Book.objects.get(id=book_id)
    delete_book.delete()
    print("** Deleting the book")
    return redirect('/books')

# def logout(request):
#     # Have the logout link clear the session
#     del request.session['userid']
#     # request.session.clear()
#     #requeset.session.pop('userid')
#     print("***you're logged out")
#     return redirect('/')

def logout(request):
    request.session.clear()
    
    print("**Logged Out!")
    messages.success(request, "You have been logged out")
    return redirect('/')