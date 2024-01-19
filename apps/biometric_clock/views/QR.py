from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from apps.biometric_clock.components import clean_employee_data, employee_query, clock_confirmation
import json

class ScannerQR(View):
    template_name = 'scannerQR/ScannerQR.html'
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            qr_content = data.get('qr_content')
            
            first_name, last_name, dni, email, condition = clean_employee_data(qr_content)
            
            if condition:
                employee = employee_query(first_name, last_name, dni, email)
                
                if employee is not None:
                    
                    message = clock_confirmation(employee)
                    return JsonResponse({'success': True, 'message': message})
                
                else:
                    #En caso del que el empleado sea None (cambiar)
                    return JsonResponse({'success': False, 'message': 'El empleado no existe dentro de la base de datos, contacte a sistemas'})
            else:
                #En caso de que los datos no sean los correctos
                return JsonResponse({'success': False, 'message': 'Los datos proporcionados en el QR no son correctos!'})
           
            
        except Exception as e:
            print('Error: {}'.format(e))
            return JsonResponse({'success': False, 'message': str(e)})
           
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context = {})