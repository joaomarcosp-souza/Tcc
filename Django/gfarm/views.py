from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
# Importa tudo que tem em models.py
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render
# Aqui precisa de todos sim
# Importar as Views para inserir, alterar
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
# Função usada para redirecionar o usuário quando um registro é inserido/alterado
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import auth
from django.shortcuts import get_object_or_404
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from django.utils.safestring import mark_safe
from django.contrib.auth.mixins import LoginRequiredMixin
from calendar import day_name, different_locale
from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
import locale
from django.contrib.auth.mixins import LoginRequiredMixin
from calendar import day_name, different_locale
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import DetailView

# Importar de outros apps deve ser feito dessa forma
from cal.views import get_date, prev_month, next_month
from cal.utils import Calendar
from cal.forms import EventForm
from cal.models import Event

import locale
from django.utils import timezone
import datetime
from django.http import HttpResponse

# Import Json
from django.http import JsonResponse
import json

# Import datetime
import datetime

from movimentacao.models import Transferencia_Animal, Transferencia_Alimento, Transferencia_Medicamento

@login_required
def home(request):
    return render(request, 'core/home.html')

# Cria uma classe com herança de TemplateView para exibir
# um arquivo HTML normal (com o conteúdo dele)
class PaginaInicialView(TemplateView):
    template_name = "index.html"

