from datetime import datetime
from rrhhs.const import CREDIT_INTEREST
import json
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from ventas.forms.factura import CabeceraForm
from ventas.models import Cabecera, Detalle, Product
from apps.security.mixins.mixins import ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin, PermissionMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.db.models import Q


class CabeceraListView(PermissionMixin, ListViewMixin, ListView):
    model = Cabecera
    template_name = 'factura/list.html'
    context_object_name = 'factura'
    permission_required = "view_cabecera"

    def get_queryset(self):

        q1 = self.request.GET.get('q1')
        if q1 is not None:
            self.query.add(Q(client__last_name__icontains=q1), Q.AND)
        print("request", self.request.user)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'factura'
        context['create_url'] = reverse_lazy('ventas:cabecera_create')
        context['permission_add'] = context['permissions'].get(
            'add_cabecera', '')

        return context


class CabeceraCreateView(PermissionMixin, CreateViewMixin, CreateView,):
    model = Cabecera
    template_name = 'factura/form.html'
    form_class = CabeceraForm
    success_url = reverse_lazy('ventas:cabecera_list')
    permission_required = "add_cabecera"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar factura'
        context['back_url'] = self.success_url
        context['products'] = Product.objects.filter(
            stock__gt=0).order_by('id')
        context['details'] = []
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            print("form:", form.errors)
            return JsonResponse({}, status=400)
        data = request.POST
        client = data['client']
        date = data['date']
        subtotal = data['subtotal']
        total = data['total']
        iva = CREDIT_INTEREST[int(data['iva'])-1][1]
        cabecera = Cabecera.objects.create(
            client_id=client,
            # date=date,
            date=datetime.strptime(date[:10], '%Y-%m-%d'),
            subtotal=subtotal,
            total=total,
            iva=iva
        )

        details = json.loads(request.POST['detail'])
        Detalle.objects.filter(cabecera_id=cabecera.id).delete()
        for detail in details:
            Detalle.objects.create(
                cabecera_id=cabecera.id,
                product_id=detail['product'],
                quantity=detail['quantity'],
                subtotal=detail['subtotal']
            )
        return JsonResponse({}, status=200)


class CabeceraUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Cabecera
    template_name = 'factura/form.html'
    form_class = CabeceraForm
    success_url = reverse_lazy('ventas:cabecera_list')
    permission_required = "update_cabecera"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Factura'
        context['back_url'] = self.success_url
        context['products'] = Product.objects.filter(
            stock__gt=0).order_by('id')
        detCabecera = list(Detalle.objects.filter(
            cabecera_id=self.object.id).values(
            "product__name",
            "quantity",
            "product__price",
            "product__id",
            "subtotal"
        ))
        lista = []
        for det in detCabecera:
            lista.append(
                {"prod": det['product__name'],
                 "quant": float(det["quantity"]),
                 "price": float(det['product__price']),
                 "product_id": float(det['product__id']),
                 "subtotal": float(det["subtotal"]),
                 })

        context['details'] = json.dumps(lista)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            return JsonResponse({}, status=400)
        data = request.POST
        client = data['client']
        # date = data['date']
        date = datetime.strptime(data['date'][:10], '%Y-%m-%d')
        subtotal = data['subtotal']
        total = data['total']
        iva = CREDIT_INTEREST[int(data['iva'])-1][1]
        cabecera = Cabecera.objects.get(id=self.kwargs.get('pk'))
        cabecera.client_id = client
        cabecera.date = date
        cabecera.subtotal = subtotal
        cabecera.total = total
        cabecera.iva = iva
        cabecera.save()
        details = json.loads(request.POST['detail'])
        Detalle.objects.filter(cabecera_id=cabecera.id).delete()
        for detail in details:
            Detalle.objects.create(
                cabecera_id=cabecera.id,
                product_id=detail['product'],
                quantity=detail['quantity'],
                subtotal=detail['subtotal']
            )
        return JsonResponse({}, status=200)


class CabeceraDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):

    model = Cabecera
    template_name = 'factura/delete.html'
    success_url = reverse_lazy('ventas:cabecera_list')
    permission_required = "delete_cabecera"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar factura'
        context['description'] = f"""
        ¿Desea Eliminar la factura de los registros:
        de {self.object.client}?"""
        context['back_url'] = self.success_url

        return context


class CabeceraDetailView(PermissionMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            cabecera = Cabecera.objects.get(
                id=request.GET.get('id')
            )

            det_cabecera = Detalle.objects.filter(
                cabecera_id=cabecera.id)
            # model_to_dict(overtime)
            lista = []
            for det in det_cabecera:
                lista.append({
                    "product": det.product.name,
                    "quantity": det.quantity,
                    "value": det.subtotal
                })
            return JsonResponse({'factura':
                                 {'id': cabecera.id,
                                  'client': cabecera.client.getFullName(),
                                  'date': cabecera.date,
                                  'total': cabecera.total,
                                  'iva': cabecera.iva,
                                  },
                                 "detail": lista
                                 }, status=200)

        except Exception as ex:
            return JsonResponse({"message": ex}, status=400)
