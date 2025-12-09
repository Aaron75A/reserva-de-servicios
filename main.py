import copy
import re
import sys
from datetime import datetime

# Todas las variables dentro de clase a las que se le declara un tipo list deben de tener = [], de otro modo si las revisamos y aun no se declaran dan un AttributeError
# Notese que esto sucede con cualquier variable que aun no este declarada, es simplemente que en el programa recurrimos mas a revisar listas que pueden estar vacias, por eso unicamente les asignamos un valor a la lista.
# Todas las variables mutables se agregan en __init__ para evitar problemas con la memoria
class Reserva:
    def __init__(self, nombre_empleado: str, nombre_cliente: str, fecha: str, hora: list = []):
        self.nombre_empleado = nombre_empleado
        self.nombre_cliente = nombre_cliente
        self.fecha = fecha
        self.hora = hora
    def save(self, fname):
        with open(fname, 'w') as f: json.dump(self._dict_, f, indent=4)

class Usuario:
    def __init__(self):
        self.reservas: list[Reserva] = []
        self.nombre: str
    def save(self, fname):
        with open(fname, 'w') as f: json.dump(self._dict_, f, indent=4)

class Empleado:
    def __init__(self):
        self.disponibilidad: list = []
        self.reservas: list[Reserva] = []
        self.nombre: str
        self.apellido: str
        self.email: str
        self.cedula: int
        self.cel: int
    horario = "8:00-17:00"
    def save(self, fname):
        with open(fname, 'w') as f: json.dump(self._dict_, f, indent=4)

class Servicio:
    def __init__(self):
        self.empleados: list[Empleado] = []
        self.nombre: str
        self.Iduracion: int
        self.Sduracion: str
        self.costo: int
    def save(self, fname):
        with open(fname, 'w') as f: json.dump(self._dict_, f, indent=4)

fecha_hoy = datetime.now().strftime('%B %d, %Y | %A')

# Lista que contendra todos los servicios que declaremos para el sistema.
servicios = []

#Usuario por default, nuevamente no tiene mayor fin mas que dar practicidad a la hora de testear.
usuarios = []
#Funcion para usarla en cada operacion del sistema, para asi salir de la misma, esta es para inputs generales, retorna permitido para evitar errores
#Las funciones de validacion también, pero hay algunas que podía retornar True como isint
def cancelar_opcion(texto):
    if texto == "0":
        print("Regresando al menú principal...")
        return "permitido"
    elif texto == "-1":
        print("Finalizando programa...")
        sys.exit()
    else:
        return texto


def mostrar_date(d,f = "%B %d, %Y | %A"):
    #datetime.strptime crea un objeto datetime en base a un string d y un formato dado
    #sirve para modificar el formato en que se ven las horas y manipulacion horaria accesible, por ejemplo si queremos saber si es martes
    datetime_p = datetime.strptime(d, "%Y-%m-%d")
    return datetime_p.strftime(f)
#A valid date le añadí verificación de si es 0 o -1, si es -1 el sistema termina por completo y si es 0 devuelve True
def valid_date(s):
    c = datetime.now().strftime('%Y-%m-%d').split('-')
    for i in range(0,len(c)): c[i] = int(c[i])
    while True:
        p = input(s)
        if p == "0":
            print("Regresando al menú principal...")
            return "permitido"
        elif p == "-1":
            print("Finalizando programa...")
            sys.exit()
            
        try:
            # Datetime da un error si el formato del string no es identico al que pide (%Y-%m-%d en este caso)
            datetime_p = datetime.strptime(p, "%Y-%m-%d")
        except ValueError:
            print("El formato en el que ingreso la fecha no es valido, por favor ingrese una fecha con formato valido.")
            continue
        if(datetime_p.strftime('%A') == "Sunday"):
            print("La fecha ingresada corresponde a un dia domingo, por favor recuerde que en estos dias no se trabaja.")
            continue
        d = p
        # Si el formato es correcto lo particiono en partes enteras para calcular la distancia entre la fecha actual y la ingresada
        d = d.split('-')
        for i in range(0,len(d)): d[i] = int(d[i])
        separacion_meses = (((d[0] - c[0]) * 12) + d[1]) - c[1]
        if(d[0]<c[0] or (d[0] == c[0] and d[1]<c[1]) or (d[0] == c[0] and d[1]==c[1] and d[2]<c[2])):
            print("La fecha ingresada es anterior a la fecha actual, por favor ingrese una fecha valida para la reserva.")
        elif separacion_meses > 12:
            print("No se puede reservar para una fecha tan lejana, por favor ingrese una fecha que no este a mas de 12 meses de la fecha actual.")
        else: break
    return p
