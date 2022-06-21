from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # for checking renewal date range.
from .models import Movie
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'
        # fields = ('title', 'actors', 'director', 'date_of_release', 'language', 'genre', 'running_time')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'title'}),
            'actors': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'director': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'date_of_release': DateInput(),
            'language': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'genre': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'running_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie length in minutes'}),
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
