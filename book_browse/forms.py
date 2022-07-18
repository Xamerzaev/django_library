from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime


class BookSearch(forms.Form):
    search = forms.CharField(
        label="Поиск по названию книги", required=False,
        widget=forms.TextInput(
            attrs={'class': "field__input", 'id': 'search', 'autofocus': True,
                   'aria-label': "search", 'aria-describedby': "search",
                   'placeholder': 'Поиск книги'}))


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
            help_text="Введите дату между\
                настоящим моментом и 4 неделями (по умолчанию 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('\
                Недействительная дата - продление в прошлом'))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('\
            Недействительная дата - продление более чем на 4 недели вперед'))
        return data
