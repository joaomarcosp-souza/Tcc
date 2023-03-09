from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, ButtonHolder, Div, HTML
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from dal import autocomplete


class PessoaForm(forms.ModelForm):

    class Meta:
        model = Pessoa
        fields = [
            'nome_pessoa',
            'rg',
            'cpf',
            'sexo',
            'dataNascimento',
            'email',
            'categoria',
            'telefone',
            'cidade',
            'uf',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = self.fields['categoria'].queryset.filter(
            usuario=user)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados De Cadastro',
                Row(
                    Column('nome_pessoa', css_class='form-group col-lg mb-4'),
                    Column('rg', css_class='form-group col-lg mb-0'),
                    Column('cpf', css_class='form-group col-lg mb-0'),
                    Column('sexo', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('dataNascimento', css_class='form-group col-lg mb-1'),
                    Column('email', css_class='form-group col-lg mb-0'),
                    Column('telefone', css_class='form-group col-lg mb-0'),
                    Column('categoria', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('cidade', css_class='form-group col-md-5'),
                    Column('uf', css_class='form-group mb-0 col-md-2'),
                ),
            ),
            ButtonHolder(
                Div(
                    HTML("""
                            <button type="submit" class="btn btn-outline-success mt-1">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                    HTML("""
                            <a href="{% url 'listarPessoa' %}" class="btn btn-outline-secondary mt-1">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                ),
            )
        )


class PessoaCategoriaForm(forms.ModelForm):
    class Meta:
        model = CategoriaPessoa
        fields = [
            'categoria',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados De Cadastro',
                Row(
                    Column('categoria', css_class='form-group col-lg mb-4'),
                ),
                ButtonHolder(
                    Div(
                        HTML("""
                            <button type="submit" class="btn btn-outline-success mt-1">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                        HTML("""
                            <a href="{% url 'listarCategoriaPessoa' %}" class="btn btn-outline-secondary mt-1">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                    ),
                )
            )
        )


class FazendaForm(forms.ModelForm):

    class Meta:
        model = Fazenda
        fields = [
            'nome',
            'endereco',
            'complemento',
            'hectares',
            'cidade',
            'uf',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados De Cadastro',
                Row(
                    Column('nome', css_class='form-group col-lg mb-4'),
                    Column('endereco', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('complemento', css_class='form-group col-lg mb-0'),
                    Column('hectares', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('cidade', css_class='form-group col-md-5'),
                    Column('uf', css_class='form-group col-md-2'),
                ),
            ),
            ButtonHolder(
                Div(
                    HTML("""
                            <button type="submit" class="btn btn-outline-success mt-1">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                    HTML("""
                            <a href="{% url 'listarFazenda' %}" class="btn btn-outline-secondary mt-1">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                ),
            )

        )


class AnimalForm(forms.ModelForm):

    class Meta:
        model = Animal
        fields = [
            'identificacao',
            'marcacao',
            'dataNascimento',
            'sexo',
            'raca',
            'pelagem',
            'categoria',

        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['raca'].queryset = self.fields['raca'].queryset.filter(
            usuario=user)
        self.fields['pelagem'].queryset = self.fields['pelagem'].queryset.filter(
            usuario=user)
        self.fields['categoria'].queryset = self.fields['categoria'].queryset.filter(
            usuario=user)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados De Cadastro',
                Row(
                    Column('identificacao', css_class='form-group col-lg mb-4'),
                    Column('marcacao', css_class='form-group col-lg mb-0'),
                    Column('dataNascimento', css_class='form-group col-md-3'),
                ),
                Row(
                    Column('sexo', css_class='form-group col-md-2'),
                    Column('raca', css_class='form-group col-md-4'),
                ),
                Row(
                    Column('pelagem', css_class='form-group col-md-4'),
                    Column('categoria', css_class='form-group col-md-4'),
                ),
            ),
            ButtonHolder(
                Div(
                    HTML("""
                            <button type="submit" class="btn btn-outline-success mt-1">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                    HTML("""
                            <a href="{% url 'listarAnimal' %}" class="btn btn-outline-secondary mt-1">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                ),
            )

        )


class AlimentoFomr(forms.ModelForm):

    class Meta:
        model = Alimento
        fields = [
            'marca',
            'qtde_estoque',
            'categoriaAlimento',
            'local',
            'principioAtivo',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['categoriaAlimento'].queryset = self.fields['categoriaAlimento'].queryset.filter(
            usuario=user)
        self.fields['local'].queryset = self.fields['local'].queryset.filter(
            usuario=user)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Dados De Cadastro',
                Row(
                    Column('marca', css_class='form-group col-lg mb-4'),
                    Column('qtde_estoque', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('local', css_class='form-group col-md-5'),
                    Column('categoriaAlimento',
                           css_class='form-group col-md-5'),
                ),
                Row(
                    Column('principioAtivo', css_class='form-group col-md-7'),
                ),
            ),
            ButtonHolder(
                Div(
                    HTML("""
                            <button type="submit" class="btn btn-outline-primary mt-1">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                    HTML("""
                            <a href="{% url 'listarAlimento' %}" class="btn btn-outline-secondary mt-1">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                ),
            )

        )


class CategoriaAlimentoForm(forms.ModelForm):

    class Meta:
        model = CategoriaAlimento
        fields = [
            'categoriaAlimento',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados De Cadastro',
                Row(
                    Column('categoriaAlimento',
                           css_class='form-group col-lg mb-0'),
                ),
            ),
            ButtonHolder(
                Div(
                    HTML("""
                            <button type="submit" class="btn btn-outline-primary mt-1">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                    HTML("""
                            <a href="{% url 'listarCategoriaAlimento' %}" class="btn btn-outline-secondary mt-1">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                ),
            )

        )


class CategoriaMedicamentoForm(forms.ModelForm):

    class Meta:
        model = CategoriaMedicamento
        fields = [
            'tipomedicamento',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados De Cadastro',
                Row(
                    Column('tipomedicamento',
                           css_class='form-group col-lg mb-0'),
                ),
            ),
            ButtonHolder(
                Div(
                    HTML("""
                            <button type="submit" class="btn btn-outline-primary mt-1">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                    HTML("""
                            <a href="{% url 'listarCategoriaMedicamento' %}" class="btn btn-outline-secondary mt-1">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                ),
            )

        )


class MedicamentoForm(forms.ModelForm):

    class Meta:
        model = Medicamento
        fields = [
            'fabricante',
            'qtde_estoque',
            'tipomedicamento',
            'local',
            'principio_ativo',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['local'].queryset = self.fields['local'].queryset.filter(
            usuario=user)
        self.fields['tipomedicamento'].queryset = self.fields['tipomedicamento'].queryset.filter(
            usuario=user)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados De Cadastro',
                Row(
                    Column('fabricante', css_class='form-group col-lg mb-4'),
                    Column('qtde_estoque', css_class='form-group col-lg mb-0'),
                ),
                Row(
                    Column('tipomedicamento', css_class='form-group col-md-5'),
                    Column('local', css_class='form-group col-md-3'),
                ),
                Row(
                    Column('principio_ativo', css_class='form-group col-md-7'),
                ),
            ),
            ButtonHolder(
                Div(
                    HTML("""
                            <button type="submit" class="btn btn-outline-primary mt-1">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                    HTML("""
                            <a href="{% url 'listarMedicamento' %}" class="btn btn-outline-secondary mt-1">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                ),
            )

        )

# SUB-CLASSE DE ANIMAL


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = AnimalCategoria
        fields = [
            'categoria',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados De Cadastro',
                Row(
                    Column('categoria', css_class='form-group col-lg mb-4'),
                ),
                ButtonHolder(
                    Div(
                        HTML("""
                            <button type="submit" class="btn btn-outline-success mt-1">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                        HTML("""
                            <a href="{% url 'listarCategoria' %}" class="btn btn-outline-secondary mt-1">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                    ),
                )
            )
        )


class RacaForm(forms.ModelForm):
    class Meta:
        model = AnimalRaca
        fields = [
            'raca',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados De Cadastro',
                Row(
                    Column('raca', css_class='form-group col-lg mb-4'),
                ),
                ButtonHolder(
                    Div(
                        HTML("""
                            <button type="submit" class="btn btn-outline-success mt-1">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                        HTML("""
                            <a href="{% url 'listarRaca' %}" class="btn btn-outline-secondary mt-1">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                    ),
                )
            )
        )


class PesagensForm(forms.ModelForm):
    class Meta:
        model = Pesagens
        fields = [
            'dataPesagem',
            'peso',
            'animal',
        ]
        widgets = {
            'animal': autocomplete.ModelSelect2(url='animal-autocomplete')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados De Cadastro',
                Row(
                    Column('dataPesagem', css_class='form-group col-lg-3 mb-4'),
                    Column('peso', css_class='form-group col-lg-2 mb-4'),
                    Column('animal', css_class='form-group col-lg mb-4'),
                ),
                ButtonHolder(
                    Div(
                        HTML("""
                            <button type="submit" class="btn btn-outline-success mt-1">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                        HTML("""
                            <a href="{% url 'listarPesagem' %}" class="btn btn-outline-secondary mt-1">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                    ),
                )
            )
        )


class PelagemForm(forms.ModelForm):
    class Meta:
        model = AnimalPelagem
        fields = [
            'pelagem',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados De Cadastro',
                Row(
                    Column('pelagem', css_class='form-group col-lg mb-4'),
                ),
                ButtonHolder(
                    Div(
                        HTML("""
                            <button type="submit" class="btn btn-outline-success mt-1">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                        HTML("""
                            <a href="{% url 'listarPelagem' %}" class="btn btn-outline-secondary mt-1">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                    ),
                )
            )
        )


class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = [
            'local',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados De Cadastro',
                Row(
                    Column('local', css_class='form-group col-lg mb-4'),
                ),
                ButtonHolder(
                    Div(
                        HTML("""
                            <button type="submit" class="btn btn-outline-primary mt-1">
                                <i class="fa fa-check" aria-hidden="true"></i>
                                Salvar
                            </button>
                        """),
                        HTML("""
                            <a href="{% url 'listarLocal' %}" class="btn btn-outline-secondary mt-1">
                                <i class="fas fa-times"></i>
                                Cancelar
                            </a>
                        """),
                    ),
                )
            )
        )


class VacinacaoForm(forms.ModelForm):
    class Meta:
        model = Vacinacao
        fields = [
            'medicamento',
            'dataVacina',
            'dataVencimento',
            'animal',
            'observacao',
        ]
        # Aqui eu to falando que tal atributo sera o campo de busca
        widgets = {
            'animal': autocomplete.ModelSelect2(
                url='animal-autocomplete',
                attrs={
                    # Set some placeholder
                    'data-placeholder': 'Digite a identificação, sexo, raça para buscar',
                },
            ),
            'medicamento': autocomplete.ModelSelect2(
                url='medicamento-autocomplete',
                attrs={
                    # Set some placeholder
                    'data-placeholder': 'Digite o fabricante ou tipo medicamento para buscar',
                },
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Dados De Cadastro',
                Row(
                    Column('medicamento', css_class='form-group col-lg mb-4'),
                    Column('animal', css_class='form-group col-lg mb-4'),
                ),
                Row(
                    Column('dataVacina', css_class='form-group col-lg mb-4'),
                    Column('dataVencimento', css_class='form-group col-lg mb-4'),
                ),
                Row(
                    Column('observacao', css_class='form-group col-lg-8 mb-2'),
                ),
                ButtonHolder(
                    Div(
                        HTML("""
                                    <button type="submit" class="btn btn-outline-success mt-1">
                                        <i class="fa fa-check" aria-hidden="true"></i>
                                        Salvar
                                    </button>
                                """),
                        HTML("""
                                    <a href="{% url 'listarVacinacao' %}" class="btn btn-outline-secondary mt-1">
                                        <i class="fas fa-times"></i>
                                        Cancelar
                            </a>
                        """),
                    ),
                )
            )
        )


class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = [
            'nome',
            'email',
            'soma',
            'mensagem',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(

            Fieldset(
                'Informações da Mensagem',
                Row(
                    Column('nome', css_class='form-group col-lg-6 mb-4'),
                    Column('email', css_class='form-group col-lg-6 mb-4'),
                ),
                Row(
                    Column('soma', css_class='form-group col-lg-6 mb-4'),
                ),
                Row(
                    Column('mensagem', css_class='form-group col-lg-8 mb-2'),
                ),
                ButtonHolder(
                    Div(
                        HTML("""
                                    <button type="submit" class="btn btn-primary mt-1">
                                        <i class="fa fa-check" aria-hidden="true"></i>
                                        Enviar
                                    </button>

                                    <a href="{% url 'index' %}" class="btn btn-dark btn-cancelar mt-1">
                                          <i class="fas fa-times" aria-hidden="true"></i>
                                        Cancelar
                            </a>
                                """),
                    ),
                )
            )
        )
