from django.contrib import admin
from .models import Aluno, ListaDia, Presenca

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'user']

@admin.register(ListaDia)
class ListaDiaAdmin(admin.ModelAdmin):
    list_display = ['data', 'aberta']

@admin.register(Presenca)
class PresencaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'lista', 'confirmado_em']
