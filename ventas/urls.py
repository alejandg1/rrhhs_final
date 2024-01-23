from django.urls import path
from ventas.views import ventas as cabecera
from ventas.views.pdf import generar_pdf

app_name = "ventas"
urlpatterns = []

urlpatterns += [
    path('factura/list',
         cabecera.CabeceraListView.as_view(),
         name="cabecera_list"),
    path('factura/create',
         cabecera.CabeceraCreateView.as_view(),
         name="cabecera_create"),
    path('factura/update/<int:pk>',
         cabecera.CabeceraUpdateView.as_view(),
         name="cabecera_update"),
    path('factura/delete/<int:pk>',
         cabecera.CabeceraDeleteView.as_view(),
         name="cabecera_delete"),
    path('factura/detail', cabecera.CabeceraDetailView.as_view(),
         name="cabecera_detail"),
    path('factura/generar_pdf/', generar_pdf, name="generar_pdf"),
]
