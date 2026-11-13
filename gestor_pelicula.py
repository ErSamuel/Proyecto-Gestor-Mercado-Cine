import csv
import os
from clase_pelicula import Pelicula

class GestorCine:
    def __init__(self, ruta_csv="peliculas.csv"):
        self.ruta_csv = ruta_csv
        self.catalogo = {}
        self.cargar_desde_csv()

    def cargar_desde_csv(self):
        if not os.path.exists(self.ruta_csv):
            return

        with open(self.ruta_csv, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                p_id = fila['id']
                
                # Leemos el valor del CSV, lo pasamos a minúsculas y quitamos espacios
                valor_disp = fila.get('disponibilidad', 'True').strip().lower()
                
                # Será False si el texto indica negación ('no', 'false', 'falso', '0'); de lo contrario será True
                disponibilidad = valor_disp not in ('false', 'falso', 'no', '0', 'off')
                
                self.catalogo[p_id] = Pelicula(
                    nombre=fila['nombre'],
                    descripcion=fila['descripcion'],
                    duracion=int(fila['duracion']),
                    costo=float(fila['costo']),
                    fecha_de_estreno=fila['fecha_de_estreno'],
                    disponibilidad=disponibilidad,
                    id_pelicula=p_id
                )

    def agregar_y_guardar_pelicula(self, nombre, descripcion, duracion, costo, fecha_de_estreno, disponibilidad=True):
        nueva_pelicula = Pelicula(
            nombre=nombre,
            descripcion=descripcion,
            duracion=duracion,
            costo=costo,
            fecha_de_estreno=fecha_de_estreno,
            disponibilidad=disponibilidad
        )

        if nueva_pelicula.id in self.catalogo:
            print("Aviso: Ya existe una película con este mismo hash identificador.")
            return

        self.catalogo[nueva_pelicula.id] = nueva_pelicula

        archivo_existe = os.path.exists(self.ruta_csv)
        with open(self.ruta_csv, mode='a', newline='', encoding='utf-8') as archivo:
            campos = ['id', 'nombre', 'descripcion', 'duracion', 'costo', 'fecha_de_estreno', 'disponibilidad']
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            
            if not archivo_existe:
                escritor.writeheader()
                
            escritor.writerow({
                'id': nueva_pelicula.id,
                'nombre': nueva_pelicula.nombre,
                'descripcion': nueva_pelicula.descripcion,
                'duracion': nueva_pelicula.duracion,
                'costo': nueva_pelicula.costo,
                'fecha_de_estreno': nueva_pelicula.fecha_de_estreno,
                'disponibilidad': nueva_pelicula.disponibilidad
            })

        print(f"¡Éxito! Película agregada con ID [{nueva_pelicula.id}] y guardada al final del CSV.")
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
            estado = "Disponible" if p.disponibilidad else "No disponible"
            resultado.append((p.nombre, estado))
        return resultado
    def registrar_venta(self, pelicula):
        """Registra una venta de boleto en el archivo reporte_ventas.csv."""
        ruta_ventas = "reporte_ventas.csv"
        archivo_existe = os.path.exists(ruta_ventas)

        with open(ruta_ventas, mode='a', newline='', encoding='utf-8') as archivo:
            campos = ['id_pelicula', 'nombre_pelicula', 'costo']
            escritor = csv.DictWriter(archivo, fieldnames=campos)

            # Si el archivo no existe, escribimos la cabecera primero
            if not archivo_existe:
                escritor.writeheader()

            escritor.writerow({
                'id_pelicula': pelicula.id,
                'nombre_pelicula': pelicula.nombre,
                'costo': pelicula.costo
            })