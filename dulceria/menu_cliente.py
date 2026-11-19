# Archivo: dulceria/menu_cliente.py
# Interfaz de Dulceria para el Cliente (Rol 2): consultar, buscar y comprar snacks.

import os
from config import RUTA_REPORTE_VENTAS, RUTA_STOCK
from dulceria.gestor_inventario import (
    buscar_snack,
    cargar_snacks_desde_csv,
    guardar_snacks_en_csv,
    mostrar_catalogo_snacks
)
from finanzas.pagos import procesar_pago, registrar_en_reporte
# Importa la clase Colores unificada desde nucleo/colores.py
from nucleo.colores import Colores
from nucleo.consola import (
    confirmar_accion,
    limpiar_pantalla,
    mostrar_encabezado,
    pausar
)


def menu_snacks_usuario(diccionario_snacks=None, ruta_csv=None):
    """Submenu de dulceria para consultar, buscar y comprar snacks sincronizado con disco."""
    usar_disco = diccionario_snacks is None or ruta_csv is not None
    ruta_objetivo = ruta_csv if ruta_csv is not None else RUTA_STOCK
    ruta_reporte = (
        os.path.join(os.path.dirname(os.path.abspath(ruta_objetivo)), "reporte_ventas.csv")
        if ruta_csv is not None else RUTA_REPORTE_VENTAS
    )

    if diccionario_snacks is None:
        diccionario_snacks = cargar_snacks_desde_csv(ruta_objetivo)

    while True:
        limpiar_pantalla()
        mostrar_encabezado("MENÚ DE DULCERÍA", ancho=45)
        print(f"  {Colores.VERDE}[1]{Colores.RESET} Ver todos los snacks disponibles")
        print(f"  {Colores.VERDE}[2]{Colores.RESET} Buscar un snack específico (por nombre o ID)")
        print(f"  {Colores.VERDE}[3]{Colores.RESET} Comprar un snack")
        print(f"  {Colores.ROJO}[4]{Colores.RESET} Volver al menú anterior")

        opcion = input("\nSeleccione una opción (1-4): ").strip()

        if opcion == "1":
            if usar_disco:
                diccionario_snacks = cargar_snacks_desde_csv(ruta_objetivo)
            limpiar_pantalla()
            mostrar_catalogo_snacks(diccionario_snacks)
            pausar()
        elif opcion == "2":
            if usar_disco:
                diccionario_snacks = cargar_snacks_desde_csv(ruta_objetivo)
            limpiar_pantalla()
            buscar_snack(diccionario_snacks)
            pausar()
        elif opcion == "3":
            if usar_disco:
                diccionario_snacks = cargar_snacks_desde_csv(ruta_objetivo)
            limpiar_pantalla()
            print(f"\n{Colores.AZUL}{Colores.NEGRITA}--- COMPRA DE SNACKS ---{Colores.RESET}")
            mostrar_catalogo_snacks(diccionario_snacks)

            if not any(s.get_cantidad() > 0 for s in diccionario_snacks.values()):
                pausar()
                continue

            id_elegido = input(f"\n{Colores.AMARILLO}Ingrese el ID del snack que desea comprar (0 para cancelar): {Colores.RESET}").strip().upper()
            if id_elegido == "0":
                continue

            snack = diccionario_snacks.get(id_elegido)
            if not snack:
                print(f"\n{Colores.ROJO}Error: El ID ingresado no existe en la dulcería.{Colores.RESET}")
                pausar()
                continue

            if snack.get_cantidad() <= 0:
                print(f"\n{Colores.ROJO}Lo sentimos, el snack '{snack.get_nombre()}' se encuentra agotado.{Colores.RESET}")
                pausar()
                continue

            print(f"\nSnack seleccionado: {Colores.NEGRITA}{snack.get_nombre()}{Colores.RESET}")
            print(f"Costo unitario: {Colores.VERDE}${snack.get_precio():.2f}{Colores.RESET} | Stock disponible: {snack.get_cantidad()}")

            cantidad = None
            while True:
                entrada_cant = input("¿Cuántas unidades desea comprar? (0 para cancelar): ").strip()
                if entrada_cant == "0":
                    print(f"\n{Colores.AMARILLO}Compra cancelada.{Colores.RESET}")
                    pausar()
                    break
                try:
                    valor = int(entrada_cant)
                    if valor <= 0:
                        print(f"{Colores.ROJO}La cantidad debe ser mayor a cero.{Colores.RESET}")
                    elif valor > snack.get_cantidad():
                        print(f"{Colores.ROJO}Lo sentimos, solo hay {snack.get_cantidad()} unidades disponibles.{Colores.RESET}")
                    else:
                        cantidad = valor
                        break
                except ValueError:
                    print(f"{Colores.ROJO}Debe ingresar un número entero válido para la cantidad.{Colores.RESET}")

            if cantidad is None:
                continue

            total = round(cantidad * snack.get_precio(), 2)
            print(f"\nTotal a pagar: {Colores.VERDE}${total:.2f}{Colores.RESET}")

            # Usa la utilidad compartida confirmar_accion sin cancelar por entrada invalida
            if confirmar_accion("¿Desea proceder al pago?"):
                if procesar_pago(total):
                    stock_actualizado = snack.get_cantidad() - cantidad
                    snack.set_cantidad(stock_actualizado)

                    if usar_disco:
                        guardar_snacks_en_csv(diccionario_snacks, ruta_objetivo)

                    registrar_en_reporte("Dulce", snack.get_nombre(), cantidad, total, ruta_ventas=ruta_reporte)
                    print(f"\n{Colores.VERDE}¡Compra de dulces exitosa! Registrada en el reporte de métricas.{Colores.RESET}")
                pausar()
            else:
                print(f"\n{Colores.AMARILLO}Compra de dulces cancelada.{Colores.RESET}")
                pausar()

        elif opcion == "4":
            print(f"\n{Colores.AMARILLO}Regresando al menú anterior...{Colores.RESET}")
            break
        else:
            print(f"\n{Colores.ROJO}Opción no válida. Por favor, intente de nuevo.{Colores.RESET}")
            pausar()


def iniciar_dulceria_cliente(ruta_csv=None):
    """Carga el inventario actualizado desde stock.csv y abre el menu de dulceria para cliente."""
    ruta_objetivo = ruta_csv if ruta_csv is not None else RUTA_STOCK
    diccionario_snacks = cargar_snacks_desde_csv(ruta_objetivo)
    menu_snacks_usuario(diccionario_snacks, ruta_csv=ruta_objetivo)
