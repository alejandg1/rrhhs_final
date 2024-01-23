from apps.security.mixins.mixins import ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin, PermissionMixin
from datetime import datetime
from django.db.models import Q
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from apps.personal_debt.forms.credit import CreditForm
from apps.personal_debt.models import Credit, CreditsDetail
from rrhhs.const import CREDIT_STATUS
from django.views import View
from django.http import JsonResponse
from django.urls import reverse_lazy
import json


class CreditListView(ListViewMixin, ListView):
    model = Credit
    template_name = 'credit/list.html'
    context_object_name = 'credits'
    permission_required = 'view_credit'

    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q1')  # ver
        if q1 is not None:
            self.query.add(Q(employee__last_name__icontains=q1), Q.AND)
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

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            print("form: ", form.errors)
            return JsonResponse({}, status=400)
        data = request.POST
        item_id = data['item']
        emp_id = data['employee']
        datec = data['date_credit']
        datei = data['date_initial']
        interest = data['interest']
        loan_val = data['loan_val']
        statusid = data['statusid']
        # active = data['active']
        if 'active' in request.POST:
            active = data['active']
        else:
            active = 'off'
        nume_quota = data['nume_quota']
        # credit = Credit.objects.get(id=self.kwargs.get('pk'))
        credit = Credit.objects.create(
            item_id=item_id,
            employee_id=emp_id,
            date_initial=datetime.strptime(datei[:10], '%Y-%m-%d'),
            date_credit=datetime.strptime(datec[:10], '%Y-%m-%d'),
            interest=int(interest),
            loan_val=float(loan_val),
            statusid=int(statusid),
            active=True if active == "on" else False,
            nume_quota=nume_quota
        )
        # credit.save()
        details = json.loads(request.POST['detail'])
        for detail in details:
            CreditsDetail.objects.create(
                credit_id=credit.id,
                date_discount=datetime.strptime(
                    detail['date'][:10], '%Y-%m-%d'),
                quota=detail['quote'],
                # status=True if detail['status'] == "on" else False,
                balance_quota=detail['balance']
            )
        return JsonResponse({}, status=200)


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
        detcretit = list(
            CreditsDetail.objects.filter(
                credit=self.object.id).values(
                'id',
                'balance_quota',
                'status',
                'date_discount',
                'quota')
        )
        lista = []
        for det in detcretit:
            lista.append({"det_id": det['id'],
                          "bal": float(det['balance_quota']),
                          # "status": det['status'],
                          "quote": det['quota'],
                          "date": det['date_discount'].isoformat()
                          })
        context['detail_credit'] = json.dumps(lista)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            return JsonResponse({}, status=400)
        data = request.POST
        item_id = data['item']
        emp_id = data['employee']
        datec = datetime.strptime(data['date_credit'][:10], '%Y-%m-%d')
        datei = datetime.strptime(data['date_initial'][:10], '%Y-%m-%d')
        interest = data['interest']
        loan_val = data['loan_val']
        statusid = data['statusid']
        if 'active' in request.POST:
            active = True if data['active'] == "on" else False
        else:
            active = False
        nume_quota = data['nume_quota']
        credit = Credit.objects.get(id=self.kwargs.get('pk'))
        credit.item_id = item_id
        credit.employee_id = emp_id
        credit.date_initial = datei
        credit.date_credit = datec
        credit.interest = int(interest)
        credit.loan_val = float(loan_val)
        credit.statusid = int(statusid)
        credit.active = active
        credit.nume_quota = nume_quota
        credit.save()
        details = json.loads(request.POST['detail'])
        CreditsDetail.objects.filter(credit=credit.id).delete()
        for detail in details:
            CreditsDetail.objects.create(
                credit_id=credit.id,
                date_discount=datetime.strptime(
                    detail['date'][:10], '%Y-%m-%d'),
                quota=detail['quote'],
                # status=True if detail['status'] == "on" else False,
                balance_quota=detail['balance']
            )
        return JsonResponse({}, status=200)


class CreditDeleteView(DeleteViewMixin, DeleteView):
    model = Credit
    template_name = 'credit/delete.html'
    success_url = reverse_lazy('personal_debt:credit_list')
    permission_required = 'delete_credit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar credito'
        context['description'] = f"""¿Desea Eliminar el credito:
        {self.object.id}?"""
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
            print(det_credit)
            for det in det_credit:
                lista.append({"id": det.id,
                              "dat": det.date_discount,
                              "quo": det.quota,
                              "balance": det.balance_quota
                              })
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
