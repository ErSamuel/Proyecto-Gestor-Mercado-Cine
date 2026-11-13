# Archivo: main_rol3.py
# Gestiona la cartelera, ver salas, compra de entradas y pago (Rol 3) con colores ANSI

from modelo_pelicula import Pelicula

# Colores ANSI (importados conceptualmente del main o definidos aquí para independencia del módulo)
AZUL = "\033[94m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
RESET = "\033[0m"
NEGRITA = "\033[1m"

def cargar_cartelera_inicial():
    """Retorna un diccionario con películas de ejemplo en cartelera."""
    cartelera = {
        "PEL-01": Pelicula("PEL-01", "Avatar: El Camino del Agua", "04:00 PM", "Sala 2", 5.00, 40),
        "PEL-02": Pelicula("PEL-02", "Spider-Man: Across the Spider-Verse", "07:00 PM", "Sala 1", 5.00, 25),
        "PEL-03": Pelicula("PEL-03", "Interestelar (Reestreno)", "09:30 PM", "Sala 3", 5.00, 15)
    }
    return cartelera

def ver_salas_y_cartelera(cartelera):
    """Muestra las salas y películas disponibles con formato de colores."""
    print("\n" + AZUL + "=" * 78 + RESET)
    print(f"{NEGRITA}{VERDE}                    CARTELERA Y SALAS DISPONIBLES{RESET}")
    print(AZUL + "=" * 78 + RESET)
    for id_pel, pelicula in cartelera.items():
        print(f"{AMARILLO}ID: {pelicula.get_id()}{RESET} | Película: {NEGRITA}{pelicula.get_titulo()}{RESET} | Horario: {pelicula.get_horario()} | Sala: {AZUL}{pelicula.get_sala()}{RESET} | Precio: {VERDE}${pelicula.get_precio():.2f}{RESET} | Asientos Libres: {pelicula.get_asientos()}")
    print(AZUL + "=" * 78 + RESET)

def procesar_pago(total_a_pagar):
    """Simula el proceso de pago con avisos coloridos."""
    print(f"\n{AMARILLO}--- PASARELA DE PAGO ---{RESET}")
    print(f"Total a cancelar: {VERDE}${total_a_pagar:.2f}{RESET}")
    print(f"{AZUL}[1]{RESET} Pago Móvil / Tarjeta de Débito")
    print(f"{AZUL}[2]{RESET} Efectivo en taquilla")
    
    metodo = input("Seleccione método de pago (1 o 2): ").strip()
    if metodo in ["1", "2"]:
        print(f"\n{VERDE}¡Pago procesado con éxito! Generando sus entradas...{RESET}")
        return True
    else:
        print(f"\n{ROJO}Método de pago inválido. Operación cancelada.{RESET}")
        return False

def comprar_entradas(cartelera):
    """Gestiona la compra de boletos y actualización de asientos."""
    ver_salas_y_cartelera(cartelera)
    
    id_elegido = input(f"\n{AMARILLO}Ingrese el ID de la película que desea ver (ej. PEL-01): {RESET}").strip().upper()
    
    if id_elegido not in cartelera:
        print(f"{ROJO}Error: El ID de la película no existe en la cartelera.{RESET}")
        return

    pelicula = cartelera[id_elegido]
    
    try:
        cantidad = int(input(f"¿Cuántas entradas desea para '{pelicula.get_titulo()}'?: "))
        if cantidad <= 0:
            print(f"{ROJO}La cantidad debe ser mayor a cero.{RESET}")
            return
        
        if cantidad > pelicula.get_asientos():
            print(f"{ROJO}Lo sentimos, solo quedan {pelicula.get_asientos()} asientos disponibles.{RESET}")
            return
            
    except ValueError:
        print(f"{ROJO}Por favor, ingrese un número válido.{RESET}")
        return

    total = cantidad * pelicula.get_precio()
    print(f"\n{NEGRITA}Resumen de compra:{RESET}")
    print(f"- Película: {pelicula.get_titulo()} ({pelicula.get_horario()} - {pelicula.get_sala()})")
    print(f"- Entradas: {cantidad}")
    print(f"- Total a pagar: {VERDE}${total:.2f}{RESET}")
    
    confirmar = input(f"{AMARILLO}¿Desea proceder al pago? (s/n): {RESET}").strip().lower()
    if confirmar == 's':
        if procesar_pago(total):
            # Actualizamos el stock de asientos de la película
            nuevo_stock = pelicula.get_asientos() - cantidad
            pelicula.set_asientos(nuevo_stock)
            print(f"\n{VERDE}¡Disfrute su función! Sus asientos han sido reservados.{RESET}")
    else:
        print(f"{AMARILLO}Compra cancelada.{RESET}")

def iniciar_modulo_boleteria():
    """Función principal del Rol 3 con menú en colores."""
    cartelera = cargar_cartelera_inicial()
    
    while True:
        print(f"\n{AZUL}--- MENÚ DE BOLETERÍA ---{RESET}")
        print(f"{VERDE}[1]{RESET} Ver salas y cartelera")
        print(f"{AMARILLO}[2]{RESET} Comprar entradas")
        print(f"{ROJO}[3]{RESET} Volver al menú principal")
        
        opcion = input("Seleccione una opción (1-3): ").strip()
        
        if opcion == "1":
            ver_salas_y_cartelera(cartelera)
        elif opcion == "2":
            comprar_entradas(cartelera)
        elif opcion == "3":
            print(f"{AMARILLO}Regresando al menú principal...{RESET}")
            break
        else:
            print(f"{ROJO}Opción inválida. Por favor, intente de nuevo.{RESET}")