# Archivo: boleteria/pelicula.py
# Entidad Pelicula unificada con clasificacion, formato y capacidad de sala.

from datetime import datetime, timedelta
import hashlib
import math


class Pelicula:
    """
    Representa una pelicula en cartelera con sus datos de ficha tecnica,
    horario, sala, formato, clasificacion y capacidad fisica de asientos disponibles.
    Ofrece tanto @property como getters/setters explicitos para mantener
    consistencia OOP en todo el proyecto.
    """

    def __init__(
        self,
        nombre,
        descripcion,
        duracion,
        costo,
        fecha_de_estreno,
        horario="Por definir",
        sala="Sala 1",
        disponibilidad=30,
        clasificacion="A",
        formato="2D",
        id_pelicula=None
    ):
        nombre_limpio = str(nombre).strip()
        if not nombre_limpio:
            raise ValueError("El nombre de la película no puede estar vacío.")
        self._nombre = nombre_limpio
        self._descripcion = str(descripcion).strip()
        self._duracion = self._validar_duracion(duracion)
        self._costo = self._validar_costo(costo)
        self._fecha_de_estreno = str(fecha_de_estreno).strip()
        self._horario = str(horario).strip() or "Por definir"
        self._sala = str(sala).strip() or "Sala 1"
        self._disponibilidad = self._validar_disponibilidad(disponibilidad)
        self._clasificacion = str(clasificacion).strip().upper() or "A"
        self._formato = str(formato).strip().upper() or "2D"

        if id_pelicula is None:
            self._id = self.generar_id_hash(self._nombre, limite=8)
        else:
            self._id = str(id_pelicula).strip()

    @staticmethod
    def _validar_duracion(valor):
        """Valida que la duracion en minutos sea un entero positivo."""
        if isinstance(valor, (bool, float)):
            raise ValueError("La duración debe ser un número entero positivo en minutos.")
        duracion = int(valor)
        if duracion <= 0:
            raise ValueError("La duración debe ser mayor a cero.")
        return duracion

    @staticmethod
    def _validar_costo(valor):
        """Valida que el costo del boleto sea un numero finito mayor o igual a cero."""
        costo = float(valor)
        if not math.isfinite(costo) or costo < 0:
            raise ValueError("El costo del boleto debe ser un número finito mayor o igual a cero.")
        return round(costo, 2)

    @staticmethod
    def _validar_disponibilidad(valor):
        """Valida que los asientos disponibles sean un numero entero mayor o igual a cero."""
        if isinstance(valor, (bool, float)):
            raise ValueError("La disponibilidad debe ser un número entero mayor o igual a cero.")
        entero = int(valor)
        if entero < 0:
            raise ValueError("La disponibilidad no puede ser negativa.")
        return entero

    @staticmethod
    def generar_id_hash(nombre, limite=8):
        """Genera un identificador hash deterministico a partir del nombre de la pelicula."""
        hash_obj = hashlib.sha256(str(nombre).strip().lower().encode("utf-8"))
        return hash_obj.hexdigest()[:limite]

    # --- Propiedades Pythonicas ---
    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        texto = str(valor).strip()
        if not texto:
            raise ValueError("El nombre de la película no puede estar vacío.")
        self._nombre = texto

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = str(valor).strip()

    @property
    def duracion(self):
        return self._duracion

    @duracion.setter
    def duracion(self, valor):
        self._duracion = self._validar_duracion(valor)

    @property
    def costo(self):
        return self._costo

    @costo.setter
    def costo(self, valor):
        self._costo = self._validar_costo(valor)

    @property
    def fecha_de_estreno(self):
        return self._fecha_de_estreno

    @fecha_de_estreno.setter
    def fecha_de_estreno(self, valor):
        self._fecha_de_estreno = str(valor).strip()

    @property
    def horario(self):
        return self._horario

    @horario.setter
    def horario(self, valor):
        self._horario = str(valor).strip() or "Por definir"

    @property
    def sala(self):
        return self._sala

    @sala.setter
    def sala(self, valor):
        self._sala = str(valor).strip() or "Sala 1"

    @property
    def disponibilidad(self):
        return self._disponibilidad

    @disponibilidad.setter
    def disponibilidad(self, valor):
        self._disponibilidad = self._validar_disponibilidad(valor)

    @property
    def clasificacion(self):
        return self._clasificacion

    @clasificacion.setter
    def clasificacion(self, valor):
        self._clasificacion = str(valor).strip().upper() or "A"

    @property
    def formato(self):
        return self._formato

    @formato.setter
    def formato(self, valor):
        self._formato = str(valor).strip().upper() or "2D"

    @property
    def hora_fin(self):
        """Calcula la hora aproximada de finalizacion sumando la duracion al horario de inicio."""
        if not self._horario or self._horario.strip().lower() in ("por definir", "sin asignar", "n/d", "-"):
            return "Por definir"
        try:
            horario_limpio = self._horario.strip()
            formatos = ("%I:%M %p", "%H:%M", "%I:%M%p", "%I %p")
            for fmt in formatos:
                try:
                    inicio = datetime.strptime(horario_limpio, fmt)
                    fin = inicio + timedelta(minutes=self._duracion)
                    return fin.strftime("%I:%M %p")
                except ValueError:
                    continue
        except Exception:
            pass
        return f"+{self._duracion}m"

    # --- Getters y Setters explicitos (estandar OOP del documento PDF) ---
    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_descripcion(self):
        return self._descripcion

    def get_duracion(self):
        return self._duracion

    def get_costo(self):
        return self._costo

    def get_fecha_de_estreno(self):
        return self._fecha_de_estreno

    def get_horario(self):
        return self._horario

    def get_sala(self):
        return self._sala

    def get_disponibilidad(self):
        return self._disponibilidad

    def get_clasificacion(self):
        return self._clasificacion

    def get_formato(self):
        return self._formato

    def get_hora_fin(self):
        return self.hora_fin

    def set_nombre(self, nuevo_nombre):
        self.nombre = nuevo_nombre

    def set_descripcion(self, nueva_descripcion):
        self.descripcion = nueva_descripcion

    def set_duracion(self, nueva_duracion):
        self.duracion = nueva_duracion

    def set_costo(self, nuevo_costo):
        self.costo = nuevo_costo

    def set_horario(self, nuevo_horario):
        self.horario = nuevo_horario

    def set_sala(self, nueva_sala):
        self.sala = nueva_sala

    def set_disponibilidad(self, nuevos_asientos):
        self.disponibilidad = nuevos_asientos

    def set_clasificacion(self, nueva_clasificacion):
        self.clasificacion = nueva_clasificacion

    def set_formato(self, nuevo_formato):
        self.formato = nuevo_formato

    def __str__(self):
        estado = f"Disponible ({self._disponibilidad} asientos)" if self._disponibilidad > 0 else "Agotada / No disponible"
        return (
            f"Película: {self._nombre} [{self._formato}] (ID: {self._id}) | Clasificación: {self._clasificacion}\n"
            f"Descripción: {self._descripcion}\n"
            f"Duración: {self._duracion} min | Horario: {self._horario} (Fin est.: {self.hora_fin}) | {self._sala}\n"
            f"Costo: ${self._costo:.2f} | Estreno: {self._fecha_de_estreno} | Estado: [{estado}]"
        )
