from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event


class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formata um dia como uma td
	# Filtra os eventos por dia
	def formatday(self, day, events):
		events_per_day = events.filter(start_time__day=day)
		d = ''
		for event in events_per_day:
			d += '<li> '+ event.get_html_url + '</li>'

		if day != 0:
			return "<td><span class='date'>{}</span><ul> {} </ul></td>".format(day, d)
		return '<td></td>'

	# Formata uma semana como tr	
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return '<tr> {} </tr>'.format(week)

	# formata um mês como uma tabela
	# filtrar eventos por ano e mês
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(
		start_time__year=self.year, start_time__month=self.month)

		cal = '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += self.formatmonthname(self.year, self.month, withyear=withyear)+'\n'
		cal += self.formatweekheader()+'\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += self.formatweek(week, events)+'\n'
		return cal