class AtivarFazendaView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, *args, **kwargs):
        
        context = super(AtivarFazendaView, self).get_context_data(
            *args, **kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['fazendas'] = Fazenda.objects.filter(usuario=self.request.user).count()
        context['animais'] = Animal.objects.filter(usuario=self.request.user).count()
        context['medicamento'] = Medicamento.objects.filter(usuario=self.request.user).count()
        context['alimento'] = Alimento.objects.filter(usuario=self.request.user).count()

        context['evento'] = Event.objects.filter(usuario=self.request.user).order_by("-start_time")
        return context


    def dispatch(self, request, *args, **kwargs):
        # Busca a fazenda que vai ativar
        fazenda = get_object_or_404(Fazenda, pk=kwargs['pk'], usuario=request.user)

        request.session['fazenda_ativa']= fazenda.pk
        request.session['fazenda_ativa_nome']= fazenda.nome
        
        return super().dispatch(request, *args, **kwargs)


# Página "Sobre"
class SobreView(TemplateView):
    template_name = "sobre.html"

# PAGINA AJUDA 

class AjudaView(LoginRequiredMixin,  TemplateView):
    template_name = "ajuda.html"

# Página de dash

class dashView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = "dashboard.html"

    def dispatch(self, request, *args, **kwargs):

         # Busca a lista de fazendas do usuário
        fazendas = Fazenda.objects.filter(usuario=request.user)
        fazendas_id = {}
        # Adiciona cada id numa lista porque a sessão nnão aceita objetos
        for faz in fazendas:
            # adiciona o id no vetor
            fazendas_id[faz.id] = faz.nome

        request.session['fazendas'] = fazendas_id # {'13': 'Matilda', 'pos2': 'valor2'}

        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super(dashView, self).get_context_data(
            *args, **kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['titulo'] = 'Cadastro De Fazenda'
        context['fazendas'] = Fazenda.objects.filter(usuario=self.request.user).count()
        context['animais'] = Animal.objects.filter(usuario=self.request.user).count()
        context['medicamento'] = Medicamento.objects.filter(usuario=self.request.user).count()
        context['alimento'] = Alimento.objects.filter(usuario=self.request.user).count()
      
        return context

# Página Base

class baseView(TemplateView):
    template_name = "base.html"

# class cadastroPessoaView(TemplateView):
#     template_name = "cadastroPessoa.html"


class formView(TemplateView):
    template_name = "form.html"


class formEstoqueView(TemplateView):
    template_name = "formEstoque.html"

# CADASTROS Inserir Dados

class PessoaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = Pessoa
    success_url = reverse_lazy('listarPessoa')
    form_class = PessoaForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Pessoa criada com Sucesso"

    def get_context_data(self,*args, **kwargs):
        context = super(PessoaCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar nova pessoa'
        context['object_list'] = Pessoa.objects.all()

        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user

        try:
            if(self.request.session['fazenda_ativa']):
                fazenda = get_object_or_404(
                    Fazenda, pk=self.request.session['fazenda_ativa'], usuario=self.request.user)
                form.instance.nome = fazenda
        except:
            form.add_error(
                None, 'Você precisa ativar uma fazenda antes de salvar uma Pessoa.')
            return self.form_invalid(form)

        url = super().form_valid(form)
        return url


class FazendaCreateView(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = Fazenda
    success_url = reverse_lazy('dash')
    form_class = FazendaForm

    def get_context_data(self, *args, **kwargs):
        context = super(FazendaCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar nova fazenda'
        context['object_list'] = Fazenda.objects.all()
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Fazenda cadastrada com Sucesso"

    def form_valid(self, form):
        form.instance.usuario = self.request.user

        if(Fazenda.objects.filter(usuario=self.request.user).count() < 3):
            url = super().form_valid(form)
            return url
        else:
            form.add_error(None, 'Você ja atingiu a quantidade maxima de fazendas que é 3')
            return self.form_invalid(form)

class AnimalCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = Animal
    success_url = reverse_lazy('listarAnimal')
    form_class = AnimalForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Animal registrado com sucesso"

    def get_context_data(self, *args, **kwargs):
        context = super(AnimalCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar novo animal'
        context['object_list'] = Animal.objects.all()
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        
        try:
            if(self.request.session['fazenda_ativa']):
                fazenda = get_object_or_404(Fazenda, pk=self.request.session['fazenda_ativa'], usuario=self.request.user)
                form.instance.nome = fazenda
        except:
            form.add_error(None, 'Você precisa ativar uma fazenda antes de salvar um animal.')
            return self.form_invalid(form)
        
        url = super().form_valid(form)
        return url


class AnimalCategoriaView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = AnimalCategoria
    success_url = reverse_lazy('listarCategoria')
    form_class = CategoriaForm

    def get_context_data(self, *args, **kwargs):
        context = super(AnimalCategoriaView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar nova categoria'
        context['object_list'] = AnimalCategoria.objects.all()
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Nova Categoria de animal cadastrada com sucesso"

    def form_valid(self, form):
        # Define o usuário como usuário logado
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
    # Salva o objeto novamente
        self.object.save()
        return url


class AnimalRacaView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = AnimalRaca
    success_url = reverse_lazy('listarRaca')
    form_class = RacaForm

    def get_context_data(self, *args, **kwargs):
        context = super(AnimalRacaView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar nova Raça'
        context['object_list'] = AnimalRaca.objects.all()
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Nova raça de animal cadastrada com sucesso"

    def form_valid(self, form):
        # Define o usuário como usuário logado
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
    # Salva o objeto novamente
        self.object.save()
        return url


class AnimalPelagemView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = AnimalPelagem
    success_url = reverse_lazy('listarPelagem')
    form_class = PelagemForm

    def get_context_data(self, *args, **kwargs):
        context = super(AnimalPelagemView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar nova Pelagem'
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Nova pelagem de animal cadastrada com sucesso"


    def form_valid(self, form):
        # Define o usuário como usuário logado
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
    # Salva o objeto novamente
        self.object.save()
        return url


class PessoaCategoriaView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = CategoriaPessoa
    success_url = reverse_lazy('listarCategoriaPessoa')
    form_class = PessoaCategoriaForm

    def get_context_data(self, *args, **kwargs):
        context = super(PessoaCategoriaView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar nova Categoria'
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Nova função de pessoa cadastrada com sucesso"

    def form_valid(self, form):
        # Define o usuário como usuário logado
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
    # Salva o objeto novamente
        self.object.save()
        return url



class AlimentoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = Alimento
    success_url = reverse_lazy('listarAlimento')
    form_class = AlimentoFomr

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Perecível cadastrado com Sucesso"

    def get_context_data(self, *args, **kwargs):
        context = super(AlimentoCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar novo perecível'
        context['object_list'] = Alimento.objects.all()
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user

        try:
            if(self.request.session['fazenda_ativa']):
                fazenda = get_object_or_404(
                    Fazenda, pk=self.request.session['fazenda_ativa'], usuario=self.request.user)
                form.instance.nome = fazenda
        except:
            form.add_error(
                None, 'Você precisa ativar uma fazenda antes de salvar um novo Alimento.')
            return self.form_invalid(form)

        url = super().form_valid(form)
        return url


class AlimentoCategoriaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = CategoriaAlimento
    success_url = reverse_lazy('listarCategoriaAlimento')
    form_class = CategoriaAlimentoForm

    def get_context_data(self, *args, **kwargs):
        context = super(AlimentoCategoriaCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar nova categoria perecível'
        context['object_list'] = CategoriaAlimento.objects.all()
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "nova categoria de perecível cadastrada com Sucesso"

    def form_valid(self, form):
        # Define o usuário como usuário logado
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
    # Salva o objeto novamente
        self.object.save()
        return url


class MedicamentoCategoriaCreatView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = CategoriaMedicamento
    success_url = reverse_lazy('listarCategoriaMedicamento')
    form_class = CategoriaMedicamentoForm

    def get_context_data(self, *args, **kwargs):
        context = super(MedicamentoCategoriaCreatView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar novo tipo Medicamento'
        context['object_list'] = CategoriaMedicamento.objects.all()
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "nova tipo Medicamento cadastrado com Sucesso"

    def form_valid(self, form):
        # Define o usuário como usuário logado
        form.instance.usuario = self.request.user
        url = super().form_valid(form)
    # Salva o objeto novamente
        self.object.save()
        return url


class MedicamentoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = Medicamento
    success_url = reverse_lazy('listarMedicamento')
    form_class = MedicamentoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Medicamento cadastro com Sucesso"

    def get_context_data(self, *args, **kwargs):
        context = super(MedicamentoCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar novo medicamento'
        context['object_list'] = Medicamento.objects.all()
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user

        try:
            if(self.request.session['fazenda_ativa']):
                fazenda = get_object_or_404(
                    Fazenda, pk=self.request.session['fazenda_ativa'], usuario=self.request.user)
                form.instance.nome = fazenda
        except:
            form.add_error(
                None, 'Você precisa ativar uma fazenda antes de salvar um novo medicamento.')
            return self.form_invalid(form)

        url = super().form_valid(form)
        return url


class VacinacaoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = Vacinacao
    success_url = reverse_lazy('listarVacinacao')
    form_class = VacinacaoForm

    def get_context_data(self, *args, **kwargs):
        context = super(VacinacaoCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Realizar nova Vacinação'

        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Nova vacinação realizada com Sucesso"

    def form_valid(self, form):
        form.instance.usuario = self.request.user

        if ((form.instance.dataVacina) <= ((form.instance.dataVencimento))):
            url = super().form_valid(form)
            return url
        else:
            form.add_error(None, 'A data de vencimento e menor que a data de aplicação')
            return self.form_invalid(form)
        
    def form_valid(self, form):
        form.instance.usuario = self.request.user

        try:
            if(self.request.session['fazenda_ativa']):
                fazenda = get_object_or_404(
                    Fazenda, pk=self.request.session['fazenda_ativa'], usuario=self.request.user)
                form.instance.nome = fazenda
        except:
            form.add_error(
                None, 'Você precisa ativar uma fazenda antes de salvar um animal.')
            return self.form_invalid(form)

        url = super().form_valid(form)
        return url


class PesagensCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = Pesagens
    success_url = reverse_lazy('listarPesagem')
    form_class = PesagensForm

    def get_context_data(self, *args, **kwargs):
        context = super(PesagensCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar nova pesagem'
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Nova Pesagem realizada com Sucesso"

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        
        try:
            if(self.request.session['fazenda_ativa']):
                fazenda = get_object_or_404(Fazenda, pk=self.request.session['fazenda_ativa'], usuario=self.request.user)
                form.instance.nome = fazenda
        except:
            form.add_error(None, 'Você precisa ativar uma fazenda antes de realizar uma Pesagem nova.')
            return self.form_invalid(form)
        
        url = super().form_valid(form)
        return url


class MensagemCreateView(CreateView, SuccessMessageMixin,):
    template_name = "contato.html"
    model = Mensagem
    success_url = reverse_lazy('mensagem')
    form_class = MensagemForm
    

    def get_context_data(self, *args, **kwargs):
        context = super(MensagemCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Entre em Contato'
        return context        
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Nova Pesagem realizada com Sucesso"


class LocalCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = Local
    success_url = reverse_lazy('listarLocal')
    form_class = LocalForm

    def get_context_data(self, *args, **kwargs):
        context = super(LocalCreateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar nova local'
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Local registrado com Sucesso"
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user

        try:
            if(self.request.session['fazenda_ativa']):
                fazenda = get_object_or_404(
                    Fazenda, pk=self.request.session['fazenda_ativa'], usuario=self.request.user)
                form.instance.nome = fazenda
        except:
            form.add_error(
                None, 'Você precisa ativar uma fazenda antes de salvar um animal.')
            return self.form_invalid(form)

        url = super().form_valid(form)
        return url


##########################################    UPDATE    ##########################################


class PessoaUpdateView(LoginRequiredMixin, SuccessMessageMixin,  UpdateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = Pessoa
    success_url = reverse_lazy('listarPessoa')
    form_class = PessoaForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Registro atualizado com sucesso"

    def get_context_data(self, *args, **kwargs):
        context = super(PessoaUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Alterar pessoas'
        return context

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Pessoa, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class FazendaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = Fazenda
    success_url = reverse_lazy('listarFazenda')
    form_class = FazendaForm

    def get_context_data(self, *args, **kwargs):
        context = super(FazendaUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Alterar fazenda'
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Registro atualizado com sucesso"

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Fazenda, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class AnimalUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = Animal
    success_url = reverse_lazy('listarAnimal')
    form_class = AnimalForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Registro atualizado com sucesso"

    def get_context_data(self, *args, **kwargs):
        context = super(AnimalUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Alterar animal'
        return context

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Animal, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object



class AlimentoCategoriaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = CategoriaAlimento
    success_url = reverse_lazy('listarCategoriaAlimento')
    form_class = CategoriaAlimentoForm

    def get_context_data(self, *args, **kwargs):
        context = super(AlimentoCategoriaUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar novo perecível'
        context['object_list'] = CategoriaAlimento.objects.all()
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Registro atualizado com sucesso"

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            CategoriaAlimento, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class MedicamentoCategoriaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = CategoriaMedicamento
    success_url = reverse_lazy('listarCategoriaMedicamento')
    form_class = CategoriaMedicamentoForm

    def get_context_data(self, *args, **kwargs):
        context = super(MedicamentoCategoriaUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar novo perecível'
        context['object_list'] = CategoriaMedicamento.objects.all()
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Registro atualizado com sucesso"

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            CategoriaMedicamento, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class AnimalCategoriaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = AnimalCategoria
    success_url = reverse_lazy('listarCategoria')
    form_class = CategoriaForm

    def get_context_data(self, *args, **kwargs):
        context = super(AnimalCategoriaUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Alterar espécie'
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Registro atualizado com sucesso"

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            AnimalCategoria, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class AnimalRacaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = AnimalRaca
    success_url = reverse_lazy('listarRaca')
    form_class = RacaForm

    def get_context_data(self, *args, **kwargs):
        context = super(AnimalRacaUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Alterar Raça'
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Registro atualizado com sucesso"

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            AnimalRaca, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object

class AnimalPelagemUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = AnimalPelagem
    success_url = reverse_lazy('listarPelagem')
    form_class = PelagemForm

    def get_context_data(self, *args, **kwargs):
        context = super(AnimalPelagemUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'ALterar Pelagem'
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Registro atualizado com sucesso"

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            AnimalPelagem, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class PessoaCategoriaUpdatesView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = CategoriaPessoa
    success_url = reverse_lazy('listarCategoriaPessoa')
    form_class = PessoaCategoriaForm

    def get_context_data(self, *args, **kwargs):
        context = super(PessoaCategoriaUpdatesView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar nova categoria para pessoa'
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Registro atualizado com sucesso"

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            CategoriaPessoa, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class LocalUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = Local
    success_url = reverse_lazy('listarLocal')
    form_class = LocalForm

    def get_context_data(self, *args, **kwargs):
        context = super(LocalUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Adicionar novo local'
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Registro atualizado com sucesso"

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Local, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class AlimentoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = Alimento
    success_url = reverse_lazy('listarAlimento')
    form_class = AlimentoFomr

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Registro atualizado com sucesso"

    def get_context_data(self, *args, **kwargs):
        context = super(AlimentoUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Alterar perecível'
        return context

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Alimento, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class MedicamentoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = "cadastro/form.html"
    model = Medicamento
    success_url = reverse_lazy('listarMedicamento')
    form_class = MedicamentoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Registro atualizado com sucesso"

    def get_context_data(self, *args, **kwargs):
        context = super(MedicamentoUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Alterar medicamento'
        return context

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Medicamento, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class PesagemUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login')
    template_name = "lista/listaDePesagem.html"
    model = Pesagens
    success_url = reverse_lazy('cadastroPesagem')
    form_class = PesagensForm

    def get_context_data(self, *args, **kwargs):
        context = super(PesagemUpdateView, self).get_context_data(
            *args, **kwargs)
        context['titulo'] = 'Alterar pesagem'
        return context
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Registro atualizado com sucesso"

    # Altera a query para buscar o objeto do usuário logado
    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Pesagens, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


##########################################    LISTAS    ##########################################


class PessoaList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Pessoa
    template_name = 'lista/listaDePessoa.html'

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = Pessoa.objects.filter(usuario=self.request.user)
        return self.object_list


class AnimalList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Animal
    template_name = 'lista/listaDeAnimal.html'

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = Animal.objects.filter(usuario=self.request.user)
        return self.object_list


class FazendaList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Fazenda
    template_name = 'lista/listaDeFazenda.html'

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = Fazenda.objects.filter(usuario=self.request.user)
        return self.object_list


class AlimentoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Alimento
    template_name = 'lista/listaDeAlimento.html'

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = Alimento.objects.filter(usuario=self.request.user)
        return self.object_list


class MedicamentoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Medicamento
    template_name = 'lista/listaDeMedicamento.html'

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = Medicamento.objects.filter(
            usuario=self.request.user)
        return self.object_list


class PesagemList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Pesagens
    template_name = 'lista/listaDePesagem.html'

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = Pesagens.objects.filter(usuario=self.request.user)
        return self.object_list


class VacinacaoList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Vacinacao
    template_name = 'lista/listaDeVacinacao.html'

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = Vacinacao.objects.filter(usuario=self.request.user)
        return self.object_list


class AlimentoCategoriaList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = CategoriaAlimento
    template_name = 'lista/listaDeCategoriaAlimento.html'

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = CategoriaAlimento.objects.filter(
            usuario=self.request.user)
        return self.object_list


class MedicamentoCategoriaList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = CategoriaMedicamento
    template_name = 'lista/listaDeCategoriaMedicamento.html'

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = CategoriaMedicamento.objects.filter(
            usuario=self.request.user)
        return self.object_list



class CategoriaList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = AnimalCategoria
    template_name = 'lista/listaDeCategoriaAnimal.html'

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = AnimalCategoria.objects.filter(
            usuario=self.request.user)
        return self.object_list


class RacaList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = AnimalRaca
    template_name = 'lista/listaDeRaca.html'

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = AnimalRaca.objects.filter(usuario=self.request.user)
        return self.object_list


class PelagemList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = AnimalPelagem
    template_name = 'lista/listaDePelagem.html'

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = AnimalPelagem.objects.filter(
            usuario=self.request.user)
        return self.object_list

# Pessoa Categoria


class CategoriaPessoaList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = CategoriaPessoa
    template_name = 'lista/listaDeCategoriaPessoa.html'

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = CategoriaPessoa.objects.filter(
            usuario=self.request.user)
        return self.object_list


class LocalList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Local
    template_name = 'lista/listaDeLocal.html'

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = Local.objects.filter(usuario=self.request.user)
        return self.object_list


##########################################    DELETAR    ##########################################


class DeletePessoa(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Pessoa
    template_name = 'formExcluir.html'
    success_url = reverse_lazy('listarPessoa')
    success_message = "Registro excluido com sucesso"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeletePessoa, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Pessoa, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object

class DeleteAnimal(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Animal
    template_name = 'formExcluir.html'
    success_url = reverse_lazy('listarAnimal')
    success_message = "Registro excluido com sucesso"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteAnimal, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Animal, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object

class DeleteFazenda(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Fazenda
    template_name = 'formExcluir.html'
    success_url = reverse_lazy('listarFazenda')
    success_message = "Registro excluido com sucesso"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteFazenda, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Fazenda, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class DeleteAlimento(LoginRequiredMixin,  DeleteView):
    login_url = reverse_lazy('login')
    model = Alimento
    template_name = 'formExcluir.html'
    success_url = reverse_lazy('listarAlimento')
    success_message = "Registro excluido com sucesso"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteAlimento, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Alimento, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class DelteMedicamento(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Medicamento
    template_name = 'formExcluir.html'
    success_url = reverse_lazy('listarMedicamento')
    success_message = "Registro excluido com sucesso"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DelteMedicamento, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Medicamento, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class DeletePesagem(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Pesagens
    template_name = 'formExcluir.html'
    success_url = reverse_lazy('cadastroPesagem')
    success_message = "Registro excluido com sucesso"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeletePesagem, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Pesagens, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object
    

# DELETAR DOS CADASTROS SECUNDARIOS DE ANIMAL


class DeleteCategoria(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = AnimalCategoria
    template_name = 'formExcluir.html'
    success_url = reverse_lazy('listarCategoria')
    success_message = "Registro excluido com sucesso"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteCategoria, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            AnimalCategoria, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object

class DeleteRaca(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = AnimalRaca
    template_name = 'formExcluir.html'
    success_url = reverse_lazy('listarRaca')
    success_message = "Registro excluido com sucesso"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteRaca, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            AnimalRaca, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object

    
class DeletePelagem(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = AnimalPelagem
    template_name = 'formExcluir.html'
    success_url = reverse_lazy('listarPelagem')
    success_message = "Registro excluido com sucesso"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeletePelagem, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            AnimalPelagem, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object



class DeleteLocal(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Local
    template_name = 'formExcluir.html'
    success_url = reverse_lazy('listarLocal')
    success_message = "Registro excluido com sucesso"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteLocal, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Local, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object

class DeleteCategoriaPessoa(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = CategoriaPessoa
    template_name = 'formExcluir.html'
    success_url = reverse_lazy('listarCategoriaPessoa')
    success_message = "Registro excluido com sucesso"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteCategoriaPessoa, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            CategoriaPessoa, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class AlimentoCategoriaDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = CategoriaAlimento
    template_name = 'formExcluir.html'
    success_url = reverse_lazy('listarCategoriaAlimento')
    success_message = "Registro excluido com sucesso"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(AlimentoCategoriaDelete, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            CategoriaAlimento, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object


class MedicamentoCategoriaDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = CategoriaMedicamento
    template_name = 'formExcluir.html'
    success_url = reverse_lazy('listarCategoriaMedicamento')
    success_message = "Registro excluido com sucesso"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(MedicamentoCategoriaDelete, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            CategoriaMedicamento, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object



##################################################### HISTORICO #####################################################

class AnimalHistoricoInfoView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Animal
    template_name = 'historico/animalHistorico.html'

    # Filtra o animal do usuário logado
    def get_object(self, queryset=None):
        self.object = get_object_or_404(Animal, usuario=self.request.user, pk=self.kwargs['pk'])
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['pesagem'] = Pesagens.objects.filter(usuario=self.request.user, animal=self.object).order_by("-dataPesagem")
        context['vacina'] = Vacinacao.objects.filter(usuario=self.request.user, animal=self.object).order_by("-dataVacina")
        context['Movimentacao'] = Transferencia_Animal.objects.filter(usuario=self.request.user, animal=self.object).order_by("-data")

        context['pesagemTotal'] = Pesagens.objects.filter(usuario=self.request.user, animal=self.object).count()
        context['vacinaTotal'] = Vacinacao.objects.filter(usuario=self.request.user, animal=self.object).count()
        context['MovimentacaoTotal'] = Transferencia_Animal.objects.filter(usuario=self.request.user, animal=self.object).count()
        context['timezone'] = timezone.now()
        return context

class AnimalListView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Fazenda
    template_name = 'historico/animalList.html'

    # Filtra o animal do usuário logado
    def get_object(self, queryset=None):
        self.object = get_object_or_404(Fazenda, usuario=self.request.user, pk=self.kwargs['pk'])
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['animais'] = Animal.objects.filter(usuario=self.request.user, nome=self.object)
        context['timezone'] = timezone.now()

        return context


class HistoricoView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Fazenda
    template_name = 'historico/historico.html'

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = Fazenda.objects.filter(usuario=self.request.user)
        return self.object_list


##################################################### RELATORIO #####################################################

class RelatorioGeralView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Fazenda
    template_name = 'relatorio/relatorio.html'

    # Filtra o animal do usuário logado
    def get_object(self, queryset=None):
        self.object = get_object_or_404(Fazenda, usuario=self.request.user, pk=self.kwargs['pk'])
        return self.object

    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data(*args, **kwargs)
        
        context['alimento'] = Alimento.objects.filter(usuario=self.request.user, nome=self.object)
        context['medicamento'] = Medicamento.objects.filter(usuario=self.request.user, nome=self.object)
        context['local'] = Local.objects.filter(usuario=self.request.user , nome=self.object)
        context['pessoas'] = Pessoa.objects.filter(usuario=self.request.user, nome=self.object)
        context['pesagem'] = Pesagens.objects.filter(usuario=self.request.user, nome=self.object)
        context['vacinacao'] = Vacinacao.objects.filter(usuario=self.request.user, nome=self.object )

        
        context['medicamentoTotal'] = Medicamento.objects.filter(usuario=self.request.user).count()
        context['alimentoTotal'] = Alimento.objects.filter(usuario=self.request.user).count()
        context['timezone'] = timezone.now()
        
        return context

class RelatorioPesagemView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Fazenda
    template_name = 'relatorio/relatorioPesagem.html'

    # Filtra o animal do usuário logado
    def get_object(self, queryset=None):
        self.object = get_object_or_404(Fazenda, usuario=self.request.user, pk=self.kwargs['pk'])
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['pesagem'] = Pesagens.objects.filter(usuario=self.request.user, nome=self.object)
        context['animalTotal'] = Animal.objects.filter(usuario=self.request.user).count()
        context['timezone'] = timezone.now()

        return context


class RelatorioAnimalView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Fazenda
    template_name = 'relatorio/relatorioAnimal.html'

    # Filtra o animal do usuário logado
    def get_object(self, queryset=None):
        self.object = get_object_or_404(Fazenda, usuario=self.request.user, pk=self.kwargs['pk'])
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['animal'] = Animal.objects.filter(usuario=self.request.user, nome=self.object)
        context['timezone'] = timezone.now()

        return context


class RelatorioVacinacaoView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Fazenda
    template_name = 'relatorio/relatorioVacinacao.html'

    # Filtra o animal do usuário logado
    def get_object(self, queryset=None):
        self.object = get_object_or_404(Fazenda, usuario=self.request.user, pk=self.kwargs['pk'])
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['vacina'] = Vacinacao.objects.filter(usuario=self.request.user, nome=self.object)
        context['timezone'] = timezone.now()

        return context


class detalhesRelatorioView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Fazenda
    template_name = "relatorio/detalhesRelatorio.html"

    def get_queryset(self):
        # O object_list armazena uma lista de objetos de um ListView
        self.object_list = Fazenda.objects.filter(usuario=self.request.user)
        return self.object_list

class relatorioView(LoginRequiredMixin, TemplateView):
    template_name = "relatorio/relatorio.html"  
