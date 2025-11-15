import copy

# Todas las variables dentro de clase a las que se le declara un tipo list deben de tener = [], de otro modo si las revisamos y aun no se declaran dan un AttributeError
# Notese que esto sucede con cualquier variable que aun no este declarada, es simplemente que en el programa recurrimos mas a revisar listas que pueden estar vacias, por eso unicamente les asignamos un valor a la lista.
class Reserva:
    def __init__(self, nombre_empleado):
        self.nombre_empleado = nombre_empleado
    nombre_cliente: str
    fecha: str
    hora: list = []

class Empleado:
    nombre: str
    apellido: str
    email: str
    cedula: int
    cel: int
    disponibilidad: list = []
    horario: str
    reservas: list[Reserva] = []

class Servicio:
    nombre: str
    Iduracion: int
    Sduracion: str
    costo: int
    empleados: list[Empleado] = []

# Lista que contendra todos los servicios que declaremos para el sistema.
servicios = []

#Usuario por default, nuevamente no tiene mayor fin mas que dar practicidad a la hora de testear.
usuarios = []

#convierte string en formato "10:00-12:20" en una lista de la forma [10.00, 12.20]
def horario_empleado(x):
    x = x.split('-') # Separa el 10:00 del 12:20 en un alista
    inicio = x[0] # 10:00
    final = x[1] # 12:20
    inicio = inicio.replace(':', '.') # Luego cambia el 10:00 a 10.0 para operar con posteriormente
    final = final.replace(':', '.')
    inicio = float(inicio)
    final = float(final)
    return [inicio, final] # Retorna finalmente [10.0, 12.2]

#NumeroString_split
def ns_split(x):
    sduracion = "" #Placeholder para agregar la parte que es solo texto
    for i in x:
        if(i.isdigit() == False):
            sduracion += i # Si i es texto entonces agregar ese caracter al placeholder
            x = x.replace(i, "") #Elimina el caracter no entero de la variable, nos dejaria solamente el numero
    return [int(x), sduracion] # Retona [tiempo, formato], eje: [30, 'min']

def creacion_citas(info_servicio, horario):
    duracion = 0 #Placeholder, lo uso por comodidad pues esto luego almacenara la duracion en un formato estandar (minutos)
    ultima_jornada = horario[0] * 60 # Placeholder nuevamente, si el horario es [20, 40] esto seria = 40, lo que permite seguir con [40, 60] de manera mas facil
    lista_horas = []
    if(info_servicio['SDuracion'] == "hr"): duracion = info_servicio['IDuracion'] * 60
    elif(info_servicio['SDuracion'] == "min"): duracion = info_servicio['IDuracion']
    tiempo_jornada = (horario[1]*60) - (horario[0]*60) # Si se trabaja de 7am a 1pm esto seria 360, que son 6hr por eje
    for i in range(0, int(tiempo_jornada / duracion)):
        x = [ultima_jornada, ultima_jornada+duracion]
        ultima_jornada = x[1]
        x[0] /= 60 #Paso de minutos a horas
        x[1] /= 60
        x1_minutos = (x[0] - int(x[0])) * 60 #los minutos son simplemente la parte decimal que queda como residuo de la conversion a horas, por eso tomo la parte decimal y la multiplico por 60 (Si son 0.25 es 1/4 de hora, o sea, 15min)
        x2_minutos = (x[1] - int(x[1])) * 60
        if(int(x1_minutos)== 0): x1_minutos = "00" #Esto es para el formato, si la division da exacta no hay parte decimal, por lo que agrego manualmente los 00 al final
        else: x1_minutos = str(int(round(x1_minutos))) #Redondeo porque la precision decimal de python se vuelve loca a veces
        if(int(x2_minutos)== 0): x2_minutos = "00"
        else: x2_minutos = str(int(round(x2_minutos)))
        
        x[0] = str(int(x[0])) + ":" + x1_minutos
        x[1] = str(int(x[1])) + ":" + x2_minutos
        lista_horas.append(x.copy()) #Olvide agregar esto en el anterior commit, dejarlo en la entrega final, de otra manera no funcionaria completamente bien.
    return lista_horas

