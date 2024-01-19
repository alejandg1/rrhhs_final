from django.forms import ModelForm
from apps.biometric_clock.models import MarcadaReloj

class MarcadaRelojForm(ModelForm):
    class Meta:
        model = MarcadaReloj
        fields = '__all__'
