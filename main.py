def mostrar_menu():
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
    print("0. Salir")

def ejecutar_menu():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            '''print()
        elif opcion == "2":
            print()
        elif opcion == "3":
            print()
        elif opcion == "4":
            print()
        elif opcion == "5":
            print()
        elif opcion == "6":
            print()
        elif opcion == "7":
            print()
        elif opcion == "8":
            print()
        elif opcion == "9":
            print()
        elif opcion == "10":
            print()
        elif opcion == "0":
            print()
            break
        else:
            print("Opción inválida. Intente de nuevo.")
'''
# Ejecutar el menú
ejecutar_menu()