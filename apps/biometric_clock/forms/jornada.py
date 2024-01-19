from django.forms import ModelForm
from apps.biometric_clock.models import Jornada

class JornadaForm(ModelForm):
    class Meta:
        model = Jornada
        fields = '__all__'