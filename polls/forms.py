from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # for checking renewal date range.
from .models import Movie, Series, Actor, Director
from django import forms
from .models import Game
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

class EditUserForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length= 100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length= 100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length= 100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_login = forms.CharField(max_length= 100, widget=forms.TextInput(attrs={'class': 'form-control'}))
   # is_superuser = forms.CharField(max_length= 100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
   # is_staff = forms.CharField(max_length= 100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
   # is_active = forms.CharField(max_length= 100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    date_joined = forms.CharField(max_length= 100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password','last_login','date_joined')


class DateInput(forms.DateInput):
    input_type = 'date'

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('title','developer','date_of_release','genre','mode','summary')
       #fields = ('title','developer','date_of_release','genre','mode','summary','game_image')

        #fields = ('title','developer','date_of_release')

        widgets ={'title':  forms.TextInput(attrs={'class': 'form-control','placeholder':'tytul'}),
                 'developer': forms.Select(attrs={'class': 'form-control'}),
                 'date_of_release': DateInput(),
                 'genre': forms.SelectMultiple(attrs={'class': 'form-control'}),
                 'mode': forms.SelectMultiple(attrs={'class': 'form-control'}),
                 'summary': forms.Textarea(attrs={'class': 'form-control'}),
                 }



class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        #fields = '__all__'
        fields = ('title', 'actors', 'director', 'date_of_release', 'language', 'genre', 'running_time', 'summary')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'title'}),
            'actors': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'director': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'date_of_release': DateInput(),
            'language': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'genre': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'running_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Movie length in minutes'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),

        }


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        #fields = '__all__'
        fields = ('title', 'actors', 'director', 'date_of_release', 'language', 'genre', 'number_of_seasons', 'summary')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'title'}),
            'actors': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'director': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'date_of_release': DateInput(),
            'language': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'genre': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'number_of_seasons': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'number of seasons'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        #fields = '__all__'
        fields = ('first_name', 'last_name', 'date_of_birth', 'date_of_death', 'specialisation')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'last name'}),
            'date_of_birth': DateInput(),
            'date_of_death': DateInput(),
            'specialisation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'specialisation'}),
        }


class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        #fields = '__all__'
        fields = ('first_name', 'last_name', 'date_of_birth', 'date_of_death', 'amount_of_films')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'last name'}),
            'date_of_birth': DateInput(),
            'date_of_death': DateInput(),
            'amount_of_films': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class RenewBookForm(forms.Form):
    """Form for a librarian to renew books."""
    renewal_date = forms.DateField(
            help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        # Check date is in range librarian allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password1 = forms.CharField(max_length= 100, widget=forms.PasswordInput(attrs={'class': 'form-control','type':'password'}))
    new_password2 = forms.CharField(max_length= 100, widget=forms.PasswordInput(attrs={'class': 'form-control','type':'password'}))

    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password2')

