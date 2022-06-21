from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from polls.forms import RenewBookForm
from .models import Book, Author, BookInstance
from .models import Movie, Series, Actor, Director
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from polls.models import Author


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
    template_name = "polls/movie_list.html"
    model = Movie
    paginate_by = 10


class MovieDetailView(generic.DetailView):
    template_name = "polls/movie_detail.html"
    model = Movie


class MovieDelete(UserPassesTestMixin, DeleteView):
    model = Movie
    template_name = "polls/movie_delete.html"
    success_url = reverse_lazy('movies')
    login_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.is_superuser


class MovieCreate(CreateView):
    model = Movie
    template_name = "polls/movie_create.html"
    fields = ['title', 'actors', 'director', 'date_of_release', 'language', 'genre', 'running_time']


class SeriesListView(generic.ListView):
    template_name = "polls/series_list.html"
    model = Series
    paginate_by = 10


class SeriesDetailView(generic.DetailView):
    template_name = "polls/series_detail.html"
    model = Series


class SeriesDelete(UserPassesTestMixin, DeleteView):
    model = Series
    template_name = ""
    success_url = reverse_lazy('series')
    login_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.is_superuser


class SeriesCreate(CreateView):
    model = Series
    template_name = "polls/series_create.html"
    fields = ['title', 'actors', 'director', 'date_of_release', 'language', 'genre', 'number_of_seasons']


class ActorListView(generic.ListView):
    template_name = "polls/actor_list.html"
    model = Actor
    paginate_by = 10


class ActorDetailView(generic.DetailView):
    template_name = "polls/actor_detail.html"
    model = Actor


class ActorDelete(UserPassesTestMixin, DeleteView):
    model = Actor
    template_name = ""
    success_url = reverse_lazy('actors')
    login_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.is_superuser


class ActorCreate(CreateView):
    model = Actor
    template_name = "polls/actor_create.html"
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'specialisation']


class DirectorListView(generic.ListView):
    template_name = "polls/director_list.html"
    model = Director
    paginate_by = 10


class DirectorDetailView(generic.DetailView):
    template_name = "polls/director_detail.html"
    model = Director


class DirectorDelete(UserPassesTestMixin, DeleteView):
    model = Director
    template_name = ""
    success_url = reverse_lazy('directors')
    login_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user.is_superuser


class DirectorCreate(CreateView):
    model = Director
    template_name = "polls/director_create.html"
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death', 'amount_of_films']


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


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


class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
