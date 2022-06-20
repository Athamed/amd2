from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # for checking renewal date range.
from django import forms
from .models import Game



class DateInput(forms.DateInput):
    input_type = 'date'


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('title','developer','date_of_release','genre','mode','summary')
        #fields = ('title','developer','date_of_release')

        widgets ={'title':  forms.TextInput(attrs={'class': 'form-control','placeholder':'tytul'}),
                 'developer': forms.Select(attrs={'class': 'form-control'}),
                 'date_of_release': DateInput(),
                 'genre': forms.SelectMultiple(attrs={'class': 'form-control'}),
                 'mode': forms.Select(attrs={'class': 'form-control'}),
                 'summary': forms.Textarea(attrs={'class': 'form-control'}),
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
