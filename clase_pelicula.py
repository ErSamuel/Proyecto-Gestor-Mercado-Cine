import hashlib

class Pelicula:
    def __init__(self, nombre, descripcion, duracion, costo, fecha_de_estreno, disponibilidad=True, id_pelicula=None):
        self._nombre = nombre
        self._descripcion = descripcion
        self._duracion = duracion
        self._costo = costo
        self._fecha_de_estreno = fecha_de_estreno
        self._disponibilidad = bool(disponibilidad)  # Asegura que sea True o False
        
        if id_pelicula is None: #si el id de la pelicula no se pasa por parametro se crea como un cod-hash
            self._id = self.generar_id_hash(nombre, limite=8)
        else:
            self._id = str(id_pelicula)

    #limite 8 por defecto , se puede cambiar
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
        self._disponibilidad = bool(valor)

    def __str__(self):
        estado = "Disponible en cartelera" if self._disponibilidad else "No disponible"
        return (f"Película: {self._nombre} (ID : {self._id})\n"
                f"Descripción: {self._descripcion}\n"
                f"Duración: {self._duracion} min | Costo: ${self._costo:.2f}\n"
                f"Fecha de estreno: {self._fecha_de_estreno} | Estado: [{estado}]")