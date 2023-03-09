from django.contrib import admin
from .models import *


admin.site.register (Pessoa)
admin.site.register (Fazenda)
admin.site.register (Animal)
admin.site.register (Pesagens)
admin.site.register (Alimento)
admin.site.register (Medicamento)
admin.site.register (Mensagem)
admin.site.register (Vacinacao)

admin.site.register(AnimalCategoria)
admin.site.register (AnimalRaca)
admin.site.register (AnimalPelagem)

