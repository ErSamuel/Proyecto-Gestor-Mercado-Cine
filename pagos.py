# pagos.py
import csv
import os

#variables globales
# Colores ANSI
AZUL = "\033[94m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
RESET = "\033[0m"
NEGRITA = "\033[1m"

def procesar_pago(total_a_pagar):
    """Maneja la interfaz y validación de la pasarela de pago universal."""
    print(f"\n{AZUL}--- PASARELA DE PAGO ---{RESET}")
    print(f"Total a cancelar: {VERDE}${total_a_pagar:.2f}{RESET}")
    print(f"{AZUL}[1]{RESET} Pago Móvil / Tarjeta de Débito")
    print(f"{AZUL}[2]{RESET} Efectivo en taquilla")
    
    metodo = input("Seleccione método de pago (1 o 2): ").strip()
    if metodo in ["1", "2"]:
        print(f"\n{VERDE}¡Pago procesado con éxito!{RESET}")
        return True
    else:
        print(f"\n{ROJO}Método de pago inválido. Operación cancelada.{RESET}")
        return False


def registrar_en_reporte(tipo_item, nombre, cantidad, costo_total):
    """Registra cualquier venta (Boleto o Dulce) en el reporte general para métricas."""
    ruta_ventas = "reporte_ventas.csv"
    archivo_existe = os.path.exists(ruta_ventas)

    with open(ruta_ventas, mode='a', newline='', encoding='utf-8') as archivo:
        # Columnas estándar para métricas e historiales
        campos = ['tipo', 'nombre_item', 'cantidad', 'total_pagado']
        escritor = csv.DictWriter(archivo, fieldnames=campos)

        if not archivo_existe:
            escritor.writeheader()

        escritor.writerow({
            'tipo': tipo_item,
            'nombre_item': nombre,
            'cantidad': cantidad,
            'total_pagado': costo_total
        })