#A valid email le añadí verificación de si es 0 o -1, si es -1 el sistema termina por completo y si es 0 devuelve permitido para evitar error
def valid_email(s):
    while True:
        e = input(s)
        # el string dentro de re.match significa lo siguiente: (cualquier caracter)@(cualquier caracter).(minimo 2 caracteres de a-z o A-Z)
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', e)
        if valid: break
        elif e == "0":
            print("Regresando al menú principal...")
            return "permitido"
        elif e == "-1":
            print("Finalizando programa...")
            sys.exit()


        else: print("El email ingresado no es valido, intentelo de nuevo.")
    return e
#Valid numero queda con "permitido" en vez de True para que no de error
def valid_numero(s,c):
    while True:
        e = input(s)
        valid = re.match(r'^[0-9]\d{9}$', e)
        if valid: break
        elif e == "0":
            print("Regresando al menú principal...")
            return "permitido"
        elif e == "-1":
            print("Finalizando programa...")
            sys.exit()

        else:
            print(c)
            print("La entrada debe de contener exactamente 10 digitos.")
    return int(e)
#A isint le añadí verificación de si es 0 o -1, si es -1 el sistema termina por completo y si es 0 devuelve True
def isint(s, e = "El valor ingresado para este campo no es valido, intentelo de nuevo."):
    while True:
        n = input(s)
        if n == "0":
           print("Saliendo al menú principal...")
           return "permitido"
        elif n == "-1":
            print("Finalizando programa...")    
            sys.exit()
        try:
            return int(n)
        
        except ValueError:
            print(e)
            continue
        
        break
    return n
#A valid cost le añadí verificación de si es 0 o -1, si es -1 el sistema termina por completo y si es 0 devuelve True
def valid_cost(c):
    while(1):
        n = isint(c)
        if n == "permitido":
            return "permitido"
        if(n <= 0): 
            print("El valor del producto debe de ser positivo y distinto a 0, intentelo de nuevo.")
        else: break
    return n

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
#A valid duracion le añadí verificación de si es 0 o -1, si es -1 el sistema termina por completo y si es 0 nuevamente devuelve "permitido"
#Queda un poco feo pero sirve
def valid_duracion(s):
    while(1):
        n = input(s)
        if n == "0":
            print("Regresando al menú principal...")
            return "permitido"
        elif n == "-1":
            print("Finalizando programa...")
            sys.exit()
    
        try:
            n = ns_split(n)
        except: 
            print("El valor ingresado para este campo es invalido, intentelo de nuevo.")
            continue
        
        if (n[1].lower() in ["hr", "min"]) == False:
            print(f"La unidad de tiempo {n[1].lower()} es invalida, intentelo de nuevo.")
            continue
        if(n[1].lower() == "hr"): d = 1
        elif(n[1].lower() == "min"): d = 60
        d = n[0] / d
        if(d > 9):
            print(f"La duracion del servicio sobrepasa la cantidad de horas laborales del empleado, por favor ingrese una duracion menor.")
            continue
        else: break
    return n

