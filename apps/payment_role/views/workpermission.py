from django.urls import reverse_lazy
from apps.payment_role.forms.workpermission import WorkpermissionForm
from apps.payment_role.models import WorkPermission

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q

from apps.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin


class WorkpermissionListView(PermissionMixin, ListViewMixin, ListView):
    model = WorkPermission
    template_name = 'workpermission/list.html'
    context_object_name = 'workpermission'
    permission_required = "view_workpermission"

    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q1')  # ver
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.AND)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('payment_role:workpermission_create')
        context['permission_add'] = context['permissions'].get('add_workpermission', '')
        return context


class WorkpermissionCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = WorkPermission
    template_name = 'workpermission/form.html'
    form_class = WorkpermissionForm
    success_url = reverse_lazy('payment_role:workpermission_list')
    permission_required = "add_workpermission"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Tipo de Permiso'
        context['back_url'] = self.success_url
        return context


class WorkpermissionUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = WorkPermission
    template_name = 'workpermission/form.html'
    form_class = WorkpermissionForm
    success_url = reverse_lazy('payment_role:workpermission_list')
    permission_required = "change_workpermission"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar workpermission'
        context['back_url'] = self.success_url
        return context


class WorkpermissionDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = WorkPermission
    template_name = 'workpermission/delete.html'
    success_url = reverse_lazy('payment_role:workpermission_list')
    permission_required = "delete_workpermission"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Tipo de permiso'
        context['description'] = f"¿Desea Eliminar El Tipo de Permiso: {self.object.get_full_name()}?"
        context['back_url'] = self.success_url
        return context
