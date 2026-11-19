# Archivo: modelo_pelicula.py
# Define la clase Pelicula para la boletería (Rol 3)

import math


class Pelicula:
    def __init__(self, id_pelicula, titulo, horario, sala, precio_boleto, asientos_disponibles):
        self.__id_pelicula = str(id_pelicula)
        self.__titulo = str(titulo)
        self.__horario = str(horario)
        self.__sala = str(sala)
        # Valida precio finito >= 0 y asientos enteros >= 0 al construir el objeto
        self.__precio_boleto = self._validar_precio(precio_boleto)
        self.__asientos_disponibles = self._validar_asientos(asientos_disponibles)

    @staticmethod
    def _validar_precio(valor):
        """Valida que el precio del boleto sea un numero finito >= 0."""
        precio = float(valor)
        if not math.isfinite(precio) or precio < 0:
            raise ValueError("El precio del boleto debe ser un número finito mayor o igual a cero.")
        return round(precio, 2)

    @staticmethod
    def _validar_asientos(valor):
        """Valida que la cantidad de asientos sea un entero >= 0."""
        if isinstance(valor, (bool, float)):
            raise ValueError("Los asientos disponibles deben ser un número entero mayor o igual a cero.")
        asientos = int(valor)
        if asientos < 0:
            raise ValueError("Los asientos disponibles no pueden ser negativos.")
        return asientos

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
        # Valida antes de actualizar para impedir valores negativos o no enteros
        self.__asientos_disponibles = self._validar_asientos(nuevos_asientos)

    # --- MÉTODO PARA MOSTRAR LA INFORMACIÓN ---
    def mostrar_cartelera_info(self):
        return (
            f"ID: {self.__id_pelicula} | Película: {self.__titulo} "
            f"| Horario: {self.__horario} | Sala: {self.__sala} "
            f"| Precio: ${self.__precio_boleto:.2f} | Asientos Libres: {self.__asientos_disponibles}"
        )