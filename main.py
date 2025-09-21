# Notas (TODO): Convencion de nombre especialista/empleado en funciones relacionadas con estos.

# Lista que contendra todos los servicios que declaremos para el sistema.
servicios = []

#Servicios predefinidos para que no inicie el programa vacio.
servicio1 = [{'Nombre':'x', 'Duracion':10, 'Costo': 2000}, {'Empleados':[]}]
servicio2 = [{'Nombre':'y', 'Duracion':30, 'Costo': 15000}, {'Empleados':[]}]

# Los servicios se anaden como copias a la lista para evitar errores con la memoria del programa
# Por ejemplo, si anado dos veces servicio1 y modifico informacion de este se modificara en las dos copias que anadi, usar .copy() evita esto.
servicios.append(servicio1.copy())
servicios.append(servicio2.copy())
print(servicios)

def crear_servicio():
    nombre = input("Ingrese el nombre del servicio: ")
    duracion = int(input("Ingrese la duracion del servicio: "))
    costo = int(input("Ingrese el costo del servicio: "))
    servicio = [{'Nombre': nombre, 'Duracion': duracion, 'Costo': costo}, {'Empleados':[]}]
    servicios.append(servicio.copy()) #Usamos append con un servicio.copy para que usar un memory address diferente y poder hacer modificaciones a gusto sin que se este cambiando siempre el mismo servicio.

def modificar_servicio():
    print("Lista de servicios disponibles: \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i][0]['Nombre']}")
    x = int(input("Seleccione el servicio que desea modificar: "))
    x = x - 1 # El X ingresado se hace con la convencion de 1 hasta len(servicios), pero asi no funciona la lista, esto lo soluciona.
    variable = input("Que variable desea modificar? (Nombre, Duracion o Costo): ")
    if(variable.lower() == "nombre"):
        nuevo_nombre = input("Ingrese el nuevo nombre del servicio: ")
        servicios[x][0]['Nombre'] = nuevo_nombre
    if(variable.lower() == "duracion"):
        nueva_duracion = input("Ingrese la nueva duracion del servicio: ")
        servicios[x][0]['Duracion'] = nueva_duracion
    if(variable.lower() == "costo"):
        nuevo_costo = input("Ingrese el nuevo costo del servicio: ")
        servicios[x][0]['Costo'] = nuevo_costo
    else:
        print("La variable que usted quiere modificar no existe, por favor intente de nuevo.")

def eliminar_servicio():
    print("Lista de servicios disponibles: \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i][0]['Nombre']}")
    x = int(input("Seleccione el servicio que desea eliminar: "))
    x = x-1 #convencion.
    if(x < 0 or x > len(servicios)):
        print("El servicio que usted desea eliminar no existe, por favor intentelo de nuevo.")
    else:
        servicios.pop(x)

def informacion_servicio():
    print("De que servicio desea adquirir informacion?: \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i][0]['Nombre']}")
    x = int(input("Elija un servicio: "))
    # Nuevamente por convencion
    x = x-1
    if(x < 0 or x > len(servicios)):
        print("El servicio que usted eligio no existe, intentelo de nuevo.\n")
    else:
        print(f"\nNombre: {servicios[x][0]['Nombre']}")
        print(f"Duracion: {servicios[x][0]['Duracion']}")
        print(f"Costo: {servicios[x][0]['Costo']}")
        print(f"Cantidad de empleados: {len(servicios[x][1]['Empleados'])}")
        if(len(servicios[x][1]['Empleados']) == 0):
            print("No existen empleados.\n")
        else:
            print("A continuacion se mostraran los empleados del servicio: ")
            for i in range(0, len(servicios[x][1]['Empleados'])):
                # El +1 que se usa en la primera linea se usa para usar una convencion de rango 1 hasta la cantidad de elementos, saltando el 0 (Fines esteticos).
                print(f"\nEmpleado {i+1}: ")
                print(f"Nombres: {servicios[x][1]['Empleados'][i]['Nombre']}")
                print(f"Apellidos: {servicios[x][1]['Empleados'][i]['Apellidos']}")
                print(f"Cedula: {servicios[x][1]['Empleados'][i]['Cedula']}")
                print(f"Celular: {servicios[x][1]['Empleados'][i]['Cel']}")
                print(f"Email: {servicios[x][1]['Empleados'][i]['Email']}")
                print(f"Horario: {servicios[x][1]['Empleados'][i]['Horario']}\n")

