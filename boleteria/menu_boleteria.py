# Archivo: boleteria/menu_boleteria.py
# Interfaz de cliente para la compra de boletos en taquilla (unifica main_peliculas y main_rol3).

import os
from boleteria.gestor_cartelera import GestorCartelera
from config import LIMITE_BOLETOS_POR_COMPRA
from finanzas.pagos import procesar_pago
# Importa la clase Colores unificada desde nucleo/colores.py
from nucleo.colores import Colores
from nucleo.consola import (
    confirmar_accion,
    limpiar_pantalla,
    mostrar_encabezado,
    pausar
)


def ejecutar_menu_boleteria(ruta_csv=None):
    """Gestiona la cartelera, seleccion de entradas, pago y guardado en metricas."""
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

    while True:
        limpiar_pantalla()
        mostrar_encabezado("CARTELERA DE PELÍCULAS Y SALAS", ancho=75)

        # Muestra las peliculas numeradas con horario y sala, sin exponer IDs internos al cliente
        for indice, p in enumerate(lista_de_peliculas, start=1):
            if p.disponibilidad > 0:
                estado_str = f"{Colores.VERDE}[Disponible: {p.disponibilidad} asientos]{Colores.RESET}"
            else:
                estado_str = f"{Colores.ROJO}[Agotada / No disponible]{Colores.RESET}"
            print(
                f"  {Colores.VERDE}[{indice}]{Colores.RESET} {Colores.NEGRITA}{p.nombre}{Colores.RESET} ({p.duracion} min) | "
                f"{Colores.AZUL}{p.horario}{Colores.RESET} - {p.sala} | Boleto: {Colores.VERDE}${p.costo:.2f}{Colores.RESET} {estado_str}"
            )
            print("  " + "-" * 71)

        print(f"  {Colores.ROJO}[0]{Colores.RESET} Volver al menú anterior\n")

        opcion = input(f"{Colores.AMARILLO}Seleccione el número de la película que desea comprar (0 para volver): {Colores.RESET}").strip()
        if opcion == "0":
            return

        try:
            indice_elegido = int(opcion)
            if not (1 <= indice_elegido <= len(lista_de_peliculas)):
                print(f"{Colores.ROJO}Error: Seleccione una opción válida entre 0 y {len(lista_de_peliculas)}.{Colores.RESET}")
                pausar()
                continue
        except ValueError:
            print(f"{Colores.ROJO}Error: Debe ingresar un número entero válido.{Colores.RESET}")
            pausar()
            continue

        pelicula = lista_de_peliculas[indice_elegido - 1]

        if pelicula.disponibilidad <= 0:
            print(f"{Colores.ROJO}Lo sentimos, la función '{pelicula.nombre}' está agotada o no disponible.{Colores.RESET}")
            pausar()
            continue

        max_permitido = min(LIMITE_BOLETOS_POR_COMPRA, pelicula.disponibilidad)
        print(f"\nPelícula seleccionada: {Colores.NEGRITA}{pelicula.nombre}{Colores.RESET} ({pelicula.horario} - {pelicula.sala})")
        print(f"Costo por boleto: {Colores.VERDE}${pelicula.costo:.2f}{Colores.RESET} | Asientos disponibles: {pelicula.disponibilidad}")
        print(f"Límite máximo por compra: {max_permitido} boletos")

        cantidad = None
        while True:
            entrada_cant = input("¿Cuántas entradas desea comprar? (0 para cancelar): ").strip()
            if entrada_cant == "0":
                print(f"{Colores.AMARILLO}Selección cancelada.{Colores.RESET}")
                pausar()
                break
            try:
                valor = int(entrada_cant)
                if valor <= 0:
                    print(f"{Colores.ROJO}La cantidad debe ser mayor a cero.{Colores.RESET}")
                elif valor > LIMITE_BOLETOS_POR_COMPRA:
                    print(f"{Colores.ROJO}Límite excedido: máximo {LIMITE_BOLETOS_POR_COMPRA} boletos por compra.{Colores.RESET}")
                elif valor > pelicula.disponibilidad:
                    print(f"{Colores.ROJO}Lo sentimos, solo quedan {pelicula.disponibilidad} asientos disponibles.{Colores.RESET}")
                else:
                    cantidad = valor
                    break
            except ValueError:
                print(f"{Colores.ROJO}Debe ingresar un número entero válido.{Colores.RESET}")

        if cantidad is None:
            continue

        total = round(cantidad * pelicula.costo, 2)
        print(f"\n{Colores.NEGRITA}Resumen de compra:{Colores.RESET}")
        print(f"  - Función:  {pelicula.nombre} ({pelicula.horario} - {pelicula.sala})")
        print(f"  - Entradas: {cantidad}")
        print(f"  - Total:    {Colores.VERDE}${total:.2f}{Colores.RESET}\n")

        # Utiliza la utilidad compartida confirmar_accion (no cancela por entrada invalida)
        if confirmar_accion("¿Desea proceder al pago?"):
            if procesar_pago(total):
                pelicula.disponibilidad = pelicula.disponibilidad - cantidad
                gestor.guardar_catalogo_en_csv()
                gestor.registrar_venta(pelicula, cantidad)
                print(
                    f"\n{Colores.VERDE}¡Compra exitosa! Quedan {pelicula.disponibilidad} asientos "
                    f"para '{pelicula.nombre}' ({pelicula.horario}).{Colores.RESET}"
                )
            pausar()
            return
        else:
            print(f"{Colores.AMARILLO}Compra cancelada.{Colores.RESET}")
            pausar()