def crear_servicio():
    s1 = Servicio()
    s1.nombre = input("Ingrese el nombre del servicio: ")
    duracion = input("Ingrese la duracion del servicio (formato: numero-(hr/min/s), eje: 30min, 1hr, 20s): ")
    duracion = ns_split(duracion)
    s1.Iduracion = duracion[0]
    s1.Sduracion = duracion[1]
    s1.costo = int(input("Ingrese el costo del servicio: "))
    servicios.append(copy.copy(s1)) # Lo mismo que con las listas. Las clases son objetos mutables, por lo tanto si no usas .copy se pasan por referencia y eso no nos conviene.
    print(servicios)

def modificar_servicio():
    if(len(servicios) == 0):
        print("No existe ningun servicio para modificar.")
        return

    print("Lista de servicios disponibles: \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i].nombre}")
    x = int(input("Seleccione el servicio que desea modificar: ")) - 1 # El X ingresado se hace con la convencion de 1 hasta len(servicios), pero asi no funciona la lista, esto lo soluciona.
    if x < 0 or x > len(servicios):
        print("El servicio que usted desea modificar no existe, por favor intentelo de nuevo.\n")
        return

    variable = input("Que variable desea modificar? (Nombre, Duracion o Costo): ")
    # Aca uso lower porque al recibir input string es mas facil verificarlo de esta manera
    if(variable.lower() == "nombre"):
        servicios[x].nombre = input("Ingrese el nuevo nombre del servicio: ")
    elif(variable.lower() == "duracion"):
        existe_reserva = False
        # Solo se puede modificar la duracion del servicio si no hay reservas disponibles
        for i in range(0, len(servicios[x].empleados)):
            if(len(servicios[x].empleados[i].reservas) != 0):
                existe_reserva = True
        
        if(existe_reserva):
            print(f"La duracion del servicio {servicios[x].nombre} no se puede modificar puesto que aun hay reservas activas, estas deben completarse o eliminarse primero.\n")

        else:
            nueva_duracion = input("Ingrese la nueva duracion del servicio (formato: numero-(hr/min/s), eje: 30min, 1hr, 20s): ")
            nueva_duracion = ns_split(nueva_duracion)
            servicios[x].Iduracion = nueva_duracion[0]
            servicios[x].Sduracion = nueva_duracion[1]

    elif(variable.lower() == "costo"):
        servicios[x].costo = int(input("Ingrese el nuevo costo del servicio: "))
    else:
        print("La variable que usted quiere modificar no existe, por favor intente de nuevo.")

def eliminar_servicio():
    if(len(servicios) == 0):
        print("No existe ningun servicio para eliminar.")
        return

    print("Lista de servicios disponibles: \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i].nombre}")

    x = int(input("Seleccione el servicio que desea eliminar: ")) - 1 #convencion.
    if(x < 0 or x > len(servicios)):
        print("El servicio que usted desea eliminar no existe, por favor intentelo de nuevo.\n")
        return

    existe_reserva = False
    for i in range(0, len(servicios[x].empleados)):
        if(len(servicios[x].empleados[i].reservas) != 0):
            existe_reserva = True
    
    if(existe_reserva):
        print(f"El servicio {servicios[x].nombre} no se puede eliminar puesto que aun hay reservas activas, estas deben completarse o eliminarse primero.\n")
    elif(len(servicios[x].empleados) != 0):
        print(f"El servicio {servicios[x].nombre} no se puede eliminar puesto que aun hay empleados activos, estos deben ser eliminados primero.")
    else:
        servicios.pop(x)
        print("El servicio ha sido eliminado con exito.\n")

def informacion_servicio():
    if(len(servicios) == 0):
        print("No existe ningun servicio del cual adquirir informacion.")
        return

    print("De que servicio desea adquirir informacion?: \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i].nombre}")
    x = int(input("Elija un servicio: ")) - 1
    if(x < 0 or x > len(servicios)):
        print("El servicio que usted eligio no existe, intentelo de nuevo.\n")
    else:
        print(f"\nNombre: {servicios[x].nombre}")
        print(f"Duracion: {servicios[x].Iduracion}{servicios[x].Sduracion}")
        print(f"Costo: {servicios[x].costo}")
        if(len(servicios[x].empleados) == 0):
            print("No existen empleados.\n")
        else:
            print(f"Cantidad de empleados: {len(servicios[x].empleados)}")
            print("A continuacion se mostraran los empleados del servicio: ")
            for i in range(0, len(servicios[x].empleados)):
                # El +1 que se usa en la primera linea se usa para usar una convencion de rango 1 hasta la cantidad de elementos, saltando el 0 (Fines esteticos).
                print(f"\nEmpleado {i+1}: ")
                print(f"Nombres: {servicios[x].empleado[i].nombre}")
                print(f"Apellidos: {servicios[x].empleado[i].apellido}")
                print(f"Cedula: {servicios[x].empleado[i].cedula}")
                print(f"Celular: {servicios[x].empleado[i].cel}")
                print(f"Email: {servicios[x].empleado[i].email}")
                print(f"Horario: {servicios[x].empleado[i].horario}")
                print(f"Disponibilidad (Horas en las que admite cita.): ")
                for a in range(0, len(servicios[x][1]['Empleados'][i]['Disponibilidad'])):
                    print(f"[{a+1}] {servicios[x].empleados[i].disponibilidad[a]}")

