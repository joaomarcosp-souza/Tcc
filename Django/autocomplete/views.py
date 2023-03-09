
from dal import autocomplete
from django.db.models import Q
from django.http import Http404
from gfarm.models import Animal, Mensagem, Alimento, Medicamento

##################### AUTOCOMPLETE ANIMAL #####################
class AnimalAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            raise Http404
        # Filtrar os animais por usuario que está logado
        qs = Animal.objects.filter(usuario=self.request.user)

        if self.q:
            qs = qs.filter(
                Q(identificacao__icontains=self.q) |
                Q(sexo__icontains=self.q) |
                Q(raca__raca__icontains=self.q) |
                Q(pelagem__pelagem__icontains=self.q)
            )

        return qs

##################### AUTOCOMPLETE MEDICAMENTO #####################
class MedicamentoAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            raise Http404
        # Filtrar os animais por usuario que está logado
        qs = Medicamento.objects.filter(usuario=self.request.user)

        if self.q:
            qs = qs.filter(
                Q(fabricante__icontains=self.q) |
                Q(tipomedicamento__tipomedicamento__icontains=self.q) |
                Q(principio_ativo__icontains=self.q)
            )

        return qs

##################### AUTOCOMPLETE ALIMENTO #####################
class AlimentoAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            raise Http404
        # Filtrar os animais por usuario que está logado
        qs = Alimento.objects.filter(usuario=self.request.user)

        if self.q:
            qs = qs.filter(
                Q(marca__icontains=self.q) |
                Q(qtde_estoque__icontains=self.q) |
                Q(categoriaAlimento__categoriaAlimento__icontains=self.q) |
                Q(principioAtivo__icontains=self.q)
            )

        return qs


##################### AUTOCOMPLETE ERRO #####################
class ErroAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            raise Http404
        # Filtrar os animais por usuario que está logado
        qs = Mensagem.objects.filter(usuario=self.request.user)

        if self.q:
            qs = qs.filter(
                Q(erro__icontains=self.q)
            )

        return qs
