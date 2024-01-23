from django import forms
from django.forms import ModelForm
from ventas.models import Cabecera, Detalle


class CabeceraForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
        )
    )

    class Meta:
        model = Cabecera
        fields = '__all__'
        # exclude = ['id']

    # class Meta:
    #     model = Detalle
    #     fields = '__all__'
