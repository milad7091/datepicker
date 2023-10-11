from django import forms
from .models import Test
from .widgets import DateTimePicker


class DateForm(forms.ModelForm):
    datetime = forms.DateTimeField(
        widget=DateTimePicker(),
        input_formats=['%Y-%m-%d %H:%M:%S']
    )

    class Meta:
        model = Test
        widgets = {
            "datetime": DateTimePicker(
            )
        }
        fields = ["dateOnly", "datetime"]
