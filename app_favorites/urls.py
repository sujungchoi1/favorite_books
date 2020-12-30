from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.books),
    path('processNewBook', views.processNewBook),
    path('processUpdate/<int:book_id>', views.processUpdate),
    path('books/update/<int:book_id>', views.update),
    path('books/detail/<int:book_id>', views.detail),
    path('<int:book_id>/delete', views.delete),
    path('logout', views.logout),
]
