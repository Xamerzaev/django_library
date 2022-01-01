from django import forms
from .models import TimePhase, FirstPhase

def time_choice():
    time_list = []
    for hour in range(0, 24):
        time_list.append((hour, hour))
    choices = tuple(time_list)
    return choices

class TimePhaseForm(forms.ModelForm):
    first = forms.IntegerField(min_value=1, initial=1, label='Длительность первой фазы')
    second = forms.IntegerField(min_value=1, initial=1, label='Длительность второй фазы')

    class Meta:
        model = TimePhase
        fields = ['first', 'second']

class EventTitle(forms.CharField):

    def to_python(self, value):
        return value.title()

class FirstPhaseForm(forms.ModelForm):
    time = forms.ChoiceField(choices=time_choice, label='Время')
    event = EventTitle()

    class Meta:
        model = FirstPhase
        fields = ['time', 'event']