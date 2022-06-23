from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.mixins import PermissionRequiredMixin
import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from polls.forms import RenewBookForm
from .models import Book, Author, BookInstance, Game, Developer
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
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
    #fields = ['title', 'developer', 'date_of_release', 'genre', 'mode', 'summary']
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
    #login_url = '/polls/error401'
    #redirect_field_name = None

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
    #form_class = PasswordChangeForm #domyślne
    form_class =  PasswordChangingForm #Nowe z forms.py
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

