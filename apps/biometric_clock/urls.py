from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from apps.biometric_clock.views import QR,jornada,marcada_reloj

app_name = "biometric_clock"

# urls de las vistas de organizacion 
urlpatterns = [
    path('scanner_qr/', QR.ScannerQR.as_view(), name="scanner_QR"),
]
urlpatterns += [
    path('jornada/list',jornada.JornadaListView.as_view(),name="jornada_list" ),
    path('jornada/create',jornada.JornadaCreateView.as_view(),name="jornada_create" ),
    path('jornada/update/<int:pk>',jornada.JornadaUpdateView.as_view() ,name="jornada_update" ),
    path('jornada/delete/<int:pk>',jornada.JornadaDeleteView.as_view() ,name="jornada_delete" ),
]
urlpatterns += [
    path('marcada_reloj/list',marcada_reloj.MarcadaRelojListView.as_view(),name="marcada_reloj_list" ),
    path('marcada_reloj/create',marcada_reloj.Marcada_RelojCreateView.as_view(),name="marcada_reloj_create" ),
    path('marcada_reloj/update/<int:pk>',marcada_reloj.Marcada_RelojUpdateView.as_view() ,name="marcada_reloj_update" ),
    path('marcada_reloj/delete/<int:pk>',marcada_reloj.Marcada_RelojDeleteView.as_view() ,name="marcada_reloj_delete" ),
]