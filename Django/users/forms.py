from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, ButtonHolder, Div, HTML
from django import forms
from .models import Profile


class FormRegistroUsuario(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'nome_completo',
            'rg',
            'cpf',
            'sexo',
            'funcao',
            'telefone',
            'image',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados De Perfil',
                Row(
                    Column('rg', css_class='form-group col-lg mb-0'),
                    Column('cpf', css_class='form-group col-lg mb-0'),
                    Column('telefone', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('sexo', css_class='form-group col-lg mb-0'),
                    Column('funcao', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('image', css_class='form-group col-lg mb-0'),

                ),
            ),
            ButtonHolder(
                Div(
                    HTML("""
                            <button type="submit" class="btn btn-outline-primary">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                    HTML("""
                            <a href="{% url 'dash' %}" class="btn btn-outline-secondary">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                ),
            )

        )
