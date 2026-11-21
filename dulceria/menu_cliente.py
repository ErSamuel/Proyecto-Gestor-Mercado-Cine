# Archivo: dulceria/menu_cliente.py
# Interfaz de Dulceria para el Cliente (Rol 2): listado directo y compra por seleccion numerica.

import os
from config import RUTA_REPORTE_VENTAS, RUTA_STOCK
from dulceria.gestor_inventario import (
    cargar_snacks_desde_csv,
    guardar_snacks_en_csv
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


def _color_por_stock(cantidad):
    """Devuelve el color de semaforo segun la disponibilidad del snack."""
    return Colores.VERDE if cantidad > 5 else Colores.AMARILLO


def _mostrar_listado_snacks(snacks_disponibles):
    """Imprime la lista numerada de snacks disponibles resaltando indice, precio y stock."""
    for indice, snack in enumerate(snacks_disponibles, start=1):
        cant = snack.get_cantidad()
        color_stock = _color_por_stock(cant)

        # Formatea y alinea antes de envolver en codigos ANSI para evitar desalineaciones
        nombre = snack.get_nombre()
        nombre_col = nombre[:21] + "..." if len(nombre) > 24 else nombre
        precio_str = f"${snack.get_precio():.2f}"
        stock_str = f"[Disponible: {cant} uds]"

        print(
            f"  {Colores.VERDE}[{indice}]{Colores.RESET} "
            f"{Colores.NEGRITA}{nombre_col:<24}{Colores.RESET} | "
            f"Precio: {Colores.VERDE}{Colores.NEGRITA}{precio_str:<8}{Colores.RESET} | "
            f"{color_stock}{stock_str}{Colores.RESET}"
        )
        print(f"  {Colores.AZUL}{'-' * 76}{Colores.RESET}")

    print(f"  {Colores.ROJO}[0]{Colores.RESET} Volver al menú anterior\n")


def _mostrar_detalle_snack(snack):
    """Muestra la ficha completa del producto seleccionado antes de pedir la cantidad."""
    cant = snack.get_cantidad()
    color_stock = _color_por_stock(cant)
    borde = "=" * 76

    print(f"\n{Colores.AZUL}{borde}{Colores.RESET}")
    print(f"{Colores.CYAN}{Colores.NEGRITA}  DETALLE DEL PRODUCTO SELECCIONADO{Colores.RESET}")
    print(f"{Colores.AZUL}{borde}{Colores.RESET}")
    print(f"  Producto:         {Colores.NEGRITA}{snack.get_nombre()}{Colores.RESET}")
    print(f"  Descripción:      {Colores.CYAN}{snack.get_descripcion()}{Colores.RESET}")
    print(f"  Precio unitario:  {Colores.VERDE}{Colores.NEGRITA}${snack.get_precio():.2f}{Colores.RESET}")
    print(f"  Stock disponible: {color_stock}{cant} unidades{Colores.RESET}")
    print(f"{Colores.AZUL}{borde}{Colores.RESET}\n")


def _pedir_cantidad_snack(snack):
    """Solicita y valida la cantidad de unidades a comprar; retorna None si el usuario cancela."""
    stock_disponible = snack.get_cantidad()

    while True:
        entrada_cant = input("¿Cuántas unidades desea comprar? (0 para cancelar): ").strip()
        if entrada_cant == "0":
            print(f"\n{Colores.AMARILLO}Compra cancelada.{Colores.RESET}")
            pausar()
            return None
        try:
            valor = int(entrada_cant)
            if valor <= 0:
                print(f"{Colores.ROJO}La cantidad debe ser mayor a cero.{Colores.RESET}")
            elif valor > stock_disponible:
                print(f"{Colores.ROJO}Lo sentimos, solo hay {stock_disponible} unidades disponibles.{Colores.RESET}")
            else:
                return valor
        except ValueError:
            print(f"{Colores.ROJO}Debe ingresar un número entero válido para la cantidad.{Colores.RESET}")


def _mostrar_resumen_compra(snack, cantidad, total):
    """Imprime el resumen detallado del producto y el total antes de confirmar el pago."""
    borde = "=" * 76
    print(f"\n{Colores.AZUL}{Colores.NEGRITA}{borde}{Colores.RESET}")
    print(f"{Colores.CYAN}{Colores.NEGRITA}  RESUMEN DE COMPRA{Colores.RESET}")
    print(f"{Colores.AZUL}{Colores.NEGRITA}{borde}{Colores.RESET}")
    print(f"  Producto:         {Colores.NEGRITA}{snack.get_nombre()}{Colores.RESET}")
    print(f"  Descripción:      {Colores.CYAN}{snack.get_descripcion()}{Colores.RESET}")
    print(f"  Precio unitario:  {Colores.VERDE}${snack.get_precio():.2f}{Colores.RESET}")
    print(f"  Cantidad:         {Colores.AMARILLO}{cantidad} unidad(es){Colores.RESET}")
    print(f"  Total a pagar:    {Colores.VERDE}{Colores.NEGRITA}${total:.2f}{Colores.RESET}")
    print(f"{Colores.AZUL}{Colores.NEGRITA}{borde}{Colores.RESET}\n")


def menu_snacks_usuario(diccionario_snacks=None, ruta_csv=None):
    """
    Muestra directamente el catalogo numerado de snacks disponibles al cliente,
    permite elegir por indice, visualizar los detalles del producto y procesar la compra.
    """
    usar_disco = diccionario_snacks is None or ruta_csv is not None
    ruta_objetivo = ruta_csv if ruta_csv is not None else RUTA_STOCK
    ruta_reporte = (
        os.path.join(os.path.dirname(os.path.abspath(ruta_objetivo)), "reporte_ventas.csv")
        if ruta_csv is not None else RUTA_REPORTE_VENTAS
    )

    if diccionario_snacks is None:
        diccionario_snacks = cargar_snacks_desde_csv(ruta_objetivo)

    while True:
        # Sincroniza inventario desde disco en cada iteracion si aplica
        if usar_disco:
            diccionario_snacks = cargar_snacks_desde_csv(ruta_objetivo)

        snacks_disponibles = [s for s in diccionario_snacks.values() if s.get_cantidad() > 0]

        if not snacks_disponibles:
            limpiar_pantalla()
            mostrar_encabezado("MENÚ DE DULCERÍA - SNACKS DISPONIBLES", ancho=80)
            print(f"{Colores.ROJO}No hay snacks disponibles en la dulcería en este momento.{Colores.RESET}")
            pausar()
            return

        limpiar_pantalla()
        mostrar_encabezado("MENÚ DE DULCERÍA - SNACKS DISPONIBLES", ancho=80)
        _mostrar_listado_snacks(snacks_disponibles)

        opcion = input(
            f"{Colores.AMARILLO}Seleccione el número del snack que desea comprar (0 para volver): {Colores.RESET}"
        ).strip()

        if opcion == "0":
            print(f"\n{Colores.AMARILLO}Regresando al menú anterior...{Colores.RESET}")
            return

        # Valida seleccion numerica dentro del rango visible
        try:
            indice_elegido = int(opcion)
            if not (1 <= indice_elegido <= len(snacks_disponibles)):
                print(f"{Colores.ROJO}Error: Seleccione un número válido entre 1 y {len(snacks_disponibles)} (o 0 para volver).{Colores.RESET}")
                pausar()
                continue
        except ValueError:
            print(f"{Colores.ROJO}Error: Debe ingresar un número entero válido.{Colores.RESET}")
            pausar()
            continue

        snack = snacks_disponibles[indice_elegido - 1]

        # Muestra la ficha tecnica del snack seleccionado y pide cantidad
        limpiar_pantalla()
        _mostrar_detalle_snack(snack)
        cantidad = _pedir_cantidad_snack(snack)
        if cantidad is None:
            continue

        total = round(cantidad * snack.get_precio(), 2)
        _mostrar_resumen_compra(snack, cantidad, total)

        # Confirma y procesa el pago protegiendo la integridad del inventario en disco
        if confirmar_accion("¿Desea proceder al pago?"):
            if procesar_pago(total):
                stock_anterior = snack.get_cantidad()
                snack.set_cantidad(stock_anterior - cantidad)

                if usar_disco:
                    guardado_ok = guardar_snacks_en_csv(diccionario_snacks, ruta_objetivo)
                    if not guardado_ok:
                        snack.set_cantidad(stock_anterior)
                        print(f"\n{Colores.ROJO}Error: No se pudo guardar la actualización de inventario. Compra revertida.{Colores.RESET}")
                        pausar()
                        continue

                registrado_ok = registrar_en_reporte(
                    "Dulce", snack.get_nombre(), cantidad, total, ruta_ventas=ruta_reporte
                )
                print(
                    f"\n{Colores.VERDE}{Colores.NEGRITA}¡Compra de dulces exitosa! "
                    f"Quedan {snack.get_cantidad()} unidades de '{snack.get_nombre()}'.{Colores.RESET}"
                )
                if not registrado_ok:
                    print(
                        f"{Colores.AMARILLO}[AVISO] La compra se procesó, pero el registro en "
                        f"'reporte_ventas.csv' fue omitido.{Colores.RESET}"
                    )
            pausar()
        else:
            print(f"\n{Colores.AMARILLO}Compra de dulces cancelada.{Colores.RESET}")
            pausar()


def iniciar_dulceria_cliente(ruta_csv=None):
    """Carga el inventario actualizado desde stock.csv y abre el menu de dulceria para cliente."""
    ruta_objetivo = ruta_csv if ruta_csv is not None else RUTA_STOCK
    diccionario_snacks = cargar_snacks_desde_csv(ruta_objetivo)
    menu_snacks_usuario(diccionario_snacks, ruta_csv=ruta_objetivo)
