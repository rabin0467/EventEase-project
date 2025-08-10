from django import forms
from events.models import Event, Category
from datetime import date
from django.forms.widgets import SelectDateWidget


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    default_classes = "border-2 bg-gray-300 w-full rounded shadow-sm"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_classes ,
                    'placeholder': f"Enter { field.label.lower()}"
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': self.default_classes,
                })
            elif isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter { field.label.lower()}"
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    'type': 'time',
                    'class': self.default_classes,
                    'placeholder':'HH:MM'
                })
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class': self.default_classes
                })
            

class EventModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model= Event
        fields = '__all__'  


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date'].widget = SelectDateWidget(
            years=range(date.today().year, date.today().year + 10)
        )


        self.apply_styled_widgets()

        self.fields['date'].initial = date.today()

        self.fields['category'].widget.attrs.update({
            'class': self.default_classes
        })




class CategoryModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        