def creacion_citas(info_servicio, horario):
    duracion = 0 #Placeholder, lo uso por comodidad pues esto luego almacenara la duracion en un formato estandar (minutos)
    ultima_jornada = horario[0] * 60 # Placeholder nuevamente, si el horario es [20, 40] esto seria = 40, lo que permite seguir con [40, 60] de manera mas facil
    lista_horas = []
    if(info_servicio.Sduracion == "hr"): duracion = info_servicio.Iduracion * 60
    elif(info_servicio.Sduracion == "min"): duracion = info_servicio.Iduracion
    tiempo_jornada = (horario[1]*60) - (horario[0]*60) # Si se trabaja de 7am a 1pm esto seria 360, que son 6hr por eje
    for i in range(0, int(tiempo_jornada / duracion)):
        x = [ultima_jornada, ultima_jornada+duracion]
        ultima_jornada = x[1]
        x[0] /= 60 #Paso de minutos a horas
        x[1] /= 60
        x1_minutos = (x[0] - int(x[0])) * 60 #los minutos son simplemente la parte decimal que queda como residuo de la conversion a horas, por eso tomo la parte decimal y la multiplico por 60 (Si son 0.25 es 1/4 de hora, o sea, 15min)
        x2_minutos = (x[1] - int(x[1])) * 60
        x1_minutos = int(round(x1_minutos)) #Redondeo porque la precision decimal de python se vuelve loca a veces
        x2_minutos = int(round(x2_minutos))
        
        x[0] = str(int(x[0])) + ":" + "{:02d}".format(x1_minutos)
        x[1] = str(int(x[1])) + ":" + "{:02d}".format(x2_minutos)
        lista_horas.append(x.copy()) #Olvide agregar esto en el anterior commit, dejarlo en la entrega final, de otra manera no funcionaria completamente bien.
    return lista_horas

def crear_servicio():
    s1 = Servicio()
    print("Presione 0 en cualquier campo para volver al menú")
    print("Presione -1 en cualquier campo para salir del sistema \n")
    s1.nombre = cancelar_opcion(input("Ingrese el nombre del servicio: "))
    if s1.nombre == "permitido":
        return
    
    duracion = valid_duracion("Ingrese la duracion del servicio (formato: numero-(hr/min/s), eje: 30min, 1hr): ")
    if duracion == "permitido":
        return
    s1.Iduracion = duracion[0]
    s1.Sduracion = duracion[1]
    s1.costo = valid_cost("Ingrese el costo del servicio: ")
    if s1.costo == "permitido":
        return
    servicios.append(copy.copy(s1)) # Lo mismo que con las listas. Las clases son objetos mutables, por lo tanto si no usas .copy se pasan por referencia y eso no nos conviene.
    print("Servicio creado con exito!")

def modificar_servicio():
    if(len(servicios) == 0):
        print("No existe ningun servicio para modificar.")
        return
    
    print("Lista de servicios disponibles")
    print("Presione 0 en cualquier campo para volver al menú")
    print("Presione -1 en cualquier campo para salir del sistema \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i].nombre}")
    x = isint("Seleccione el servicio que desea modificar: ")# El X ingresado se hace con la convencion de 1 hasta len(servicios), pero asi no funciona la lista, esto lo soluciona.
    #Añadí la convención despúes de verificar si es 0 o -1 para que no diera error
    if x == "permitido":
        return
    elif x != "permitido":
        x -= 1
    elif x < 0 or x >= len(servicios):
        print("El servicio que usted desea modificar no existe, por favor intentelo de nuevo.\n")
        return

    variable = cancelar_opcion(input("Que variable desea modificar? (Nombre, Duracion, Costo o Todo): "))
    if variable == "permitido":
        return
    if(variable.lower() == "nombre" or variable.lower() == "todo"):
        servicios[x].nombre = cancelar_opcion(input("Ingrese el nuevo nombre del servicio: "))
        if servicios[x].nombre == "permitido":
            return
    if(variable.lower() == "duracion" or variable.lower() == "todo"):
        existe_reserva = False
        for i in range(0, len(servicios[x].empleados)):
            if(len(servicios[x].empleados[i].reservas) != 0):
                existe_reserva = True
        
        if(existe_reserva):
            print(f"La duracion del servicio {servicios[x].nombre} no se puede modificar puesto que aun hay reservas activas, estas deben completarse o eliminarse primero.\n")
        else:
            nueva_duracion = valid_duracion("Ingrese la nueva duracion del servicio (formato: numero-(hr/min/s), eje: 30min, 1hr): ")
            if nueva_duracion == "permitido":
                return
            servicios[x].Iduracion = nueva_duracion[0]
            servicios[x].Sduracion = nueva_duracion[1]
    if(variable.lower() == "costo" or variable.lower() == "todo"):
        servicios[x].costo = valid_cost("Ingrese el nuevo costo del servicio: ")
        if servicios[x].costo == "permitido":
            return

    if(variable.lower() == "todo"): print(f"La informacion de {servicios[x].nombre} ha sido modificada con exito")
    else: print(f"El/la {variable.lower()} del servicio ha sido modificado/a")