def ingresar_especialista():
    print("A que servicio desea anadir un especialista?: \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i][0]['Nombre']}")
    x = int(input("Elija el servicio: ")) - 1
    if(x<0 or x>len(servicios)):
        print("El servicio que ha elegido no existe, intentelo de nuevo.\n")
    else:
        print("\nIngrese los datos del empleado: ")
        nombre = input("Nombres: ")
        apellidos = input("Apellidos: ")
        cedula = int(input("Cedula: "))
        cel = int(input("Celular: "))
        email = input("Email: ")
        horario = input("Horario (Se usa formato 24hr y separacion por '-', eje: 8:00-15:20): ")
        reservas = []
        horas = horario_empleado(horario)
        lista_horas = creacion_citas(servicios[x][0], horas)

        empleado = {
            'Nombre': nombre,
            'Apellidos': apellidos,
            'Cedula': cedula,
            'Cel': cel,
            'Email': email,
            'Disponibilidad': lista_horas,
            'Horario': horario,
            'Reservas': reservas
            }

        servicios[x][1]['Empleados'].append(empleado.copy())
        print(f"\nEl empleado/especialista {empleado['Nombre']} ha sido agregado con exito.\n")

def modificar_especialista():
    print("A que servicio pertenece el especialista?: \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i][0]['Nombre']}")
    x = int(input("Elija el servicio: ")) - 1
    if(x < 0 or x> len(servicios)):
        print("El servicio seleccionado no existe, intentelo nuevamente.\n")
        return

    print("Lista de empleados: \n")
    for i in range(0, len(servicios[x][1]['Empleados'])):
        print(f"[{i+1}] {servicios[x][1]['Empleados'][i]['Nombre']} {servicios[x][1]['Empleados'][i]['Apellidos']}")
    y = int(input("Seleccione el especialista al cual desea modificarle informacion: ")) - 1
    if(y<0 or y>len(servicios[x][1]['Empleados'])):
        print("El empleado que usted selecciono no existe, intentelo de nuevo.\n")
        return


    # Para facilidad no se puede modificar informacion de un especialista si este tiene reservas activas
    if(len(servicios[x][1]['Empleados'][y]['Reservas']) != 0):
        print(f"\nEl empleado {servicios[x][1]['Empleados'][y]['Nombre']} tiene reservas activas en este momento por lo que no es posible modificar su informacion en el sistema, las reservas deben completarse o eliminarse primero.\n")
        return

    tipo_modificacion = input("Desea modificar toda su informacion o solo un dato en especifico? (completa/especifica): ")
    # Aqui uso nuevamente el lower para facil verificacion
    if(tipo_modificacion.lower() == "completa"):
        servicios[x][1]['Empleados'][y]['Cedula'] = int(input("Nuevo No. cedula: "))
        servicios[x][1]['Empleados'][y]['Cel'] = int(input("Nuevo No. Cel: "))
        servicios[x][1]['Empleados'][y]['Email'] = input("Nuevo Email: ")
        servicios[x][1]['Empleados'][y]['Horario'] = input("Nuevo Horario (Se usa formato 24hr y separacion por '-', eje: 8:00-15:20): ")
        horas = horario_empleado(servicios[x][1]['Empleados'][y]['Horario'])
        lista_horas = creacion_citas(servicios[x][0], horas)
        servicios[x][1]['Empleados'][y]['Disponibilidad'] = lista_horas

        print(f"La informacion de {servicios[x][1]['Empleados'][y]['Nombre']} ha sido modificada con exito.\n")
    elif(tipo_modificacion.lower() == "especifica"):
        variable = input("Que variable desea modificar? (cedula, celular, email u horario): ")
        if(variable.lower() == "cedula"):
            servicios[x][1]['Empleados'][y]['Cedula'] = int(input("Nuevo No. cedula: "))
            print(f"La Cedula de {servicios[x][1]['Empleados'][y]['Nombre']} ha sido modificada con exito.\n")
        elif(variable.lower() == "celular"):
            servicios[x][1]['Empleados'][y]['Cel'] = int(input("Nuevo No. cel: "))
            print(f"El celular de {servicios[x][1]['Empleados'][y]['Nombre']} ha sido modificado con exito.\n")
        elif(variable.lower() == "email"):
            servicios[x][1]['Empleados'][y]['Email'] = input("Nuevo Email: ")
            print(f"El Email de {servicios[x][1]['Empleados'][y]['Nombre']} ha sido modificado con exito.\n")
        elif(variable.lower() == "horario"):
            servicios[x][1]['Empleados'][y]['Horario'] = input("Nuevo Horario (Se usa formato 24hr y separacion por '-', eje: 8:00-15:20): ")
            horas = horario_empleado(servicios[x][1]['Empleados'][y]['Horario'])
            #Si el horario es modificado la lista horaria con disponibilidad tambien cambia
            lista_horas = creacion_citas(servicios[x][0], horas)
            servicios[x][1]['Empleados'][y]['Disponibilidad'] = lista_horas
            print(f"El horario de {servicios[x][1]['Empleados'][y]['Nombre']} ha sido modificado con exito.\n")


