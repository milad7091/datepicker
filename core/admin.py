from django.contrib import admin
from .models import Test
from .widgets import DatePicker, DateTimePicker
from django.db import models
from .forms import DateForm


class TestAdmin(admin.ModelAdmin):
    form = DateForm
    list_display = ("dateOnly", "datetime")
    list_editable = ("datetime",)
    formfield_overrides = {
        models.DateField: {'widget': DatePicker},
        models.DateTimeField: {'widget': DateTimePicker}
    }


admin.site.register(Test, TestAdmin)