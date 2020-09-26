from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.books),
    path('logout', views.logout),
    path('add_book', views.add_book),
    path('book_info/<int:id>', views.book_info),
    path('edit_book/<int:id>', views.edit_book),
    path('delete_book/<int:id>', views.delete_book),
    path('favorite/<int:id>', views.favorite),
    path('unfavorite/<int:id>', views.unfavorite),
]