from django.urls import reverse_lazy
from apps.biometric_clock.forms.jornada import JornadaForm
from apps.biometric_clock.models import Jornada

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q

from apps.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin


class JornadaListView(PermissionMixin,ListViewMixin,ListView):
    model = Jornada
    template_name = 'jornada/list.html'
    context_object_name = 'jornada'
    permission_required="view_jornada"
    # paginate_by = 3
    # query=None
    
    def get_queryset(self):
        self.query=Q()
        q1 = self.request.GET.get('q1') # ver
        if q1 is not None:
            self.query.add(Q(descripcion__icontains=q1), Q.AND) 
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('biometric_clock:jornada_create')
        context['permission_add'] = context['permissions'].get('add_jornada','')
        
        return context
    
class JornadaCreateView(PermissionMixin,CreateViewMixin,CreateView,):
    model = Jornada
    template_name = 'jornada/form.html'
    form_class = JornadaForm
    success_url = reverse_lazy('biometric_clock:jornada_list')
    permission_required="add_jornada"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Jornada'
        context['back_url'] = self.success_url
        return context

class JornadaUpdateView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = Jornada
    template_name = 'jornada/form.html'
    form_class = JornadaForm
    success_url = reverse_lazy('biometric_clock:jornada_list')
    permission_required="update_jornada"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Jornada'
        context['back_url'] = self.success_url
        return context
    
class JornadaDeleteView(PermissionMixin,DeleteViewMixin,DeleteView):
    model = Jornada
    template_name = 'jornada/delete.html'
    success_url = reverse_lazy('biometric_clock:jornada_list')
    permission_required="delete_jornada"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Jornada'
        context['description'] = f"¿Desea Eliminar La Jornada: {self.object.get_full_name()}?"
        context['back_url'] = self.success_url
        return context