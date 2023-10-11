from django.forms import DateTimeInput


class DateTimePicker(DateTimeInput):
    template_name = 'widgets/datetimepicker.html'
    showTime = True

    def get_context(self, name, value, attrs):

        datetimepicker_id = f'datetimepicker_{name}'
        if attrs is None: attrs = dict()
        attrs['data-target'] = f'#{datetimepicker_id}'
        attrs['class'] = 'form-control datetimepicker-input'
        context = super().get_context(name, value, attrs)
        context['widget']['datetimepicker_id'] = datetimepicker_id
        context['showTime'] = self.showTime
        return context

    class Media:
        css = {
            "all": (
                "https://unpkg.com/persian-datepicker@latest/dist/css/persian-datepicker.css",
            )
        }
        js = (
            "https://code.jquery.com/jquery-3.4.1.min.js",
            "https://unpkg.com/persian-date@latest/dist/persian-date.js",
            "https://unpkg.com/persian-datepicker@latest/dist/js/persian-datepicker.js",
        )


class DatePicker(DateTimePicker):
    showTime = False
    pass
