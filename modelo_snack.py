# Archivo: modelo_snack.py
# Define la clase Snack con sus respectivos getters y setters

import math


class Snack:
    def __init__(self, id_snack, nombre, descripcion, precio, cantidad):
        self.__id_snack = str(id_snack)
        self.__nombre = str(nombre)
        self.__descripcion = str(descripcion)
        # Valida precio y cantidad al instanciar para evitar NaN, Inf o negativos
        self.__precio = self._validar_precio(precio)
        self.__cantidad = self._validar_cantidad(cantidad)

    @staticmethod
    def _validar_precio(valor):
        """Valida que el precio sea un numero finito mayor o igual a cero."""
        precio_float = float(valor)
        if not math.isfinite(precio_float) or precio_float < 0:
            raise ValueError("El precio debe ser un número finito mayor o igual a cero.")
        return round(precio_float, 2)

    @staticmethod
    def _validar_cantidad(valor):
        """Valida que la cantidad sea un numero entero mayor o igual a cero."""
        if isinstance(valor, (bool, float)):
            raise ValueError("La cantidad debe ser un número entero mayor o igual a cero.")
        cant_int = int(valor)
        if cant_int < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        return cant_int

    # --- GETTERS (Lectura para el Rol Usuario y consultas) ---
    def get_id_snack(self):
        return self.__id_snack

    def get_nombre(self):
        return self.__nombre

    def get_descripcion(self):
        return self.__descripcion

    def get_precio(self):
        return self.__precio

    def get_cantidad(self):
        return self.__cantidad

    # --- SETTERS (Escritura para el Rol Administrador y ventas) ---
    def set_nombre(self, nuevo_nombre):
        self.__nombre = str(nuevo_nombre)

    def set_descripcion(self, nueva_descripcion):
        self.__descripcion = str(nueva_descripcion)

    def set_precio(self, nuevo_precio):
        self.__precio = self._validar_precio(nuevo_precio)

    def set_cantidad(self, nueva_cantidad):
        self.__cantidad = self._validar_cantidad(nueva_cantidad)

    # Metodo para formatear la informacion del snack en pantalla
    def mostrar_info(self):
        estado = "Disponible (" + str(self.__cantidad) + " uds)" if self.__cantidad > 0 else "AGOTADO"
        return (
            "ID: " + self.__id_snack +
            " | Producto: " + self.__nombre +
            " | Desc: " + self.__descripcion +
            " | Precio: $" + "{:.2f}".format(self.__precio) +
            " | Stock: " + estado
        )
