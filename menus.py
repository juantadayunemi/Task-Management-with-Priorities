from gestor_tareas import GestorTarea

# Funciones auxiliares de consola
def MostrarMenu():
    print("\n" + "MENU DE ACCESO " + "-" * 10)
    print('1. Agregar tarea')
    print('2. Eliminar tarea')
    print('3. Procesar tareas')
    print('4. Mostrar tarea')
    print('5. Carga masiva de tareas')
    print('6. Salir')

def MenuEliminar():
    print('1. Eliminar por nombre')
    print('2. Eliminar todas las tareas')
    print('3. Atrás')

# Función principal
def Main():
    gestor = GestorTarea()
    while True:
        MostrarMenu()
        try:
            op = int(input('Ingrese una opción del menú del 1 al 6: '))
            if op < 1 or op > 6:
                gestor.mostrar_mensaje("Opción seleccionada incorrecta. Por favor, ingrese un número entre 1 y 6.")
                continue
        except ValueError:
            gestor.mostrar_mensaje("Opción seleccionada incorrecta. Por favor, ingrese un número válido.")
            continue

        if op == 1:
            nombre = input('Ingrese el nombre de la Tarea: ')
            descripcion = input('Ingrese la descripción de la Tarea: ')
            prioridad = input("Ingrese la prioridad de la Tarea ['alta', 'media', 'baja']: ")
            gestor.agregar_tarea(nombre, descripcion, prioridad)

        elif op == 2:
            while True:
                gestor.limpiar_consola()
                MenuEliminar()
                try:
                    op1 = int(input('Ingrese una opción del menú del 1 al 3: '))
                    if op1 < 1 or op1 > 3:
                        gestor.mostrar_mensaje("Opción seleccionada incorrecta. Por favor, ingrese un número entre 1 y 3.")
                        continue
                except ValueError:
                    gestor.mostrar_mensaje("Opción seleccionada incorrecta. Por favor, ingrese un número válido.")
                    continue

                if op1 == 1:
                    nombre = input('Ingrese el nombre de la Tarea que quiere eliminar: ')
                    gestor.eliminar_tarea(nombre, True)
                elif op1 == 2:
                    confirmacion = input("¿Está seguro de eliminar todas las tareas? Esto borrará todos los datos actuales. (s/n): ").strip().lower()
                    if confirmacion == 's':
                        gestor.eliminar_tarea(None, False)
                    else:
                        gestor.mostrar_mensaje("No se eliminaron las tareas.")
                else:
                    gestor.limpiar_consola()
                    break

        elif op == 3:
            gestor.procesar_tarea()
        elif op == 4:
            gestor.mostrar_tarea()
        elif op == 5:
            gestor.carga_masiva(50)  # Llama a la función de carga masiva
        elif op == 6:
            gestor.mostrar_mensaje('Saliendo del menú...')
            break

Main()
