from django.contrib import admin
from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path(r'borrowed/', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),

    path('movie/', views.MovieListView.as_view(), name='movies'),
    path('movie/<int:pk>', views.MovieDetailView.as_view(), name='movie-detail'),
    path('movie/<int:pk>/delete', views.MovieDelete.as_view(), name='movie-delete'),
    path('movie/create', views.MovieCreate.as_view(), name='movie-create'),

    path('series/', views.SeriesListView.as_view(), name='series'),
    path('series/<int:pk>', views.SeriesDetailView.as_view(), name='series-detail'),
    path('series/<int:pk>/delete', views.SeriesDelete.as_view(), name='series-delete'),
    path('series/create', views.SeriesCreate.as_view(), name='series-create'),

    path('actor/', views.ActorListView.as_view(), name='actors'),
    path('actor/<int:pk>', views.ActorDetailView.as_view(), name='actor-detail'),
    path('actor/<int:pk>/delete', views.ActorDelete.as_view(), name='actor-delete'),
    path('actor/create', views.ActorCreate.as_view(), name='actor-create'),

    path('director/', views.DirectorListView.as_view(), name='directors'),
    path('director/<int:pk>', views.DirectorDetailView.as_view(), name='director-detail'),
    path('director/<int:pk>/delete', views.DirectorDelete.as_view(), name='director-delete'),
    path('director/create', views.DirectorCreate.as_view(), name='director-create'),

]
