from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from apps.personal_debt.models import Credit


class CreditForm(ModelForm):
    class Meta:
        model = Credit
        fields = '__all__'
        exclude = ['status','calendar_processed',
                   'status_processed', 'balance_processed', 'interestval', 'balance']
        widgets = {
            'date_credit': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_initial': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean(self):
        credit_clean = super().clean()
        date_credit = credit_clean.get('date_credit')
        date_initial = credit_clean.get('date_initial')
        if date_credit > date_initial:
            raise ValidationError(
                'La fecha de inicio no puede ser menor a la fecha de crédito')
        return credit_clean
