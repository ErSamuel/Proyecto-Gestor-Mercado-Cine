import csv
import math
import os
from clase_pelicula import Pelicula
from pagos import registrar_en_reporte

# Ruta base del modulo para independizar peliculas.csv del directorio de trabajo (CWD)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_PELICULAS_DEFECTO = os.path.join(BASE_DIR, "peliculas.csv")
# Capacidad por defecto al migrar registros booleanos antiguos ('True'/'Si') a entero
CAPACIDAD_SALA_DEFECTO = 30


class GestorCine:
    def __init__(self, ruta_csv=None):
        # Si no se indica una ruta explicita, usa la ruta absoluta junto al modulo
        self.ruta_csv = ruta_csv if ruta_csv is not None else RUTA_PELICULAS_DEFECTO
        self.catalogo = {}
        self.cargar_desde_csv()

    @staticmethod
    def _parsear_disponibilidad(valor_crudo):
        """Convierte la disponibilidad a entero >= 0 con soporte retrocompatible para booleanos."""
        texto = str(valor_crudo).strip().lower()
        # Soporte retrocompatible por si el CSV aun tuviera valores booleanos heredados
        if texto in ('false', 'falso', 'no', 'off', ''):
            return 0
        if texto in ('true', 'verdadero', 'si', 'sí', 'on'):
            return CAPACIDAD_SALA_DEFECTO
        # Valor entero normal: no permite asientos negativos
        entero = int(texto)
        return max(0, entero)

    def cargar_desde_csv(self):
        # Reinicia el catalogo antes de cargar para evitar datos residuales en recargas
        self.catalogo = {}
        if not os.path.exists(self.ruta_csv):
            return

        try:
            with open(self.ruta_csv, mode='r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                for num_linea, fila in enumerate(lector, start=2):
                    try:
                        p_id = str(fila['id']).strip()
                        if not p_id:
                            continue
                        disponibilidad = self._parsear_disponibilidad(fila.get('disponibilidad', '30'))
                        costo = float(fila['costo'])
                        duracion = int(fila['duracion'])
                        if not math.isfinite(costo) or costo < 0 or duracion <= 0:
                            raise ValueError("Valores numericos fuera de rango.")

                        self.catalogo[p_id] = Pelicula(
                            nombre=fila['nombre'].strip(),
                            descripcion=fila['descripcion'].strip(),
                            duracion=duracion,
                            costo=costo,
                            fecha_de_estreno=fila['fecha_de_estreno'].strip(),
                            disponibilidad=disponibilidad,
                            id_pelicula=p_id
                        )
                    except (KeyError, ValueError, TypeError) as err:
                        # Omite unicamente la fila corrupta sin detener el arranque del sistema
                        print(f"Aviso: Fila {num_linea} omitida en {self.ruta_csv} por formato inválido ({err}).")
        except (OSError, csv.Error) as err:
            print(f"Error al leer el archivo de cartelera '{self.ruta_csv}': {err}")

    def guardar_catalogo_en_csv(self):
        """Guarda todo el catalogo actual en el CSV garantizando formato limpio y salto de linea final."""
        campos = ['id', 'nombre', 'descripcion', 'duracion', 'costo', 'fecha_de_estreno', 'disponibilidad']
        with open(self.ruta_csv, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            for pelicula in self.catalogo.values():
                escritor.writerow({
                    'id': pelicula.id,
                    'nombre': pelicula.nombre,
                    'descripcion': pelicula.descripcion,
                    'duracion': pelicula.duracion,
                    'costo': f"{pelicula.costo:.2f}",
                    'fecha_de_estreno': pelicula.fecha_de_estreno,
                    'disponibilidad': pelicula.disponibilidad
                })

    def agregar_y_guardar_pelicula(self, nombre, descripcion, duracion, costo, fecha_de_estreno, disponibilidad=CAPACIDAD_SALA_DEFECTO):
        # Valida parametros antes de instanciar y guardar la nueva pelicula
        if isinstance(disponibilidad, (bool, float)) or int(disponibilidad) < 0:
            raise ValueError("La disponibilidad debe ser un entero mayor o igual a cero.")
        costo_val = float(costo)
        if not math.isfinite(costo_val) or costo_val < 0:
            raise ValueError("El costo debe ser un número finito mayor o igual a cero.")

        nueva_pelicula = Pelicula(
            nombre=nombre,
            descripcion=descripcion,
            duracion=int(duracion),
            costo=costo_val,
            fecha_de_estreno=fecha_de_estreno,
            disponibilidad=int(disponibilidad)
        )

        if nueva_pelicula.id in self.catalogo:
            print("Aviso: Ya existe una película con este mismo hash identificador.")
            return None

        self.catalogo[nueva_pelicula.id] = nueva_pelicula
        # Reescribe el CSV completo para evitar corrupcion si el archivo carecia de salto de linea final
        self.guardar_catalogo_en_csv()

        print(f"¡Éxito! Película agregada con ID [{nueva_pelicula.id}] y guardada en el CSV.")
        return nueva_pelicula

    def buscar_por_id(self, pelicula_id):
        return self.catalogo.get(pelicula_id, None)

    def buscar_por_nombre(self, termino):
        termino = termino.lower()
        return [p for p in self.catalogo.values() if termino in p.nombre.lower()]

    def listar_todas(self):
        return list(self.catalogo.values())
    
    def listar_peliculas_por_nombres(self):
        """Devuelve una lista de tuplas con el nombre y el estado de cada película."""
        resultado = []
        for p in self.catalogo.values():
            estado = f"Disponible ({p.disponibilidad} asientos)" if p.disponibilidad > 0 else "Agotada"
            resultado.append((p.nombre, estado))
        return resultado

    def registrar_venta(self, pelicula, cantidad=1):
        """Registra una venta de boleto delegando en el formato unificado de pagos.py."""
        ruta_reporte = os.path.join(os.path.dirname(os.path.abspath(self.ruta_csv)), "reporte_ventas.csv")
        total = round(pelicula.costo * int(cantidad), 2)
        registrar_en_reporte("Boleto", pelicula.nombre, int(cantidad), total, ruta_ventas=ruta_reporte)