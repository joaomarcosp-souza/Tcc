from django.urls import path,include

from . views import *

app_name = 'cal'
urlpatterns = [
    path('calendario/',  CalendarView.as_view(), name='calendar'),
    path('novo/evento/', CalendarCreat.as_view(), name='event_new'),
	path('editar/evento/<event_id>/', event, name='event_edit'),
    path('excluir/deletar-evento/<event_id>/', EventoDelete.as_view(), name="delet_event"),
]