def eliminar_servicio():
    if(len(servicios) == 0):
        print("No existe ningun servicio para eliminar.")
        return

    print("Lista de servicios disponibles")
    print("Presione 0 en cualquier campo para volver al menú")
    print("Presione -1 en cualquier campo para salir del sistema \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i].nombre}")

    x = isint("Seleccione el servicio que desea eliminar: ") #convencion.
    if x == "permitido":
        return
    elif x != "permitido":
        x -= 1
    elif(x < 0 or x >= len(servicios)):
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

    print("De que servicio desea adquirir informacion?")
    print("Presione 0 en cualquier campo para volver al menú")
    print("Presione -1 en cualquier campo para salir del sistema \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i].nombre}")
    x = isint("Elija un servicio: ") 
    if x == "permitido": return
    else: x-=1
    
    if(x < 0 or x >= len(servicios)):
        print("El servicio que usted eligio no existe, intentelo de nuevo.\n")
    else:
        print(f"\nNombre: {servicios[x].nombre}")
        print(f"Duracion: {servicios[x].Iduracion}{servicios[x].Sduracion}")
        print(f"Costo: {servicios[x].costo}$")
        if(len(servicios[x].empleados) == 0):
            print("No existen empleados.\n")
        else:
            print(f"Cantidad de empleados: {len(servicios[x].empleados)}")
            print("A continuacion se mostraran los empleados del servicio: ")
            for i in range(0, len(servicios[x].empleados)):
                # El +1 que se usa en la primera linea se usa para usar una convencion de rango 1 hasta la cantidad de elementos, saltando el 0 (Fines esteticos).
                print(f"\nEmpleado {i+1}: ")
                print(f"Nombres: {servicios[x].empleados[i].nombre}")
                print(f"Apellidos: {servicios[x].empleados[i].apellido}")
                print(f"Cedula: {servicios[x].empleados[i].cedula}")
                print(f"Celular: {servicios[x].empleados[i].cel}")
                print(f"Email: {servicios[x].empleados[i].email}")
                print(f"Horario: {servicios[x].empleados[i].horario}")
                print(f"Disponibilidad (Horas en las que admite cita.): ")
                for a in range(0, len(servicios[x].empleados[i].disponibilidad)):
                    print(f"[{a+1}] {servicios[x].empleados[i].disponibilidad[a]}")

def ingresar_empleado():
    if len(servicios) == 0:
        print("No existe ningun servicio al cual ingresar un empleado, cree uno primero.")
        return
    print("A que servicio desea anadir un empleado?: \n")
    print("Presione 0 en cualquier campo para volver al menú")
    print("Presione -1 en cualquier campo para salir del sistema \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i].nombre}")
    x = isint("Elija el servicio: ")
    if x == "permitido": return
    else: x -= 1

    if(x < 0 or x >= len(servicios)):
        print("El servicio que ha elegido no existe, intentelo de nuevo.\n")
        return

    p1 = Empleado()
    print("\nIngrese los datos del empleado: ")
    p1.nombre = cancelar_opcion(input("Nombres: "))
    if p1.nombre == "permitido":
        return
    p1.apellido = cancelar_opcion(input("Apellidos: "))
    if p1.apellido == "permitido":
        return
    p1.cedula = valid_numero("Cedula: ", "El valor ingresado para la cedula es incorrecto")
    if p1.cedula == "permitido":
        return
    p1.cel = valid_numero("Celular: ", "El valor ingresado para el celular es incorrecto")
    if p1.cel == "permitido":
        return
    p1.email = valid_email("Email: ")
    if p1.email == "permitido":
        return
    horas = horario_empleado(p1.horario)
    lista_horas = creacion_citas(servicios[x], horas)
    p1.disponibilidad = lista_horas
    servicios[x].empleados.append(copy.copy(p1))
    print(f"\nEl empleado {p1.nombre} ha sido agregado a {servicios[x].nombre} con exito.\n")

