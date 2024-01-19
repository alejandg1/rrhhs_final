from django.urls import reverse_lazy
from rrhhs.const import CREDIT_STATUS
from apps.personal_debt.models import Credit
from apps.personal_debt.forms.credit import CreditForm

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q
from apps.security.mixins.mixins import ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin, PermissionMixin


class CreditListView(ListViewMixin, ListView):
    model = Credit
    template_name = 'credit/list.html'
    context_object_name = 'credits'
    permission_required = 'view_credit'

    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q1')  # ver
        if q1 is not None:
            self.query.add(Q(code__icontains=q1), Q.AND)
        # q2 = self.request.GET.get('q2') # ver
        # if q2 is not None:
        #     query.add(Q(estado__icontains=q2), Q.AND)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creditos'
        context['estado'] = CREDIT_STATUS
        context['create_url'] = reverse_lazy('personal_debt:credit_create')
        context['permission_add'] = context['permissions'].get(
            'add_credit', '')
        return context


class CreditCreateView(CreateViewMixin, CreateView):
    model = Credit
    template_name = 'credit/form.html'
    form_class = CreditForm
    success_url = reverse_lazy('personal_debt:credit_list')
    permission_required = 'add_credit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar credito'
        context['back_url'] = self.success_url
        return context


class CreditUpdateView(UpdateViewMixin, UpdateView):
    model = Credit
    template_name = 'credit/form.html'
    form_class = CreditForm
    success_url = reverse_lazy('personal_debt:credit_list')
    permission_required = 'change_credit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar credito'
        context['back_url'] = self.success_url
        return context


class CreditDeleteView(DeleteViewMixin, DeleteView):
    model = Credit
    template_name = 'credit/delete.html'
    success_url = reverse_lazy('personal_debt:credit_list')
    permission_required = 'delete_credit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar credito'
        context['description'] = f"¿Desea Eliminar el credito: {self.object.id}?"
        context['back_url'] = self.success_url
        return context
