
from django.urls import path
from apps.payment_role.views import overtime, typepermission,workpermission
app_name = "payment_role"
urlpatterns = []
# urls de las vistas de organizacion 
urlpatterns += [
    path('overtime/list',overtime.OvertimeListView.as_view(),name="overtime_list" ),
    path('overtime/create',overtime.OvertimeCreateView.as_view(),name="overtime_create" ),
    path('overtime/update/<int:pk>',overtime.OvertimeUpdateView.as_view() ,name="overtime_update" ),
    path('overtime/detail',overtime.OvertimeDetailView.as_view() ,name="overtime_detail" ),
    path('overtime/delete/<int:pk>',overtime.OvertimeDeleteView.as_view() ,name="overtime_delete" ),
    path('overtime/data_employee',overtime.OvertimeValueHours.as_view() ,name="overtime_value_hours" ),
]
urlpatterns += [
    path('typePermission/list',typepermission.TypePermissionListView.as_view(),name="typePermission_list" ),
    path('typePermission/create',typepermission.TypePermissionCreateView.as_view(),name="typePermission_create" ),
    path('typePermission/update/<int:pk>',typepermission.TypePermissionUpdateView.as_view() ,name="typePermission_update" ),
    path('typePermission/delete/<int:pk>',typepermission.TypePermissionDeleteView.as_view() ,name="typePermission_delete" ),
]
urlpatterns += [
    path('workpermission/list',workpermission.WorkpermissionListView.as_view(),name="workpermission_list" ),
    path('workpermission/create',workpermission.WorkpermissionCreateView.as_view(),name="workpermission_create" ),
    path('workpermission/update/<int:pk>',workpermission.WorkpermissionUpdateView.as_view() ,name="workpermission_update" ),
    path('workpermission/delete/<int:pk>',workpermission.WorkpermissionDeleteView.as_view() ,name="workpermission_delete" ),
]