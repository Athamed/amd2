from django.contrib import admin
from django.urls import path
from . import views
from .views import SignUpView, UserEditView, PasswordsChangeView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path(r'borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),

    path("signup/", SignUpView.as_view(), name="signup"),
    path("edit_user/", UserEditView.as_view(), name="edit_user"),

    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),

    path('games/', views.GameListView.as_view(), name='games'),
    path('game/<int:pk>', views.GameDetailView.as_view(), name='game-detail'),
    path('game/<int:pk>/update/', views.GameUpdate.as_view(), name='game-update'),
    path('game/<int:pk>/delete/', views.GameDelete.as_view(), name='game-delete'),
    path('game/<int:pk>/verify/', views.GameVerify.as_view(), name='game-verify'),
    path('game/<int:pk>/unverify/', views.GameUnverify.as_view(), name='game-unverify'),

    path('game/create/', views.GameCreate.as_view(), name='game-create'),

    path('developers/', views.DeveloperListView.as_view(), name='developers'),
    path('developer/<int:pk>', views.DeveloperDetailView.as_view(), name='developer-detail'),
    path('developer/<int:pk>/update', views.DeveloperUpdate.as_view(), name='developer-update'),

    path('developer/<int:pk>/delete', views.DeveloperDelete.as_view(), name='developer-delete'),
    path('developer/create/', views.DeveloperCreate.as_view(), name='developer-create'),

    #path('password/',auth_views.PasswordChangeView.as_view(template_name='polls/Profile/change_password.html')),
    path('password/',PasswordsChangeView.as_view(template_name='polls/Profile/change_password.html')),
    path('password_success', views.password_change_success, name="password_success"),

]
