import os
from gestor_pelicula import GestorCine  # importar para la clase cine
from pagos import procesar_pago, registrar_en_reporte

# Limite maximo de boletos permitidos por transaccion para proteger la capacidad de sala
LIMITE_BOLETOS_POR_COMPRA = 10

# variables globales
# Colores ANSI
AZUL = "\033[94m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
RESET = "\033[0m"
NEGRITA = "\033[1m"


def limpiar_pantalla():
    """Limpia la pantalla de la terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input(f"\n{AMARILLO}Presione Enter para continuar...{RESET}")


def ejecutar_menu_boleteria():
    """Gestiona la cartelera, selección de entradas, pago y guardado en métricas."""
    # Instancia GestorCine al entrar al modulo para recargar cambios recientes del CSV
    cine = GestorCine()

    # Valida existencia fisica del archivo de peliculas antes de mostrar el menu
    if not os.path.exists(cine.ruta_csv):
        limpiar_pantalla()
        print(f"{ROJO}Error: No se encontró el archivo de cartelera '{cine.ruta_csv}'.{RESET}")
        pausar()
        return

    lista_de_peliculas = cine.listar_todas()
    if not lista_de_peliculas:
        limpiar_pantalla()
        print(f"{ROJO}No hay películas registradas en la cartelera en este momento.{RESET}")
        pausar()
        return

    # Bucle principal de seleccion en boleteria para reintentar sin salir abruptamente
    while True:
        limpiar_pantalla()
        print(f"\n{AZUL}{NEGRITA}--- CARTELERA DE PELÍCULAS ---{RESET}\n")

        # Muestra las peliculas numeradas sin exponer la casilla ID al cliente
        for indice, p in enumerate(lista_de_peliculas, start=1):
            if p.disponibilidad > 0:
                estado_str = f"{VERDE}[Disponible: {p.disponibilidad} asientos]{RESET}"
            else:
                estado_str = f"{ROJO}[Agotada / No disponible]{RESET}"
            print(f"  {VERDE}[{indice}]{RESET} {NEGRITA}{p.nombre}{RESET} ({p.duracion} min) - Boleto: ${p.costo:.2f} {estado_str}")
            print("  " + "-" * 65)

        print(f"  {ROJO}[0]{RESET} Volver al menú anterior\n")

        opcion = input(f"{AMARILLO}Seleccione el número de la película que desea comprar (0 para volver): {RESET}").strip()
        if opcion == "0":
            return

        try:
            indice_elegido = int(opcion)
            if not (1 <= indice_elegido <= len(lista_de_peliculas)):
                print(f"{ROJO}Error: Seleccione una opción válida entre 0 y {len(lista_de_peliculas)}.{RESET}")
                pausar()
                continue
        except ValueError:
            print(f"{ROJO}Error: Debe ingresar un número entero válido.{RESET}")
            pausar()
            continue

        pelicula = lista_de_peliculas[indice_elegido - 1]

        # Verifica disponibilidad real en asientos antes de pedir cantidad
        if pelicula.disponibilidad <= 0:
            print(f"{ROJO}Lo sentimos, la función '{pelicula.nombre}' está agotada o no disponible.{RESET}")
            pausar()
            continue

        max_permitido = min(LIMITE_BOLETOS_POR_COMPRA, pelicula.disponibilidad)
        print(f"\nPelícula seleccionada: {NEGRITA}{pelicula.nombre}{RESET}")
        print(f"Costo por boleto: {VERDE}${pelicula.costo:.2f}{RESET} | Asientos disponibles: {pelicula.disponibilidad}")
        print(f"Límite máximo por compra: {max_permitido} boletos")

        # Bucle de validacion para la cantidad de boletos
        cantidad = None
        while True:
            entrada_cant = input("¿Cuántas entradas desea comprar? (0 para cancelar): ").strip()
            if entrada_cant == "0":
                print(f"{AMARILLO}Selección cancelada.{RESET}")
                pausar()
                break
            try:
                valor = int(entrada_cant)
                if valor <= 0:
                    print(f"{ROJO}La cantidad debe ser mayor a cero.{RESET}")
                elif valor > LIMITE_BOLETOS_POR_COMPRA:
                    print(f"{ROJO}Límite excedido: máximo {LIMITE_BOLETOS_POR_COMPRA} boletos por compra.{RESET}")
                elif valor > pelicula.disponibilidad:
                    print(f"{ROJO}Lo sentimos, solo quedan {pelicula.disponibilidad} asientos disponibles.{RESET}")
                else:
                    cantidad = valor
                    break
            except ValueError:
                print(f"{ROJO}Debe ingresar un número entero válido.{RESET}")

        if cantidad is None:
            continue

        total = round(cantidad * pelicula.costo, 2)
        print(f"\nTotal a pagar: {VERDE}${total:.2f}{RESET}")

        # Bucle de confirmacion (s/n): ante una opcion invalida vuelve a preguntar sin cancelar
        while True:
            confirmar = input(f"{AMARILLO}¿Desea proceder al pago? (s/n): {RESET}").strip().lower()
            if confirmar in ('s', 'si', 'sí'):
                if procesar_pago(total):
                    # Descuenta los asientos ocupados y guarda en CSV al instante
                    pelicula.disponibilidad = pelicula.disponibilidad - cantidad
                    cine.guardar_catalogo_en_csv()
                    registrar_en_reporte("Boleto", pelicula.nombre, cantidad, total)
                    print(f"\n{VERDE}¡Compra exitosa! Quedan {pelicula.disponibilidad} asientos para '{pelicula.nombre}'.{RESET}")
                pausar()
                return
            elif confirmar in ('n', 'no'):
                print(f"{AMARILLO}Compra cancelada.{RESET}")
                pausar()
                break
            else:
                print(f"{ROJO}Opción inválida. Por favor ingrese 's' para continuar o 'n' para cancelar.{RESET}")