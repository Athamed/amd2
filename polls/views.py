import datetime
from time import time

import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from polls.forms import RenewBookForm, MovieForm, SeriesForm, ActorForm, DirectorForm
from polls.models import Author
from .forms import GameForm, EditUserForm, PasswordChangingForm
from .models import Book, BookInstance
from .models import Game, Developer, Profile
from .models import Movie, Series, Actor, Director, Language, MovieSeriesGenre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


# @method_decorator(login_required, name='dispatch')
class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'polls/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'polls/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'polls/book_renew_librarian.html', context)


class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}


class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__'  # Not recommended (potential security issue if more fields added)


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    template_name = "polls/book_form.html"


class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')


class GameCreate(CreateView):
    model = Game
    form_class = GameForm
    # fields = ['title', 'developer', 'date_of_release', 'genre', 'mode', 'summary']
    template_name = "polls/Game/game_form.html"


class GameDetailView(generic.DetailView):
    """Generic class-based detail view for a game."""
    model = Game
    template_name = 'polls/Game/game_detail.html'


class GameUpdate(UserPassesTestMixin, UpdateView):
    model = Game
    template_name = "polls/Game/game_form.html"
    fields = ['title', 'developer', 'date_of_release', 'genre', 'mode', 'summary', 'Verified']

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


# success_url = reverse_lazy('games')
#  template_name = "polls/Game/game_confirm_delete.html"


class GameDelete(UserPassesTestMixin, DeleteView):
    model = Game
    success_url = reverse_lazy('games')
    template_name = "polls/Game/game_confirm_delete.html"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class GameListView(generic.ListView):
    model = Game
    paginate_by = 10
    template_name = "polls/Game/game_list.html"

    def get_context_data(self, *args, **kwargs):
        game_list = Game.objects.order_by('title')
        context = super(GameListView, self).get_context_data(*args, **kwargs)
        context["game_list"] = game_list
        return context


class GameVerify(UserPassesTestMixin, generic.DetailView):
    model = Game
    # login_url = '/polls/error401'
    # redirect_field_name = None

    template_name = "polls/Game/game_verify.html"
    success_url = reverse_lazy('games')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class GameUnverify(UserPassesTestMixin, generic.DetailView):
    model = Game
    template_name = "polls/Game/game_unverify.html"
    success_url = reverse_lazy('games')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class DeveloperDetailView(generic.DetailView):
    """Generic class-based detail view for a developer."""
    model = Developer
    template_name = 'polls/Game/developer_detail.html'


class DeveloperDelete(UserPassesTestMixin, DeleteView):
    model = Developer
    success_url = reverse_lazy('developers')
    template_name = "polls/Game/developer_confirm_delete.html"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class DeveloperCreate(CreateView):
    model = Developer
    fields = ['company_name', 'date_of_foundation']
    template_name = "polls/Game/developer_form.html"


class DeveloperUpdate(UserPassesTestMixin, UpdateView):
    model = Developer
    fields = ['company_name', 'date_of_foundation']
    template_name = "polls/Game/developer_form.html"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class DeveloperListView(generic.ListView):
    model = Developer
    paginate_by = 10
    template_name = "polls/Game/developer_list.html"


class PasswordsChangeView(PasswordChangeView):
    # form_class = PasswordChangeForm #domyślne
    form_class = PasswordChangingForm  # Nowe z forms.py
    template_name = 'polls/Profile/change_password.html'
    success_url = reverse_lazy('password_success')


def password_change_success(request):
    return render(request, 'polls/Profile/password_success.html')


class UserEditView(UserPassesTestMixin, generic.UpdateView):
    form_class = EditUserForm
    success_url = reverse_lazy("index")
    template_name = "polls/Game/edit_user.html"

    def get_object(self):
        return self.request.user

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('index')

