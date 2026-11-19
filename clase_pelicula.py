import hashlib


class Pelicula:
    def __init__(self, nombre, descripcion, duracion, costo, fecha_de_estreno, disponibilidad=30, id_pelicula=None):
        self._nombre = nombre
        self._descripcion = descripcion
        self._duracion = int(duracion)
        self._costo = float(costo)
        self._fecha_de_estreno = fecha_de_estreno
        # Valida y asigna la disponibilidad como entero >= 0 (asientos disponibles)
        self._disponibilidad = self._validar_disponibilidad(disponibilidad)

        if id_pelicula is None:  # si el id de la pelicula no se pasa por parametro se crea como un cod-hash
            self._id = self.generar_id_hash(nombre, limite=8)
        else:
            self._id = str(id_pelicula)

    # Metodo auxiliar para validar que los asientos disponibles sean un entero >= 0
    @staticmethod
    def _validar_disponibilidad(valor):
        if isinstance(valor, (bool, float)):
            raise ValueError("La disponibilidad debe ser un número entero mayor o igual a cero.")
        entero = int(valor)
        if entero < 0:
            raise ValueError("La disponibilidad no puede ser negativa.")
        return entero

    # Decorador @staticmethod agregado para evitar TypeError al llamarlo desde self o la clase
    # limite 8 por defecto , se puede cambiar
    @staticmethod
    def generar_id_hash(nombre, limite=8):
        hash_obj = hashlib.sha256(nombre.strip().lower().encode('utf-8'))
        return hash_obj.hexdigest()[:limite]

    @property
    def id(self): return self._id
    
    @property
    def nombre(self): return self._nombre
    
    @property
    def descripcion(self): return self._descripcion
    
    @property
    def duracion(self): return self._duracion
    
    @property
    def costo(self): return self._costo
    
    @property
    def fecha_de_estreno(self): return self._fecha_de_estreno

    @property
    def disponibilidad(self): return self._disponibilidad

    @disponibilidad.setter
    def disponibilidad(self, valor):
        # Valida que los nuevos asientos disponibles sigan siendo un entero >= 0
        self._disponibilidad = self._validar_disponibilidad(valor)

    def __str__(self):
        # Muestra el numero de asientos disponibles o indica si la funcion esta agotada
        estado = f"Disponible ({self._disponibilidad} asientos)" if self._disponibilidad > 0 else "Agotada / No disponible"
        return (f"Película: {self._nombre} (ID : {self._id})\n"
                f"Descripción: {self._descripcion}\n"
                f"Duración: {self._duracion} min | Costo: ${self._costo:.2f}\n"
                f"Fecha de estreno: {self._fecha_de_estreno} | Estado: [{estado}]")
