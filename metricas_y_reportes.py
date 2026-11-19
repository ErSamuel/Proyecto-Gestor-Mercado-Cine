import csv
import os

# variables globales
# Colores ANSI
AZUL = "\033[94m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
RESET = "\033[0m"
NEGRITA = "\033[1m"

# funcion para limpiar la pantalla
def limpiar_pantalla():
  os.system("cls" if os.name == "nt" else "clear")

def leer_reporte():
    """Lee el archivo reporte_ventas.csv y devuelve una lista de diccionarios con las ventas."""
    ruta_ventas = "reporte_ventas.csv"
    if not os.path.exists(ruta_ventas):
        return []

    ventas = []
    with open(ruta_ventas, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            try:
                # Convertimos los tipos de datos numéricos correctamente
                fila['cantidad'] = int(fila['cantidad'])
                fila['total_pagado'] = float(fila['total_pagado'])
                ventas.append(fila)
            except ValueError:
                continue # Salta filas malformadas si las hubiera
    return ventas


def ejecutar_menu_metricas():
    """Maneja el submenú de métricas y estadísticas del cine."""
    while True:
        print(f"\n{AZUL}--- PANEL DE MÉTRICAS Y REPORTES ---{RESET}")
        print("1. Monto total vendido hasta el momento")
        print("2. Monto solo de los boleto")
        print("3. Monto solo de los dulce")
        print("4. Producto más vendido")
        print("5. Producto menos vendido")
        print("6. Resumen de unidades totales y transacciones")
        print("7. Volver al menú principal")

        opcion = input(f"\n{AMARILLO}Seleccione una opción (1-7): {RESET}").strip()
        ventas = leer_reporte()
        limpiar_pantalla()
        if not ventas and opcion in ["1", "2", "3", "4", "5", "6"]:
            print(f"\n{ROJO}No hay registros de ventas en 'reporte_ventas.csv' todavía.{RESET}")
            input("\nPresione Enter para continuar...")
            continue

        match opcion:
            case "1":
                # 1 : Monto total vendido
                total_general = sum(v['total_pagado'] for v in ventas)
                print(f"\n{VERDE}Monto total vendido hasta el momento: ${total_general:.2f}{RESET}")

            case "2":
                # 2: Monto solo en boletos
                total_boletos = sum(v['total_pagado'] for v in ventas if v['tipo'].lower() == 'boleto')
                print(f"\n{VERDE}Monto total recaudado en boletos: ${total_boletos:.2f}{RESET}")

            case "3":
                # 3: Monto solo en dulces
                total_dulces = sum(v['total_pagado'] for v in ventas if v['tipo'].lower() == 'dulce')
                print(f"\n{VERDE}Monto total recaudado en dulces: ${total_dulces:.2f}{RESET}")

            case "4":
                # 4: Producto más vendido (agrupando cantidades por nombre)
                conteo = {}
                for v in ventas:
                    nombre = v['nombre_item']
                    conteo[nombre] = conteo.get(nombre, 0) + v['cantidad']
                
                if conteo:
                    mas_vendido = max(conteo, key=conteo.get)
                    print(f"\n{VERDE}Producto más vendido: {NEGRITA}{mas_vendido}{RESET}{VERDE} ({conteo[mas_vendido]} unidades vendidas){RESET}")

            case "5":
                #5: Producto menos vendido
                conteo = {}
                for v in ventas:
                    nombre = v['nombre_item']
                    conteo[nombre] = conteo.get(nombre, 0) + v['cantidad']
                
                if conteo:
                    menos_vendido = min(conteo, key=conteo.get)
                    print(f"\n{VERDE}Producto menos vendido: {NEGRITA}{menos_vendido}{RESET}{VERDE} ({conteo[menos_vendido]} unidades vendidas){RESET}")

            case "6":
                # 6 : Conteo de transacciones y volumen físico total
                total_transacciones = len(ventas)
                unidades_fisicas = sum(v['cantidad'] for v in ventas)
                print(f"\n{AZUL}--- RESUMEN GENERAL DE OPERACIONES ---{RESET}")
                print(f"Total de compras/transacciones realizadas: {VERDE}{total_transacciones}{RESET}")
                print(f"Unidades físicas totales despachadas: {VERDE}{unidades_fisicas}{RESET}")

            case "7":
                # Opción 7: Salir al menú principal
                print(f"\n{AMARILLO}Regresando al menú principal...{RESET}")
                break
            case _:
                print(f"\n{ROJO}Opción no válida. Por favor, intente de nuevo.{RESET}")

        input("\nPresione Enter para continuar...")