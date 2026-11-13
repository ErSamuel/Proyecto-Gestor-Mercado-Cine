# Archivo: modelo_pelicula.py
# Define la clase Pelicula para la boletería (Rol 3)

class Pelicula:
    def __init__(self, id_pelicula, titulo, horario, sala, precio_boleto, asientos_disponibles):
        self.__id_pelicula = str(id_pelicula)
        self.__titulo = str(titulo)
        self.__horario = str(horario)
        self.__sala = str(sala)
        self.__precio_boleto = float(precio_boleto)
        self.__asientos_disponibles = int(asientos_disponibles)

    # --- GETTERS (Lectura de datos) ---
    def get_id(self):
        return self.__id_pelicula

    def get_titulo(self):
        return self.__titulo

    def get_horario(self):
        return self.__horario

    def get_sala(self):
        return self.__sala

    def get_precio(self):
        return self.__precio_boleto

    def get_asientos(self):
        return self.__asientos_disponibles

    # --- SETTERS (Modificar asientos al comprar) ---
    def set_asientos(self, nuevos_asientos):
        if nuevos_asientos >= 0:
            self.__asientos_disponibles = int(nuevos_asientos)

    # --- MÉTODO PARA MOSTRAR LA INFORMACIÓN ---
    def mostrar_cartelera_info(self):
        return (
            f"ID: {self.__id_pelicula} | Película: {self.__titulo} "
            f"| Horario: {self.__horario} | Sala: {self.__sala} "
            f"| Precio: ${self.__precio_boleto:.2f} | Asientos Libres: {self.__asientos_disponibles}"
        )