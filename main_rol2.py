# Archivo: main_rol2.py
# Punto de entrada para probar e integrar el Rol 2 (Estructura y Busqueda de Snacks)
import os
from pagos import procesar_pago, registrar_en_reporte
from gestor_snacks import (
    RUTA_STOCK_DEFECTO,
    cargar_snacks_desde_csv,
    guardar_snacks_en_csv,
    mostrar_catalogo_snacks,
    buscar_snack
)

# variables globales
# Colores ANSI
AZUL = "\033[94m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
RESET = "\033[0m"
NEGRITA = "\033[1m"


def limpiar_pantalla():
    """Limpia la terminal según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Pausa la ejecución para permitir leer mensajes y resultados."""
    input(f"\n{AMARILLO}Presione Enter para continuar...{RESET}")


def menu_snacks_usuario(diccionario_snacks=None, ruta_csv=None):
    """Submenú del Rol 2 para consultar, buscar y comprar snacks."""
    # Si no se entrega un diccionario manual, trabaja sincronizado con el CSV en disco
    usar_disco = diccionario_snacks is None or ruta_csv is not None
    ruta_objetivo = ruta_csv if ruta_csv is not None else RUTA_STOCK_DEFECTO
    if diccionario_snacks is None:
        diccionario_snacks = cargar_snacks_desde_csv(ruta_objetivo)

    while True:
        # Limpia la pantalla en cada ciclo para mantener la interfaz ordenada
        limpiar_pantalla()
        print(f"\n{AZUL}{NEGRITA}=========================================")
        print("            MENÚ DE DULCERÍA             ")
        print(f"========================================={RESET}\n")
        # Tabulacion uniforme y colores consistentes (verde para acciones, rojo para volver)
        print(f"  {VERDE}[1]{RESET} Ver todos los snacks disponibles")
        print(f"  {VERDE}[2]{RESET} Buscar un snack específico (por nombre o ID)")
        print(f"  {VERDE}[3]{RESET} Comprar un snack")
        print(f"  {ROJO}[4]{RESET} Volver al menú anterior")

        opcion = input("\nSeleccione una opción (1-4): ").strip()

        if opcion == "1":
            # Recarga desde disco antes de mostrar para reflejar cambios recientes de Admin
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
            print(f"\n{AZUL}{NEGRITA}--- COMPRA DE SNACKS ---{RESET}")
            mostrar_catalogo_snacks(diccionario_snacks)

            # Evita pedir ID si no existe ningun snack con stock disponible
            if not any(s.get_cantidad() > 0 for s in diccionario_snacks.values()):
                pausar()
                continue

            # Normaliza a mayusculas para no fallar si el usuario escribe 'snk-183' en minusculas
            id_elegido = input(f"\n{AMARILLO}Ingrese el ID del snack que desea comprar (0 para cancelar): {RESET}").strip().upper()
            if id_elegido == "0":
                continue

            # Buscamos el snack en el diccionario
            snack = diccionario_snacks.get(id_elegido)

            if not snack:
                print(f"\n{ROJO}Error: El ID ingresado no existe en la dulcería.{RESET}")
                pausar()
                continue

            # Bloquea la seleccion de productos agotados antes de pedir cantidad
            if snack.get_cantidad() <= 0:
                print(f"\n{ROJO}Lo sentimos, el snack '{snack.get_nombre()}' se encuentra agotado.{RESET}")
                pausar()
                continue

            # Usamos los GETTERS de la clase Snack
            print(f"\nSnack seleccionado: {NEGRITA}{snack.get_nombre()}{RESET}")
            print(f"Costo unitario: {VERDE}${snack.get_precio():.2f}{RESET} | Stock disponible: {snack.get_cantidad()}")

            # Bucle de validacion de cantidad para permitir corregir sin cancelar la operacion
            cantidad = None
            while True:
                entrada_cant = input("¿Cuántas unidades desea comprar? (0 para cancelar): ").strip()
                if entrada_cant == "0":
                    print(f"\n{AMARILLO}Compra cancelada.{RESET}")
                    pausar()
                    break
                try:
                    valor = int(entrada_cant)
                    if valor <= 0:
                        print(f"{ROJO}La cantidad debe ser mayor a cero.{RESET}")
                    elif valor > snack.get_cantidad():
                        print(f"{ROJO}Lo sentimos, solo hay {snack.get_cantidad()} unidades disponibles.{RESET}")
                    else:
                        cantidad = valor
                        break
                except ValueError:
                    print(f"{ROJO}Debe ingresar un número entero válido para la cantidad.{RESET}")

            if cantidad is None:
                continue

            total = round(cantidad * snack.get_precio(), 2)
            print(f"\nTotal a pagar: {VERDE}${total:.2f}{RESET}")

            # Bucle de confirmacion (s/n): ante entrada invalida vuelve a preguntar sin cancelar
            while True:
                confirmar = input(f"{AMARILLO}¿Desea proceder al pago? (s/n): {RESET}").strip().lower()
                if confirmar in ('s', 'si', 'sí'):
                    # 1. Usamos la pasarela de pago compartida
                    if procesar_pago(total):
                        # 2. Descontamos el stock usando set_cantidad() y get_cantidad()
                        stock_actualizado = snack.get_cantidad() - cantidad
                        snack.set_cantidad(stock_actualizado)

                        # 3. Sincronizamos el stock actualizado en el archivo stock.csv
                        if usar_disco:
                            guardar_snacks_en_csv(diccionario_snacks, ruta_objetivo)

                        # 4. Registramos la venta en el reporte general unificado
                        registrar_en_reporte("Dulce", snack.get_nombre(), cantidad, total)

                        print(f"\n{VERDE}¡Compra de dulces exitosa! Registrada en el reporte de métricas.{RESET}")
                    pausar()
                    break
                elif confirmar in ('n', 'no'):
                    print(f"\n{AMARILLO}Compra de dulces cancelada.{RESET}")
                    pausar()
                    break
                else:
                    print(f"{ROJO}Opción inválida. Por favor ingrese 's' para sí o 'n' para no.{RESET}")

        elif opcion == "4":
            print(f"\n{AMARILLO}Regresando al menú anterior...{RESET}")
            break
        else:
            # Muestra el error y pausa antes de limpiar la pantalla en la siguiente vuelta
            print(f"\n{ROJO}Opción no válida. Por favor, intente de nuevo.{RESET}")
            pausar()


def iniciar_programa():
    # 1. Al iniciar el modulo se carga automaticamente stock.csv sin sobrescribirlo innecesariamente
    diccionario_snacks = cargar_snacks_desde_csv(RUTA_STOCK_DEFECTO)

    # 2. Ejecuta el menu correspondiente al Rol 2 sincronizado con RUTA_STOCK_DEFECTO
    menu_snacks_usuario(diccionario_snacks, ruta_csv=RUTA_STOCK_DEFECTO)


if __name__ == "__main__":
    # Habilita codigos ANSI en terminales Windows al ejecutar de forma directa
    os.system("")
    iniciar_programa()
