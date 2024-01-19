from django.urls import reverse_lazy
from apps.personal_debt.models import CreditsDetail
from apps.personal_debt.forms.credit_detail import CreditsDetailForm

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q
from apps.security.mixins.mixins import ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin, PermissionMixin


class CreditsDetailListView(ListViewMixin, ListView):
    model = CreditsDetail
    template_name = 'credit_detail/list.html'
    context_object_name = 'creditsDetails'
    permission_required = 'view_creditsDetail'

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
        context['create_url'] = reverse_lazy(
            'personal_debt:creditDetail_create')
        context['permission_add'] = context['permissions'].get(
            'add_creditsdetail', '')
        return context


class CreditsDetailCreateView(CreateViewMixin, CreateView):
    model = CreditsDetail
    template_name = 'credit_detail/form.html'
    form_class = CreditsDetailForm
    success_url = reverse_lazy('personal_debt:creditDetail_list')
    permission_required = 'add_creditsdetail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar credito'
        context['back_url'] = self.success_url
        return context


class CreditsDetailUpdateView(UpdateViewMixin, UpdateView):
    model = CreditsDetail
    template_name = 'credit_detail/form.html'
    form_class = CreditsDetailForm
    success_url = reverse_lazy('personal_debt:creditDetail_list')
    permission_required = 'change_creditsdetail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar credito'
        context['back_url'] = self.success_url
        return context


class CreditsDetailDeleteView(DeleteViewMixin, DeleteView):
    model = CreditsDetail
    template_name = 'credit_detail/delete.html'
    success_url = reverse_lazy('personal_debt:creditDetail_list')
    permission_required = 'delete_creditsdetail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar credito'
        context['description'] = f"¿Desea Eliminar el credito: {self.object.id}?"
        context['back_url'] = self.success_url
        return context
