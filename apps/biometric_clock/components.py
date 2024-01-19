#Función que comprueba la veracidad de los datos y desempaqueta cada uno de ellos
def clean_employee_data(data):
    data = (data.replace('{', "")).replace('}', "")
    content = data.split(",")
    if len(content) == 4:
    
        first_name = ((content[0].split(":"))[1].replace("'", "")).strip()

        last_name = ((content[1].split(":"))[1].replace("'", "")).strip()

        dni = ((content[2].split(":"))[1].replace("'", "")).strip()

        email = ((content[3].split(":"))[1].replace("'", "")).strip()
        
        condition = True

        return first_name, last_name, dni, email, condition
    
    return "None", "None", "None", "None", False

#Función que permite facilitar la busqueda del empleado, proporcionado una vez los datos del QR
def employee_query(name, last_n, id , mail):
    from apps.personal_file.models import Employee
    try:
        employee = Employee.objects.get(
            firts_name= name,
            last_name= last_n,
            dni = id,
            email= mail
        )
        
        return employee
        
    except Employee.DoesNotExist as e:
        print('El empleado no existe: {}'.format(e))
        return None
    except Employee.MultipleObjectsReturned as e:
        print('Se encontraron varios empleados con los mismos datos: {}'.format(e))
        return None

#Función completa que permite la marcada del reloj de los distintos empleados del sistema      
def clock_confirmation(employee):
    from apps.biometric_clock.models import MarcadaReloj, Jornada
    from datetime import datetime, timedelta
    
    #Actualizar la marcada
    try:

        date_str = datetime.now().strftime("%Y-%m-%d")
        date_datetime = datetime.strptime(date_str, "%Y-%m-%d")
        date = date_datetime.date()
        
        time_str = datetime.now().strftime("%H:%M")
        time = datetime.strptime(time_str, "%H:%M").time()
        
        journey = Jornada.objects.get(
            descripcion = employee.jornada.descripcion
        )
        
        journey_start_hour = journey.hora_entrada
        journey_luch_start_hour = journey.hora_entrada_lunch
        journey_luch_end_hour = journey.hora_salida_lunch
        journey_end_hour = journey.hora_salida
        
        
        clock, created = MarcadaReloj.objects.get_or_create(
            empleado = employee,
            jornada = employee.jornada ,
            fecha = date
        )
        
        print("Empleado: {}\nJornada: {}\nFecha: {}\nHora de entrada: {}\nAtraso en entrada: {}\nHora de entrada al almuerzo: {}\nHora de salida del almuerzo: {}\nAtraso en almuerzo: {}\nHora de salida: {}\nHoras trabajadas: {}".format(
        clock.empleado,
        clock.jornada,
        clock.fecha,
        clock.hora_entrada if clock.hora_entrada else "Ninguna",
        "Atrasado "if clock.atraso_entrada else "A tiempo",
        clock.hora_entrada_lunch if clock.hora_entrada_lunch else "Ninguna",
        clock.hora_salida_lunch if clock.hora_salida_lunch else "Ninguna",
        "Atrasado" if clock.atraso_lunch else "A tiempo",
        clock.hora_salida if clock.hora_salida else "Ninguna",
        clock.horas_trabajadas
    ))
                
        employee_start_hour = clock.hora_entrada
        employee_lunch_start_hour = clock.hora_entrada_lunch
        employee_lunch_end_hour = clock.hora_salida_lunch
        employee_end_hour = clock.hora_salida
        

        #Se crea la marcada de reloj y se actualiza los primeros campos de la entrada inicial
        if created:
            try:
                clock.hora_entrada = time
                clock.atraso_entrada = time > journey_start_hour
                
                if clock.atraso_entrada:
                    clock.save()
                    print("Marcada creada; hora de entrada actualizada con exito")
                    return "Hora de entrada marcada con éxito para: {}; estás atrasado!".format(clock.empleado)
                
                else:
                    
                    clock.save()
                    print("Marcada creada; hora de entrada actualizada con exito")
                    return "Hora de entrada marcada con éxito para: {}; has llegado puntual!".format(clock.empleado)
                
                
            except Exception as e:
                print("#1 Error: {}".format(e))
                return "Ocurrio un error inesperado, contactar con el administrador del sistema: {}".format(e)
                
        #Marcar la hora de entrada del lunch
        if employee_start_hour and employee_lunch_start_hour is None and employee_lunch_end_hour is None and employee_end_hour is None:
            try:
                clock.hora_entrada_lunch = time
                clock.save()
                print("Hora de entrada de lunch actualizada con exito")
                return "Hora de entrada de lunch marcada con éxito para: {}".format(clock.empleado)
            
            except Exception as e:
                print("#2 Error: {}".format(e))
                return "Ocurrio un error inesperado, contactar con el administrador del sistema: {}".format(e)
                
        #Marcar la hora de salida del lunch
        if employee_start_hour and employee_lunch_start_hour and employee_lunch_end_hour is None and employee_end_hour is None:
            try:
                clock.hora_salida_lunch = time
                clock.atraso_lunch = time > journey_luch_end_hour
                
                if clock.atraso_lunch:
                    clock.save()
                    print("Hora de salida de lunch actualizada con exito")
                    return "Hora de salida de lunch marcada con éxito para: {}; estás atrasado!".format(clock.empleado)
                
                else:
                    
                    clock.save()
                    print("Hora de salida de lunch actualizada con exito")
                    return "Hora de salida de lunch marcada con éxito para: {}; has llegado puntual!".format(clock.empleado)
                            
            except Exception as e:   
                print("#3 Error: {}".format(e))
                return "Ocurrio un error inesperado, contactar con el administrador del sistema: {}".format(e)
       
        #Marcar la hora de salida y calcular las horas trabajadas 
        if employee_start_hour and employee_lunch_start_hour and employee_lunch_end_hour and employee_end_hour is None:
            try:
                clock.hora_salida = time
                
                entry_datetime = datetime.combine(clock.fecha, clock.hora_entrada)
                exit_datetime = datetime.combine(clock.fecha, clock.hora_salida)

                work_duration = exit_datetime - entry_datetime
                
                clock.horas_trabajadas = round(work_duration.total_seconds() / 3600, 2)
                clock.save()
                print("Hora de salida actualizada con exito")
                return "Hora de salida marcada con éxito para: {}\nTotal de horas trabajadas hoy: {}\nNos vemos!".format(clock.empleado, clock.horas_trabajadas)
            
            except Exception as e:
                    print("#4 Error: {}".format(e))
                    return "Ocurrio un error inesperado, contactar con el administrador del sistema: {}".format(e)
                
        if employee_start_hour and employee_lunch_start_hour and employee_lunch_end_hour and employee_end_hour and clock.fecha == date:
            print("Ya marcó todas las asistencias y salidas")
            return "Usted ya ha marcado todas las asistencias y salidas de hoy!"
            
    # En caso de no existir y ocurrir más excepciones, crear la marcada mediante formulario
    except MarcadaReloj.DoesNotExist as e:
        print("No existe la marcada: {}".format(e))
        from apps.biometric_clock.forms.marcada_reloj import MarcadaRelojForm
        
        form_clock = MarcadaRelojForm()
        
        default_data = {
            'empleado': employee,
            'jornada': employee.jornada,
            'fecha': date,
            'hora_entrada': time,
            'atraso_entrada': time > journey_start_hour ,
            'horas_trabajadas': 0
            
        }

        form_clock = MarcadaRelojForm(data=default_data)

        if form_clock.is_valid():
            form_clock.save()
            print("El formulario fue creado con éxito")
            
            if default_data['atraso_entrada']:
               return "Hora de entrada marcada con éxito desde formulario para: {}; estás atrasado!".format(clock.empleado)
            
            else: 
                
                return "Hora de entrada marcada con éxito desde formulario para: {}; has llegado puntual!".format(clock.empleado)
        else:
            print("El formulario no es válido: no se ha creado la marcada de reloj.")
            return "Ha ocurrido un error al momento al crear la marcada del reloj mediante formulario para: {}".format(clock.empleado)
    
    #Manejar excepción en caso de que exista más de un empleado en el sistema (personal_file es quién debe manejar que se evite la redundancia de datos en la base de datos)
    except MarcadaReloj.MultipleObjectsReturned as e:
        print('Multiple employees: {}'.format(e))
        return "Error en el sistema; existen más de un usuario con los mismos datos (contactar con el administrador del sistema): {}".format(e)
    
    #Manejo de cualquier excepción inesperada
    except Exception as e:
        print("Ocurrio un error inesperado en el sistema, contactar con el administrador del sistema: {}".format(e))
        return "Ocurrio un error inesperado, contactar con el administrador del sistema: {}".format(e)
