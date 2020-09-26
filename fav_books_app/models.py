from django.db import models
import re
import bcrypt

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UsersManager(models.Manager):
    def reg_val(self, postData):    
        errors = {}
        if len(postData['first_name']) == 0:
            errors['first_name']="First Name is required"
        elif len(postData['first_name']) < 2 or postData['first_name'].isalpha() != True :
            errors['first_name']="First Name should be at least 2 characters"
        if len(postData['last_name']) == 0:
            errors['last_name']="Last Name is required"
        elif len(postData['last_name']) < 2 or postData['last_name'].isalpha() != True :
            errors['last_name']="Last Name should be at least 2 characters"
        if len(postData['email']) == 0:
            errors['email']="Email is required"
        elif not email_regex.match(postData['email']):             
            errors['email'] = ("Invalid email address!")
        existing_user = Users.objects.filter(email=postData['email'])
        if len(existing_user) != 0:
            errors['email']="Email alredy exist"
        if len(postData['password']) == 0:
            errors['password']="Password is required"
        elif len(postData['password']) < 8:
            errors['password']="Password should be at least 8 characters"
        elif postData['password'] != postData['confirm_pw']:
            errors['confirm_pw']="Password does not match"
        return errors

    def log_val(self, postData):
        errors={}
        if len(postData['email']) == 0:
            errors['email']="Email is required"
        elif not email_regex.match(postData['email']):
            errors['email']="Invalid Email format"
        if len(postData['password']) == 0:
            errors['password']="Password is required"
        elif len(postData['password']) < 8:
            errors['password']="Password should be at least 8 characters"
        existing_user = Users.objects.filter(email=postData['email'])
        if len(existing_user) != 1:
            errors['email']="User not Found"
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) !=True:
            errors['email']="Emal and/or Password do not match"
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

class BooksManager(models.Manager):
    def book_val(self, postData):
        errors = {}
        if len(postData['title']) == 0:
            errors['title']="A title is required"
        if len(postData['desc']) == 0:
            errors['description']="A description is required"
        return errors

class Books(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(Users, related_name="books_uploaded", on_delete=models.CASCADE)
    users_likes = models.ManyToManyField(Users, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BooksManager()