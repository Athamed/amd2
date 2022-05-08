from django.contrib import admin
from django.urls import path
from . import views


# urlpatterns = [
#    path('', views.home, name="home"),
# ]

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
]
