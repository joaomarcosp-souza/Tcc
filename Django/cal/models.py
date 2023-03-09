from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Event(models.Model):
    title           = models.CharField(max_length=200, verbose_name="Titulo")
    description     = models.TextField(verbose_name="Descrição")
    start_time      = models.DateTimeField(verbose_name="Inicio da Tarefa")
    end_time        = models.DateTimeField(verbose_name="Fim da Tarefa")
    usuario         = models.ForeignKey(User, on_delete=models.PROTECT)

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return '<a href="{}"> {} </a>'.format(url, self.title)
    