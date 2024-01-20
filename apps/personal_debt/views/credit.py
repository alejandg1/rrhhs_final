from typing import Any

from django.urls import reverse_lazy
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from rrhhs.const import CREDIT_STATUS
from apps.personal_debt.models import Credit, CreditsDetail
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
        context['detail_credit'] = []
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        if not form.is_valid():
            print("form:", form.errors)
            return JsonResponse({}, status=400)
        data = request.POST
        print(data)
        return super().post(request, *args, **kwargs)
        data = request.POST
        employee = data['employee']
        item = data['item']
        date_initial = data['date_initial']
        interestval = data['interestval']
        balance = data['balance']
        loan_val = data['loan_val']
        cabezera = Credit.objects.create(
            employee_id=employee,
            item_id=item,
            date_initial=date_initial,
            interestval=interestval,
            balance=balance,
            loan_val=loan_val
        )
        details = json.loads(request.POST['detail'])
        for detail in details:
            CreditsDetail.objects.create(
                credit_id=cabezera.id,
                date_discount=detail['dat'],
                balance_quota=detail['quo'],
                status=detail['est'],
                quote=detail['quote']
            )
        return JsonResponse({'id': cabezera.id}, status=200)


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


class CreditDetailView(PermissionMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            credit = Credit.objects.get(
                id=request.GET.get('id')
            )

            det_credit = CreditsDetail.objects.filter(
                credit=credit.id)
            lista = []
            for det in det_credit:
                lista.append({"id": det.item.id,
                              "dat": det.item.date_discount,
                              "quo": det.item.quota,
                              "est": det.item.status
                              })
                print(lista)

            return JsonResponse({'credit':
                                 {'id': credit.id,
                                  'empleado': credit.employee.get_full_name(),
                                  'item': credit.item.name_short,
                                  'registro': credit.date_initial,
                                  'interes': credit.interestval,
                                  'balance': credit.balance,
                                  'prestamo': credit.loan_val,
                                  },
                                 "detail": lista
                                 }, status=200)

        except Exception as ex:
            print(ex)
            return JsonResponse({"message": "error"}, status=400)
