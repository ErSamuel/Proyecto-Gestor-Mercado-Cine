# Archivo: main_rol3.py
import os
import csv
from modelo_pelicula import Pelicula
# Reutiliza la pasarela de pago y el registro de ventas unificado de pagos.py
from pagos import procesar_pago, registrar_en_reporte

# Colores ANSI
AZUL = "\033[94m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
RESET = "\033[0m"
NEGRITA = "\033[1m"

# Ruta absoluta junto al modulo y limite maximo de boletos por transaccion
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_CSV = os.path.join(BASE_DIR, "cartelera.csv")
LIMITE_BOLETOS_POR_COMPRA = 10


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
            writer.writerow(["id", "titulo", "horario", "sala", "precio", "asientos"])  # Cabecera
            writer.writerows(peliculas_iniciales)


def cargar_cartelera_desde_csv():
    """Lee las películas desde el archivo CSV y retorna un diccionario."""
    inicializar_csv_si_no_existe()
    cartelera = {}
    try:
        with open(ARCHIVO_CSV, mode="r", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for num_linea, fila in enumerate(reader, start=2):
                try:
                    id_pel = str(fila["id"]).strip().upper()
                    if not id_pel:
                        continue
                    pel = Pelicula(
                        id_pel,
                        fila["titulo"].strip(),
                        fila["horario"].strip(),
                        fila["sala"].strip(),
                        float(fila["precio"]),
                        int(fila["asientos"])
                    )
                    cartelera[id_pel] = pel
                except (KeyError, ValueError, TypeError) as err:
                    print(f"{AMARILLO}Aviso: Fila {num_linea} omitida en cartelera.csv ({err}).{RESET}")
    except (OSError, csv.Error) as err:
        print(f"{ROJO}Error al leer '{ARCHIVO_CSV}': {err}{RESET}")
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
                # Formatea siempre el precio con 2 decimales
                f"{pelicula.get_precio():.2f}",
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


def comprar_entradas(cartelera):
    """Gestiona la compra de boletos, actualiza asientos y guarda en CSV."""
    ver_salas_y_cartelera(cartelera)

    id_elegido = input(f"\n{AMARILLO}Ingrese el ID de la película que desea ver (ej. PEL-01, o 0 para cancelar): {RESET}").strip().upper()
    if id_elegido == "0":
        return

    if id_elegido not in cartelera:
        print(f"{ROJO}Error: El ID de la película no existe en la cartelera.{RESET}")
        return

    pelicula = cartelera[id_elegido]

    # Rechaza funciones sin asientos antes de pedir cantidad
    if pelicula.get_asientos() <= 0:
        print(f"{ROJO}Lo sentimos, no quedan asientos disponibles para '{pelicula.get_titulo()}'.{RESET}")
        return

    # Bucle de validacion para la cantidad de boletos
    cantidad = None
    while True:
        entrada_cant = input(f"¿Cuántas entradas desea para '{pelicula.get_titulo()}'? (máx. {LIMITE_BOLETOS_POR_COMPRA}, 0 para cancelar): ").strip()
        if entrada_cant == "0":
            print(f"{AMARILLO}Compra cancelada.{RESET}")
            return
        try:
            valor = int(entrada_cant)
            if valor <= 0:
                print(f"{ROJO}La cantidad debe ser mayor a cero.{RESET}")
            elif valor > LIMITE_BOLETOS_POR_COMPRA:
                print(f"{ROJO}Límite excedido: máximo {LIMITE_BOLETOS_POR_COMPRA} boletos por compra.{RESET}")
            elif valor > pelicula.get_asientos():
                print(f"{ROJO}Lo sentimos, solo quedan {pelicula.get_asientos()} asientos disponibles.{RESET}")
            else:
                cantidad = valor
                break
        except ValueError:
            print(f"{ROJO}Por favor, ingrese un número válido.{RESET}")

    total = round(cantidad * pelicula.get_precio(), 2)
    print(f"\n{NEGRITA}Resumen de compra:{RESET}")
    print(f"- Película: {pelicula.get_titulo()} ({pelicula.get_horario()} - {pelicula.get_sala()})")
    print(f"- Entradas: {cantidad}")
    print(f"- Total a pagar: {VERDE}${total:.2f}{RESET}")

    # Bucle de confirmacion (s/n): acepta 's'/'si' y 'n'/'no', re-preguntando en entradas invalidas
    while True:
        confirmar = input(f"{AMARILLO}¿Desea proceder al pago? (s/n): {RESET}").strip().lower()
        if confirmar in ("s", "si", "sí"):
            if procesar_pago(total):
                # Actualizamos el stock de asientos, guardamos CSV y registramos en reporte_ventas.csv
                nuevo_stock = pelicula.get_asientos() - cantidad
                pelicula.set_asientos(nuevo_stock)
                guardar_cartelera_en_csv(cartelera)
                registrar_en_reporte("Boleto", pelicula.get_titulo(), cantidad, total)
                print(f"\n{VERDE}¡Disfrute su función! Sus asientos han sido reservados y guardados.{RESET}")
            break
        elif confirmar in ("n", "no"):
            print(f"{AMARILLO}Compra cancelada.{RESET}")
            break
        else:
            print(f"{ROJO}Opción inválida. Por favor ingrese 's' para sí o 'n' para no.{RESET}")


def iniciar_modulo_boleteria():
    """Función principal del Rol 3 cargando datos desde CSV."""
    cartelera = cargar_cartelera_desde_csv()

    while True:
        print(f"\n{AZUL}--- MENÚ DE BOLETERÍA ---{RESET}")
        print(f"{VERDE}[1]{RESET} Ver salas y cartelera")
        print(f"{VERDE}[2]{RESET} Comprar entradas")
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


if __name__ == "__main__":
    # Habilita codigos ANSI en Windows y permite ejecutar el modulo de forma independiente
    os.system("")
    iniciar_modulo_boleteria()