# Archivo: gestor_snacks.py
# Gestiona la carga del archivo CSV, el diccionario de objetos Snack y la busqueda (Rol 2)

import csv
import os
from modelo_snack import Snack


def generar_id_hash(nombre_producto):
    """
    Genera una clave hash unica y constante a partir del nombre del producto.
    Ejemplo: 'Cotufas Grandes' -> 'SNK-743'
    """
    nombre_limpio = nombre_producto.strip().lower()
    valor_hash = 0
    for indice, caracter in enumerate(nombre_limpio):
        valor_hash += (indice + 1) * ord(caracter)
    codigo = valor_hash % 1000
    return "SNK-" + "{:03d}".format(codigo)


def cargar_snacks_desde_csv(ruta_archivo="stock.csv"):
    """
    Lee el archivo stock.csv al iniciar el programa y retorna un diccionario
    donde la clave es el ID hash y el valor es el objeto de tipo Snack.
    """
    diccionario_snacks = {}

    if not os.path.exists(ruta_archivo):
        print("Aviso: No se encontro el archivo " + ruta_archivo + ". Se creara uno con datos base.")
        crear_csv_por_defecto(ruta_archivo)

    with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            # Generamos o validamos el ID hash desde el nombre del producto
            id_generado = generar_id_hash(fila["nombre"])
            nuevo_snack = Snack(
                id_snack=id_generado,
                nombre=fila["nombre"],
                descripcion=fila["descripcion"],
                precio=float(fila["precio"]),
                cantidad=int(fila["cantidad"])
            )
            diccionario_snacks[id_generado] = nuevo_snack

    return diccionario_snacks


def guardar_snacks_en_csv(diccionario_snacks, ruta_archivo="stock.csv"):
    """
    Guarda el estado actual del diccionario de objetos Snack en el archivo stock.csv.
    Util para sincronizar los IDs hash y para que los Roles 3 y 4 actualicen el stock.
    """
    campos = ["id_hash", "nombre", "descripcion", "precio", "cantidad"]
    with open(ruta_archivo, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for id_clave, objeto_snack in diccionario_snacks.items():
            escritor.writerow({
                "id_hash": objeto_snack.get_id_snack(),
                "nombre": objeto_snack.get_nombre(),
                "descripcion": objeto_snack.get_descripcion(),
                "precio": "{:.2f}".format(objeto_snack.get_precio()),
                "cantidad": objeto_snack.get_cantidad()
            })


def crear_csv_por_defecto(ruta_archivo="stock.csv"):
    """Crea la base de datos inicial en caso de que el archivo no exista."""
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
        id_hash = generar_id_hash(nombre)
        diccionario_temporal[id_hash] = Snack(id_hash, nombre, desc, precio, cant)
    guardar_snacks_en_csv(diccionario_temporal, ruta_archivo)


# =========================================================================
# FUNCIONES PRINCIPALES DEL ROL 2: VER Y BUSCAR SNACKS (SOLO LECTURA)
# =========================================================================

def mostrar_catalogo_snacks(diccionario_snacks):
    """Muestra todos los snacks disponibles en el diccionario."""
    print("\n" + "=" * 78)
    print("                     CATALOGO DE SNACKS DISPONIBLES")
    print("=" * 78)

    if not diccionario_snacks:
        print("No hay snacks registrados en el sistema en este momento.")
        return

    snacks_en_stock = 0
    for id_snack, snack in diccionario_snacks.items():
        if snack.get_cantidad() > 0:
            print(snack.mostrar_info())
            snacks_en_stock += 1

    if snacks_en_stock == 0:
        print("Todos los productos se encuentran agotados temporalmente.")
    print("=" * 78)


def buscar_snack(diccionario_snacks):
    """
    Permite al usuario buscar un snack por su nombre exacto (usando la clave hash)
    o por coincidencia parcial de texto o ID.
    """
    print("\n--- BUSCADOR DE SNACKS ---")
    criterio = input("Ingrese el nombre o ID del snack que desea buscar: ").strip()

    if not criterio:
        print("Debe ingresar un texto valido para realizar la busqueda.")
        return

    # 1. Intento de busqueda directa O(1) generando la clave hash desde el nombre
    posible_hash = generar_id_hash(criterio)
    if posible_hash in diccionario_snacks:
        snack_encontrado = diccionario_snacks[posible_hash]
        print("\n[Coincidencia exacta por clave Hash (" + posible_hash + ")]:")
        print(snack_encontrado.mostrar_info())
        return

    # 2. Busqueda por ID directo (ej. SNK-743) o coincidencia parcial en el nombre
    resultados = []
    criterio_lower = criterio.lower()

    for id_clave, snack in diccionario_snacks.items():
        if (criterio_lower in snack.get_nombre().lower() or
                criterio_lower in snack.get_descripcion().lower() or
                criterio_lower == id_clave.lower()):
            resultados.append(snack)

    if len(resultados) > 0:
        print("\nSe encontraron " + str(len(resultados)) + " coincidencia(s):")
        print("-" * 78)
        for item in resultados:
            print(item.mostrar_info())
        print("-" * 78)
    else:
        print("\nNo se encontro ningun snack relacionado con: '" + criterio + "'.")
