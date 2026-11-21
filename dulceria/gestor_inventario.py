# Archivo: dulceria/gestor_inventario.py
# Gestiona la carga/guardado de datos/stock.csv, claves hash unicas y busquedas (Rol 2 / Rol 4).

import csv
import os
from config import RUTA_STOCK
from dulceria.snack import Snack
from nucleo.consola import guardar_csv_seguro


def generar_id_hash(nombre_producto):
    """
    Genera una clave hash unica y constante a partir del nombre del producto.
    Ejemplo: 'Cotufas Grandes' -> '183'
    """
    nombre_limpio = nombre_producto.strip().lower()
    valor_hash = 0
    for indice, caracter in enumerate(nombre_limpio):
        valor_hash += (indice + 1) * ord(caracter)
    codigo = valor_hash % 1000
    return f"{codigo:03d}"


def generar_id_unico(nombre_producto, diccionario_snacks):
    """
    Genera un ID hash evitando colisiones destructivas si otro producto distinto
    ya ocupa el mismo codigo modular (sondeo lineal dentro del rango 000-999).
    """
    nombre_limpio = nombre_producto.strip().lower()
    valor_hash = 0
    for indice, caracter in enumerate(nombre_limpio):
        valor_hash += (indice + 1) * ord(caracter)
    codigo_base = valor_hash % 1000

    for intento in range(1000):
        candidato = f"{(codigo_base + intento) % 1000:03d}"
        if candidato not in diccionario_snacks:
            return candidato
        if diccionario_snacks[candidato].get_nombre().strip().lower() == nombre_limpio:
            return candidato

    raise RuntimeError("No quedan códigos SNK disponibles en el rango 000-999.")


