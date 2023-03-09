from django.db import models
from gfarm.models import Animal, Alimento, Medicamento, Fazenda
from django.contrib.auth.models import User

########### MOVIMENTAR ANIMAL ###########
class Transferencia_Animal(models.Model):
    fazenda_origem = models.ForeignKey(Fazenda, on_delete=models.PROTECT, related_name="origem")
    fazenda_destino = models.ForeignKey(Fazenda, on_delete=models.PROTECT, related_name="destino")
    data = models.DateField(verbose_name="Data Transeferêcia")
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return "{} -- {} -> {}".format(self.animal, self.fazenda_origem.nome, self.fazenda_destino.nome)

    class Meta:
        verbose_name = "Transeferêcia de animal"
        verbose_name_plural = "Transeferêcias de animais"

########### MOVIMENTAR MEDICAMENTO ###########
class Transferencia_Medicamento(models.Model):
    fazenda_origem = models.ForeignKey(Fazenda, on_delete=models.PROTECT, related_name="origem_medicamento")
    fazenda_destino = models.ForeignKey(Fazenda, on_delete=models.PROTECT, related_name="destino_medicamento")
    data = models.DateField(verbose_name="Data Transeferêcia")
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
    quantidade_transferida = models.FloatField()
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return "{} -- {} -> {}".format(self.medicamento, self.fazenda_origem.nome, self.fazenda_destino.nome)

    class Meta:
        verbose_name = "Transeferêcia de medicamento"
        verbose_name_plural = "Transeferêcias de medicamentos"

########### MOVIMENTAR ALIMENTO ###########
class Transferencia_Alimento(models.Model):
    fazenda_origem = models.ForeignKey(Fazenda, on_delete=models.PROTECT, related_name="origem_alimento")
    fazenda_destino = models.ForeignKey(Fazenda, on_delete=models.PROTECT, related_name="destino_alimento")
    data = models.DateField(verbose_name="Data Transeferêcia")
    alimento = models.ForeignKey(Alimento, on_delete=models.PROTECT)
    quantidade_transferida = models.FloatField()
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return "{} -- {} -> {}".format(self.alimento, self.fazenda_origem.nome, self.fazenda_destino.nome)

    class Meta:
        verbose_name = "Transeferêcia de alimento"
        verbose_name_plural = "Transeferêcias de alimentos"


########### ENTRADA DE MEDICAMENTO #########
class Entrada_Medicamento(models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
    quantidade_entrada = models.FloatField()
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return "{} -> {}".format(self.medicamento, self.quantidade_entrada)


########### ENTRADA DE ALIMENTO #########
class Entrada_Alimento(models.Model):
    alimento = models.ForeignKey(Alimento, on_delete=models.PROTECT)
    quantidade_entrada = models.FloatField()
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return "{} -> {}".format(self.alimento, self.quantidade_entrada)