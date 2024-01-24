from django.urls import path
from apps.personal_debt.views import credit_detail, credit
from apps.personal_debt.views.pdf import generar_pdf_prestamo
app_name = "personal_debt"
urlpatterns = []

urlpatterns += [
    path('Credit/list',
         credit.CreditListView.as_view(),
         name="credit_list"),
    path('Credit/create',
         credit.CreditCreateView.as_view(),
         name="credit_create"),
    path('Credit/update/<int:pk>',
         credit.CreditUpdateView.as_view(),
         name="credit_update"),
    path('Credit/delete/<int:pk>',
         credit.CreditDeleteView.as_view(),
         name="credit_delete"),
    path('Credit/detail', credit.CreditDetailView.as_view(),
         name="credit_detail"),

    path('CreditDetail/list',
         credit_detail.CreditsDetailListView.as_view(),
         name="creditDetail_list"),
    path('CreditDetail/create',
         credit_detail.CreditsDetailCreateView.as_view(),
         name="creditDetail_create"),
    path('CreditDetail/update/<int:pk>',
         credit_detail.CreditsDetailUpdateView.as_view(),
         name="creditDetail_update"),
    path('CreditDetail/delete/<int:pk>',
         credit_detail.CreditsDetailDeleteView.as_view(),
         name="creditDetail_delete"),

    path('prestamos/generar_pdf/<int:credit_id>', generar_pdf_prestamo,
         name='generar_pdf_prestamo'),
]
