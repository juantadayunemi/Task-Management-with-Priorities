class Tarea:
    def __init__(self, nombre, descripcion, prioridad):
        self.nombre = self.validar_nombre(nombre)
        self.descripcion = self.validar_descripcion(descripcion)
        self.prioridad = self.validar_prioridad(prioridad)
    
    def validar_nombre(self, nombre):
        if not nombre:
            raise ValueError("La tarea debe tener un nombre")
        return nombre
    
    def validar_descripcion(self, descripcion):
        if not descripcion:
            raise ValueError("La tarea debe tener una descripción")
        return descripcion

    def validar_prioridad(self, prioridad):
        if prioridad.lower() not in ['alta', 'media', 'baja']:
            raise ValueError("Prioridad debe ser 'alta', 'media' o 'baja'")
        return prioridad.lower()
