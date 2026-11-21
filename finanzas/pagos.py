# Archivo: finanzas/pagos.py
# Pasarela de pago universal y registro unificado de transacciones en reporte_ventas.csv.

import csv
import os
from config import RUTA_REPORTE_VENTAS
from nucleo.colores import Colores
from nucleo.consola import append_csv_seguro


def procesar_pago(total_a_pagar):
    """Maneja la interfaz y validacion de la pasarela de pago universal."""
    try:
        monto = float(total_a_pagar)
    except (ValueError, TypeError):
        print(f"\n{Colores.ROJO}Error: Monto de pago inválido.{Colores.RESET}")
        return False

    if monto <= 0:
        print(f"\n{Colores.ROJO}Error: El total a cancelar debe ser mayor a cero.{Colores.RESET}")
        return False

    # Bucle de validacion para no cancelar la compra ante una entrada invalida
    while True:
        print(f"\n{Colores.AZUL}--- PASARELA DE PAGO ---{Colores.RESET}")
        print(f"Total a cancelar: {Colores.VERDE}${monto:.2f}{Colores.RESET}")
        print(f"  {Colores.VERDE}[1]{Colores.RESET} Pago Móvil / Tarjeta de Débito")
        print(f"  {Colores.VERDE}[2]{Colores.RESET} Efectivo en taquilla")
        print(f"  {Colores.ROJO}[0]{Colores.RESET} Cancelar pago")

        metodo = input("Seleccione método de pago (1, 2 o 0 para cancelar): ").strip()
        if metodo in ("1", "2"):
            print(f"\n{Colores.VERDE}¡Pago procesado con éxito!{Colores.RESET}")
            return True
        if metodo == "0":
            print(f"\n{Colores.AMARILLO}Pago cancelado por el usuario.{Colores.RESET}")
            return False

        # Muestra el error y vuelve a solicitar el metodo sin abortar la compra
        print(f"\n{Colores.ROJO}Opción inválida. Por favor seleccione 1, 2 o 0 para cancelar.{Colores.RESET}")


def registrar_en_reporte(tipo_item, nombre, cantidad, costo_total, ruta_ventas=RUTA_REPORTE_VENTAS):
    """Registra cualquier venta (Boleto o Dulce) en el reporte general para metricas de forma segura ante bloqueos."""
    monto_formateado = f"{round(float(costo_total), 2):.2f}"
    campos = ["tipo", "nombre_item", "cantidad", "total_pagado"]
    fila = {
        "tipo": tipo_item,
        "nombre_item": nombre,
        "cantidad": int(cantidad),
        "total_pagado": monto_formateado
    }
    return append_csv_seguro(ruta_ventas, campos, fila)
