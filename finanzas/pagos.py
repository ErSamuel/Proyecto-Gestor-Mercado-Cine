# Archivo: finanzas/pagos.py
# Pasarela de pago universal y registro unificado de transacciones en reporte_ventas.csv.

import csv
import os
from config import RUTA_REPORTE_VENTAS
# Importa la clase Colores unificada desde nucleo/colores.py
from nucleo.colores import Colores


def procesar_pago(total_a_pagar):
    """Maneja la interfaz y validacion de la pasarela de pago universal."""
    # Bucle de validacion para no cancelar la compra ante una entrada invalida
    while True:
        print(f"\n{Colores.AZUL}--- PASARELA DE PAGO ---{Colores.RESET}")
        print(f"Total a cancelar: {Colores.VERDE}${float(total_a_pagar):.2f}{Colores.RESET}")
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
    """Registra cualquier venta (Boleto o Dulce) en el reporte general para metricas."""
    # Garantiza que el directorio destino exista antes de escribir
    carpeta_destino = os.path.dirname(os.path.abspath(ruta_ventas))
    if carpeta_destino:
        os.makedirs(carpeta_destino, exist_ok=True)

    # Verifica tanto si el archivo no existe como si existe vacio (0 bytes) para escribir cabecera
    necesita_cabecera = (not os.path.exists(ruta_ventas)) or (os.path.getsize(ruta_ventas) == 0)

    # Redondeo y formateo a 2 decimales para evitar artefactos binarios de punto flotante
    monto_formateado = f"{round(float(costo_total), 2):.2f}"

    with open(ruta_ventas, mode="a", newline="", encoding="utf-8") as archivo:
        campos = ["tipo", "nombre_item", "cantidad", "total_pagado"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)

        if necesita_cabecera:
            escritor.writeheader()

        escritor.writerow({
            "tipo": tipo_item,
            "nombre_item": nombre,
            "cantidad": int(cantidad),
            "total_pagado": monto_formateado
        })
