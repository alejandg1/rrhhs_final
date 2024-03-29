from django.urls import path
from apps.personal_file.views import employee
from django.conf.urls.static import static
from django.conf import settings
app_name = "personal_file"
urlpatterns = []
# urls de las vistas de organizacion 
urlpatterns += [
    path('employee/list',employee.EmployeeListView.as_view(),name="employee_list" ),
    path('employee/create',employee.EmployeeCreateView.as_view(),name="employee_create" ),
    path('employee/update/<int:pk>',employee.EmployeeUpdateView.as_view() ,name="employee_update" ),
    path('employee/delete/<int:pk>',employee.EmployeeDeleteView.as_view() ,name="employee_delete" ),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)