from django.db import models
import bcrypt
import re 

class UserManager(models.Manager):
    def register_validator(self, postData):
        # returns a dict with erros
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        
        # First Name - required; at least 2 characters; letters only
        # Last Name - required; at least 2 characters; letters only
        # Email - required; valid format
        # Password - required; at least 8 characters; matches password confirmation
        
        if len(postData["first_name"]) < 2:
            errors['first_name'] = "First name should be at least 2 characters"
        
        if len(postData["last_name"]) < 2:
            errors['last_name'] = "First name should be at least 2 characters"
        
        # 'string'.isalpha()
        if not (postData['first_name'].isalpha()):
            errors['first_name'] = "First name should contain letters only!"
        
        if not (postData['last_name'].isalpha()):
            errors['last_name'] = "Last name should contain letters only!"
        
        if len(postData['email']) < 5:
            errors['email'] = "email should at least be 5 characters long"
            #filter returns a list
        # to filter reg with the same email
        if len(User.objects.filter(email=postData['email'])) != 0:
            errors['email_check'] = "email already exists"
            
        if len(postData["password_hash"]) < 8:
            errors['password_hash'] = "password should at least be 8 characters long"  
        if postData["password_hash"] != postData['confirm_password']:
            errors['password_hash'] = "Password doesn't match!"
                
        return errors
    
    def login_validator(self, postData):
        errors = {}
        # EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # if not EMAIL_REGEX.match(postData['email']):
        #     errors['email'] = "Invalid email address!"
            
        user = User.objects.filter(email=postData['email'])
        
        if len(User.objects.filter(email=postData['email'])) == 0:
            # warning messages should not be specific
            errors['email'] = "Email does not match!"
        else:    
            if not bcrypt.checkpw(postData['password'].encode(), user[0].password_hash.encode()):
                errors['password'] = "Password doesn't match"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=250)
    password_hash = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    # liked_books = a list of books a given user likes
    # books_uploaded = a list of books uploaded by a given user
    objects = UserManager()

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        
        if len(postData["title"]) == 0:
            errors['title'] = "Title is required"
        
        if len(postData['description']) < 5:
            errors['description'] = "Description must have at least 5 characters"
            
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(null=True, blank=True)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    # uploaded_by = user who uploaded a given book
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    # users_who_like = a list of users who like a given book
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    objects = BookManager()
