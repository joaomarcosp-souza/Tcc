from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from .validators import validate_CPF

class CategoriaPessoa(models.Model):
    categoria = models.CharField(max_length=50, verbose_name="Categoria")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.categoria

class Fazenda(models.Model):
    unidade_federal = (
        ('AC', 'AC'),
        ('AL', 'AL'),
        ('AM', 'AM'),
        ('AP', 'AP'),
        ('BA', 'BA'),
        ('DF', 'DF'),
        ('ES', 'ES'),
        ('GO', 'GO'),
        ('MA', 'MA'),
        ('MG', 'MG'),
        ('MS', 'MS'),
        ('MT', 'MT'),
        ('PA', 'PA'),
        ('PB', 'PB'),
        ('PE', 'PE'),
        ('PI', 'PI'),
        ('PR', 'PR'),
        ('RJ', 'RJ'),
        ('RN', 'RN'),
        ('RO', 'RO'),
        ('RR', 'RR'),
        ('RS', 'RS'),
        ('SC', 'SC'),
        ('SE', 'SE'),
        ('SP', 'SP'),
        ('TO', 'TO'),
    )
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    complemento = models.CharField(max_length=100)
    hectares = models.FloatField("Hectares")
    cidade = models.CharField(max_length=50)
    uf = models.CharField(max_length=2, verbose_name="UF",
                          choices=unidade_federal)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome + ' - ' + self.endereco

    class Meta:
        unique_together = [['nome', 'usuario']]


class Pessoa(models.Model):
    unidade_federal = (
        ('AC', 'AC'),
        ('AL', 'AL'),
        ('AM', 'AM'),
        ('AP', 'AP'),
        ('BA', 'BA'),
        ('DF', 'DF'),
        ('ES', 'ES'),
        ('GO', 'GO'),
        ('MA', 'MA'),
        ('MG', 'MG'),
        ('MS', 'MS'),
        ('MT', 'MT'),
        ('PA', 'PA'),
        ('PB', 'PB'),
        ('PE', 'PE'),
        ('PI', 'PI'),
        ('PR', 'PR'),
        ('RJ', 'RJ'),
        ('RN', 'RN'),
        ('RO', 'RO'),
        ('RR', 'RR'),
        ('RS', 'RS'),
        ('SC', 'SC'),
        ('SE', 'SE'),
        ('SP', 'SP'),
        ('TO', 'TO'),
    )
    Sexo = (
        ('Masculino', 'Masculino'),
        ('Femenino', 'Feminino')
    )
    nome_pessoa = models.CharField(verbose_name="Nome Completo", max_length=100)
    rg = models.CharField(verbose_name="RG", max_length=14)
    cpf = models.CharField(verbose_name="CPF", max_length=14, validators=[validate_CPF])
    sexo = models.CharField(max_length=10, choices=Sexo)
    dataNascimento = models.DateField(verbose_name="Data Nascimento")
    email = models.EmailField(max_length=100, verbose_name="E-mail")
    telefone = models.CharField(verbose_name="Telefone", max_length=20, help_text="(xx)xxxx-xxxx")
    uf = models.CharField(
        max_length=2, choices=unidade_federal, verbose_name="UF")
    categoria = models.ForeignKey(
        CategoriaPessoa, on_delete=models.PROTECT, verbose_name="Função")
    cidade = models.CharField(max_length=50, verbose_name="Cidade")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    nome = models.ForeignKey(
        Fazenda, on_delete=models.PROTECT, verbose_name="Fazenda")
    

    class Meta:
        unique_together = [['nome_pessoa', 'usuario'], ['rg', 'usuario'],
        [ 'cpf', 'usuario'], ['email', 'usuario'], ['telefone', 'usuario']]

    def __str__(self):
        return self.nome_pessoa + ' - ' + self.email