def modificar_empleado():
    if(len(servicios) == 0):
        print("No existen servicios ni empleados disponibles, cree unos primero.")
        return
    print("A que servicio pertenece el empleado?: \n")
    print("Presione 0 en cualquier campo para volver al menú")
    print("Presione -1 en cualquier campo para salir del sistema \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i].nombre}")
    x = isint("Elija el servicio: ")
    if x == "permitido": return
    else: x -= 1

    if(x < 0 or x >= len(servicios)):
        print("El servicio seleccionado no existe, intentelo nuevamente.\n")
        return

    print("Lista de empleados: \n")
    for i in range(0, len(servicios[x].empleados)):
        print(f"[{i+1}] {servicios[x].empleados[i].nombre} {servicios[x].empleados[i].apellido}")
    y = isint("Seleccione el empleado al cual desea modificarle informacion: ")
    if y == "permitido": return
    else: y -= 1
    if(y < 0 or y >= len(servicios[x].empleados)):
        print("El empleado que usted selecciono no existe, intentelo de nuevo.\n")
        return

    # Para facilidad no se puede modificar informacion de un empleado si este tiene reservas activas
    if(len(servicios[x].empleados[y].reservas) != 0):
        print(f"\nEl empleado {servicios[x].empleados[y].nombre} tiene reservas activas en este momento por lo que no es posible modificar su informacion en el sistema, las reservas deben completarse o eliminarse primero.\n")
        return

    tipo_modificacion = cancelar_opcion(input("Desea modificar toda su informacion o solo un dato en especifico? (completa/especifica): "))
    if tipo_modificacion == "permitido": return
    variable = ""
    # Aqui uso nuevamente el lower para facil verificacion
    if(tipo_modificacion.lower() in ["especifica", "completa"]) == False:
        print("Esa opcion no existe, por favor intentelo de nuevo")
        return
    if(tipo_modificacion.lower() == "especifica"):
        variable = cancelar_opcion(input("Que variable desea modificar? (cedula, celular o email): "))
        if variable == "permitido": return
    if(variable.lower() == "cedula" or tipo_modificacion.lower() == "completa"):
        servicios[x].empleados[y].cedula = valid_numero("Nuevo No. Cedula: ", "El valor ingresado para la cedula es incorrecto")
    if(variable.lower() == "celular" or tipo_modificacion.lower() == "completa"):
        servicios[x].empleados[y].cel = valid_numero("Nuevo No. Cel: ", "El valor ingresado para el celular es incorrecto")
    if(variable.lower() == "email" or tipo_modificacion.lower() == "completa"):
        servicios[x].empleados[y].email = valid_email("Nuevo Email: ")

    if(tipo_modificacion.lower() == "completa"): print(f"La informacion de {servicios[x].empleados[y].nombre} ha sido modificada con exito")
    else: print(f"El/La {variable.lower()} de {servicios[x].empleados[y].nombre} ha sido modificado/a con exito.\n")

def eliminar_empleado():
    if(len(servicios)==0):
        print("Esta funcion no esta disponible puesto que no existen empleado para eliminar.")
        return
    print("A que servicio pertenece el empleado que desea eliminar?: \n")
    print("Presione 0 en cualquier campo para volver al menú")
    print("Presione -1 en cualquier campo para salir del sistema \n")
    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i].nombre}")
    x = isint("Elija el servicio: ")
    if x == "permitido": return
    else: x -= 1
    
    if(x < 0 or x >= len(servicios)):
        print("El servicio que usted selecciono no existe, intentelo de nuevo.\n")
    else:
        print("\nQue empleado del servicio desea eliminar?: ")
        for i in range(0, len(servicios[x].empleados)):
            print(f"[{i+1}] {servicios[x].empleados[i].nombre} {servicios[x].empleados[i].apellido}")
        y = isint("Elija un empleado: ")
        if y == "permitido": return
        else: y -= 1
        if(y < 0 or y > len(servicios[x].empleados)):
            print("El empleado que usted seleccion no existe, intentelo de nuevo.\n")
            return

        if(len(servicios[x].empleados[y].reservas) != 0):
            print(f"\nEl empleado {servicios[x].empleados[y].nombre} tiene reservas activas en este momento por lo que no es posible borrarlo del sistema, estas deben completarse o eliminarse primero.\n")
        else:
            servicios[x].empleados.pop(y)
            print("Empleado ha sido eliminado con exito.\n")

