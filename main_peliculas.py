from gestor_pelicula import GestorCine #importar para la clase cine
from pagos import procesar_pago
from pagos import registrar_en_reporte

#variables globales
# Colores ANSI
AZUL = "\033[94m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
RESET = "\033[0m"
NEGRITA = "\033[1m"

cine = GestorCine("peliculas.csv")

def ejecutar_menu_boleteria():
    """Gestiona la cartelera, selección de entradas, pago y guardado en métricas."""
    print(f"\n{AZUL}--- CARTELERA DE PELÍCULAS ---{RESET}")
    
    lista_de_peliculas = cine.listar_todas()
    for p in lista_de_peliculas:
        print(f"ID: {p.id} | {p.nombre} - Costo: ${p.costo:.2f} [{'Disponible' if p.disponibilidad else 'No disponible'}]")
        print("-" * 40)
    
    id_elegido = input(f"\n{AMARILLO}Ingrese el ID de la película que desea comprar: {RESET}").strip()
    pelicula = cine.buscar_por_id(id_elegido)
    
    if not pelicula:
        print(f"{ROJO}Error: El ID ingresado no existe.{RESET}")
        input("\nPresione Enter para continuar...")
        return

    if not pelicula.disponibilidad:
        print(f"{ROJO}Lo sentimos, esta película no está disponible en este momento.{RESET}")
        input("\nPresione Enter para continuar...")
        return

    print(f"\nPelícula seleccionada: {pelicula.nombre}")
    print(f"Costo por boleto: ${pelicula.costo:.2f}")
    
    try:
        cantidad = int(input("¿Cuántas entradas desea comprar?: "))
        if cantidad <= 0:
            print(f"{ROJO}La cantidad debe ser mayor a cero.{RESET}")
            input("\nPresione Enter para continuar...")
            return
    except ValueError:
        print(f"{ROJO}Debe ingresar un número entero válido.{RESET}")
        input("\nPresione Enter para continuar...")
        return

    total = cantidad * pelicula.costo
    print(f"Total a pagar: {VERDE}${total:.2f}{RESET}")
    
    confirmar = input(f"{AMARILLO}¿Desea proceder al pago? (s/n): {RESET}").strip().lower()
    
    if confirmar in ('s', 'si'):
        if procesar_pago(total):
            registrar_en_reporte("Boleto", pelicula.nombre, cantidad, total)
            print(f"\n{VERDE}¡Compra exitosa! Su entrada ha sido registrada en el reporte de métricas.{RESET}")
    else:
        print(f"{AMARILLO}Compra cancelada.{RESET}")

    input("\nPresione Enter para continuar...")