from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import Movimentar_Animal, Movimentar_Medicamento, Movimentar_Alimento, Lista_movimentacao_animal, Lista_movimentacao_medicamento, Entrada_medicamentoView, \
    Lista_movimentacao_alimento, Entrada_alimentoView 


urlpatterns = [

    # MOVIMENTAÇÃO DE ANIMAL
    path('movimentar/animal/', Movimentar_Animal.as_view(), name="movimentar_animal"),
    path('listar/movimentacao/animal', Lista_movimentacao_animal.as_view(), name="listar_animal_movimentado"),

    # MOVIMENTAÇÃO DE ALIMENTO
    path('movimentar/alimento/', Movimentar_Alimento.as_view(), name="movimentar_alimento"),
    path('listar/movimentacao/alimento', Lista_movimentacao_alimento.as_view(), name="listar_movimentacao_alimento"),

    # MOVIMENTAÇÃO DE MEDICAMENTO
    path('movimentar/medicamento/', Movimentar_Medicamento.as_view(), name="movimentar_medicamento"),
    path('listar/movimentacao/medicamento', Lista_movimentacao_medicamento.as_view(), name="listar_movimentacao_medicamento"),

    # ENTRADA MEDICAMENTO
    path('entrada/medicamento/', Entrada_medicamentoView.as_view(), name="entrada_medicamento"),

    # ENTRADA ALIMENTO
    path('entrada/alimento/', Entrada_alimentoView.as_view(), name="entrada_alimento"),
    
]