def eliminar_especialista():
    print("A que servicio pertenece el especialista que desea eliminar?: \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i][0]['Nombre']}")
    x = int(input("Elija el servicio: "))
    x = x - 1 #Convencion.
    if(x<0 or x > len(servicios)):
        print("El servicio que usted selecciono no existe, intentelo de nuevo.\n")
        return
    
    else:
        print("\nQue empleado del servicio desea eliminar?: ")
        for i in range(0, len(servicios[x][1]['Empleados'])):
            print(f"[{i+1}] {servicios[x][1]['Empleados'][i]['Nombre']} {servicios[x][1]['Empleados'][i]['Apellidos']}")
        y = int(input("Elija un empleado: "))
        y = y-1 # Convencion.
        if(y < 0 or y > len(servicios[x][1]['Empleados'])):
            print("El empleado que usted seleccion no existe, intentelo de nuevo.\n")
            return

        if(len(servicios[x][1]['Empleados'][y]['Reservas']) != 0):
            print(f"\nEl empleado {servicios[x][1]['Empleados'][y]['Nombre']} tiene reservas activas en este momento por lo que no es posible borrarlo del sistema, estas deben completarse o eliminarse primero.\n")
        else:
            servicios[x][1]['Empleados'].pop(y)
            print("Empleado ha sido eliminado con exito.\n")




def anadir_reserva(user_index):
    print("\nEn que servicio desea realizar su reserva?: ")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i][0]['Nombre']}\n")
    servicio = int(input("Que servicio desea: ")) - 1
    print("\nCon que empleado desea realizar su reserva?: ")
    for i in range(0, len(servicios[servicio][1]['Empleados'])):
        print(f"\nEmpleado {i+1}: ")
        print(f"Nombres: {servicios[servicio][1]['Empleados'][i]['Nombre']}")
        print(f"Apellidos: {servicios[servicio][1]['Empleados'][i]['Apellidos']}")
        print(f"Cedula: {servicios[servicio][1]['Empleados'][i]['Cedula']}")
        print(f"Celular: {servicios[servicio][1]['Empleados'][i]['Cel']}")
        print(f"Email: {servicios[servicio][1]['Empleados'][i]['Email']}")
    empleado = (int(input("Seleccione el empleado que desea: "))) - 1
    fecha = input("En que fecha lo desea? (se usa formato dd/mm/yy, eje: 09/03/14): ")
    for i in range(0, len(servicios[servicio][1]['Empleados'][i]['Disponibilidad'])):
        print(f"Horario {i+1}: {servicios[servicio][1]['Empleados'][empleado]['Disponibilidad'][i]}")
    hora = int(input("En que horario lo desea?: ")) - 1
    hora_seleccionada = servicios[servicio][1]['Empleados'][empleado]['Disponibilidad'][hora]
    ocupado = False
    for r in servicios[servicio][1]['Empleados'][empleado]['Reservas']:
        if r['Fecha'] == fecha and r['Hora'] == hora_seleccionada:
            ocupado = True
            break
    if ocupado:
        print(f"\n El horario {hora_seleccionada} en la fecha {fecha} NO está disponible con {servicios[servicio][1]['Empleados'][empleado]['Nombre']}, seleccione otra fecha, hora o empleado.")
        return
    reserva_empleado = {'Cliente': usuarios[user_index]['Nombre'], 
                        'Fecha':fecha, 'Hora':hora_seleccionada}
    servicios[servicio][1]['Empleados'][empleado]['Reservas'].append(reserva_empleado.copy())
    reserva_cliente = {'Empleado': servicios[servicio][1]['Empleados'][empleado]['Nombre'], 
                        'Fecha':fecha, 'Hora':hora_seleccionada}
    usuarios[user_index]['Reservas'].append(reserva_cliente.copy())


    print("RESERVA REALIZADA...\n")
    print(f"Nombres de Empleado: {usuarios[user_index]['Reservas'][-1]['Empleado']}")
    print(f"Fecha: {usuarios[user_index]['Reservas'][-1]['Fecha']}")
    print(f"Hora: {usuarios[user_index]['Reservas'][-1]['Hora']}")

