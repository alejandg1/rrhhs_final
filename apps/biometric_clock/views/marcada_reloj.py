from django.urls import reverse_lazy
from apps.biometric_clock.forms.marcada_reloj import MarcadaRelojForm
from apps.biometric_clock.models import MarcadaReloj


from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q

from apps.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin

class MarcadaRelojListView(PermissionMixin,ListViewMixin,ListView):
    model = MarcadaReloj
    template_name = 'marcada_reloj/list.html'
    context_object_name = 'marcadas_reloj'
    permission_required="view_marcadareloj"
    
    def get_queryset(self):
        query = self.request.GET.get('q1')

        if query:
            queryset = self.model.objects.filter(Q(empleado__firts_name__icontains=query))
            return queryset
        else:
            return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('biometric_clock:marcada_reloj_create')
        context['permission_add'] = context['permissions'].get('add_marcadareloj','')
        
        return context
    
class Marcada_RelojCreateView(PermissionMixin,CreateViewMixin,CreateView,):
    model = MarcadaReloj
    template_name = 'marcada_reloj/form.html'
    form_class = MarcadaRelojForm
    success_url = reverse_lazy('biometric_clock:marcada_reloj_list')
    permission_required="add_marcadareloj"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar marcada de reloj'
        context['back_url'] = self.success_url
        return context

class Marcada_RelojUpdateView(PermissionMixin,UpdateViewMixin,UpdateView):
    model = MarcadaReloj
    template_name = 'marcada_reloj/form.html'
    form_class = MarcadaRelojForm
    success_url = reverse_lazy('biometric_clock:marcada_reloj_list')
    permission_required="change_marcadareloj"
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar reloj'
        context['back_url'] = self.success_url
        return context
    
class Marcada_RelojDeleteView(PermissionMixin,DeleteViewMixin,DeleteView):
    model = MarcadaReloj
    template_name = 'marcada_reloj/delete.html'
    success_url = reverse_lazy('biometric_clock:marcada_reloj_list')
    permission_required="delete_marcadareloj"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Reloj'
        context['description'] = f"¿Desea Eliminar la asistencia?: {self.object.get_full_name()}?"
        context['back_url'] = self.success_url
        return context