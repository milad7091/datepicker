from django import forms
from .models import Test
from .widgets import DateTimePicker


class DateForm(forms.ModelForm):
    datetime = forms.DateTimeField(widget=DateTimePicker,)

