# Archivo: finanzas/reportes.py
# Modulo de Control y Reportes (Rol 6): evolucion unificada y corregida de metricas_y_reportes.py.

import csv
import math
import os
from config import RUTA_REPORTE_VENTAS
# Importa la clase Colores unificada desde nucleo/colores.py
from nucleo.colores import Colores
from nucleo.consola import (
    limpiar_pantalla,
    mostrar_encabezado,
    pausar
)


def leer_reporte(ruta_ventas=RUTA_REPORTE_VENTAS):
    """
    Lee reporte_ventas.csv usando ruta absoluta configurada y devuelve una lista
    de diccionarios validados. Maneja archivos faltantes, vacios o filas corruptas.
    """
    if not os.path.exists(ruta_ventas):
        return []

    ventas = []
    try:
        with open(ruta_ventas, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for num_linea, fila in enumerate(lector, start=2):
                try:
                    tipo = str(fila["tipo"]).strip()
                    nombre_item = str(fila["nombre_item"]).strip()
                    cantidad = int(fila["cantidad"])
                    total_pagado = float(fila["total_pagado"])

                    if not tipo or not nombre_item:
                        continue
                    if not math.isfinite(total_pagado) or total_pagado < 0 or cantidad <= 0:
                        continue

                    ventas.append({
                        "tipo": tipo,
                        "nombre_item": nombre_item,
                        "cantidad": cantidad,
                        "total_pagado": round(total_pagado, 2)
                    })
                except (KeyError, ValueError, TypeError):
                    # Omite filas danadas sin interrumpir las estadisticas validas
                    continue
    except (OSError, csv.Error) as err:
        print(f"{Colores.ROJO}Error al leer el archivo de reportes '{ruta_ventas}': {err}{Colores.RESET}")

    return ventas


def _normalizar_nombre_item(nombre, tipo):
    """
    Normaliza el nombre del producto o película.
    Para películas (tipo 'Boleto'), elimina sufijos de formato como ' (2D)', ' [3D]', ' (IMAX)'
    para que ventas del mismo título en diferentes formatos se agrupen correctamente.
    """
    nombre_limpio = str(nombre).strip()
    if tipo.lower() == "boleto":
        import re
        nombre_limpio = re.sub(r"\s*(\(|\[)\s*(2D|3D|IMAX)\s*(\)|\])\s*$", "", nombre_limpio, flags=re.IGNORECASE).strip()
    return nombre_limpio


def _agrupar_unidades(ventas, tipo_filtro=None):
    """
    Agrupa la cantidad total de unidades vendidas por nombre de producto/pelicula.
    Si tipo_filtro se especifica ('Dulce' o 'Boleto'), filtra por esa categoria.
    """
    conteo = {}
    for venta in ventas:
        if tipo_filtro is not None and venta["tipo"].lower() != tipo_filtro.lower():
            continue
        nombre = _normalizar_nombre_item(venta["nombre_item"], venta["tipo"])
        conteo[nombre] = conteo.get(nombre, 0) + venta["cantidad"]
    return conteo


def _formatear_extremos(conteo, buscar_max=True):
    """
    Retorna los items que alcanzan el maximo o minimo de unidades vendidas
    manejando empates de forma clara.
    """
    if not conteo:
        return None, 0
    valor_objetivo = max(conteo.values()) if buscar_max else min(conteo.values())
    ganadores = [nombre for nombre, cant in conteo.items() if cant == valor_objetivo]
    return ", ".join(ganadores), valor_objetivo


def _mostrar_ranking_extremo(ventas, buscar_max=True):
    """Imprime el ranking de mas o menos vendidos de forma unificada (general y por categoria)."""
    etiqueta = "MÁS VENDIDOS" if buscar_max else "MENOS VENDIDOS"
    adjetivo = "más vendido" if buscar_max else "menos vendido"
    adjetivo_fem = "más vendida" if buscar_max else "menos vendida"

    print(f"\n{Colores.AZUL}{Colores.NEGRITA}--- RANKING DE PRODUCTOS {etiqueta} ---{Colores.RESET}")

    # Ranking general combinado
    conteo_general = _agrupar_unidades(ventas)
    nombre_gen, cant_gen = _formatear_extremos(conteo_general, buscar_max=buscar_max)
    if nombre_gen:
        print(f"  General ({adjetivo}): {Colores.VERDE}{Colores.NEGRITA}{nombre_gen}{Colores.RESET} ({cant_gen} unidades)")

    # Ranking especifico de dulceria segun especificacion del PDF
    conteo_dulces = _agrupar_unidades(ventas, tipo_filtro="dulce")
    nombre_dulce, cant_dulce = _formatear_extremos(conteo_dulces, buscar_max=buscar_max)
    if nombre_dulce:
        print(f"  Dulce {adjetivo}:       {Colores.VERDE}{Colores.NEGRITA}{nombre_dulce}{Colores.RESET} ({cant_dulce} unidades)")
    else:
        print(f"  Dulce {adjetivo}:       {Colores.AMARILLO}Sin ventas de dulcería registradas{Colores.RESET}")

    # Ranking especifico de boleteria segun especificacion del PDF
    conteo_boletos = _agrupar_unidades(ventas, tipo_filtro="boleto")
    nombre_peli, cant_peli = _formatear_extremos(conteo_boletos, buscar_max=buscar_max)
    if nombre_peli:
        print(f"  Película {adjetivo_fem}:  {Colores.VERDE}{Colores.NEGRITA}{nombre_peli}{Colores.RESET} ({cant_peli} boletos)")
    else:
        print(f"  Película {adjetivo_fem}:  {Colores.AMARILLO}Sin ventas de boletos registradas{Colores.RESET}")


def _mostrar_historial_ventas(ventas):
    """Imprime la tabla completa de transacciones registradas en reporte_ventas.csv."""
    print(f"\n{Colores.AZUL}{Colores.NEGRITA}" + "=" * 75 + f"{Colores.RESET}")
    print(f"{Colores.CYAN}{Colores.NEGRITA}{'HISTORIAL COMPLETO DE VENTAS':^75}{Colores.RESET}")
    print(f"{Colores.AZUL}{Colores.NEGRITA}" + "=" * 75 + f"{Colores.RESET}")
    print(f"{Colores.NEGRITA}{'N°':<4} | {'TIPO':<8} | {'PRODUCTO / PELÍCULA':<35} | {'CANT.':<6} | {'TOTAL':>10}{Colores.RESET}")
    print(f"{Colores.AZUL}" + "-" * 75 + f"{Colores.RESET}")

    for idx, venta in enumerate(ventas, start=1):
        item = venta["nombre_item"]
        if len(item) > 35:
            item = item[:32] + "..."
        total_txt = f"${venta['total_pagado']:.2f}"
        print(f"{idx:<4} | {venta['tipo']:<8} | {item:<35} | {venta['cantidad']:<6} | {Colores.VERDE}{total_txt:>10}{Colores.RESET}")

    print(f"{Colores.AZUL}{Colores.NEGRITA}" + "=" * 75 + f"{Colores.RESET}")


def ejecutar_menu_metricas(ruta_ventas=RUTA_REPORTE_VENTAS):
    """Maneja el submenu de control, historial y metricas del cine (Rol 6)."""
    while True:
        limpiar_pantalla()
        mostrar_encabezado("ROL 6: CONTROL, MÉTRICAS Y REPORTES")
        print(f"  {Colores.VERDE}[1]{Colores.RESET} Monto total vendido hasta el momento")
        print(f"  {Colores.VERDE}[2]{Colores.RESET} Monto recaudado solo en boletos")
        print(f"  {Colores.VERDE}[3]{Colores.RESET} Monto recaudado solo en dulces")
        print(f"  {Colores.VERDE}[4]{Colores.RESET} Productos más vendidos (general, dulce y película)")
        print(f"  {Colores.VERDE}[5]{Colores.RESET} Productos menos vendidos (general, dulce y película)")
        print(f"  {Colores.VERDE}[6]{Colores.RESET} Resumen de transacciones y unidades totales")
        print(f"  {Colores.VERDE}[7]{Colores.RESET} Ver historial completo de ventas")
        print(f"  {Colores.ROJO}[8]{Colores.RESET} Volver al menú de administrador")

        opcion = input(f"\n{Colores.AMARILLO}Seleccione una opción (1-8): {Colores.RESET}").strip()

        if opcion == "8":
            print(f"\n{Colores.AMARILLO}Regresando al menú de administrador...{Colores.RESET}")
            break

        if opcion in ("1", "2", "3", "4", "5", "6", "7"):
            ventas = leer_reporte(ruta_ventas)
            if not ventas:
                print(f"\n{Colores.ROJO}No hay registros de ventas válidos en '{os.path.basename(ruta_ventas)}' todavía.{Colores.RESET}")
                pausar()
                continue

            limpiar_pantalla()
            match opcion:
                case "1":
                    total_general = sum(v["total_pagado"] for v in ventas)
                    print(f"\n{Colores.VERDE}{Colores.NEGRITA}Monto total vendido hasta el momento: ${total_general:.2f}{Colores.RESET}")
                case "2":
                    total_boletos = sum(v["total_pagado"] for v in ventas if v["tipo"].lower() == "boleto")
                    print(f"\n{Colores.VERDE}{Colores.NEGRITA}Monto total recaudado en boletos: ${total_boletos:.2f}{Colores.RESET}")
                case "3":
                    total_dulces = sum(v["total_pagado"] for v in ventas if v["tipo"].lower() == "dulce")
                    print(f"\n{Colores.VERDE}{Colores.NEGRITA}Monto total recaudado en dulces: ${total_dulces:.2f}{Colores.RESET}")
                case "4":
                    _mostrar_ranking_extremo(ventas, buscar_max=True)
                case "5":
                    _mostrar_ranking_extremo(ventas, buscar_max=False)
                case "6":
                    total_transacciones = len(ventas)
                    unidades_fisicas = sum(v["cantidad"] for v in ventas)
                    total_general = sum(v["total_pagado"] for v in ventas)
                    print(f"\n{Colores.AZUL}{Colores.NEGRITA}--- RESUMEN GENERAL DE OPERACIONES ---{Colores.RESET}")
                    print(f"  Total de compras/transacciones realizadas: {Colores.VERDE}{total_transacciones}{Colores.RESET}")
                    print(f"  Unidades físicas totales despachadas:      {Colores.VERDE}{unidades_fisicas}{Colores.RESET}")
                    print(f"  Recaudación acumulada total:               {Colores.VERDE}${total_general:.2f}{Colores.RESET}")
                case "7":
                    _mostrar_historial_ventas(ventas)

            pausar()
        else:
            print(f"\n{Colores.ROJO}Opción inválida. Por favor, seleccione un número entre 1 y 8.{Colores.RESET}")
            pausar()