#Editar reserva
def editar_reserva(user_index):
    if len(usuarios[user_index]['Reservas']) == 0:
        print("Usted no tiene reservas")
        return

    for i in range(len(usuarios[user_index]['Reservas'])):
        print(f"[{i+1}] {usuarios[user_index]['Reservas'][i]}")

    reserva_editar = int(input("\n¿Qué reserva desea editar?: ")) - 1
    if reserva_editar < 0 or reserva_editar >= len(usuarios[user_index]['Reservas']):
        print("Reserva inválida.")
        return

    reserva = usuarios[user_index]['Reservas'][reserva_editar]
    fecha_actual, hora_actual = reserva['Fecha'], reserva['Hora']
    nombre_empleado = reserva['Empleado']

    # localizar empleado
    for s in range(len(servicios)):
        for e in range(len(servicios[s][1]['Empleados'])):
            if servicios[s][1]['Empleados'][e]['Nombre'] == nombre_empleado:
                empleado = servicios[s][1]['Empleados'][e]

    print(f"\nReserva actual con {empleado['Nombre']} el {fecha_actual} a las {hora_actual}")
    opcion = input("¿Qué desea cambiar? (fecha/hora/ambas): ")

    nueva_fecha = input("Nueva fecha (dd/mm/yy): ") if opcion in ["fecha","ambas"] else fecha_actual
    if opcion in ["hora","ambas"]:
        for i in range(len(empleado['Disponibilidad'])):
            print(f"[{i+1}] {empleado['Disponibilidad'][i]}")
        hr = int(input("Seleccione nueva hora: ")) - 1
        if hr < 0 or hr >= len(empleado['Disponibilidad']):
            print("Hora inválida.")
            return
        nueva_hora = empleado['Disponibilidad'][hr]
    else:
        nueva_hora = hora_actual

    # verificar disponibilidad
    for r in empleado['Reservas']:
        if r['Fecha'] == nueva_fecha and r['Hora'] == nueva_hora:
            print("Ese horario ya está ocupado.")
            return

    # actualizar
    for r in empleado['Reservas']:
        if r['Cliente'] == usuarios[user_index]['Nombre'] and r['Fecha'] == fecha_actual and r['Hora'] == hora_actual:
            r['Fecha'], r['Hora'] = nueva_fecha, nueva_hora
    reserva['Fecha'], reserva['Hora'] = nueva_fecha, nueva_hora

    print(f"\nReserva modificada: {empleado['Nombre']} - {nueva_fecha} {nueva_hora}")

#Cancelar la reserva
def cancelar_reserva(user_index):
        print("Lista de usuarios con reservas: \n")
        if len(usuarios[user_index]['Reservas']) == 0:
            print("No tienes reservas para cancelar.\n")
            return
        
        for i in range(0, len(usuarios[user_index]['Reservas'])):
            print(f"[{i+1}] {usuarios[user_index]['Reservas'][i]}")
        
        reserva_cancelar = int(input("¿Qué reserva desea cancelar?: ")) - 1 #convencion
        if reserva_cancelar < 0 or reserva_cancelar >= len(usuarios[user_index]['Reservas']):
            print("La reserva que seleccionaste no existe.\n")
        else:
            reserva_eliminada = usuarios[user_index]['Reservas'].pop(reserva_cancelar)
            print(f"¡Tu reserva {reserva_eliminada} ha sido cancelada correctamente!\n")