class AnimalCategoria(models.Model):
    categoria = models.CharField(verbose_name=" Categoria ", max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.categoria


class AnimalRaca(models.Model):
    raca = models.CharField(verbose_name=" Raça ", max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.raca

class AnimalPelagem(models.Model):
    pelagem = models.CharField(verbose_name=" Pelagem ", max_length=20)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.pelagem

#  COMEÇO DA CLASSE ANIMAL


class Animal(models.Model):

    sexo = (
        ('Macho', 'Macho'),
        ('Femea', 'Femea')
    )
    identificacao = models.CharField(
        max_length=15, help_text="Brinco do Animal")
    marcacao = models.CharField(
        max_length=100, help_text="Sigla da Fazenda ou nome Fazenda", verbose_name="Marcação")
    sexo = models.CharField(max_length=10, choices=sexo,
                            verbose_name="Sexo Do Animal")
    dataNascimento = models.DateField(verbose_name="Data Nascimento")
    raca = models.ForeignKey(
        AnimalRaca, on_delete=models.PROTECT, verbose_name="Raça")
    pelagem = models.ForeignKey(
        AnimalPelagem, on_delete=models.PROTECT, verbose_name="Pelagem")
    categoria = models.ForeignKey(
        AnimalCategoria, on_delete=models.PROTECT, verbose_name="Categoria")
    nome = models.ForeignKey(
        Fazenda, on_delete=models.PROTECT, verbose_name="Fazenda")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return "[{}] {} - {}/{}".format(self.identificacao, self.sexo, self.raca, self.pelagem)

    # Isso e para que tal usuario so tera um atributo com aquele nome
    class Meta:
        unique_together = [['identificacao', 'usuario']]


class Pesagens(models.Model):
    dataPesagem = models.DateField(verbose_name=" Dia Da Pesagem ")
    peso = models.FloatField(verbose_name=" Peso ")
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT, verbose_name="Animal",
                               help_text="Buscar por identificação, sexo, raça e pelagem")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    nome = models.ForeignKey(
        Fazenda, on_delete=models.PROTECT, verbose_name="Fazenda")
    

    def __str__(self):
        return "[{}] {} - {}".format(self.dataPesagem, self.peso, self.animal.identificacao)
    
    

class CategoriaAlimento(models.Model):
    categoriaAlimento = models.FloatField(
        verbose_name=" Categoria do alimento ", max_length=20)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.categoriaAlimento


class Local(models.Model):
    local = models.CharField(max_length=50, verbose_name="Armazém")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    nome = models.ForeignKey(
        Fazenda, on_delete=models.PROTECT, verbose_name="Fazenda")
    

    def __str__(self):
        return "[{}] {}".format(self.nome, self.local)


class Alimento(models.Model):

    marca = models.CharField(max_length=100, verbose_name="Nome Do Produto")
    qtde_estoque = models.FloatField(verbose_name="Quantidade em Estoque")
    categoriaAlimento = models.ForeignKey(
        CategoriaAlimento, on_delete=models.PROTECT, verbose_name="Categoria Alimento")
    local = models.ForeignKey(
        Local, on_delete=models.PROTECT, verbose_name="Barracão", null=True, blank=True)
    principioAtivo = models.TextField(
        max_length=1000, verbose_name="Descrição", null=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    nome = models.ForeignKey(
        Fazenda, on_delete=models.PROTECT, verbose_name="Fazenda")
    

    def __str__(self):
        return self.marca

#  FIM DA CLASSE ALIMENTO


class CategoriaMedicamento(models.Model):
    tipomedicamento = models.CharField(
        max_length=100, verbose_name="Tipo Medicamento")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.tipomedicamento


class Medicamento(models.Model):

    fabricante = models.CharField(
        max_length=100, verbose_name="Fabricante", help_text="Fornecedor")
    qtde_estoque = models.FloatField(verbose_name="Quantidade em estoque", help_text="Quantidade do Produto em Estoque no momento")
    tipomedicamento = models.ForeignKey(
        CategoriaMedicamento, on_delete=models.PROTECT, verbose_name="Tipo medicamento")
    local = models.ForeignKey(
        Local, on_delete=models.PROTECT, verbose_name="Barracão", blank=True, null=True)
    principio_ativo = models.TextField(
        max_length=1000, verbose_name=" Principio Ativo")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    nome = models.ForeignKey(
        Fazenda, on_delete=models.PROTECT, verbose_name="Fazenda")
    

    def __str__(self):
        return "{} - ({}) - {} ".format(self.fabricante, self.tipomedicamento, self.local)


class Vacinacao(models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
    dataVacina = models.DateField(verbose_name="Data da vacinação")
    dataVencimento = models.DateField(verbose_name="Data de vencimento")
    observacao = models.TextField(verbose_name="Observação sobre a vacina")
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT, verbose_name="Animal")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    nome = models.ForeignKey(
        Fazenda, on_delete=models.PROTECT, verbose_name="Fazenda")

    def __str__(self):
        return "{} ({}) - {}".format(self.medicamento.principio_ativo, self.dataVacina, self.animal.identificacao)

class Mensagem(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    email = models.EmailField(max_length=100)
    soma = models.CharField(max_length=100)
    mensagem = models.TextField(max_length=100)

    def __str__(self):
        return self.nome + ' - ' + self.mensagem + ' - ' + self.email