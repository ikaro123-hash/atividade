from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class ListaDia(models.Model):
    data = models.DateField(default=timezone.now, unique=True)
    aberta = models.BooleanField(default=True)

    def __str__(self):
        return f'Lista {self.data.strftime("%d/%m/%Y")} - {"Aberta" if self.aberta else "Fechada"}'

class Presenca(models.Model):
    lista = models.ForeignKey(ListaDia, on_delete=models.CASCADE, related_name='presencas')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    confirmado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lista', 'aluno')
        ordering = ['confirmado_em']  # garante ordem cronológica

    def posicao(self):
        # Posição na lista (1 a n)
        presencas = Presenca.objects.filter(lista=self.lista).order_by('confirmado_em').values_list('id', flat=True)
        try:
            return list(presencas).index(self.id) + 1
        except ValueError:
            return None

