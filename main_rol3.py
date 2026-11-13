# Archivo: main_rol3.py
import os
import csv
from modelo_pelicula import Pelicula

# Colores ANSI
AZUL = "\033[94m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
RESET = "\033[0m"
NEGRITA = "\033[1m"

ARCHIVO_CSV = "cartelera.csv"

def inicializar_csv_si_no_existe():
    """Crea el archivo CSV con datos iniciales si no existe en la carpeta."""
    if not os.path.exists(ARCHIVO_CSV):
        peliculas_iniciales = [
            ["PEL-01", "Avatar: El Camino del Agua", "04:00 PM", "Sala 2", "5.00", "40"],
            ["PEL-02", "Spider-Man: Across the Spider-Verse", "07:00 PM", "Sala 1", "5.00", "25"],
            ["PEL-03", "Interestelar (Reestreno)", "09:30 PM", "Sala 3", "5.00", "15"]
        ]
        with open(ARCHIVO_CSV, mode="w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["id", "titulo", "horario", "sala", "precio", "asientos"]) # Cabecera
            writer.writerows(peliculas_iniciales)

def cargar_cartelera_desde_csv():
    """Lee las películas desde el archivo CSV y retorna un diccionario."""
    inicializar_csv_si_no_existe()
    cartelera = {}
    with open(ARCHIVO_CSV, mode="r", encoding="utf-8") as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            pel = Pelicula(
                fila["id"],
                fila["titulo"],
                fila["horario"],
                fila["sala"],
                float(fila["precio"]),
                int(fila["asientos"])
            )
            cartelera[fila["id"]] = pel
    return cartelera

def guardar_cartelera_en_csv(cartelera):
    """Guarda el estado actual de la cartelera (y sus asientos) de vuelta en el CSV."""
    with open(ARCHIVO_CSV, mode="w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["id", "titulo", "horario", "sala", "precio", "asientos"])
        for pelicula in cartelera.values():
            writer.writerow([
                pelicula.get_id(),
                pelicula.get_titulo(),
                pelicula.get_horario(),
                pelicula.get_sala(),
                pelicula.get_precio(),
                pelicula.get_asientos()
            ])

def ver_salas_y_cartelera(cartelera):
    """Muestra las salas y películas disponibles con formato de colores."""
    print("\n" + AZUL + "=" * 78 + RESET)
    print(f"{NEGRITA}{VERDE}                    CARTELERA Y SALAS DISPONIBLES{RESET}")
    print(AZUL + "=" * 78 + RESET)
    for id_pel, pelicula in cartelera.items():
        print(f"{AMARILLO}ID: {pelicula.get_id()}{RESET} | Película: {NEGRITA}{pelicula.get_titulo()}{RESET} | Horario: {pelicula.get_horario()} | Sala: {AZUL}{pelicula.get_sala()}{RESET} | Precio: {VERDE}${pelicula.get_precio():.2f}{RESET} | Asientos Libres: {pelicula.get_asientos()}")
    print(AZUL + "=" * 78 + RESET)

def procesar_pago(total_a_pagar):
    """Simula el proceso de pago con avisos coloridos."""
    print(f"\n{AMARILLO}--- PASARELA DE PAGO ---{RESET}")
    print(f"Total a cancelar: {VERDE}${total_a_pagar:.2f}{RESET}")
    print(f"{AZUL}[1]{RESET} Pago Móvil / Tarjeta de Débito")
    print(f"{AZUL}[2]{RESET} Efectivo en taquilla")
    
    metodo = input("Seleccione método de pago (1 o 2): ").strip()
    if metodo in ["1", "2"]:
        print(f"\n{VERDE}¡Pago procesado con éxito! Generando sus entradas...{RESET}")
        return True
    else:
        print(f"\n{ROJO}Método de pago inválido. Operación cancelada.{RESET}")
        return False

def comprar_entradas(cartelera):
    """Gestiona la compra de boletos, actualiza asientos y guarda en CSV."""
    ver_salas_y_cartelera(cartelera)
    
    id_elegido = input(f"\n{AMARILLO}Ingrese el ID de la película que desea ver (ej. PEL-01): {RESET}").strip().upper()
    
    if id_elegido not in cartelera:
        print(f"{ROJO}Error: El ID de la película no existe en la cartelera.{RESET}")
        return

    pelicula = cartelera[id_elegido]
    
    try:
        cantidad = int(input(f"¿Cuántas entradas desea para '{pelicula.get_titulo()}'?: "))
        if cantidad <= 0:
            print(f"{ROJO}La cantidad debe ser mayor a cero.{RESET}")
            return
        
        if cantidad > pelicula.get_asientos():
            print(f"{ROJO}Lo sentimos, solo quedan {pelicula.get_asientos()} asientos disponibles.{RESET}")
            return
            
    except ValueError:
        print(f"{ROJO}Por favor, ingrese un número válido.{RESET}")
        return

    total = cantidad * pelicula.get_precio()
    print(f"\n{NEGRITA}Resumen de compra:{RESET}")
    print(f"- Película: {pelicula.get_titulo()} ({pelicula.get_horario()} - {pelicula.get_sala()})")
    print(f"- Entradas: {cantidad}")
    print(f"- Total a pagar: {VERDE}${total:.2f}{RESET}")
    
    confirmar = input(f"{AMARILLO}¿Desea proceder al pago? (s/n): {RESET}").strip().lower()
    if confirmar == 's':
        if procesar_pago(total):
            # Actualizamos el stock de asientos y guardamos en el archivo CSV
            nuevo_stock = pelicula.get_asientos() - cantidad
            pelicula.set_asientos(nuevo_stock)
            guardar_cartelera_en_csv(cartelera)
            print(f"\n{VERDE}¡Disfrute su función! Sus asientos han sido reservados y guardados.{RESET}")
    else:
        print(f"{AMARILLO}Compra cancelada.{RESET}")

def iniciar_modulo_boleteria():
    """Función principal del Rol 3 cargando datos desde CSV."""
    cartelera = cargar_cartelera_desde_csv()
    
    while True:
        print(f"\n{AZUL}--- MENÚ DE BOLETERÍA ---{RESET}")
        print(f"{VERDE}[1]{RESET} Ver salas y cartelera")
        print(f"{AMARILLO}[2]{RESET} Comprar entradas")
        print(f"{ROJO}[3]{RESET} Volver al menú principal")
        
        opcion = input("Seleccione una opción (1-3): ").strip()
        
        if opcion == "1":
            ver_salas_y_cartelera(cartelera)
        elif opcion == "2":
            comprar_entradas(cartelera)
        elif opcion == "3":
            print(f"{AMARILLO}Regresando al menú principal...{RESET}")
            break
        else:
            print(f"{ROJO}Opción inválida. Por favor, intente de nuevo.{RESET}")