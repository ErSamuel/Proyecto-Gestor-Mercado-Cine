# pagos.py
import csv
import os

# Ruta base del modulo para independizar los archivos CSV del directorio de trabajo (CWD)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_REPORTE_VENTAS = os.path.join(BASE_DIR, "reporte_ventas.csv")

# variables globales
# Colores ANSI
AZUL = "\033[94m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
RESET = "\033[0m"
NEGRITA = "\033[1m"


def procesar_pago(total_a_pagar):
    """Maneja la interfaz y validación de la pasarela de pago universal."""
    # Bucle de validacion para no cancelar la compra ante una entrada invalida
    while True:
        print(f"\n{AZUL}--- PASARELA DE PAGO ---{RESET}")
        print(f"Total a cancelar: {VERDE}${float(total_a_pagar):.2f}{RESET}")
        print(f"{VERDE}[1]{RESET} Pago Móvil / Tarjeta de Débito")
        print(f"{VERDE}[2]{RESET} Efectivo en taquilla")
        print(f"{ROJO}[0]{RESET} Cancelar pago")

        metodo = input("Seleccione método de pago (1, 2 o 0 para cancelar): ").strip()
        if metodo in ("1", "2"):
            print(f"\n{VERDE}¡Pago procesado con éxito!{RESET}")
            return True
        elif metodo == "0":
            print(f"\n{AMARILLO}Pago cancelado por el usuario.{RESET}")
            return False
        else:
            # Muestra el error y vuelve a solicitar el metodo sin abortar la compra
            print(f"\n{ROJO}Opción inválida. Por favor seleccione 1, 2 o 0 para cancelar.{RESET}")


def registrar_en_reporte(tipo_item, nombre, cantidad, costo_total, ruta_ventas=RUTA_REPORTE_VENTAS):
    """Registra cualquier venta (Boleto o Dulce) en el reporte general para métricas."""
    # Verifica tanto si el archivo no existe como si existe vacio (0 bytes) para escribir cabecera
    necesita_cabecera = (not os.path.exists(ruta_ventas)) or (os.path.getsize(ruta_ventas) == 0)

    # Redondeo y formateo a 2 decimales para evitar artefactos binarios de punto flotante
    monto_formateado = f"{round(float(costo_total), 2):.2f}"

    with open(ruta_ventas, mode='a', newline='', encoding='utf-8') as archivo:
        # Columnas estándar para métricas e historiales
        campos = ['tipo', 'nombre_item', 'cantidad', 'total_pagado']
        escritor = csv.DictWriter(archivo, fieldnames=campos)

        if necesita_cabecera:
            escritor.writeheader()

        escritor.writerow({
            'tipo': tipo_item,
            'nombre_item': nombre,
            'cantidad': int(cantidad),
            'total_pagado': monto_formateado
        })