def anadir_reserva(user_index):
    if(len(servicios) == 0):
        print("No existe ningun servicio al cual ingresar una reserva.")
        return
    print("En que servicio desea realizar su reserva?: ")
    print("Presione 0 en cualquier campo para volver al menú")
    print("Presione -1 en cualquier campo para salir del sistema \n")

    for i in range(0, len(servicios)):
        print(f"[{i+1}] {servicios[i].nombre}")
    servicio = isint("Que servicio desea?: ")
    if servicio == "permitido": return
    else: servicio -= 1

    print("\nCon que empleado desea realizar su reserva?: ")
    for i in range(0, len(servicios[servicio].empleados)):
        print(f"\nEmpleado {i+1}: ") 
        print(f"Nombres: {servicios[servicio].empleados[i].nombre}")
        print(f"Apellidos: {servicios[servicio].empleados[i].apellido}")
        print(f"Cedula: {servicios[servicio].empleados[i].cedula}")
        print(f"Celular: {servicios[servicio].empleados[i].cel}")
        print(f"Email: {servicios[servicio].empleados[i].email}")

    empleado = isint("Seleccione el empleado que desea: ")
    if empleado == "permitido": return
    else: empleado -= 1
    
    fecha = valid_date("En que fecha lo desea? (se usa formato yyyy-mm-dd, eje: 2024-03-26): ")
    if fecha == "permitido": return
    for i in range(0, len(servicios[servicio].empleados[i].disponibilidad)):
        print(f"Horario {i+1}: {servicios[servicio].empleados[empleado].disponibilidad[i]}")
    hora = isint("En que horario lo desea?: ")
    if hora == "permitido": return
    else: hora -= 1

    hora_seleccionada = servicios[servicio].empleados[empleado].disponibilidad[hora]
    ocupado = False
    # Si la cantidad de reservas es nula entonces el for dara un error puesto que habria un AttributeError por la clase (Fecha y hora vacia).
    if(len(servicios[servicio].empleados[empleado].reservas) != 0):
        for r in servicios[servicio].empleados[empleado].reservas:
            if r.fecha == fecha and r.hora == hora_seleccionada:
                ocupado = True
                break
    if ocupado:
        print(f"\n El horario {hora_seleccionada} en la fecha {fecha} NO está disponible con {servicios[servicio].empleados[empleado].nombre}, seleccione otra fecha, hora o empleado.")
        return

    reserva = Reserva(servicios[servicio].empleados[empleado].nombre, usuarios[user_index].nombre, fecha, hora_seleccionada)

    servicios[servicio].empleados[empleado].reservas.append(copy.copy(reserva))
    usuarios[user_index].reservas.append(copy.copy(reserva))

    print("RESERVA REALIZADA...\n")
    print(f"Nombres de Empleado: {usuarios[user_index].reservas[-1].nombre_empleado}")
    print(f"Fecha: {mostrar_date(fecha)}")
    print(f"Hora: {hora_seleccionada}")

