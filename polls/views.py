from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from polls.forms import RenewBookForm, MovieForm, SeriesForm, ActorForm, DirectorForm
from .models import Book, Author, BookInstance
from .models import Movie, Series, Actor, Director, Language
from polls.forms import RenewBookForm
from .models import Book, Author, BookInstance, Game, Developer
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from polls.models import Author

from bs4 import BeautifulSoup
import pandas as pd
import requests
from rest_framework import generics
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from time import time

from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordChangeView
from .forms import GameForm, EditUserForm, PasswordChangingForm


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


"""
def scrape(request):
    url = "https://www.imdb.com/chart/top"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find('table',  {'class': 'chart full-width'})
    rows = table.find_all('tr')
    movies = []
    for row in rows:
        image = row.find('img')
        if image:
            movies.append(image['alt'])
            Movie.objects.create(title=image['alt'], date_of_release='2020-10-10')
    return render(request, "polls/movie/scrape_test.html", {'movies': movies})


def scrape_actors(request):
    url = "https://www.imdb.com/list/ls060678014/?sort=list_order,asc&mode=detail&page=1&ref_=nmls_vm_dtl"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    actors_data = soup.findAll('div', attrs={'class': 'lister-item mode-detail'})
    # rows = table.find_all('tr')
    actors = []
    for actor_div in actors_data:
        link = actor_div.h3.a
        url2 = "https://www.imdb.com"+link['href']
        response2 = requests.get(url2)
        soup2 = BeautifulSoup(response2.content, "html.parser")
        actor = soup2.find('div', attrs={'class': 'name-overview-widget'})

        name = actor.h1.span.text
        name = name.split()
        first_name = name[0]
        last_name = name[1]
        specialisation = actor.a.span.text.replace('\n', '')
        date_of_birth = actor.find('div', attrs={'id': 'name-born-info'})
        date_of_death = actor.find('div', attrs={'id': 'name-death-info'})

        if date_of_birth:
            #actors.append(date_of_birth.time['datetime'])
            Actor.objects.update_or_create(
                first_name=first_name,
                last_name=last_name,
                #specialisation=specialisation,
                #date_of_birth=date_of_birth.time['datetime'],
                #date_of_death=date_of_death.time['datetime'],
                #Verified=True,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'specialisation': specialisation,
                    'date_of_birth': date_of_birth.time['datetime'],
                    'Verified': True
                }
            )
        else:
            Actor.objects.create(
                first_name=first_name,
                last_name=last_name,
                #specialisation=specialisation,
                #date_of_birth=date_of_birth.time['datetime'],
                #Verified=True,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'specialisation': specialisation,
                    #'date_of_birth': date_of_birth.time['datetime'],
                    'Verified': True
                }
            )
    return render(request, "polls/movie/scrape.html")
"""


def scrape_movies(request):
    languages_pk = []
    start = time()
    url = "https://www.imdb.com/chart/top"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find('table', {'class': 'chart full-width'})
    movies_data = table.tbody.find_all('tr')
    movies = []
    for tr in movies_data:
        link = tr.td.a
        url = "https://www.imdb.com" + link['href']
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        movie = soup.find('div', attrs={'class': 'ipc-page-grid ipc-page-grid--bias-left'})

        language_release_date = movie.find_all('section')[11]
        language_release_date = language_release_date.find('div', attrs={'class': 'sc-f65f65be-0 ktSkVi'})
        language_release_date = language_release_date.find('ul', attrs={
            'class': 'ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base'})
        language = language_release_date.find('li', attrs={'data-testid': 'title-details-languages'})
        languages = language.div.ul.find_all('li')
        language_release_date = language_release_date.find_all('li')
        release_date = language_release_date[0].div.ul.li.a.text.split(" ")
        release_date = " ".join(release_date[0:3])
        # languages = language.div.ul.find_all('li')
        for li in languages:
            language = Language.objects.filter(name=li.a.text).first()
            if language:
                language_pk = language.pk
                languages_pk.append(language_pk)
            else:
                language_instance = Language.objects.create(name=li.a.text)
                languages_pk.append(language_instance.pk)
        running_time = movie.find('div', attrs={'class': 'sc-94726ce4-3 eSKKHi'}).ul.find_all('li')
        running_time = running_time[2].text
        title = movie.find('div', attrs={'class': 'sc-94726ce4-2 khmuXj'}).h1.text
        # name = movie.find('div', attrs={'class': 'sc-fa02f843-0 fjLeDR'}).ul.li.div.ul.li.a.text
        # name = name.split()
        # first_name = name[0]
        # last_name = name[1]
        directors = movie.find('div', attrs={'class': 'sc-fa02f843-0 fjLeDR'}).ul.li.div.ul
        try:
            directors = directors.find_all('li')
        except AttributeError:
            directors = directors.li
        pk_list = []
        for li in directors:
            name = li.a.text
            name = name.split()
            first_name = name[0]
            last_name = name[1]
            director = Director.objects.filter(first_name=first_name, last_name=last_name).first()
            if director:
                director_pk = director.pk
                pk_list.append(director_pk)
            else:
                link = li.a['href']
                url = "https://www.imdb.com" + link
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                director = soup.find('div', attrs={'class': 'name-overview-widget'})
                name = director.h1.span.text
                name = name.split()
                first_name = name[0]
                last_name = name[1]
                date_of_birth = director.find('div', attrs={'id': 'name-born-info'})
                date_of_death = director.find('div', attrs={'id': 'name-death-info'})
                # to jest do zmiany
                amount_of_films = 10

                if not date_of_birth:
                    date_of_birth = None
                else:
                    date_of_birth = date_of_birth.time['datetime']

                if not date_of_death:
                    date_of_death = None
                else:
                    date_of_death = date_of_death.time['datetime']

                director_instance = Director.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=date_of_birth,
                    date_of_death=date_of_death,
                    Verified=True,
                    amount_of_films=amount_of_films
                )
                pk_list.append(director_instance.pk)
        # specialisation = actor.a.span.text.replace('\n', '')
        # date_of_birth = actor.find('div', attrs={'id': 'name-born-info'})
        # date_of_death = actor.find('div', attrs={'id': 'name-death-info'})

        if title:
            movies.append(title)
        movie_object = Movie.objects.create(title=title, date_of_release=release_date, running_time=running_time)
        # movie_object = Movie.objects.create()
        # movie_object.director = pk_list

        movie_object.director.set(pk_list)

        break
    end = time()
    return render(request, "polls/movie/scrape_movies.html", {'movies': movies, 'time': end - start})


""""
def scrape2(request):
    url = "https://www.imdb.com/list/ls060678014/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    actors = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})
    vector = []
    # enumerate rows to include index inside class name
    # starting index from 1
    for actor in actors:
        name = actor.h3.a.text
        vector.append(name)
        name = name.split()
        first_name = name[0]
        last_name = name[1]
        specialisation = actor.find('p', class_='text-muted text-small').text

        print({'first_name': first_name, 'last_name': last_name, 'specialisation': specialisation})

        # create objects in database
        Actor.objects.create(
            first_name=first_name,
            last_name=last_name,
            specialisation=specialisation,
        )
        # sleep few seconds to avoid database block
        # sleep(5)
    return render(request, "polls/movie/scrape.html", {'actors': vector})
"""


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
