from django.forms import ModelForm
from apps.payment_role.models import WorkPermission

class WorkpermissionForm(ModelForm):
    class Meta:
        model = WorkPermission
        fields = '__all__'
        exclude = ['date_to', 'time_earring']