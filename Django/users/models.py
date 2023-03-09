from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from gfarm.validators import validate_CPF

def user_directory_path(instance, filename):
    # a foto sera salva na rota MEDIA_ROOT/user_<id>/<filename>
    return '{0}/user_{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    Sexo = (
        ('Masculino', 'Masculino'),
        ('Femenino', 'Feminino')
    )
    funcao = (
        ('Proprietário', 'Proprietário'),
        ('Funcionário', 'Funcionário')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, max_length=100)
    nome_completo = models.CharField(verbose_name="Nome Completo", max_length=100)
    rg = models.CharField(verbose_name="RG", max_length=14)
    cpf = models.CharField(verbose_name="CPF", max_length=14, validators=[validate_CPF])
    sexo = models.CharField(max_length=10, choices=Sexo)
    funcao = models.CharField(choices=funcao, max_length=15, verbose_name='Função')
    telefone = models.CharField(verbose_name="Telefone", max_length=20, help_text="(xx)xxxx-xxxx")
    image = models.ImageField(default='default.jpg', upload_to=user_directory_path, verbose_name='Imagem')

    def __str__(self):
        return self.user.username
