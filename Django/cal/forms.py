from django.forms import ModelForm, DateInput
from cal.models import Event
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, ButtonHolder, Div, HTML
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from dal import autocomplete


class EventForm(ModelForm):

    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'start_time',
            'end_time',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados do evento',
                Row(
                    Column('title', css_class='form-group col-lg mb-4'),
                    Column('start_time', css_class='form-group col-lg mb-0'),
                    Column('end_time', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('description', css_class='form-group col-lg mb-0'),
                ),
            ),
            ButtonHolder(
                Div(
                    HTML("""
                            <button type="submit" class="btn btn-outline-success">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
    
                ),
            )
        )
