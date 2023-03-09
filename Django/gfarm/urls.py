# módulo do Django para criar urls
from django.urls import path,include

# pip install python-social-auth[django]

# Importe todas suas classes do views.py
from . views import *
from users import views as register
from django.core.exceptions import PermissionDenied

urlpatterns = [
    # path('caminho/da/url', ClasseLáDoView.as_view(), name="nomeDessaURL" )
    path('', PaginaInicialView.as_view(),name="index"),

    path('ativar/fazenda/<int:pk>/', AtivarFazendaView.as_view(),name="ativar-fazenda"),

    path('sobre/', SobreView.as_view(),name="sobre"),
    path('painel-de-controle/', dashView.as_view(),name="dash", ),
    path('formulario/', formView.as_view(),name="form"),
    path('formulario/estoque/', formEstoqueView.as_view(), name="formEstoque"),
    path('modulo/ajuda/', AjudaView.as_view(), name="ajuda"),


    #Historico
    path('historico/animal/<int:pk>/',AnimalHistoricoInfoView.as_view(), name="historicoInformacoes"),
    path('fazenda/<int:pk>/animais/',AnimalListView.as_view(), name="animalList"),
    path('listar/fazendas/', HistoricoView.as_view(), name="historico"),


    #Relatorio
    path('modulo/ajuda/relatorio', detalhesRelatorioView.as_view(), name="detalheRelatorio"),
    path('imprimir/relatorio/', relatorioView.as_view(), name="relatorio"),
    path('relatorio/<int:pk>/geral', RelatorioGeralView.as_view(), name="relatorioFazenda"),
    path('relatorio/<int:pk>/vacina/', RelatorioVacinacaoView.as_view(), name="relatorioVacina"),
    path('relatorio/<int:pk>/pesagem/', RelatorioPesagemView.as_view(), name="relatorioPesagem"),
    path('relatorio/<int:pk>/animal/', RelatorioAnimalView.as_view(), name="relatorioAnimal"),

    # INFORMAÇÕES DE PESSOA
    path('cadastrar/cadastro-de-pessoa/', PessoaCreateView.as_view(), name="cadastroPessoa"),
    path('atualizar/alterar-pessoa/<int:pk>/', PessoaUpdateView.as_view(), name="atualizarPessoa"),
    path('excluir/deletar-Pessoa/<int:pk>/', DeletePessoa.as_view(), name="deletarPessoa"),
    path('listar/lista-de-pessoa/', PessoaList.as_view(), name="listarPessoa"),

    # INFORMAÇÕES DE FAZENDA
    path('cadastrar/cadastro-de-fazenda/', FazendaCreateView.as_view(), name="cadastroFazenda"),
    path('atualizar/alterar-fazenda/<int:pk>/', FazendaUpdateView.as_view(), name="atualizarFazenda"),
    path('excluir/deletar-Fazenda/<int:pk>/', DeleteFazenda.as_view(), name="deletarFazenda"),
    path('listar/lista-de-fazenda/', FazendaList.as_view(), name="listarFazenda"),

    # INFORMAÇÕES DE ANIMAL
    path('cadastrar/cadastro-de-animal/', AnimalCreateView.as_view(), name="cadastroAnimal"),
    path('atualizar/alterar-animal/<int:pk>/', AnimalUpdateView.as_view(), name="atualizarAnimal"),
    path('excluir/deletar-Animal/<int:pk>/', DeleteAnimal.as_view(), name="deletarAnimal"),
    path('listar/lista-de-animal/', AnimalList.as_view(), name="listarAnimal"),

    # INFORMAÇÕES DE CADASTRO-ALIMENTO
    path('cadastrar/cadastro-de-alimento/', AlimentoCreateView.as_view(), name="cadastroAlimento"),
    path('atualizar/alterar-alimento/<int:pk>/', AlimentoUpdateView.as_view(), name="atualizarAlimento"),
    path('excluir/deletar-Alimento/<int:pk>/', DeleteAlimento.as_view(), name="deletarAlimento"),
    path('listar/lista-de-alimento/', AlimentoList.as_view(), name="listarAlimento"),

    # INFORMAÇÕES DE CADASTRO-MEDICAMENTO
    path('cadastrar/cadastro-de-medicamento/', MedicamentoCreateView.as_view(), name="cadastroMedicamento"),
    path('atualizar/alterar-medicamento/<int:pk>/', MedicamentoUpdateView.as_view(), name="atualizarMedicamento"),
    path('excluir/deletar-Medicamento/<int:pk>/', DelteMedicamento.as_view(), name="deletarMedicamento"),
    path('listar/lista-de-medicamento/', MedicamentoList.as_view(), name="listarMedicamento"),


    # INFORMAÇÕES DE MENSAGEM
    path('cadastrar/mensagem/', MensagemCreateView.as_view(), name="mensagem"),

    # INFORMAÇÕES DE PESAGENS
    path('cadastrar/pesagem/', PesagensCreateView.as_view(), name="cadastroPesagem"),
    path('excluir/deletar-Pesagem/<int:pk>/', DeletePesagem.as_view(), name="deletePesagem"),
    path('listar/lista-de-pesagens/', PesagemList.as_view(), name="listarPesagem"),

    # INFORMAÇÕES DE VACINAÇÃO
    path('cadastrar/vacinacao/', VacinacaoCreateView.as_view(), name="cadastroVacinacao"),
    path('listar/lista-de-vacinacoes/', VacinacaoList.as_view(), name="listarVacinacao"),


    # INFORMAÇÕES DE ANIMAL-CATEGORIA
    path('cadastrar/nova/categoria/', AnimalCategoriaView.as_view(), name="cadastroCategoria"),
    path('atualizar/alterar-categoria/<int:pk>/', AnimalCategoriaUpdateView.as_view(), name="atualizarCategoria"),
    path('excluir/deletar-categoria/<int:pk>/', DeleteCategoria.as_view(), name="deletarCategoria"),
    path('listar/lista-de-categoria/', CategoriaList.as_view(), name="listarCategoria"),

    # INFORMAÇÕES DE RAÇA
    path('cadastrar/nova/raca/', AnimalRacaView.as_view(), name="cadastroRaca"),
    path('atualizar/alterar-raca/<int:pk>/', AnimalRacaUpdateView.as_view(), name="atualizarRaca"),
    path('excluir/deletar-raca/<int:pk>/', DeleteRaca.as_view(), name="deletarRaca"),
    path('listar/lista-de-raca/', RacaList.as_view(), name="listarRaca"),

    # INFORMAÇÕES DE PELAGEM
    path('cadastrar/nova/pelagem/', AnimalPelagemView.as_view(), name="cadastroPelagem"),
    path('atualizar/alterar-pelagem/<int:pk>/', AnimalPelagemUpdateView.as_view(), name="atualizarPelagem"),
    path('excluir/deletar-pelagem/<int:pk>/', DeletePelagem.as_view(), name="deletarPelagem"),
    path('listar/lista-de-pelagem/', PelagemList.as_view(), name="listarPelagem"),
    

    # INFORMAÇÕES DE CATEGORIA-PESSOA
    path('cadastrar/nova/categoria-pessoa/', PessoaCategoriaView.as_view(), name="cadastroCategoriaPessoa"),
    path('atualizar/alterar-categoria-pessoa/<int:pk>/', PessoaCategoriaUpdatesView.as_view(), name="atualizarCategoriaPessoa"),
    path('excluir/deletar-categoria-pessoa/<int:pk>/', DeleteCategoriaPessoa.as_view(), name="deletarPessoaCategoria"),
    path('listar/lista-de-categoria-pessoa/', CategoriaPessoaList.as_view(), name="listarCategoriaPessoa"),

    # INFORMAÇÕES DE LOCAL
    path('cadastrar/novo/local/', LocalCreateView.as_view(), name="cadastroLocal"),
    path('atualizar/alterar-local/<int:pk>/', LocalUpdateView.as_view(), name="atualizarLocal"),
    path('excluir/deletar-local/<int:pk>/', DeleteLocal.as_view(), name="deletarLocal"),
    path('listar/lista-de-local/', LocalList.as_view(), name="listarLocal"),

    # INFORMAÇÕES DE CATEGORIA-ALIMENTO
    path('cadastrar/categoria-alimento/', AlimentoCategoriaCreateView.as_view(), name="cadastroCategoriaAliemento"),
    path('atualizar/alterar-categoria-alimento/<int:pk>/', AlimentoCategoriaUpdateView.as_view(), name="atualizarCategoriaAlimento"),
    path('excluir/deletar-categoria-alimento/<int:pk>/', AlimentoCategoriaDelete.as_view(), name="deletarCategoriaAlimento"),
    path('listar/lista-de-categorias-alimento/', AlimentoCategoriaList.as_view(), name="listarCategoriaAlimento"),

    # INFORMAÇÕES DE CATEGORIA-MEDICAMENTO
    path('cadastrar/categoria-medicamento/', MedicamentoCategoriaCreatView.as_view(), name="cadastroCategoriaMedicamento"),
    path('atualizar/alterar-categoria-medicamento/<int:pk>/', MedicamentoCategoriaUpdateView.as_view(), name="atualizarCategoriaMedicamento"),
    path('excluir/deletar-categoria-medicamento/<int:pk>/', MedicamentoCategoriaDelete.as_view(), name="deletarCategoriaMedicamento"),
    path('listar/lista-de-categorias-medicamento/', MedicamentoCategoriaList.as_view(), name="listarCategoriaMedicamento"),


    

   

]




