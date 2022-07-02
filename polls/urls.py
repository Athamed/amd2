from django.urls import path

from . import views
from .views import SignUpView, UserEditView, PasswordsChangeView, ProfilePageView, LikeView, UserProfileEditView

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
    path("edit_profile/", UserProfileEditView.as_view(), name="edit_profile"),

    path("profile/<int:pk>", ProfilePageView.as_view(), name="profile-page"),
    path("like/<int:pk>", LikeView, name="like_profile"),

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

    path('password/', PasswordsChangeView.as_view()),
    path('password_success', views.password_change_success, name="password_success"),

    path('movie/', views.MovieListView.as_view(), name='movies'),
    path('movie/<int:pk>', views.MovieDetailView.as_view(), name='movie-detail'),
    path('movie/<int:pk>/delete', views.MovieDelete.as_view(), name='movie-delete'),
    path('movie/create', views.MovieCreate.as_view(), name='movie-create'),
    path('movie/<int:pk>/update', views.MovieUpdate.as_view(), name='movie-update'),
    path('movie/<int:pk>/verify', views.MovieVerify.as_view(), name='movie-verify'),
    path('movie/<int:pk>/unverify', views.MovieUnverify.as_view(), name='movie-unverify'),
    # TO JEST PRAWDOPODOBNIE DO ZMIANY LUB WYWALENIA
    # ZAKOMENTOWANE DLA BEZPIECZEŃSTWA BO TO WORK IN PROGRESS
    # path('scrape/', views.scrape, name='scrape'),
    # path('scrape/', views.scrape_actors, name='scrape'),
    path('scrapemovies/', views.scrape_movies, name='scrape-movies'),

    path('series/', views.SeriesListView.as_view(), name='series'),
    path('series/<int:pk>', views.SeriesDetailView.as_view(), name='series-detail'),
    path('series/<int:pk>/delete', views.SeriesDelete.as_view(), name='series-delete'),
    path('series/create', views.SeriesCreate.as_view(), name='series-create'),
    path('series/<int:pk>/update', views.SeriesUpdate.as_view(), name='series-update'),
    path('series/<int:pk>/verify', views.SeriesVerify.as_view(), name='series-verify'),
    path('series/<int:pk>/unverify', views.SeriesUnverify.as_view(), name='series-unverify'),

    path('actor/', views.ActorListView.as_view(), name='actors'),
    path('actor/<int:pk>', views.ActorDetailView.as_view(), name='actor-detail'),
    path('actor/<int:pk>/delete', views.ActorDelete.as_view(), name='actor-delete'),
    path('actor/create', views.ActorCreate.as_view(), name='actor-create'),
    path('actor/<int:pk>/update', views.ActorUpdate.as_view(), name='actor-update'),
    path('actor/<int:pk>/verify', views.ActorVerify.as_view(), name='actor-verify'),
    path('actor/<int:pk>/unverify', views.ActorUnverify.as_view(), name='actor-unverify'),

    path('director/', views.DirectorListView.as_view(), name='directors'),
    path('director/<int:pk>', views.DirectorDetailView.as_view(), name='director-detail'),
    path('director/<int:pk>/delete', views.DirectorDelete.as_view(), name='director-delete'),
    path('director/create', views.DirectorCreate.as_view(), name='director-create'),
    path('director/<int:pk>/update', views.DirectorUpdate.as_view(), name='director-update'),
    path('director/<int:pk>/verify', views.DirectorVerify.as_view(), name='director-verify'),
    path('director/<int:pk>/unverify', views.DirectorUnverify.as_view(), name='director-unverify'),

]