#Editar reserva
def editar_reserva(user_index):
    if len(usuarios[user_index].reservas) == 0:
        print("Usted no tiene reservas.")
        return

    for i in range(len(usuarios[user_index].reservas)):
        print(f"[{i+1}] {usuarios[user_index].reservas[i]}")
    print("Presione 0 en cualquier campo para volver al menú")
    print("Presione -1 en cualquier campo para salir del sistema \n")
    reserva_editar = isint("\n¿Qué reserva desea editar?: ")
    if reserva_editar == "permitido": return
    else: reserva_editar -= 1
    
    if reserva_editar < 0 or reserva_editar >= len(usuarios[user_index].reservas):
        print("Reserva inválida.")
        return

    reserva = usuarios[user_index].reservas[reserva_editar]
    fecha_actual, hora_actual = reserva.fecha, reserva.hora
    nombre_empleado = reserva.nombre_empleado

    # localizar empleado
    for s in range(len(servicios)):
        for e in range(len(servicios[s].empleados)):
            if servicios[s].empleados[e].nombre == nombre_empleado:
                empleado = servicios[s].empleados[e]

    print(f"\nReserva actual con {empleado.nombre} el {fecha_actual} a las {hora_actual}")
    opcion = cancelar_opcion(input("¿Qué desea cambiar? (fecha/hora/ambas): "))
    if opcion == "permitido": return

    if opcion.lower() == "fecha" or opcion.lower() == "ambas": 
        nueva_fecha = valid_date("Nueva fecha (yyyy-mm-dd): ")
        if nueva_fecha == "permitido": return
    else: nueva_fecha = fecha_actual

    if opcion.lower() == "hora" or opcion.lower() == "ambas":
        for i in range(len(empleado.disponibilidad)):
            print(f"[{i+1}] {empleado['Disponibilidad'][i]}")
        hr = isint("Seleccione nueva hora: ")
        if hr == "permitido": return
        else: hr -= 1
        if hr < 0 or hr >= len(empleado.disponibilidad):
            print("Hora inválida.")
            return
        nueva_hora = empleado.disponibilidad[hr]
    else: nueva_hora = hora_actual

    if (opcion.lower() in ["fecha", "ambas", "hora"]) == False:
        print("Esa opcion no existe.")
        return

    # verificar disponibilidad
    for r in empleado.reservas:
        if r.fecha == nueva_fecha and r.hora == nueva_hora:
            print("Ese horario ya está ocupado.")
            return

    # actualizar
    for r in empleado.reservas:
        if r.fecha == fecha_actual and r.fecha == hora_actual:
            r.fecha, r.hora = nueva_fecha, nueva_hora
    reserva.fecha, reserva.hora = nueva_fecha, nueva_hora

    print(f"\nReserva modificada: {empleado.nombre} - {mostrar_date(nueva_fecha)} {nueva_hora}")

def cancelar_reserva(user_index):
        if len(usuarios[user_index].reservas) == 0:
            print("No tienes reservas para cancelar.\n")
            return

        print("Lista de usuarios con reservas: \n")
        print("Presione 0 en cualquier campo para volver al menú")
        print("Presione -1 en cualquier campo para salir del sistema \n")
        for i in range(0, len(usuarios[user_index].reservas)):
            print(f"[{i+1}] {usuarios[user_index].reservas[i]}")
        
        reserva_cancelar = isint("¿Qué reserva desea cancelar?: ") #convencion
        if reserva_cancelar == "permitido": return
        else: reserva_cancelar -= 1
        if reserva_cancelar < 0 or reserva_cancelar >= len(usuarios[user_index].reservas):
            print("La reserva que seleccionaste no existe.\n")
        else:
            reserva_eliminada = usuarios[user_index].reservas.pop(reserva_cancelar)
            print(f"¡Tu reserva {reserva_eliminada} ha sido cancelada correctamente!\n")

def mostrar_reservas():   #Con esta funcion voy a mostrar las reservas de todos los servicios, me tocó aprender a usar 'enumerate'
    print("\n----->LISTA DE TODAS LAS RESERVAS<-----\n")
    for s, servicio in enumerate(servicios):  # Con esto recorremos todos los servicios
        print(f"Servicio {s+1}: {servicio.nombre}")
        empleados = servicio.empleados
        for e, empleado in enumerate(empleados):  # y esto para recorrer empleados de cada servicio
            if len(empleado.reservas) > 0:
                print(f"  Empleado {e+1}: {empleado.nombre} {empleado.apellido}")
                for r, reserva in enumerate(empleado.reservas):
                    print(f"    Reserva {r+1}: Cliente: {reserva.nombre_cliente}, Fecha: {mostrar_date(reserva.fecha)}, Hora: {reserva.hora}")
            else:
                print(f"  Empleado {e+1}: {empleado.nombre} {empleado.apellido} (Sin reservas)")
        print()  

def crear_usuario_inicio():
    print("\nCreando un nuevo usuario.")
    print("Presione -1 en cualquier campo para salir del sistema \n")
    
    user = Usuario()
    user.nombre = input("Ingrese su nombre completo: ")
    if user.nombre == "-1":
        print("Finalizando programa...")
        sys.exit()
    usuarios.append(copy.copy(user))
    print(f"Se ha creado al usuario {user.nombre} con exito.\n")

