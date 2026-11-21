# Archivo: boleteria/gestor_cartelera.py
# Gestor unificado de cartelera y persistencia en datos/cartelera.csv con soporte para formato y clasificacion.

import csv
import math
import os
from boleteria.pelicula import Pelicula
from config import CAPACIDAD_SALA_DEFECTO, RUTA_CARTELERA
from finanzas.pagos import registrar_en_reporte


class GestorCartelera:
    """Administra la carga, consulta, actualizacion y guardado de funciones en cartelera.csv."""

    def __init__(self, ruta_csv=None):
        self.ruta_csv = ruta_csv if ruta_csv is not None else RUTA_CARTELERA
        self.catalogo = {}
        self.cargar_desde_csv()

    @staticmethod
    def _parsear_disponibilidad(valor_crudo):
        """Convierte disponibilidad a entero >= 0 con retrocompatibilidad booleana."""
        texto = str(valor_crudo).strip().lower()
        if texto in ("false", "falso", "no", "off", ""):
            return 0
        if texto in ("true", "verdadero", "si", "sí", "on"):
            return CAPACIDAD_SALA_DEFECTO
        return max(0, int(texto))

    def cargar_desde_csv(self):
        """Carga las peliculas desde cartelera.csv omitiendo filas corruptas de forma segura."""
        self.catalogo = {}
        if not os.path.exists(self.ruta_csv):
            return

        try:
            with open(self.ruta_csv, mode="r", encoding="utf-8") as archivo:
                lector = csv.DictReader(archivo)
                for num_linea, fila in enumerate(lector, start=2):
                    try:
                        p_id = str(fila["id"]).strip()
                        if not p_id:
                            continue

                        # Soporte flexible de encabezados si proviene de CSV previo
                        nombre = str(fila.get("nombre") or fila.get("titulo") or "").strip()
                        descripcion = str(fila.get("descripcion") or "Sin descripción").strip()
                        duracion = int(fila.get("duracion", 120))
                        costo = float(fila.get("costo") or fila.get("precio"))
                        fecha_estreno = str(fila.get("fecha_de_estreno") or "N/D").strip()
                        horario = str(fila.get("horario") or "Por definir").strip()
                        sala = str(fila.get("sala") or "Sala 1").strip()
                        disp_raw = fila.get("disponibilidad", fila.get("asientos", CAPACIDAD_SALA_DEFECTO))
                        disponibilidad = self._parsear_disponibilidad(disp_raw)

                        clasificacion = str(fila.get("clasificacion") or "A").strip().upper()
                        formato = str(fila.get("formato") or "2D").strip().upper()

                        if not nombre or not math.isfinite(costo) or costo < 0 or duracion <= 0:
                            raise ValueError("Datos inválidos en el registro de película.")

                        self.catalogo[p_id] = Pelicula(
                            nombre=nombre,
                            descripcion=descripcion,
                            duracion=duracion,
                            costo=costo,
                            fecha_de_estreno=fecha_estreno,
                            horario=horario,
                            sala=sala,
                            disponibilidad=disponibilidad,
                            clasificacion=clasificacion,
                            formato=formato,
                            id_pelicula=p_id
                        )
                    except (KeyError, ValueError, TypeError) as err:
                        print(f"Aviso: Fila {num_linea} omitida en {self.ruta_csv} ({err}).")
        except (OSError, csv.Error) as err:
            print(f"Error al leer el archivo de cartelera '{self.ruta_csv}': {err}")

    def guardar_catalogo_en_csv(self):
        """Reescribe cartelera.csv con todos los campos unificados y formato limpio."""
        carpeta = os.path.dirname(os.path.abspath(self.ruta_csv))
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)

        campos = [
            "id", "nombre", "descripcion", "duracion",
            "costo", "fecha_de_estreno", "horario", "sala",
            "disponibilidad", "clasificacion", "formato"
        ]
        with open(self.ruta_csv, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            for pelicula in self.catalogo.values():
                escritor.writerow({
                    "id": pelicula.id,
                    "nombre": pelicula.nombre,
                    "descripcion": pelicula.descripcion,
                    "duracion": pelicula.duracion,
                    "costo": f"{pelicula.costo:.2f}",
                    "fecha_de_estreno": pelicula.fecha_de_estreno,
                    "horario": pelicula.horario,
                    "sala": pelicula.sala,
                    "disponibilidad": pelicula.disponibilidad,
                    "clasificacion": pelicula.clasificacion,
                    "formato": pelicula.formato
                })

    def agregar_y_guardar_pelicula(
        self,
        nombre,
        descripcion,
        duracion,
        costo,
        fecha_de_estreno,
        horario="Por definir",
        sala="Sin asignar",
        disponibilidad=0,
        clasificacion="A",
        formato="2D",
        id_personalizado=None
    ):
        """Crea una nueva Pelicula validada y la persiste de inmediato en cartelera.csv."""
        nueva_pelicula = Pelicula(
            nombre=nombre,
            descripcion=descripcion,
            duracion=duracion,
            costo=costo,
            fecha_de_estreno=fecha_de_estreno,
            horario=horario,
            sala=sala,
            disponibilidad=disponibilidad,
            clasificacion=clasificacion,
            formato=formato,
            id_pelicula=id_personalizado
        )

        if nueva_pelicula.id in self.catalogo:
            print("Aviso: Ya existe una película con este mismo identificador.")
            return None

        self.catalogo[nueva_pelicula.id] = nueva_pelicula
        self.guardar_catalogo_en_csv()
        return nueva_pelicula

    def eliminar_pelicula(self, pelicula_id):
        """Elimina una película de la cartelera y persiste los cambios."""
        if pelicula_id in self.catalogo:
            eliminada = self.catalogo.pop(pelicula_id)
            self.guardar_catalogo_en_csv()
            return eliminada
        return None

    def cambiar_horario(self, pelicula_id, nuevo_horario):
        """Actualiza el horario de una película y guarda en disco."""
        pelicula = self.buscar_por_id(pelicula_id)
        if pelicula:
            pelicula.set_horario(nuevo_horario)
            self.guardar_catalogo_en_csv()
            return True
        return False

    def buscar_por_id(self, pelicula_id):
        return self.catalogo.get(pelicula_id, None)

    def buscar_por_nombre(self, termino):
        termino = termino.lower()
        return [p for p in self.catalogo.values() if termino in p.nombre.lower()]

    def listar_todas(self):
        return list(self.catalogo.values())

    def listar_peliculas_por_nombres(self):
        """Devuelve una lista de tuplas con el nombre, horario/sala y disponibilidad."""
        resultado = []
        for p in self.catalogo.values():
            estado = f"Disponible ({p.disponibilidad} asientos)" if p.disponibilidad > 0 else "Agotada"
            resultado.append((p.nombre, f"{p.horario} - {p.sala} [{p.formato}]", estado))
        return resultado

    def registrar_venta(self, pelicula, cantidad=1):
        """Registra la venta de boletos en reporte_ventas.csv mediante finanzas/pagos.py."""
        ruta_reporte = os.path.join(os.path.dirname(os.path.abspath(self.ruta_csv)), "reporte_ventas.csv")
        total = round(pelicula.costo * int(cantidad), 2)
        registrar_en_reporte("Boleto", f"{pelicula.nombre} ({pelicula.formato})", int(cantidad), total, ruta_ventas=ruta_reporte)


# Alias mantenido por compatibilidad con referencias previas a GestorCine
GestorCine = GestorCartelera
