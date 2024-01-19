from django.urls import reverse_lazy
from apps.payment_role.forms.typepermission import TypepermissionForm
from apps.payment_role.models import TypePermission

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q

from apps.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin


class TypePermissionListView(PermissionMixin, ListViewMixin, ListView):
    model = TypePermission
    template_name = 'typePermission/list.html'
    context_object_name = 'typePermission'
    permission_required = "view_typepermission"

    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q1')  # ver
        if q1 is not None:
            self.query.add(Q(name__icontains=q1), Q.AND)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('payment_role:typePermission_create')
        context['permission_add'] = context['permissions'].get('add_typepermission', '')
        return context


class TypePermissionCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = TypePermission
    template_name = 'typePermission/form.html'
    form_class = TypepermissionForm
    success_url = reverse_lazy('payment_role:typePermission_list')
    permission_required = "add_typepermission"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Tipo de Permiso'
        context['back_url'] = self.success_url
        return context


class TypePermissionUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = TypePermission
    template_name = 'typePermission/form.html'
    form_class = TypepermissionForm
    success_url = reverse_lazy('payment_role:typePermission_list')
    permission_required = "change_typepermission"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar typePermission'
        context['back_url'] = self.success_url
        return context


class TypePermissionDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = TypePermission
    template_name = 'typePermission/delete.html'
    success_url = reverse_lazy('payment_role:typePermission_list')
    permission_required = "delete_typepermission"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Tipo de permiso'
        context['description'] = f"¿Desea Eliminar El Tipo de Permiso: {self.object.get_full_name()}?"
        context['back_url'] = self.success_url
        return context
