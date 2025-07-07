from django.urls import path
from . import views

app_name = 'principal'

urlpatterns = [
    path('aluno/', views.menu_aluno, name='menu_aluno'),
    path('admin-menu/', views.menu_admin, name='menu_admin'),

    # Rotas para gerenciamento de alunos com prefixo painel/
    path('painel/alunos/', views.listar_alunos, name='listar_alunos'),
    path('painel/alunos/novo/', views.criar_aluno, name='criar_aluno'),
    path('painel/alunos/<int:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('painel/alunos/<int:aluno_id>/excluir/', views.excluir_aluno, name='excluir_aluno'),
]
