from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    # Authentication
    path('', views.home_redirect, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    
    # Books
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    
    # Members
    path('members/', views.members, name='members'),
    
    # Borrow/Return
    path('borrow/<int:book_id>/<int:member_id>/', views.borrow_book, name='borrow_book'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    
    # Logs
    path('logs/', views.logs, name='logs'),
    path('my-borrows/', views.my_borrows, name='my_borrows'),
] 