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

from .models import *
from .utils import Calendar
from .forms import EventForm
from gfarm.models import Fazenda, Animal, Medicamento, Alimento

from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required  # SOCIAL DJANGO

from django.contrib import messages


import locale

class CalendarView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'dashboard.html'
    locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['fazendas'] = Fazenda.objects.filter(usuario=self.request.user).count()
        context['animais'] = Animal.objects.filter(usuario=self.request.user).count()
        context['medicamento'] = Medicamento.objects.filter(usuario=self.request.user).count()
        context['alimento'] = Alimento.objects.filter(usuario=self.request.user).count()

        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required #e a mesma coisa que o LoginRequiredMixin mas para metodos, precisa importar somente se necessitar de um usuario
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.instance.usuario = request.user
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form})

class CalendarCreat(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = "cal/event.html"
    model = Event
    success_url = reverse_lazy('cal:calendar')
    form_class = EventForm

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Tarefa registrada com sucesso"

    def form_valid(self, form):
        form.instance.usuario = self.request.user

        if ((form.instance.start_time) < ((form.instance.end_time))):
            url = super().form_valid(form)
            return url
        else:
            form.add_error(None, 'o campo "Fim da Tarefa" não pode ser menor que o campo "Inicio da Tarefa". Corrigir Por Favor.')
            return self.form_invalid(form)

class EventoDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Event
    template_name = 'cal/formExcluir.html'
    success_url = reverse_lazy('cal:calendar')
    success_message = "Evento excluido com sucesso"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(EventoDelete, self).delete(request, *args, **kwargs)

    def get_object(self, queryset=None):
        self.object = get_object_or_404(
            Event, pk=self.kwargs['pk'], usuario=self.request.user)
        return self.object