def ingresar_especialista():
    print("A que servicio desea anadir un especialista?: \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i][0]['Nombre']}")
    x = int(input("Elija el servicio: "))
    x = x - 1
    if(x<0 or x>len(servicios)):
        print("El servicio que ha elegido no existe, intentelo de nuevo.\n")
    else:
        print("\nIngrese los datos del empleado: ")
        nombre = input("Nombres: ")
        apellidos = input("Apellidos: ")
        cedula = int(input("Cedula: "))
        cel = int(input("Celular: "))
        email = input("Email: ")
        horario = input("Horario (Ingreselo como inicio(am/pm)-final(am/pm)): ")

        empleado = {
            'Nombre': nombre,
            'Apellidos': apellidos,
            'Cedula': cedula,
            'Cel': cel,
            'Email': email,
            'Horario': horario,
            }

        servicios[x][1]['Empleados'].append(empleado.copy())
        print(f"\nEl empleado/especialista {empleado['Nombre']} ha sido agregado con exito.\n")

def modificar_especialista():
    print("A que servicio pertenece el especialista?: \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i][0]['Nombre']}")
    x = int(input("Elija el servicio: "))
    x = x - 1 # Convencion.
    if(x < 0 or x> len(servicios)):
        print("El servicio seleccionado no existe, intentelo nuevamente.\n")

    print("Lista de empleados: \n")
    for i in range(0, len(servicios[x][1]['Empleados'])):
        print(f"[{i+1}] {servicios[x][1]['Empleados'][i]['Nombre']} {servicios[x][1]['Empleados'][i]['Apellidos']}")
    y = int(input("Seleccione el especialista al cual desea modificarle informacion: "))
    y = y-1 # Convencion.
    if(y<0 or y>len(servicios[x][1]['Empleados'])):
        print("El empleado que usted selecciono no existe, intentelo de nuevo.\n")

    tipo_modificacion = input("Desea modificar toda su informacion o solo un dato en especifico? (completa/especifica): ")
    if(tipo_modificacion.lower() == "completa"):
        servicios[x][1]['Empleados'][y]['Cedula'] = int(input("Nuevo No. cedula: "))
        servicios[x][1]['Empleados'][y]['Cel'] = int(input("Nuevo No. Cel: "))
        servicios[x][1]['Empleados'][y]['Email'] = input("Nuevo Email: ")
        servicios[x][1]['Empleados'][y]['Horario'] = input("Nuevo Horario (Ingreselo como inicio(am/pm)-final(am/pm)): ")
        print(f"La informacion de {servicios[x][1]['Empleados'][y]['Nombre']} ha sido modificada con exito.\n")
    elif(tipo_modificacion.lower() == "especifica"):
        variable = input("Que variable desea modificar? (cedula, celular, email u horario): ")
        if(variable.lower() == "cedula"):
            servicios[x][1]['Empleados'][y]['Cedula'] = int(input("Nuevo No. cedula: "))
            print(f"La Cedula de {servicios[x][1]['Empleados'][y]['Nombre']} ha sido modificada con exito.\n")
        if(variable.lower() == "celular"):
            servicios[x][1]['Empleados'][y]['Cel'] = int(input("Nuevo No. cel: "))
            print(f"El celular de {servicios[x][1]['Empleados'][y]['Nombre']} ha sido modificado con exito.\n")
        if(variable.lower() == "email"):
            servicios[x][1]['Empleados'][y]['Email'] = input("Nuevo Email: ")
            print(f"El Email de {servicios[x][1]['Empleados'][y]['Nombre']} ha sido modificado con exito.\n")
        if(variable.lower() == "horario"):
            servicios[x][1]['Empleados'][y]['Horario'] = input("Nuevo Horario (Ingreselo como inicio(am/pm)-final(am/pm)): ")
            print(f"El horario de {servicios[x][1]['Empleados'][y]['Nombre']} ha sido modificado con exito.\n")


