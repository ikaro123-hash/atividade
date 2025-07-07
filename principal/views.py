from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Aluno, ListaDia, Presenca
from .forms import ConfirmaPresencaForm
from datetime import date

def is_admin(user):
    return user.is_staff

@login_required
def menu_aluno(request):
    aluno = get_object_or_404(Aluno, user=request.user)
    hoje = date.today()
    lista, created = ListaDia.objects.get_or_create(data=hoje)
    presenca = Presenca.objects.filter(lista=lista, aluno=aluno).first()
    max_usuarios = 50
    total_confirmados = lista.presencas.count()

    if request.method == 'POST':
        if not lista.aberta:
            messages.error(request, 'Lista fechada. Não é possível confirmar.')
            return redirect('principal:menu_aluno')

        if 'confirmar' in request.POST:
            if presenca:
                messages.warning(request, 'Você já está na lista.')
            elif total_confirmados >= max_usuarios:
                messages.error(request, 'Lista cheia. Aguarde próxima oportunidade.')
            else:
                Presenca.objects.create(lista=lista, aluno=aluno)
                messages.success(request, 'Presença confirmada!')

        elif 'remover' in request.POST:
            if presenca:
                presenca.delete()
                messages.success(request, 'Presença removida da lista.')
            else:
                messages.warning(request, 'Você não está na lista.')

        return redirect('principal:menu_aluno')

    presencas = lista.presencas.select_related('aluno').order_by('confirmado_em')

    return render(request, 'principal/menu_aluno.html', {
        'lista': lista,
        'presenca': presenca,
        'presencas': presencas,
        'max_usuarios': max_usuarios,
        'total_confirmados': total_confirmados,
    })


@login_required
@user_passes_test(is_admin)
def menu_admin(request):
    hoje = date.today()
    lista, created = ListaDia.objects.get_or_create(data=hoje)
    presencas = lista.presencas.select_related('aluno').order_by('confirmado_em')
    total_confirmados = presencas.count()
    max_usuarios = 50

    if request.method == 'POST':
        if 'abrir' in request.POST:
            lista.aberta = True
            lista.save()
            messages.success(request, 'Lista aberta.')
        elif 'fechar' in request.POST:
            lista.aberta = False
            lista.save()
            messages.success(request, 'Lista fechada.')

        return redirect('principal:menu_admin')

    return render(request, 'principal/menu_admin.html', {
        'lista': lista,
        'presencas': presencas,
        'total_confirmados': total_confirmados,
        'max_usuarios': max_usuarios,
    })


# --- Views para CRUD de alunos (somente admin) ---

@login_required
@user_passes_test(is_admin)
def listar_alunos(request):
    alunos = Aluno.objects.select_related('user').all()
    return render(request, 'principal/listar_alunos.html', {'alunos': alunos})


@login_required
@user_passes_test(is_admin)
def criar_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Usuário já existe.')
            else:
                user = User.objects.create_user(username=username, password=password)
                aluno = form.save(commit=False)
                aluno.user = user
                aluno.save()
                messages.success(request, 'Aluno criado com sucesso!')
                return redirect('principal:listar_alunos')
    else:
        form = AlunoForm()
    return render(request, 'principal/form_aluno.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            aluno = form.save(commit=False)
            senha = form.cleaned_data.get('password')
            if senha:
                aluno.user.set_password(senha)
                aluno.user.save()
            aluno.save()
            messages.success(request, 'Aluno atualizado com sucesso!')
            return redirect('principal:listar_alunos')
    else:
        initial = {'username': aluno.user.username, 'password': ''}
        form = AlunoForm(instance=aluno, initial=initial)
    return render(request, 'principal/form_aluno.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def excluir_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    if request.method == 'POST':
        aluno.user.delete()
        aluno.delete()
        messages.success(request, 'Aluno excluído com sucesso!')
        return redirect('principal:listar_alunos')
    return render(request, 'principal/confirma_exclusao.html', {'aluno': aluno})
