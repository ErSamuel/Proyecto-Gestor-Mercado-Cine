# Archivo: modelo_snack.py
# Define la clase Snack con sus respectivos getters y setters

class Snack:
    def __init__(self, id_snack, nombre, descripcion, precio, cantidad):
        self.__id_snack = str(id_snack)
        self.__nombre = str(nombre)
        self.__descripcion = str(descripcion)
        self.__precio = float(precio)
        self.__cantidad = int(cantidad)

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
        if float(nuevo_precio) >= 0:
            self.__precio = float(nuevo_precio)

    def set_cantidad(self, nueva_cantidad):
        if int(nueva_cantidad) >= 0:
            self.__cantidad = int(nueva_cantidad)

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
