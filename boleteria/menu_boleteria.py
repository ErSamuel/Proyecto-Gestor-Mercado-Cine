# Archivo: boleteria/menu_boleteria.py
# Interfaz de cliente para la compra de boletos en taquilla.
# Incorpora las 3 clases de entradas (General, Mayor de edad, Niño), formato de duracion y promocion de lunes (15%).

from datetime import datetime
import os
from boleteria.gestor_cartelera import GestorCartelera
from config import (
    DESCUENTO_LUNES,
    LIMITE_BOLETOS_POR_COMPRA,
    TARIFAS_CLASES
)
from finanzas.pagos import procesar_pago
from nucleo.colores import Colores
from nucleo.consola import (
    confirmar_accion,
    conversor_de_minutos,
    limpiar_pantalla,
    mostrar_encabezado,
    pausar
)


def ejecutar_menu_boleteria(ruta_csv=None):
    """Gestiona la cartelera, seleccion de entradas por clases, calculo de promociones y pago."""
    gestor = GestorCartelera(ruta_csv=ruta_csv)

    if not os.path.exists(gestor.ruta_csv):
        limpiar_pantalla()
        print(f"{Colores.ROJO}Error: No se encontró el archivo de cartelera '{gestor.ruta_csv}'.{Colores.RESET}")
        pausar()
        return

    lista_de_peliculas = gestor.listar_todas()
    if not lista_de_peliculas:
        limpiar_pantalla()
        print(f"{Colores.ROJO}No hay películas registradas en la cartelera en este momento.{Colores.RESET}")
        pausar()
        return

    # Comprobacion de si hoy es lunes (dia de la semana 0 en Python)
    es_lunes = (datetime.now().weekday() == 0)

    while True:
        limpiar_pantalla()
        mostrar_encabezado("CARTELERA DE PELÍCULAS Y SALAS", ancho=80)

        if es_lunes:
            print(f"{Colores.VERDE}{Colores.NEGRITA}★ ¡HOY ES LUNES DE CINE! 15% DE DESCUENTO EN TODAS LAS ENTRADAS ★{Colores.RESET}\n")

        # Muestra las peliculas numeradas con horario, formato, sala y butacas
        for indice, p in enumerate(lista_de_peliculas, start=1):
            if p.sala.lower() in ("sin asignar", "por definir"):
                estado_str = f"{Colores.AMARILLO}[Próximamente / Sin sala asignada]{Colores.RESET}"
            elif p.disponibilidad > 0:
                estado_str = f"{Colores.VERDE}[Disponible: {p.disponibilidad} butacas]{Colores.RESET}"
            else:
                estado_str = f"{Colores.ROJO}[Agotada]{Colores.RESET}"

            horario_info = f"{p.horario} - {p.sala}" if p.sala != "Sin asignar" else "En catálogo"
            print(
                f"  {Colores.VERDE}[{indice}]{Colores.RESET} {Colores.NEGRITA}{p.nombre}{Colores.RESET} "
                f"{Colores.CYAN}[{p.formato}]{Colores.RESET} ({p.clasificacion}) ({conversor_de_minutos(p.duracion)}) | "
                f"{Colores.AZUL}{horario_info}{Colores.RESET} | Boleto base: {Colores.VERDE}${p.costo:.2f}{Colores.RESET} {estado_str}"
            )
            print("  " + "-" * 80)

        print(f"  {Colores.ROJO}[0]{Colores.RESET} Volver al menú anterior\n")

        opcion = input(f"{Colores.AMARILLO}Seleccione el número de la película que desea comprar (0 para volver): {Colores.RESET}").strip()
        if opcion == "0":
            return

        try:
            indice_elegido = int(opcion.strip())
            if not (1 <= indice_elegido <= len(lista_de_peliculas)):
                print(f"{Colores.AMARILLO}Ingrese un número válido para la cartelera mostrada.\n{Colores.RESET}")
                pausar()
                continue
        except ValueError:
            print(f"{Colores.ROJO}Error: Debe ingresar un número entero válido.{Colores.RESET}")
            pausar()
            continue

        pelicula = lista_de_peliculas[indice_elegido - 1]

        # Validar si tiene sala y horario asignado
        if pelicula.sala.lower() in ("sin asignar", "por definir") or pelicula.horario.lower() in ("por definir", "sin asignar"):
            print(f"\n{Colores.AMARILLO}La película '{pelicula.nombre}' aún no tiene sala u horario programado para venta.{Colores.RESET}")
            pausar()
            continue

        if pelicula.disponibilidad <= 0:
            print(f"\n{Colores.ROJO}Lo sentimos, la función '{pelicula.nombre}' está agotada.{Colores.RESET}")
            pausar()
            continue

        limpiar_pantalla()
        max_permitido = min(LIMITE_BOLETOS_POR_COMPRA, pelicula.disponibilidad)

        # Calculo de precios base segun las 3 clases
        precio_base = pelicula.costo
        precio_general = round(precio_base * TARIFAS_CLASES.get("General", 1.0), 2)
        precio_mayor = round(precio_base * TARIFAS_CLASES.get("Mayor de edad", 0.80), 2)
        precio_nino = round(precio_base * TARIFAS_CLASES.get("Niño", 0.70), 2)

        separador = "-" * 80
        print(f"\n{Colores.AZUL}{separador}{Colores.RESET}")
        print(f"{Colores.NEGRITA}{pelicula.nombre}{Colores.RESET} {Colores.CYAN}[{pelicula.formato}]{Colores.RESET} ({pelicula.clasificacion})")
        print(f"Duración: {conversor_de_minutos(pelicula.duracion)} ({pelicula.duracion} min)")
        print(f"Descripción: {pelicula.descripcion}")
        print(f"Función: {Colores.AZUL}{pelicula.horario} - {pelicula.sala}{Colores.RESET} (Finaliza aprox.: {pelicula.hora_fin})")
        print(f"Butacas disponibles: {Colores.VERDE}{pelicula.disponibilidad}{Colores.RESET} (Máx. {max_permitido} por compra)")
        print(f"{Colores.AZUL}{separador}{Colores.RESET}")

        print(f"\n{Colores.CYAN}{Colores.NEGRITA}--- CLASES DE ENTRADAS DISPONIBLES ---{Colores.RESET}")
        print(f"  [1] General (Adulto):        ${precio_general:.2f}")
        print(f"  [2] Mayor de edad (+60):     ${precio_mayor:.2f}")
        print(f"  [3] Niño (hasta 12 años):    ${precio_nino:.2f}")
        print("  [4] Mixto (distribuir varias clases)")
        print(f"  {Colores.ROJO}[0] Cancelar selección{Colores.RESET}")

        opcion_clase = input("\nSeleccione el tipo de entrada a adquirir (1-4, o 0 para cancelar): ").strip()
        if opcion_clase == "0":
            continue

        cant_gen = 0
        cant_may = 0
        cant_nin = 0

        if opcion_clase == "1":
            try:
                cnt = int(input(f"¿Cuántas entradas 'General' desea? (máx. {max_permitido}): ").strip())
                if 1 <= cnt <= max_permitido:
                    cant_gen = cnt
                else:
                    print(f"{Colores.ROJO}Cantidad inválida o superior al límite ({max_permitido}).{Colores.RESET}")
                    pausar()
                    continue
            except ValueError:
                print(f"{Colores.ROJO}Debe ingresar un número entero.{Colores.RESET}")
                pausar()
                continue

        elif opcion_clase == "2":
            try:
                cnt = int(input(f"¿Cuántas entradas 'Mayor de edad' desea? (máx. {max_permitido}): ").strip())
                if 1 <= cnt <= max_permitido:
                    cant_may = cnt
                else:
                    print(f"{Colores.ROJO}Cantidad inválida o superior al límite ({max_permitido}).{Colores.RESET}")
                    pausar()
                    continue
            except ValueError:
                print(f"{Colores.ROJO}Debe ingresar un número entero.{Colores.RESET}")
                pausar()
                continue

        elif opcion_clase == "3":
            try:
                cnt = int(input(f"¿Cuántas entradas 'Niño' desea? (máx. {max_permitido}): ").strip())
                if 1 <= cnt <= max_permitido:
                    cant_nin = cnt
                else:
                    print(f"{Colores.ROJO}Cantidad inválida o superior al límite ({max_permitido}).{Colores.RESET}")
                    pausar()
                    continue
            except ValueError:
                print(f"{Colores.ROJO}Debe ingresar un número entero.{Colores.RESET}")
                pausar()
                continue

        elif opcion_clase == "4":
            print(f"\nIndique la cantidad de cada clase (total máximo {max_permitido}):")
            try:
                g_in = input("  - Entradas General [0]: ").strip()
                cant_gen = int(g_in) if g_in else 0
                m_in = input("  - Entradas Mayor de edad [0]: ").strip()
                cant_may = int(m_in) if m_in else 0
                n_in = input("  - Entradas Niño [0]: ").strip()
                cant_nin = int(n_in) if n_in else 0
            except ValueError:
                print(f"{Colores.ROJO}Las cantidades deben ser números enteros.{Colores.RESET}")
                pausar()
                continue
        else:
            print(f"{Colores.ROJO}Opción no válida.{Colores.RESET}")
            pausar()
            continue

        total_entradas = cant_gen + cant_may + cant_nin
        if total_entradas <= 0:
            print(f"{Colores.ROJO}Debe seleccionar al menos una entrada.{Colores.RESET}")
            pausar()
            continue
        if total_entradas > max_permitido:
            print(f"{Colores.ROJO}Supera el límite permitido de {max_permitido} butacas.{Colores.RESET}")
            pausar()
            continue

        # Calculo de subtotal
        subtotal = round(
            (cant_gen * precio_general) +
            (cant_may * precio_mayor) +
            (cant_nin * precio_nino),
            2
        )

        # Aplicacion de promocion de lunes (15%)
        descuento_lunes = round(subtotal * DESCUENTO_LUNES, 2) if es_lunes else 0.0
        total_a_pagar = round(subtotal - descuento_lunes, 2)

        # Desglose claro de compra
        print(f"\n{Colores.AZUL}{Colores.NEGRITA}================ RESUMEN DE COMPRA ================={Colores.RESET}")
        print(f"Función: {pelicula.nombre} [{pelicula.formato}] | {pelicula.horario} - {pelicula.sala}")
        if cant_gen > 0:
            print(f"  * {cant_gen}x Boleto General:       ${cant_gen * precio_general:.2f}")
        if cant_may > 0:
            print(f"  * {cant_may}x Boleto Mayor de edad: ${cant_may * precio_mayor:.2f}")
        if cant_nin > 0:
            print(f"  * {cant_nin}x Boleto Niño:          ${cant_nin * precio_nino:.2f}")
        print(f"Total butacas: {total_entradas}")
        print(f"Subtotal: {Colores.NEGRITA}${subtotal:.2f}{Colores.RESET}")

        if es_lunes:
            print(f"{Colores.VERDE}Descuento Lunes (15%): -${descuento_lunes:.2f}{Colores.RESET}")

        print(f"Total a pagar: {Colores.VERDE}{Colores.NEGRITA}${total_a_pagar:.2f}{Colores.RESET}")
        print(f"{Colores.AZUL}====================================================={Colores.RESET}")

        if confirmar_accion("¿Desea proceder al pago?"):
            if procesar_pago(total_a_pagar):
                pelicula.disponibilidad = pelicula.disponibilidad - total_entradas
                gestor.guardar_catalogo_en_csv()
                gestor.registrar_venta(pelicula, total_entradas)
                print(
                    f"\n{Colores.VERDE}¡Compra exitosa! Quedan {pelicula.disponibilidad} butacas "
                    f"para '{pelicula.nombre}' en {pelicula.sala}.{Colores.RESET}"
                )
            pausar()
            return
        else:
            print(f"{Colores.AMARILLO}Compra cancelada.{Colores.RESET}")
            pausar()
