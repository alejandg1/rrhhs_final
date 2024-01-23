
import json
from django.forms import model_to_dict
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
        # data = form.save(commit=False)
        if not form.is_valid():
            print("form:", form.errors)
            return JsonResponse({}, status=400)
        data = request.POST
        client = data['client']
        date = data['date']
        subtotal = data['subtotal']
        total = data['total']
        iva = data['iva']
        cabecera = Cabecera.objects.create(
            client_id=client,
            date=date,
            subtotal=subtotal,
            total=total,
            iva=iva
        )

        details = json.loads(request.POST['detail'])
        Detalle.objects.filter(overtime_id=cabecera.id).delete()
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
    success_url = reverse_lazy('payment_role:overtime_list')
    permission_required = "update_overtime"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Factura'
        context['back_url'] = self.success_url
        context['products'] = Product.objects.filter(
            stock__gt=0).order_by('id')
        detCabecera = list(Detalle.objects.filter(
            factura_id=self.object.id).values(
            "factura__client__first_name",
            "factura__client__last_name",
            "product__name",
            "quantity",
            "unitprice"
        ))
        lista = []
        for det in detCabecera:
            lista.append(
                {"cliente": det["factura__client__first_name"]+' '+det['factura__client__last_name'],
                 "prod": det['product__name'],
                 "quant": float(det["quantity"]),
                 "unirp": float(det["unitprice"]),
                 })

        context['details'] = json.dumps(lista)
        print(context['details'])
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            return JsonResponse({}, status=400)
        data = request.POST
        client = data['client']
        date = data['date']
        subtotal = data['subtotal']
        total = data['total']
        iva = data['iva']
        cabecera = Cabecera.objects.get(id=self.kwargs.get('pk'))
        print(cabecera)
        cabecera.client = client
        cabecera.employee_id = date
        cabecera.value_hour = subtotal
        cabecera.total = total
        cabecera.iva = iva
        cabecera.save()
        details = json.loads(request.POST['detail'])
        Detalle.objects.filter(overtime_id=cabecera.id).delete()
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
        context['description'] = f"¿Desea Eliminar la factura de los registros: de {self.object.client}?"
        context['back_url'] = self.success_url

        return context


# class CabeceraValueHours(PermissionMixin, View):

#     def get(self, request, *args, **kwargs):
#         action = request.GET.get('action', None)
#         if action == 'value_hours':
#             try:
#                 employee = Employee.objects.get(
#                     id=request.GET.get('idemp')
#                 )
#                 value_hour = str(round(employee.sueldo/240, 2))
#                 sucursal = str(employee.sucursal_id)
#                 return JsonResponse({'hour': value_hour, "sucursal": sucursal}, status=200)

#             except Exception as ex:
#                 return JsonResponse({"message": ex}, status=400)

#         return JsonResponse({}, status=400)


class CabeceraDetailView(PermissionMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            overtime = Cabecera.objects.get(
                id=request.GET.get('id')
            )

            det_overtime = Detalle.objects.filter(
                overtime_id=overtime.id)
            # model_to_dict(overtime)
            lista = []
            for det in det_overtime:
                lista.append({"id": det.item.id, "des": det.item.name_short,
                              "fac": det.item.value, "nh": det.number_hours,
                              "vh": det.value})

            return JsonResponse({'overtime': {'id': overtime.id,
                                              'calendar': overtime.calendar.codigo_rol,
                                              'empleado': overtime.employee.get_full_name(),
                                              'sucursal': overtime.sucursal.name,
                                              'value_hour': overtime.value_hour,
                                              'total': overtime.total,
                                              'proceso': overtime.processed,

                                              },
                                 "detail": lista}, status=200)

        except Exception as ex:
            return JsonResponse({"message": ex}, status=400)