def cargar_snacks_desde_csv(ruta_archivo=None):
    """
    Lee stock.csv y retorna un diccionario donde la clave es el ID hash
    y el valor es el objeto Snack.
    """
    ruta_objetivo = ruta_archivo if ruta_archivo is not None else RUTA_STOCK
    diccionario_snacks = {}

    if not os.path.exists(ruta_objetivo):
        print("Aviso: No se encontró el archivo " + ruta_objetivo + ". Se creará uno con datos base.")
        crear_csv_por_defecto(ruta_objetivo)

    try:
        with open(ruta_objetivo, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for num_linea, fila in enumerate(lector, start=2):
                try:
                    nombre = fila["nombre"].strip()
                    if not nombre:
                        continue
                    id_csv = str(fila.get("id_hash", "")).strip().upper()

                    if id_csv and id_csv not in diccionario_snacks:
                        id_asignado = id_csv
                    else:
                        id_asignado = generar_id_unico(nombre, diccionario_snacks)

                    nuevo_snack = Snack(
                        id_snack=id_asignado,
                        nombre=nombre,
                        descripcion=fila["descripcion"].strip(),
                        precio=float(fila["precio"]),
                        cantidad=int(fila["cantidad"])
                    )
                    diccionario_snacks[id_asignado] = nuevo_snack
                except (KeyError, ValueError, TypeError) as err:
                    print(f"Aviso: Fila {num_linea} omitida en {ruta_objetivo} por formato inválido ({err}).")
    except (OSError, csv.Error) as err:
        print(f"Error al leer el inventario '{ruta_objetivo}': {err}")

    return diccionario_snacks


def guardar_snacks_en_csv(diccionario_snacks, ruta_archivo=None):
    """Guarda el estado actual del diccionario de objetos Snack en stock.csv de forma segura ante bloqueos de archivo."""
    ruta_objetivo = ruta_archivo if ruta_archivo is not None else RUTA_STOCK
    campos = ["id_hash", "nombre", "descripcion", "precio", "cantidad"]
    filas = [
        {
            "id_hash": objeto_snack.get_id_snack(),
            "nombre": objeto_snack.get_nombre(),
            "descripcion": objeto_snack.get_descripcion(),
            "precio": "{:.2f}".format(objeto_snack.get_precio()),
            "cantidad": objeto_snack.get_cantidad()
        }
        for objeto_snack in diccionario_snacks.values()
    ]
    return guardar_csv_seguro(ruta_objetivo, campos, filas)


def crear_csv_por_defecto(ruta_archivo=None):
    """Crea la base de datos inicial en caso de que stock.csv no exista."""
    ruta_objetivo = ruta_archivo if ruta_archivo is not None else RUTA_STOCK
    datos_iniciales = [
        ("Cotufas Grandes", "Cotufas saladas recien hechas (150g)", 4.50, 30),
        ("Refresco Mediano", "Bebida gaseosa de dispensador (500ml)", 2.50, 45),
        ("Perro Caliente", "Pan suave con salchicha y salsas", 3.75, 20),
        ("Nachos con Queso", "Tortillas de maiz crujientes con queso fundido", 5.00, 15),
        ("Chocolate de Leche", "Barra de chocolate nacional (50g)", 1.80, 50),
        ("Agua Mineral", "Botella de agua natural sin gas (600ml)", 1.20, 40)
    ]
    diccionario_temporal = {}
    for nombre, desc, precio, cant in datos_iniciales:
        id_hash = generar_id_unico(nombre, diccionario_temporal)
        diccionario_temporal[id_hash] = Snack(id_hash, nombre, desc, precio, cant)
    guardar_snacks_en_csv(diccionario_temporal, ruta_objetivo)


def mostrar_catalogo_snacks(diccionario_snacks):
    """Muestra todos los snacks disponibles (con stock > 0) al cliente."""
    print("\n" + "=" * 98)
    print("                     CATÁLOGO DE SNACKS DISPONIBLES")
    print("=" * 98)

    if not diccionario_snacks:
        print("No hay snacks registrados en el sistema en este momento.")
        print("=" * 98)
        return

    snacks_en_stock = 0
    for snack in diccionario_snacks.values():
        if snack.get_cantidad() > 0:
            print(snack.mostrar_info())
            snacks_en_stock += 1

    if snacks_en_stock == 0:
        print("Todos los productos se encuentran agotados temporalmente.")
    print("=" * 98)


def buscar_snack(diccionario_snacks):
    """
    Permite al cliente buscar un snack disponible por ID directo, nombre exacto
    (clave hash) o coincidencia parcial. Oculta los productos agotados (stock == 0).
    """
    print("\n--- BUSCADOR DE SNACKS ---")
    criterio = input("Ingrese el nombre o ID del snack que desea buscar: ").strip()

    if not criterio:
        print("Debe ingresar un texto válido para realizar la búsqueda.")
        return

    # 1. Comprueba primero coincidencia directa por ID (insensible a mayusculas/minusculas)
    criterio_upper = criterio.upper()
    if criterio_upper in diccionario_snacks:
        snack_encontrado = diccionario_snacks[criterio_upper]
        if snack_encontrado.get_cantidad() > 0:
            print("\n[Coincidencia exacta por ID (" + criterio_upper + ")]:")
            print(snack_encontrado.mostrar_info())
        else:
            print("\nNo se encontró ningún snack disponible relacionado con: '" + criterio + "'.")
        return

    # 2. Busqueda O(1) generando clave hash si coincide tambien el nombre del producto
    posible_hash = generar_id_hash(criterio)
    if posible_hash in diccionario_snacks:
        snack_encontrado = diccionario_snacks[posible_hash]
        if snack_encontrado.get_nombre().strip().lower() == criterio.lower():
            if snack_encontrado.get_cantidad() > 0:
                print("\n[Coincidencia exacta por clave Hash (" + posible_hash + ")]:")
                print(snack_encontrado.mostrar_info())
            else:
                print("\nNo se encontró ningún snack disponible relacionado con: '" + criterio + "'.")
            return

    # 3. Busqueda por coincidencia parcial en nombre o descripcion (solo con stock > 0)
    resultados = []
    criterio_lower = criterio.lower()

    for id_clave, snack in diccionario_snacks.items():
        if snack.get_cantidad() > 0 and (
            criterio_lower in snack.get_nombre().lower() or
            criterio_lower in snack.get_descripcion().lower() or
            criterio_lower == id_clave.lower()
        ):
            resultados.append(snack)

    if resultados:
        print("\nSe encontraron " + str(len(resultados)) + " coincidencia(s):")
        print("-" * 78)
        for item in resultados:
            print(item.mostrar_info())
        print("-" * 78)
    else:
        print("\nNo se encontró ningún snack disponible relacionado con: '" + criterio + "'.")
