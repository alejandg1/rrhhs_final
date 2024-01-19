from django.forms import ModelForm
from apps.payment_role.models import TypePermission

class TypepermissionForm(ModelForm):
    class Meta:
        model = TypePermission
        fields = '__all__'