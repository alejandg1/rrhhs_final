from django.db import models
from django.forms import model_to_dict
from apps.core.models import ModelBase

 # weekday() devuelve un número donde 0 representa el lunes y 6 representa el domingo.
 # numero_dia =  fecha.weekday()

dias = (("Lunes", "Lunes"), 
        ("Martes", "Martes"), 
        ("Miercoles", "Miércoles"), 
        ("Jueves", "Jueves"), 
        ("Viernes", "Viernes"), 
        ("Sabado", "Sábado"), 
        ("Domingo", "Domingo"))

class Jornada(ModelBase):
    descripcion = models.CharField("Jornada", max_length=200)
    dia_desde = models.CharField(max_length=50, choices=dias, default="Lunes")
    dia_hasta = models.CharField(max_length=50, choices=dias, default="Viernes")
    hora_entrada = models.TimeField(null = True, blank = True)
    hora_entrada_lunch = models.TimeField(null = True, blank = True)
    hora_salida_lunch = models.TimeField(null = True, blank = True)
    hora_salida = models.TimeField(null = True, blank = True)
    horas_trabajo=models.IntegerField("Horas Trabajadas",default=8)
    
    def __str__(self):
        return self.descripcion
    
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item
    
    def get_full_name(self):
        return f"{self.descripcion}"
    
    class Meta:
        verbose_name = 'Jornada'
        verbose_name_plural = 'Jornadas'
        ordering = ('-id',)
    
from apps.personal_file.models import Employee
class MarcadaReloj(ModelBase):
    empleado = models.ForeignKey(Employee, on_delete=models.CASCADE)
    jornada = models.ForeignKey(Jornada, on_delete=models.CASCADE)
    fecha = models.DateField()
    
    hora_entrada = models.TimeField(blank=True, null=True)
    atraso_entrada = models.BooleanField(default= False)
    
    hora_entrada_lunch = models.TimeField(blank=True, null=True)
    hora_salida_lunch = models.TimeField(blank=True, null=True)
    atraso_lunch = models.BooleanField(default= False)
    
    hora_salida = models.TimeField(blank=True, null=True)
    horas_trabajadas = models.IntegerField("Horas Trabajadas",default=0)
    
    class Meta:
        ordering = ['fecha']
        get_latest_by = 'fecha'
        verbose_name = 'Marcada Reloj'
        verbose_name_plural = 'Marcadas Reloj'
    
    
    def __str__(self):
        return f"{self.empleado} - {self.fecha}"
    
    def get_full_name(self):
        return f"{self.empleado} - {self.fecha}"