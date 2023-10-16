from django.contrib import admin
from .models import Test
from .widgets import DatePicker, DateTimePicker
from django.db import models
from django import forms


class TestAdmin(admin.ModelAdmin):
    class DateForm(forms.ModelForm):
        datetime = forms.DateTimeField(widget=DateTimePicker(), )
    form = DateForm

    list_display = ("dateOnly", "datetime")

    formfield_overrides = {
        models.DateField: {'widget': DatePicker},
        models.DateTimeField: {'widget': DateTimePicker}
    }


admin.site.register(Test, TestAdmin)
