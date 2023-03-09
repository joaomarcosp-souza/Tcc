from .views import AnimalAutoComplete, ErroAutoComplete, MedicamentoAutoComplete, AlimentoAutoComplete
from django.urls import path


urlpatterns = [
    path('buscar/animal/', AnimalAutoComplete.as_view(),name="animal-autocomplete"),
    path('buscar/medicamento/', MedicamentoAutoComplete.as_view(),name="medicamento-autocomplete"),
    path('buscar/alimento/', AlimentoAutoComplete.as_view(),name="alimento-autocomplete"),
]

