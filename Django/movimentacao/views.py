from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Transferencia_Animal
from gfarm.models import Animal, Alimento, Medicamento, Fazenda
from .forms import Movimentacao_AnimalForm, Movimentacao_AlimentoForm, Movimentacao_MedicamentoForm, Entrada_MedicamentoForm, Entrada_AlimentoForm
from django.contrib.messages.views import SuccessMessageMixin
from .models import Transferencia_Alimento, Transferencia_Animal, Transferencia_Medicamento, Entrada_Medicamento, Entrada_Alimento


################## MOVIMENTAR ANIMAL ##################
class Movimentar_Animal(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Transferencia_Animal
    template_name = 'cadastro/form.html'
    success_url = reverse_lazy('listar_animal_movimentado')
    form_class = Movimentacao_AnimalForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_message(self, cleaned_data):
        return "Movimentação de animal realizada com sucesso"

    def form_valid(self, form):
        # Busca a última transfer desse animal
        ultima_tranferencia = Transferencia_Animal.objects.filter(
            usuario=self.request.user, animal=form.instance.animal).last()

        # Se existir e se a data for depois da informada...
        if(ultima_tranferencia and ultima_tranferencia.data > form.instance.data):
            form.add_error(
                None, 'Esta data é invalida! A última transferência desse animal foi em {}.'.format(ultima_tranferencia.data))
            return self.form_invalid(form)

        # Verifica se a fazenda atual é igual
        if form.instance.animal.nome == form.instance.fazenda_destino:
            form.add_error(
                None, 'O animal já está na fazenda {}'.format(form.instance.fazenda_destino))
            return self.form_invalid(form)

        form.instance.fazenda_origem = form.instance.animal.nome
        form.instance.usuario = self.request.user

        # Se tudo estiver ok, cria o registro
        url = super().form_valid(form)

        # fazer algo aqui aqui pode user o self.object

        # muda a fazenda do animal e salva o animal
        self.object.animal.nome = self.object.fazenda_destino
        self.object.animal.save()

        # Finaliza o movimento
        return url

    def get_context_data(self, *args, **kwargs):
        context = super(Movimentar_Animal, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Realizar nova movimentação para animal'
        return context

################## LISTAR MOVIMENTACAO ANIMAL ##################


class Lista_movimentacao_animal(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Transferencia_Animal
    template_name = "lista/detalhesMovimentacao.html"

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = Transferencia_Animal.objects.filter(
            usuario=self.request.user)
        return self.object_list


################## MOVIMENTAR MEDICAMENTO ##################
class Movimentar_Medicamento(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Transferencia_Medicamento
    template_name = 'cadastro/form.html'
    success_url = reverse_lazy('listar_movimentacao_medicamento')
    form_class = Movimentacao_MedicamentoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Movimentação de Medicamento realizada com sucesso"

    def form_valid(self, form):

        # Verifica se a fazenda atual é igual a do medicamento de destino
        if form.instance.medicamento.nome == form.instance.fazenda_destino:
            form.add_error(
                None, 'O medicamento já está na fazenda {}'.format(form.instance.fazenda_destino))
            return self.form_invalid(form)

        # Verifica se a quantidade em estoque e o suficiente para a transferencia se não for da um erro, caso seja ela faz a subtração
        if form.instance.medicamento.qtde_estoque < form.instance.quantidade_transferida:
            form.add_error(
                None, 'A quantidade em estoque e menor que a desejada para transferencia - Estoque atual {} unidades'.format(form.instance.medicamento.qtde_estoque))
            return self.form_invalid(form)
        else:
            form.instance.medicamento.qtde_estoque -= form.instance.quantidade_transferida
            form.instance.medicamento.save()

        form.instance.fazenda_origem = form.instance.medicamento.nome
        form.instance.usuario = self.request.user

        # Se tudo estiver ok, cria o registro
        url = super().form_valid(form)

        # Verifica buscar os objetos fabricante, tipo medicamento na fazenda de destino
        try:
            medicamento = Medicamento.objects.get(fabricante=self.object.medicamento.fabricante,
                                                  tipomedicamento=self.object.medicamento.tipomedicamento, nome=self.object.fazenda_destino)
        except:
            medicamento = False
        # Caso o medicamento exista ele soma a quantidade de estoque a quantiade trasferida, se o medicamento não existir ele cria o medicamento e duplica as informações
        if medicamento:
            medicamento.qtde_estoque += self.object.quantidade_transferida
            medicamento.save()
        else:
            m = Medicamento.objects.create(
                fabricante=self.object.medicamento.fabricante,
                tipomedicamento=self.object.medicamento.tipomedicamento,
                nome=self.object.fazenda_destino,
                qtde_estoque=self.object.quantidade_transferida,
                principio_ativo=self.object.medicamento.principio_ativo,
                usuario=self.request.user
            )
        # Finaliza o movimento
        return url

    def get_context_data(self, *args, **kwargs):
        context = super(Movimentar_Medicamento, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Realizar nova movimentação para medicamento'
        return context

class Lista_movimentacao_medicamento(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Transferencia_Medicamento
    template_name = "lista/detalhesMovimentacaoMedicamento.html"

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = Transferencia_Medicamento.objects.filter(
            usuario=self.request.user)
        return self.object_list

################## MOVIMENTAR ALIMENTO ##################


class Movimentar_Alimento(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Transferencia_Alimento
    template_name = 'cadastro/form.html'
    success_url = reverse_lazy('listar_movimentacao_alimento')
    form_class = Movimentacao_AlimentoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Movimentação de Alimento realizada com sucesso"

    def form_valid(self, form):
        # Verifica se a fazenda atual é igual a do alimento de destino
        if form.instance.alimento.nome == form.instance.fazenda_destino:
            form.add_error(
                None, 'O alimento já está na fazenda {}'.format(form.instance.fazenda_destino))
            return self.form_invalid(form)

        # Verifica se a quantidade em estoque e o suficiente para a transferencia se não for da um erro, caso seja ela faz a subtração
        if form.instance.alimento.qtde_estoque < form.instance.quantidade_transferida:
            form.add_error(
                None, 'A quantidade em estoque e menor que a desejada para transferencia - Estoque atual {} unidades'.format(form.instance.alimento.qtde_estoque))
            return self.form_invalid(form)
        else:
            form.instance.alimento.qtde_estoque -= form.instance.quantidade_transferida
            form.instance.alimento.save()

        form.instance.fazenda_origem = form.instance.alimento.nome
        form.instance.usuario = self.request.user

        # Se tudo estiver ok, cria o registro
        url = super().form_valid(form)

        # Verifica buscar os objetos fabricante, tipo alimento na fazenda de destino
        try:
            alimento = Alimento.objects.get(marca=self.object.alimento.marca,
                                                  categoriaAlimento=self.object.alimento.categoriaAlimento, nome=self.object.fazenda_destino)
        except:
            alimento = False
        # Caso o alimento exista ele soma a quantidade de estoque a quantiade trasferida, se o alimento não existir ele cria o alimento e duplica as informações
        if alimento:
            alimento.qtde_estoque += self.object.quantidade_transferida
            alimento.save()
        else:
            a = Alimento.objects.create(
                marca=self.object.alimento.marca,
                categoriaAlimento=self.object.alimento.categoriaAlimento,
                nome=self.object.fazenda_destino,
                qtde_estoque=self.object.quantidade_transferida,
                principioAtivo=self.object.alimento.principioAtivo,
                usuario=self.request.user
            )
        # Finaliza o movimento
        return url

    def get_context_data(self, *args, **kwargs):
        context = super(Movimentar_Alimento, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Realizar nova movimentação para alimento'
        return context

class Lista_movimentacao_alimento(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Transferencia_Alimento
    template_name = "lista/detalhesMovimentacaoAlimento.html"

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = Transferencia_Alimento.objects.filter(
            usuario=self.request.user)
        return self.object_list


################## ENTRADA MEDICAMENTO ##################
class Entrada_medicamentoView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Entrada_Medicamento
    template_name = 'cadastro/form.html'
    success_url = reverse_lazy('listarMedicamento')
    form_class = Entrada_MedicamentoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "A nova quantidade foi adicionada ao estoque do item"

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.medicamento.qtde_estoque += form.instance.quantidade_entrada
        form.instance.medicamento.save()

        url = super().form_valid(form)
        return url# Finaliza o movimento

    def get_context_data(self, *args, **kwargs):
        context = super(Entrada_medicamentoView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Nova entrada para medicamento'
        return context

################## ENTRADA MEDICAMENTO ##################
class Entrada_alimentoView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Entrada_Alimento
    template_name = 'cadastro/form.html'
    success_url = reverse_lazy('listarAlimento')
    form_class = Entrada_AlimentoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "A nova quantidade foi adicionada ao estoque do item"

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.alimento.qtde_estoque += form.instance.quantidade_entrada
        form.instance.alimento.save()

        url = super().form_valid(form)
        return url# Finaliza o movimento
    
    def get_context_data(self, *args, **kwargs):
        context = super(Entrada_alimentoView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Nova entrada para alimento'
        return context
