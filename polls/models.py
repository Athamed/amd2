from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique book instances
from django.contrib.auth.models import User
from datetime import date


# Create your models here.

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class GameGenre(models.Model):
    """Model representing a game genre."""
    name = models.CharField(max_length=200, help_text='Enter a game genre (e.g. Adventure)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class GameMode(models.Model):
    """Model representing a game mode."""
    name = models.CharField(max_length=200, help_text='Enter a game genre (e.g. SinglePlayer)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name



class Game(models.Model):
    """Model representing a game (but not a specific game)."""
    title = models.CharField(max_length=200)
    developer = models.ForeignKey('Developer', on_delete=models.SET_NULL, null=True)
    date_of_release = models.DateField(null=True, blank=True)

    genre = models.ManyToManyField(GameGenre, help_text='Select a genre for this game')
    mode = models.ManyToManyField(GameMode, help_text='Select which game mode is available')
    # Nwm czy to jest sens tu trzymać z language
    # language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the game')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this game."""
        return reverse('game-detail', args=[str(self.id)])



class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'



class Developer(models.Model):
    """Model representing an Developer."""
    company_name = models.CharField(max_length=100)
    date_of_foundation = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['company_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular developer instance."""
        return reverse('developer-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.company_name}'


class Person(models.Model):
    first_name = models.CharField(max_length=100, default='first name')
    last_name = models.CharField(max_length=100, default='last name')
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True


class Actor(Person):
    specialisation = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('actor-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Director(Person):
    amount_of_films = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('director-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class FilmSeries(models.Model):
    title = models.TextField(max_length=100)
    language = models.ManyToManyField('Language')
    actors = models.ManyToManyField('Actor')
    director = models.ManyToManyField('Director')
    date_of_release = models.DateField()

    def get_absolute_url(self):
        return reverse('film-series-detail', args=[str(self.id)])

    def __str__(self):
        return self.title


class FilmSeriesGenre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
