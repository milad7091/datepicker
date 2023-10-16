from django.utils.safestring import mark_safe

from django.forms import DateTimeInput
from six import string_types
import uuid

BOOTSTRAP_INPUT_TEMPLATE = """
<input readonly dir="ltr" type="text" id="%(id)sAlt" %(valueinput)s>
%(rendered_widget)s    
<script>
    $(document).ready(function () {
        $("#%(id)sAlt").pDatepicker({
            initialValue: %(initialvalue)s,
            format: '%(format)s',
            %(timePicker)s            
            %(datetype)s                
            onSelect: function (unix) {
                var date = new Date(unix);
                var d = date.toLocaleDateString('en-US').split("/");
                var y = d.splice(-1)[0];
                d.splice(0, 0, y);
                var dat = d.join("-");
                var Time = document.getElementById('%(id)sAlt').value.split(" ");
                if (Time.length > 1)
                    Time = ' ' + Time[1];
                else
                    Time = '';
                document.getElementById('%(id)s').value = dat + Time
            }
        });
    });
</script>
"""

quoted_options = set([
    'format',
    'startDate',
    'endDate',
    'startView',
    'minView',
    'maxView',
    'todayBtn',
    'language',
    'pickerPosition',
    'viewSelect',
    'initialDate',
    'weekStart',
    'minuteStep'
    'daysOfWeekDisabled',
])

# to traslate boolean object to javascript
quoted_bool_options = set([
    'autoclose',
    'todayHighlight',
    'showMeridian',
    'clearBtn',
])


def quote(key, value):
    """Certain options support string values. We want clients to be able to pass Python strings in
    but we need them to be quoted in the output. Unfortunately some of those options also allow
    numbers so we type check the value before wrapping it in quotes.
    """

    if key in quoted_options and isinstance(value, string_types):
        return "'%s'" % value

    if key in quoted_bool_options and isinstance(value, bool):
        return {True: 'true', False: 'false'}[value]

    return value


class DateTimePicker(DateTimeInput):
    def __int__(self):
        if options is None:
            options = {}
        options['format'] = options.get('format', 'dd/mm/yyyy hh:ii:ss')
        super(DateTimeWidget, self).__init__()

    def render(self, name, value, renderer=None, attrs=None):
        final_attrs = self.build_attrs(attrs)
        rendered_widget = super(DateTimePicker, self).render(name, value, final_attrs)
        if (value):
            initialvalue = 'true'
            valueinput = 'value="' + ("%s" % value) + '"'
        else:
            initialvalue = 'false'
            valueinput = ''
        rendered_widget = rendered_widget.replace('type="text"', 'type="hidden"')
        if not self.showTime:
            rendered_widget = rendered_widget.replace(' 00:00:00"', '"')
        self.options.setdefault('autoclose', True)
        options_list = []
        for key, value in iter(self.options.items()):
            options_list.append("%s: %s" % (key, quote(key, value)))
        js_options = ",\n".join(options_list)
        id = final_attrs.get('id', uuid.uuid4().hex)
        date_format = 'YYYY-MM-DD'
        time_picker = ''
        if self.showTime:
            date_format = 'YYYY-MM-DD HH:mm:ss'
            time_picker = 'timePicker: {enabled: true,},'
        datetype = """ calendarType: 'gregorian',calendar: {persian: {locale: 'en'}}, """
        datetype = ''
        return mark_safe(
            BOOTSTRAP_INPUT_TEMPLATE
            % dict(
                id=id,
                rendered_widget=rendered_widget,
                options=js_options,
                format=date_format,
                valueinput=valueinput,
                initialvalue=initialvalue,
                datetype=datetype,
                timePicker=time_picker
            )
        )

    showTime = True
    options = {}
    language = ''

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
