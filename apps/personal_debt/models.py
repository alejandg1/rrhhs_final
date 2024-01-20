from django.db import models
from django.forms import model_to_dict
from apps.core.models import ModelBase
from apps.payment_role.models import Item
from apps.personal_file.models import Employee
from rrhhs.const import CREDIT_STATUS, CREDIT_INTEREST


class Credit(ModelBase):
    employee = models.ForeignKey(
        Employee, on_delete=models.PROTECT, verbose_name='Empleado')
    item = models.ForeignKey(
        Item, on_delete=models.PROTECT, verbose_name='Tipo Descuento',
        limit_choices_to={'type_item': 2})
    date_credit = models.DateTimeField(verbose_name='Fecha desde')
    date_initial = models.DateTimeField(verbose_name='Fecha hasta')
    interest = models.IntegerField(
        verbose_name="Interes(%)",
        choices=CREDIT_INTEREST,
        default=CREDIT_INTEREST[1][1])
    interestval = models.DecimalField(
        verbose_name="Valor Interes",
        decimal_places=2,
        max_digits=10,
        null=True)
    loan_val = models.FloatField(
        verbose_name="Valor Prestamo", default=0)
    nume_quota = models.IntegerField("Numero Cuotas", blank=True, null=True)
    balance = models.DecimalField(
        verbose_name="Saldo", decimal_places=2, max_digits=10)
    statusid = models.IntegerField(
        verbose_name="estado",
        choices=CREDIT_STATUS,
        default=CREDIT_STATUS[0][0])
    status = models.CharField(verbose_name="status", default="")
    reason = models.CharField(
        verbose_name="Observacion", max_length=200, blank=True, null=True)
    active = models.BooleanField(verbose_name='Activo', default=True)
    calendar_processed = models.IntegerField(
        "Calendario Procesado", blank=True, null=True)
    status_processed = models.IntegerField(
        verbose_name='estado Procesado', default=0)
    balance_processed = models.DecimalField(
        verbose_name="Saldo Procesado", decimal_places=2, max_digits=10)

    def get_model_to_dict(self):
        model = model_to_dict(self)
        return model

    def __str__(self):
        return f'{self.item.description} - {self.employee.get_full_name()}'

    def save(self, *args, **kwargs):
        self.interestval = round((self.interest/100)*self.loan_val)
        self.balance = (self.loan_val+self.interestval)
        self.balance_processed = self.balance
        self.status = CREDIT_STATUS[self.statusid-1][1]
        self.status_processed = self.statusid
        super().save(self, *args, **kwargs)

    class Meta:
        verbose_name = 'Descuento'
        verbose_name_plural = 'Descuentos'
        ordering = ['id']


class CreditsDetail(ModelBase):
    credit = models.ForeignKey(
        Credit, on_delete=models.CASCADE, verbose_name='Credito')
    date_discount = models.DateTimeField(verbose_name='Fecha Descuento')
    quota = models.IntegerField("Numero Cuota", default=0)
    status = models.BooleanField(
        verbose_name="Procesado", default=False)
    balance_quota = models.DecimalField(
        verbose_name="Saldo Cuota", decimal_places=2, max_digits=10)
    calendar_quota_processed = models.IntegerField(
        "Calendario Procesado", blank=True, null=True)
    status_quota_processed = models.BooleanField(
        verbose_name='Activo Procesado', default=False)
    balance_quota_processed = models.DecimalField(
        verbose_name="Saldo Procesado cuotas", decimal_places=2, max_digits=10)

    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item

    def save(self, *args, **kwargs):
        self.balance_quota_processed = self.balance_quota
        self.status_quota_processed = self.status
        # self.calendar_quota_processed = self.date_discount
        super().save(self, *args, **kwargs)

    def __str__(self):
        return f'{self.date_discount} - {self.quota}'

    class Meta:
        verbose_name = 'Prestamo Detalle'
        verbose_name_plural = 'Prestamos Detalles'
        ordering = ['id']
