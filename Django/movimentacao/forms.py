from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, ButtonHolder, Div, HTML
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from dal import autocomplete


class Movimentacao_AnimalForm(forms.ModelForm):

    class Meta:
        model = Transferencia_Animal
        fields = [
            # 'fazenda_origem',
            'animal',
            'data',
            'fazenda_destino',
        ]
        widgets = {
            'animal': autocomplete.ModelSelect2(url='animal-autocomplete')
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # self.fields['fazenda_origem'].queryset = self.fields['fazenda_origem'].queryset.filter(
            # usuario=user)
        self.fields['fazenda_destino'].queryset = self.fields['fazenda_destino'].queryset.filter(
            usuario=user)
        self.fields['animal'].queryset = self.fields['animal'].queryset.filter(
            usuario=user)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados para Movimentação',
                Row(
                    Column('animal', css_class='form-group col-lg mb-4'),
                    Column('data', css_class='form-group col-lg mb-0'),
                    Column('fazenda_destino',
                           css_class='form-group col-lg mb-0'),
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
                    HTML("""
                            <a href="{% url 'dash' %}" class="btn btn-outline-secondary">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                ),
            )
        )


###################### MOVIMENTAR ALIMENTO ##################
class Movimentacao_AlimentoForm(forms.ModelForm):

    class Meta:
        model = Transferencia_Alimento
        fields = [
            'alimento',
            'data',
            'quantidade_transferida',
            'fazenda_destino',
        ]
        widgets = {
            'alimento': autocomplete.ModelSelect2(url='alimento-autocomplete')
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # self.fields['fazenda_origem'].queryset = self.fields['fazenda_origem'].queryset.filter(
        # usuario=user)
        self.fields['fazenda_destino'].queryset = self.fields['fazenda_destino'].queryset.filter(
            usuario=user)
        self.fields['alimento'].queryset = self.fields['alimento'].queryset.filter(
            usuario=user)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados para Movimentação',
                Row(
                    Column('alimento', css_class='form-group col-lg mb-4'),
                    Column('data', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('quantidade_transferida',
                           css_class='form-group col-lg mb-0'),
                    Column('fazenda_destino',
                           css_class='form-group col-lg mb-0'),
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
                    HTML("""
                            <a href="{% url 'dash' %}" class="btn btn-outline-secondary">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                ),
            )
        )


###################### MOVIMENTAR MEDICAMENTO ##################
class Movimentacao_MedicamentoForm(forms.ModelForm):

    class Meta:
        model = Transferencia_Medicamento
        fields = [
            'medicamento',
            'data',
            'quantidade_transferida',
            'fazenda_destino',
        ]
        widgets = {
            'medicamento': autocomplete.ModelSelect2(url='medicamento-autocomplete')
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # self.fields['fazenda_origem'].queryset = self.fields['fazenda_origem'].queryset.filter(
        # usuario=user)
        self.fields['fazenda_destino'].queryset = self.fields['fazenda_destino'].queryset.filter(
            usuario=user)
        self.fields['medicamento'].queryset = self.fields['medicamento'].queryset.filter(
            usuario=user)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados para Movimentação',
                Row(
                    Column('medicamento', css_class='form-group col-lg mb-4'),
                    Column('data', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('quantidade_transferida', css_class='form-group col-lg mb-0'),
                    Column('fazenda_destino', css_class='form-group col-lg mb-0'),
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
                    HTML("""
                            <a href="{% url 'dash' %}" class="btn btn-outline-secondary">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                ),
            )
        )


###################### ENTRADA MEDICAMENTO ##################
class Entrada_MedicamentoForm(forms.ModelForm):

    class Meta:
        model = Entrada_Medicamento
        fields = [
            'medicamento',
            'quantidade_entrada',
        ]
        widgets = {
            'medicamento': autocomplete.ModelSelect2(url='medicamento-autocomplete')
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['medicamento'].queryset = self.fields['medicamento'].queryset.filter(
            usuario=user)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Nova entrada para Medicamento',
                Row(
                    Column('medicamento', css_class='form-group col-lg mb-4'),
                    Column('quantidade_entrada', css_class='form-group col-lg mb-0'),
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
                    HTML("""
                            <a href="{% url 'dash' %}" class="btn btn-outline-secondary">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                ),
            )
        )


###################### ENTRADA ALIMENTO ##################
class Entrada_AlimentoForm(forms.ModelForm):

    class Meta:
        model = Entrada_Alimento
        fields = [
            'alimento',
            'quantidade_entrada',
        ]
        widgets = {
            'alimento': autocomplete.ModelSelect2(url='alimento-autocomplete')
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['alimento'].queryset = self.fields['alimento'].queryset.filter(
            usuario=user)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Nova entrada para alimento',
                Row(
                    Column('alimento', css_class='form-group col-lg mb-4'),
                    Column('quantidade_entrada', css_class='form-group col-lg mb-0'),
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
                    HTML("""
                            <a href="{% url 'dash' %}" class="btn btn-outline-secondary">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                ),
            )
        )