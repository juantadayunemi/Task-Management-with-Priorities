import csv
import random
import time
import os
import shutil

def carga_masiva_class(gestor, cantidad=50):
    # Limpiar archivo CSV y lista de tareas
    gestor.tareas.clear()
    if os.path.exists(gestor.archivo_csv):
        os.remove(gestor.archivo_csv)  # Eliminar el archivo CSV si existe

    # Limpiar el contenido de ambas carpetas: TareasPendientes y TareasProcesadas
    for carpeta in [gestor.carpetaPendiente, gestor.carpetaProcesadas]:
        if os.path.exists(carpeta):
            for archivo in os.listdir(carpeta):
                ruta_archivo = os.path.join(carpeta, archivo)
                if os.path.isfile(ruta_archivo):
                    os.remove(ruta_archivo)  # Eliminar archivo
                elif os.path.isdir(ruta_archivo):
                    shutil.rmtree(ruta_archivo)  # Eliminar carpeta de existir con el mismo nombre

    # Crear un nuevo archivo CSV y agregar encabezados
    with open(gestor.archivo_csv, mode='w', newline='') as file:
        escritor = csv.writer(file)
        escritor.writerow(['Nombre', 'Descripcion', 'Prioridad', 'Estado'])  # Encabezados

    # Generar tareas aleatorias y cargarlas
    prioridades = ['alta', 'media', 'baja']
    for i in range(1, cantidad + 1):
        nombre = f"Tarea_{str(i).zfill(3)}"
        descripcion = f"Descripción de la tarea {i}"
        prioridad = random.choice(prioridades)
        nueva_tarea = {
            'nombre': nombre,
            'descripcion': descripcion,
            'prioridad': prioridad,
            'estado': 'Pendiente'
        }

        # Obtiene ruta de carpetas
        ruta_archivo = os.path.join(gestor.carpetaPendiente, nombre)

        # Agregar tarea a la lista y al archivo CSV y guarda fisico
        gestor.tareas.append(nueva_tarea)
        gestor.guardar_archivo_fisico(nueva_tarea, ruta_archivo)

        # Mostrar progreso
        porcentaje =i / cantidad
        porcentajeView = f"{str(int(porcentaje*100)).rjust(3)}"

        print(f"Cargando tarea '{nombre}' - Progreso: {porcentajeView}%")
        time.sleep(0.1)  # Pausa para simular el tiempo de carga

    print("Carga masiva completada correctamente.")
