from django import forms

class ConfirmaPresencaForm(forms.Form):
    confirmar = forms.BooleanField(label='Confirmar presença', required=True)