def eliminar_especialista():
    print("A que servicio pertenece el especialista que desea eliminar?: \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i][0]['Nombre']}")
    x = int(input("Elija el servicio: "))
    x = x - 1 #Convencion.
    if(x<0 or x > len(servicios)):
        print("El servicio que usted selecciono no existe, intentelo de nuevo.\n")
    
    else:
        print("\nQue empleado del servicio desea eliminar?: ")
        for i in range(0, len(servicios[x][1]['Empleados'])):
            print(f"[{i+1}] {servicios[x][1]['Empleados'][i]['Nombre']} {servicios[x][1]['Empleados'][i]['Apellidos']}")
        y = int(input("Elija un empleado: "))
        y = y-1 # Convencion.
        if(y < 0 or y > len(servicios[x][1]['Empleados'])):
            print("El empleado que usted seleccion no existe, intentelo de nuevo.\n")
        else:
            servicios[x][1]['Empleados'].pop(y)
            print("Empleado ha sido eliminado con exito.\n")


# Eje Dict Empleado: (Cada empleado va dentro de la lista de empleados del servicio que presta)
#Nuevamente aclaro que esta porcion de codigo existe unicamente para no iniciar el programa vacio, si elimamos estas lineas no rompera nada, solo se usa con fines practicos.
empleado1 = {
        'Nombre': 'pepito',
        'Apellidos': 'Hernandez',
        'Cedula': '10000000',
        'Cel':'3004929192',
        'Email':'pepito@hotmail.com',
        'Horario': '9am-5pm',
        'Reservas': [{'Cliente': 'x', 'Fecha': 'Martes', 'Hora': 20}] # Solo se aceptan reservas dentro del horario, si la lista esta vacia se puede borrar servicio/empleado.
        }


servicio1[1]['Empleados'].append(empleado1.copy()) #Notese nuevamente el uso de .copy()
servicio1[1]['Empleados'].append(empleado1.copy())
servicio1[1]['Empleados'][1]['Nombre'] = "Juanito"


#Usuario por default, nuevamente no tiene mayor fin mas que dar practicidad a la hora de testear.
usuario = {
        'Nombre': 'Juan',
        'Reservas': [{'Nombre Empleado': empleado1['Nombre'], 'Fecha': 'Jueves', 'Hora': 10}]
        }


# Funcion imcompleta, no se debe de usar.
def anadir_reserva():
    for i in range(0, len(servicios)):
        print(f"[{i}] {servicios[i][0]['Nombre']}\n")

    servicio = int(input("Que servicio desea: "))
    for i in range(0, len(servicios[servicio][1]['Empleados'])):
        print(f"[{i}] Empleado: {servicios[servicio][1]['Empleados'][i]}")
    empleado = (int(input("Seleccione el empleado que desea: ")))
    fecha = input("En que fecha lo desea: ")
    hora = input("En que hora lo desea: ")
    reserva_empleado = {'Cliente': usuario['Nombre'], 'Fecha':fecha, 'Hora':hora}
    servicios[servicio][1]['Empleados'][empleado]['Reservas'].append(reserva_empleado.copy())
    reserva_cliente = {'Empleado': servicios[servicio][1]['Empleados'][empleado]['Nombre'], 'Fecha':fecha, 'Hora':hora}
    usuario['Reservas'].append(reserva_cliente.copy())

    print(servicio1[1]['Empleados'][empleado]['Reservas'])
 
  
def mostrar_menu():
    while True:

        print("\n--- SISTEMA DE GESTIÓN DE SERVICIOS ---")
        print("1. Ingresar reserva")
        print("2. Editar reserva")
        print("3. Cancelar reserva")
        print("4. Consultar reservas")
        print("5. Ingresar especialista/trabajador")
        print("6. Editar especialista/trabajador")
        print("7. Borrar especialista/trabajador")
        print("8. Ingresar servicio")
        print("9. Editar servicio")
        print("10. Borrar servicio")
        print("11. Informacion de un servicio.")
        print("0. Salir")
    
        opcion = int(input("Seleccione una opción: "))
        if opcion == 1:
            print()
        elif opcion == 2:
            print()
        elif opcion == 3:
            print()
        elif opcion == 4:
            print()
        elif opcion == 5:
            ingresar_especialista()
        elif opcion == 6:
            modificar_especialista()
        elif opcion == 7:
            eliminar_especialista()
        elif opcion == 8:
            crear_servicio()
        elif opcion == 9:
            modificar_servicio()
        elif opcion == 10:
            eliminar_servicio()
        elif opcion == 11:
            informacion_servicio()
        elif opcion == 0:
            print("Finalizando el programa.\n")
            break
        else:
            print("Opción inválida. Intente de nuevo.\n")

# Ejecutar el menú
mostrar_menu()
