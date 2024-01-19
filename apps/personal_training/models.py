from django.db import models
from crum import get_current_user
from django.forms import model_to_dict
from apps.core.models import ModelBase, Organization
from apps.personal_file.models import Employee
from django.utils.timezone import now
from django.core.validators import FileExtensionValidator

class Supplier(ModelBase):
    name = models.CharField("Nombre", max_length=100)
    address = models.CharField("Dirección", max_length=100)
    phone = models.CharField("Telefono", max_length=20,blank=True,null=True)
    email = models.EmailField("Correo", blank=True,null=True)
    website = models.CharField("Pagina web", max_length=100,blank=True,null=True)
    description = models.TextField("Descripcion", blank=True,null=True)
    state = models.BooleanField("Activo", default=True)

    def __str__(self):
        return self.name

    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'supplier'
        ordering = ['name']
        ordering = ('-id',)


class Course(ModelBase):
    name = models.CharField("Nombre", max_length=100)
    description = models.TextField("Descripcion", blank=True,null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT,verbose_name='Proveedor')
    fecha_inicio = models.DateField("Fecha de inicio", blank=True,null=True)
    fecha_fin = models.DateField("Fecha de fin", blank=True,null=True)
    state = models.BooleanField("Activo", default=True)

    def __str__(self):
        return self.name

    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'course'
        ordering = ['name']
        ordering = ('-id',)


class Application(ModelBase):
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,verbose_name='Empleado')
    course = models.ForeignKey(Course, on_delete=models.PROTECT,verbose_name='Curso')
    sucursal = models.ForeignKey(Organization,on_delete=models.PROTECT,verbose_name='Sucursal', blank=True, null=True)
    description = models.CharField("Descripcion", max_length=500)
    year = models.IntegerField(verbose_name="Año Curso")
    fecha_inicio = models.DateField("Fecha de inicio", blank=True,null=True)
    fecha_fin = models.DateField("Fecha de fin", blank=True,null=True)
    approved_boss = models.BooleanField("Aprobado jefe", default=False)
    approved_commission = models.BooleanField("Aprobado Comision", default=False)
    cost = models.DecimalField(verbose_name="Costo Curso", decimal_places=2,max_digits=18)
    state = models.BooleanField("Activo", default=False)
    

    def __str__(self):
        return self.name

    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'application'
        ordering = ('-id',)

class Certificate(ModelBase):
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,verbose_name='Empleado')
    course = models.ForeignKey(Course, on_delete=models.PROTECT,verbose_name='Curso')
    note = models.IntegerField("Nota", blank=True)
    certificado_pdf = models.FileField(upload_to='certificados/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    #certificado_pdf = models.FileField(upload_to='certificados/', verbose_name="certificado")

    def __str__(self):
        return self.employee.get_full_name() + ' - ' + self.course.name

    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'certificate'
        ordering = ('-id',)