def crear_usuario_generico():
    print("\nCreando un nuevo usuario.")
    print("Presione 0 en cualquier campo para volver al menú")
    print("Presione -1 en cualquier campo para salir del sistema \n")
    
    user = Usuario()
    user.nombre = cancelar_opcion(input("Ingrese su nombre completo: "))
    if user.nombre == "permitido": return
    usuarios.append(copy.copy(user))
    print(f"Se ha creado al usuario {user.nombre} con exito.\n")

# Aqui le paso como argumento user_index de la funcion principal por practicidad, si la funcion falla necesita de este argumento para que no termine el programa y simplemente siga usando el mismo usuario que eligio hasta el momento
def cambiar_usuario(user_index):
    if(len(usuarios) == 0):
        print("Usted es el unico usuario existente.")
        return

    print("\nUsuarios disponibles: ")
    print("Presione 0 en cualquier campo para volver al menú")
    print("Presione -1 en cualquier campo para salir del sistema \n")
    for i in range(0, len(usuarios)):
        print(f"[{i+1}] {usuarios[i].nombre}")
    nuser = isint("Que usuario desea usar?: ")
    if nuser == "permitido": return
    else: nuser -= 1
    if(nuser < 0 or nuser > len(usuarios)):
        print("El usuario que usted eligio no existe, por favor intentelo de nuevo.\n")
        return user_index #Fijate en que si falla retorna user_index, o sea, el usuario actual.
    else:
        print(f"Se ha cambiado al usuario {usuarios[nuser].nombre} con exito.\n")
        return nuser
    return user_index # Este return es el default por si falla algo arriba (como inputs), se usa por seguridad.

def mostrar_menu():
    print("\n--- Bienvenido al sistema de gestion de servicios ---")
    crear_usuario_inicio()
    user_index = 0 # Defino user_index y su default, todas las funciones que requieren saber el usuario actual la necesitan como argumento

    while True:
        print("\n--- SISTEMA DE GESTIÓN DE SERVICIOS ---")
        print(fecha_hoy)
        print(f"Hola {usuarios[user_index].nombre}, que desea realizar?")
        print("1. Ingresar reserva")
        print("2. Editar reserva")
        print("3. Cancelar reserva")
        print("4. Consultar reservas")
        print("5. Ingresar empleado")
        print("6. Editar empleado")
        print("7. Borrar empleado")
        print("8. Ingresar servicio")
        print("9. Editar servicio")
        print("10. Borrar servicio")
        print("11. Informacion de un servicio.")
        print("12. Crear nuevo usuario.")
        print("13. Cambiar de usuario.")
        print("-1. Salir")

        # Si se le pasa a esta variable un valor como 'uj3' esto permite que el programa no tire error y simplemente vuelva a pedir que ingrese la opcion
        opcion = isint("Seleccione una opción: ", "Por favor use los numeros a la izquierda, entradas con texto no son permitidas.")
                       
        if opcion == 1:
            anadir_reserva(user_index)        
        elif opcion == 2:
            editar_reserva(user_index)
        elif opcion == 3:
            cancelar_reserva(user_index)
        elif opcion == 4:
            mostrar_reservas()
        elif opcion == 5:
            ingresar_empleado()
        elif opcion == 6:
            modificar_empleado()
        elif opcion == 7:
            eliminar_empleado()
        elif opcion == 8:
            crear_servicio()
        elif opcion == 9:
            modificar_servicio()
        elif opcion == 10:
            eliminar_servicio()
        elif opcion == 11:
            informacion_servicio()
        elif opcion == 12:
            crear_usuario_generico()
        elif opcion == 13:
            user_index = cambiar_usuario(user_index) #Cambiar_usuario solo cambia el index por su valor de retorno, por eso no la llamo unicamente como a las demas y cambio directamente el user_index.
        #elif opcion == 0:
        #    print("Finalizando el programa.\n")
        #    sys.exit()
        else:
            #Para numeros fuera de rango
            print("Opción inválida. Intente de nuevo.\n")

# Ejecutar el menú
mostrar_menu()
