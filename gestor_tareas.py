import csv
import os
import shutil
from tabulate import tabulate
import time
from carga_masiva import carga_masiva_class  # Importar la función de carga masiva
from tarea import Tarea  # Importar la clase tarea

class GestorTarea:
    def __init__(self):
        self.tareas = []
        self.carpetaPendiente = os.path.join(os.getcwd(), 'venv/TareasPendientes')
        self.carpetaProcesadas = os.path.join(os.getcwd(), 'venv/TareasProcesadas')
        self.archivo_csv = 'tareas.csv'

        # Crear las carpetas si no existen
        os.makedirs(self.carpetaPendiente, exist_ok=True)
        os.makedirs(self.carpetaProcesadas, exist_ok=True)

        # Crear el archivo CSV si no existe
        if not os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, mode='w', newline='') as file:
                escritor = csv.writer(file)
                escritor.writerow(['Nombre', 'Descripcion', 'Prioridad', 'Estado'])

    def agregar_tarea(self, nombre, descripcion, prioridad):
        try:
            tarea = Tarea(nombre, descripcion, prioridad)
            nueva_tarea = {
                'nombre': tarea.nombre,
                'descripcion': tarea.descripcion,
                'prioridad': tarea.prioridad,
                'estado': 'Pendiente'
            }
            ruta_archivo = os.path.join(self.carpetaPendiente, nombre)

            if os.path.exists(ruta_archivo) or os.path.exists(os.path.join(self.carpetaProcesadas, nombre)):
                raise ValueError('El archivo ya está creado')

            self.tareas.append(nueva_tarea)
            self.guardar_archivo_fisico(nueva_tarea, ruta_archivo)
            self.mostrar_mensaje('Tarea agregada correctamente 😀')
        except ValueError as e:
            self.mostrar_mensaje(f"No se agregó la tarea 😞\nError: {e}")

 
    def mostrar_tarea(self):
        if not os.path.exists(self.archivo_csv) or sum(1 for _ in open(self.archivo_csv)) <= 1:
            self.mostrar_mensaje('No hay tareas agregadas')
            return
        tareas = []
        with open(self.archivo_csv, mode='r', newline='') as file:
            lector = csv.DictReader(file)
            for fila in lector:
                if 'Nombre' in fila:
                    tareas.append({
                        'Nombre': fila['Nombre'],
                        'Descripcion': fila['Descripcion'],
                        'Prioridad': fila['Prioridad'],
                        'Estado': fila['Estado']
                    })

        self.mostrar_mensaje("    LISTADO DE TAREAS")  # Imprime el título
        self.mostrar_mensaje(tareas, False)  # Presenta el contenido

    def eliminar_tarea(self, nombre=None, opcion=False):
        # Eliminar una tarea específica si 'opcion' es True y 'nombre' está definido
        if opcion and nombre:
            for carpeta in [self.carpetaPendiente, self.carpetaProcesadas]:
                ruta_archivo = os.path.join(carpeta, nombre)
                if os.path.exists(ruta_archivo):
                    os.remove(ruta_archivo)
                    self.actualizar_csv(nombre)
                    self.mostrar_mensaje(f"Tarea '{nombre}' eliminada correctamente")
                    return
            self.mostrar_mensaje('Error: El archivo no existe')
            return

        # Eliminar todas las tareas si 'opcion' es False
        if not os.listdir(self.carpetaPendiente) and not os.listdir(self.carpetaProcesadas):
            self.mostrar_mensaje('No hay tareas para eliminar')
            return

        for carpeta in [self.carpetaPendiente, self.carpetaProcesadas]:
            if os.path.exists(carpeta):
                archivos = os.listdir(carpeta)
                total = len(archivos)
                for i, archivo in enumerate(archivos, start=1):
                    ruta_archivo = os.path.join(carpeta, archivo)
                    os.remove(ruta_archivo)
                    porcentaje = int((i / total) * 100)
                    self.mostrar_mensaje(f'Eliminando - Progreso {porcentaje}%')

        # Limpiar contenido del archivo CSV, conservando solo el encabezado
        with open(self.archivo_csv, mode='r', newline='') as file:
            lector = csv.reader(file)
            encabezado = next(lector)  # Leer encabezado

        with open(self.archivo_csv, mode='w', newline='') as file:
            escritor = csv.writer(file)
            escritor.writerow(encabezado)  # Escribir solo el encabezado

        self.mostrar_mensaje('Las tareas se eliminaron correctamente')


    def actualizar_csv(self, nombre):
        with open(self.archivo_csv, mode='r', newline='') as file:
            lector = csv.reader(file)
            encabezados = next(lector)
            tareas_filtradas = [fila for fila in lector if fila[0] != nombre]

        with open(self.archivo_csv, mode='w', newline='') as file:
            escritor = csv.writer(file)
            escritor.writerow(encabezados)
            escritor.writerows(tareas_filtradas)

     
    
    def procesar_tarea(self):
        # Verificar si hay archivos en la carpeta de pendientes
        if not os.listdir(self.carpetaPendiente):
            self.mostrar_mensaje('No hay tareas pendientes')
            return

        # Leer todas las tareas desde el archivo CSV
        tareas = []
        with open(self.archivo_csv, mode='r', newline='') as file:
            lector = csv.DictReader(file)
            for fila in lector:
                tareas.append(fila)

        # Filtrar solo las tareas pendientes y ordenarlas por prioridad
        tareas_pendientes = [
            tarea for tarea in tareas if tarea['Estado'] == 'Pendiente'
        ]
        tareas_pendientes.sort(key=lambda x: ['alta', 'media', 'baja'].index(x['Prioridad']))

        # Procesar cada tarea pendiente en orden de prioridad
        total_tareas = len(tareas_pendientes)
        for index, tarea in enumerate(tareas_pendientes, start=1):
            nombre_tarea = tarea['Nombre']
            prioridad_tarea = f"{str(tarea['Prioridad']).rjust(5)}"
            porcentaje = index / total_tareas
            porcentajeView = f"{str(int(porcentaje*100)).rjust(3)}"

            # Mostrar progreso de procesamiento
            self.mostrar_mensaje(f"Procesando tarea '{nombre_tarea}' - {prioridad_tarea} - {porcentajeView}% completada")
            self.mostrar_mensaje("-" * int(60 * porcentaje),False)
            time.sleep(0.1)  # Pausa para simular tiempo de procesamiento

            # Actualizar el estado de la tarea y mover el archivo
            tarea['Estado'] = 'Procesada'
            ruta_archivo = os.path.join(self.carpetaPendiente, nombre_tarea)
            if os.path.exists(ruta_archivo):
                shutil.move(ruta_archivo, self.carpetaProcesadas)

        # Guardar los cambios en el archivo CSV
        tareas.sort(key=lambda x: ['alta', 'media', 'baja'].index(x['Prioridad']))
        self.guardar_tareas_csv(tareas)
        self.mostrar_mensaje('Tareas procesadas correctamente')

    # Sobreescribe el archivo csv con la lista
    def guardar_tareas_csv(self, tareas_procesadas):
        with open(self.archivo_csv, mode='w', newline='') as file:
            encabezado = ['Nombre', 'Descripcion', 'Prioridad', 'Estado']
            writer = csv.DictWriter(file, fieldnames=encabezado)
            writer.writeheader()
            writer.writerows(tareas_procesadas)

    #  Guardar archivo fisico
    def guardar_archivo_fisico(self, tarea, ruta_archivo):
        with open(ruta_archivo, 'w') as file:
            file.write(tarea['descripcion'])
        self.agrega_archivo_csv(tarea)

    # Agrega en el archivo csv
    def agrega_archivo_csv(self, tarea):
        with open(self.archivo_csv, mode='a', newline='') as file:
            escritor = csv.writer(file)
            if file.tell() == 0:
                escritor.writerow(['Nombre', 'Descripcion', 'Prioridad', 'Estado'])
            escritor.writerow([tarea['nombre'], tarea['descripcion'], tarea['prioridad'], tarea['estado']])

    def carga_masiva(self,rows):
        carga_masiva_class(self, rows) 

    def mostrar_mensaje(self,mensaje, limpiar=True):
        if limpiar:
           self.limpiar_consola()
           self.imprimeLinea(1)

        if isinstance(mensaje, list):
            print(tabulate(mensaje, headers="keys", tablefmt="grid"))
        else:
            print(mensaje)

        self.imprimeLinea(0)

    def limpiar_consola(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def imprimeLinea(self,saltoLinea=0):
        for _ in range(saltoLinea):
            print("\n")
        print("" + "-" * 60 + "\n")