class ProfilePageView(generic.DetailView):
    model = Profile
    template_name = "polls/Profile/user_profile.html"

    def get_context_data(self, *args, **kwargs):
        #users = Profile.objects.all()
        context = super(ProfilePageView, self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context["page_user"] = page_user
        return context


class MovieListView(generic.ListView):
    template_name = "polls/movie/movie_list.html"
    model = Movie
    paginate_by = 10


class MovieDetailView(generic.DetailView):
    template_name = "polls/movie/movie_detail.html"
    model = Movie


class MovieDelete(UserPassesTestMixin, DeleteView):
    model = Movie
    template_name = "polls/movie/movie_delete.html"
    success_url = reverse_lazy('movies')
    login_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class MovieCreate(UserPassesTestMixin, CreateView):
    model = Movie
    template_name = "polls/movie/movie_create.html"
    form_class = MovieForm

    # fields = ['title', 'actors', 'director', 'date_of_release', 'language', 'genre', 'running_time']

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('login')


class MovieUpdate(UserPassesTestMixin, UpdateView):
    model = Movie
    template_name = "polls/movie/movie_create.html"
    form_class = MovieForm

    # fields = ['title', 'actors', 'director', 'date_of_release', 'language', 'genre', 'running_time']

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class MovieVerify(UserPassesTestMixin, generic.DetailView):
    model = Movie
    template_name = "polls/movie/movie_verify.html"

    # success_url = reverse_lazy('movies')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class MovieUnverify(UserPassesTestMixin, generic.DetailView):
    model = Movie
    template_name = "polls/movie/movie_unverify.html"

    # success_url = reverse_lazy('movies')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class SeriesListView(generic.ListView):
    template_name = "polls/movie/series_list.html"
    model = Series
    paginate_by = 10


class SeriesDetailView(generic.DetailView):
    template_name = "polls/movie/series_detail.html"
    model = Series


class SeriesDelete(UserPassesTestMixin, DeleteView):
    model = Series
    template_name = "polls/movie/series_delete.html"
    success_url = reverse_lazy('series')
    login_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class SeriesCreate(UserPassesTestMixin, CreateView):
    model = Series
    form_class = SeriesForm
    template_name = "polls/movie/series_create.html"

    # fields = ['title', 'actors', 'director', 'date_of_release', 'language', 'genre', 'number_of_seasons']

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('login')


class SeriesUpdate(UserPassesTestMixin, UpdateView):
    model = Series
    template_name = "polls/movie/series_create.html"
    form_class = SeriesForm

    # fields = ['title', 'actors', 'director', 'date_of_release', 'language', 'genre', 'running_time']

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class SeriesVerify(UserPassesTestMixin, generic.DetailView):
    model = Series
    template_name = "polls/movie/series_verify.html"

    # success_url = reverse_lazy('series')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class SeriesUnverify(UserPassesTestMixin, generic.DetailView):
    model = Series
    template_name = "polls/movie/series_unverify.html"

    # success_url = reverse_lazy('series')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class ActorListView(generic.ListView):
    template_name = "polls/movie/actor_list.html"
    model = Actor
    paginate_by = 10


class ActorDetailView(generic.DetailView):
    template_name = "polls/movie/actor_detail.html"
    model = Actor


class ActorDelete(UserPassesTestMixin, DeleteView):
    model = Actor
    template_name = "polls/movie/actor_delete.html"
    success_url = reverse_lazy('actors')

    # login_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class ActorCreate(UserPassesTestMixin, CreateView):
    model = Actor
    form_class = ActorForm
    template_name = "polls/movie/actor_create.html"

    # fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'specialisation']

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('login')


class ActorUpdate(UserPassesTestMixin, UpdateView):
    model = Actor
    template_name = "polls/movie/actor_create.html"
    form_class = ActorForm

    # fields = ['title', 'actors', 'director', 'date_of_release', 'language', 'genre', 'running_time']

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class ActorVerify(UserPassesTestMixin, generic.DetailView):
    model = Actor
    template_name = "polls/movie/actor_verify.html"

    # success_url = reverse_lazy('series')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class ActorUnverify(UserPassesTestMixin, generic.DetailView):
    model = Actor
    template_name = "polls/movie/actor_unverify.html"

    # success_url = reverse_lazy('series')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class DirectorListView(generic.ListView):
    template_name = "polls/movie/director_list.html"
    model = Director
    paginate_by = 10


class DirectorDetailView(generic.DetailView):
    template_name = "polls/movie/director_detail.html"
    model = Director


class DirectorDelete(UserPassesTestMixin, DeleteView):
    model = Director
    template_name = "polls/movie/director_delete.html"
    success_url = reverse_lazy('directors')
    login_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class DirectorCreate(UserPassesTestMixin, CreateView):
    model = Director
    form_class = DirectorForm
    template_name = "polls/movie/director_create.html"

    # fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'amount_of_films']

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('login')


class DirectorUpdate(UserPassesTestMixin, UpdateView):
    model = Director
    template_name = "polls/movie/director_create.html"
    form_class = DirectorForm

    # fields = ['title', 'actors', 'director', 'date_of_release', 'language', 'genre', 'running_time']

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class DirectorVerify(UserPassesTestMixin, generic.DetailView):
    model = Director
    template_name = "polls/movie/director_verify.html"

    # success_url = reverse_lazy('series')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


class DirectorUnverify(UserPassesTestMixin, generic.DetailView):
    model = Director
    template_name = "polls/movie/director_unverify.html"

    # success_url = reverse_lazy('series')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('index')


def get_date_actor_director(date_of_birth, date_of_death):
    birth = [1, 1, 1]
    if date_of_birth:
        if date_of_birth.time:
            date_of_birth = date_of_birth.time['datetime']
            birth = date_of_birth.split("-")
        else:
            date_of_birth = None
    if not date_of_birth or birth[0] == '0' or birth[1] == '0' or birth[2] == '0':
        date_of_birth = None

    death = [1, 1, 1]
    if date_of_death:
        if date_of_death.time:
            date_of_death = date_of_death.time['datetime']
            death = date_of_death.split("-")
        else:
            date_of_birth = None
    if not date_of_death or birth[0] == '0' or death[1] == '0' or death[2] == '0':
        date_of_death = None
    return date_of_birth, date_of_death


def actors_scraping(movie):
    pk_list = []
    actors = movie.find_all('div', attrs={'data-testid': 'title-cast-item'})

    for actor_div in actors:
        name = actor_div.find('a', attrs={'data-testid': 'title-cast-item__actor'}).text
        # name = name.split()
        # first_name = name[0]
        # last_name = name[1]
        actor = Actor.objects.filter(full_name=name).first()
        if actor:
            director_pk = actor.pk
            pk_list.append(director_pk)
        else:
            link = actor_div.find('a', attrs={'data-testid': 'title-cast-item__actor'})
            url = "https://www.imdb.com" + link['href']
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            actor = soup.find('div', attrs={'id': 'name-overview-widget'})

            # specialisation = actor.a.span.text.replace('\n', '')
            specialisation = actor.find_all('span', attrs={'class': 'itemprop'})[1].text.replace('\n', '')
            date_of_birth = soup.find('div', attrs={'id': 'name-born-info'})
            date_of_death = soup.find('div', attrs={'id': 'name-death-info'})
            date_of_birth, date_of_death = get_date_actor_director(date_of_birth, date_of_death)

            actor_instance = Actor.objects.create(
                full_name=name,
                specialisation=specialisation,
                date_of_birth=date_of_birth,
                date_of_death=date_of_death,
                Verified=True
            )
            pk_list.append(actor_instance.pk)
    return pk_list


def language_scraping(movie):
    languages_pk = []
    languages = []
    # language = movie.find_all('section')[11]
    # try:
    # language = language.find('div', attrs={'class': 'sc-f65f65be-0 ktSkVi'})
    # language = language.find('ul', attrs={'class': 'ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base'})
    language = movie.find('li', attrs={'data-testid': 'title-details-languages'})
    languages = language.div.ul.find_all('li')
    # except AttributeError:
    #  pass
    for li in languages:
        language = Language.objects.filter(name=li.a.text).first()
        if language:
            language_pk = language.pk
            languages_pk.append(language_pk)
        else:
            language_instance = Language.objects.create(name=li.a.text)
            languages_pk.append(language_instance.pk)
    return languages_pk


def date_scraping(movie, months):
    # language_release_date = movie.find_all('section')[11]
    # language_release_date = language_release_date.find_all('li')
    date = movie.find('li', attrs={'data-testid': 'title-details-releasedate'})
    link = date.div.ul.li.a
    release_date = link.text.split(" ")
    if len(release_date) == 4:
        release_date = " ".join(release_date[0:3])
        release_date = release_date.replace(",", "")
        release_date = release_date.split()
        release_date = release_date[2] + "-" + months[release_date[0]] + "-" + release_date[1]
    if len(release_date) == 3:
        link = link['href']
        url = "https://www.imdb.com" + link
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        release_dates = soup.find_all('tr', attrs={'class': 'ipl-zebra-list__item release-date-item'})
        for date in release_dates:
            date = date.find_all('td', attrs={'class': 'release-date-item__date'}).text.split(" ")
            if len(date) == 3:
                release_date = date
                break
        release_date = release_date[2] + "-" + months[release_date[1]] + "-" + release_date[0]
    # if len(release_date[0]) == 1:
        # release_date[0] = '0' + release_date[0]

    return release_date


def directors_scraping(movie):
    pk_list = []
    directors = movie.find('div', attrs={'class': 'sc-fa02f843-0 fjLeDR'}).ul.li.div.ul
    try:
        directors = directors.find_all('li')
    except AttributeError:
        directors = directors.li
    for li in directors:
        name = li.a.text
        # name = name.split()
        # first_name = name[0]
        # last_name = name[1]
        director = Director.objects.filter(full_name=name).first()
        if director:
            director_pk = director.pk
            pk_list.append(director_pk)
        else:
            link = li.a['href']
            url = "https://www.imdb.com" + link
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            director = soup.find('div', attrs={'id': 'name-overview-widget'})
            # name = director.h1.span.text
            # name = name.split()
            # first_name = name[0]
            # last_name = name[1]
            date_of_birth = director.find('div', attrs={'id': 'name-born-info'})
            date_of_death = director.find('div', attrs={'id': 'name-death-info'})
            # to jest do zmiany
            amount_of_films = 10
            date_of_birth, date_of_death = get_date_actor_director(date_of_birth, date_of_death)

            director_instance = Director.objects.create(
                full_name=name,
                date_of_birth=date_of_birth,
                date_of_death=date_of_death,
                Verified=True,
                amount_of_films=amount_of_films
            )
            pk_list.append(director_instance.pk)
    return pk_list


def movie_genres_scraping(movie):
    pk_list = []
    # genres = movie.find('div', attrs={'class': 'sc-388740f9-0 hJjREK'})
    # genres = genres.ul
    # genres = movie.find('ul', attrs={'class': 'ipc-metadata-list ipc-metadata-list--dividers-all sc-388740f9-1 IjgYL ipc-metadata-list--base'})
    genres = movie.find('div', attrs={'data-testid': 'genres'})
    genres = genres.find_all('li')
    for name in genres:
        name = name.text
        genre = MovieSeriesGenre.objects.filter(name=name).first()
        if genre:
            pk_list.append(genre.pk)
        else:
            genre_instance = MovieSeriesGenre.objects.create(name=name)
            pk_list.append(genre_instance.pk)
    return pk_list


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def scrape_movies(request):
    times = []
    counter = 0
    months = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06", "July": "07",
              "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"}
    url = "https://www.imdb.com/chart/top"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    table = soup.find('table', {'class': 'chart full-width'})
    movies_data = table.tbody.find_all('tr')
    movies = []
    for tr in movies_data:
        start = time()
        link = tr.td.a
        url = "https://www.imdb.com" + link['href']
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        movie = soup.find('div', attrs={
            'class': 'ipc-page-content-container ipc-page-content-container--full sc-b1984961-0 kXDasd'})
        # movie = soup.find('div', attrs={'class': 'ipc-page-grid ipc-page-grid--bias-left'})
        title = movie.find('div', attrs={'class': 'sc-94726ce4-2 khmuXj'}).h1.text
        test = Movie.objects.filter(title=title).first()
        if test:
            continue
        counter += 1
        languages_pk = language_scraping(movie.find('div', attrs={'class': 'ipc-page-grid ipc-page-grid--bias-left'}))
        release_date = date_scraping(movie.find('div', attrs={'class': 'ipc-page-grid ipc-page-grid--bias-left'}),
                                     months)
        genres_pk = movie_genres_scraping(movie)
        running_time = movie.find('div', attrs={'class': 'sc-94726ce4-3 eSKKHi'}).ul.find_all('li')
        running_time = running_time[2].text
        summary = movie.find('span', attrs={'class': 'sc-16ede01-1 kgphFu'}).text
        directors_pk = directors_scraping(movie)
        actors_pk = actors_scraping(movie.find('div', attrs={'class': 'ipc-page-grid ipc-page-grid--bias-left'}))

        movie_object = Movie.objects.create(
            title=title,
            date_of_release=release_date,
            running_time=running_time,
            summary=summary,
            Verified=True
        )
        movie_object.director.set(directors_pk)
        movie_object.language.set(languages_pk)
        movie_object.genre.set(genres_pk)
        movie_object.actors.set(actors_pk)
        end = time()
        times.append(end - start)
        if counter == 10:
            break
    return render(request, "polls/movie/scrape_movies.html", {'movies': movies, 'times': times})
