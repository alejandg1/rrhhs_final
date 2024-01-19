from django import forms
from django.forms import ModelForm
from apps.personal_debt.models import CreditsDetail


class CreditsDetailForm(ModelForm):
    class Meta:
        model = CreditsDetail
        fields = '__all__'
        exclude = ['calendar_quota_processed',
                   'status_quota_processed', 'balance_quota_processed']
        widgets = {
            'date_discount': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Fecha de cuota'}),
        }