def mostrar_reservas():   #Con esta funcion voy a mostrar las reservas de todos los servicios, me tocó aprender a usar 'enumerate'
    print("\n----->LISTA DE TODAS LAS RESERVAS<-----\n")
    for s, servicio in enumerate(servicios):  # Con esto recorremos todos los servicios
        print(f"Servicio {s+1}: {servicio[0]['Nombre']}")
        empleados = servicio[1]['Empleados']
        for e, empleado in enumerate(empleados):  # y esto para recorrer empleados de cada servicio
            if len(empleado['Reservas']) > 0:
                print(f"  Empleado {e+1}: {empleado['Nombre']} {empleado['Apellidos']}")
                for r, reserva in enumerate(empleado['Reservas']):
                    print(f"    Reserva {r+1}: Cliente: {reserva['Cliente']}, Fecha: {reserva['Fecha']}, Hora: {reserva['Hora']}")
            else:
                print(f"  Empleado {e+1}: {empleado['Nombre']} {empleado['Apellidos']} (Sin reservas)")
        print()  

def crear_usuario():
    print("\nCreando un nuevo usuario.")
    nombre = input("Ingrese su nombre completo: ")
    usuario = {
            'Nombre': nombre,
            'Reservas': []
            }
    usuarios.append(usuario.copy())
    print(f"Se ha creado al usuario {usuario['Nombre']} con exito.\n")

# Aqui le paso como argumento user_index de la funcion principal por practicidad, si la funcion falla necesita de este argumento para que no termine el programa y simplemente siga usando el mismo usuario que eligio hasta el momento
def cambiar_usuario(user_index):
    print("\nUsuarios disponibles: ")
    for i in range(0, len(usuarios)):
        print(f"[{i+1}] {usuarios[i]['Nombre']}")
    nuser = int(input("Que usuario desea usar?: ")) - 1
    if(nuser < 0 or nuser> len(usuarios)):
        print("El usuario que usted eligio no existe, por favor intentelo de nuevo.\n")
        return user_index #Fijate en que si falla retorna user_index, o sea, el usuario actual.
    else:
        print(f"Se ha cambiado al usuario {usuarios[nuser]['Nombre']} con exito.\n")
        return nuser
    return user_index # Este return es el default por si falla algo arriba (como inputs), se usa por seguridad.

def mostrar_menu():
    print("\n--- Bienvenido al sistema de gestion de servicios ---")
    crear_usuario()
    user_index = 0 # Defino user_index y su default, todas las funciones que requieren saber el usuario actual la necesitan como argumento

    while True:

        print("\n--- SISTEMA DE GESTIÓN DE SERVICIOS ---")
        print(f"Hola {usuarios[user_index]['Nombre']}, que desea realizar?")
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
        print("12. Crear nuevo usuario.")
        print("13. Cambiar de usuario.")
        print("0. Salir")
    
        opcion = input("Seleccione una opción: ")
        # Si se le pasa a esta variable un valor como 'uj3' esto permite que el programa no tire error y simplemente vuelva a pedir que ingrese la opcion
        if opcion.isdigit() == False:
            print("Por favor use los numeros a la izquierda, entradas con texto no son permitidas.")
        else:
            #Si si es un digito simplemente la pasa a int y funciona como normalmente lo haria
            opcion = int(opcion)

        if opcion == 1:
            anadir_reserva(user_index)
        elif opcion == 2:
            editar_reserva(user_index)
        elif opcion == 3:
            cancelar_reserva(user_index)
        elif opcion == 4:
            mostrar_reservas()
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
        elif opcion == 12:
            crear_usuario()
        elif opcion == 13:
            user_index = cambiar_usuario(user_index) #Cambiar_usuario solo cambia el index por su valor de retorno, por eso no la llamo unicamente como a las demas y cambio directamente el user_index.
        elif opcion == 0:
            print("Finalizando el programa.\n")
            break
        else:
            #Para numeros fuera de rango
            print("Opción inválida. Intente de nuevo.\n")

# Ejecutar el menú
mostrar_menu()
