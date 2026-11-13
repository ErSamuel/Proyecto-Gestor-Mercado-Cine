from gestor_pelicula import GestorCine #importar para la clase cine

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
    """Maneja la visualización de películas, selección y compra de boletos."""
    print(f"\n{AZUL} Mostrando las peliculas disponibles... {RESET}\n")
    
    lista_de_peliculas = cine.listar_todas()
    
    for p in lista_de_peliculas:
        print(f"ID: {p.id} | {p.nombre} - Costo: ${p.costo:.2f} [{'Disponible' if p.disponibilidad else 'No disponible'}]")
        print("-" * 30)

    comprar = input("\n¿Desea comprar un boleto para alguna película? (s/n): ").strip().lower()
    
    if comprar in ('s', 'si'):
        id_ingresado = input("Ingrese el ID de la película que desea comprar: ").strip()
        
        pelicula_seleccionada = cine.buscar_por_id(id_ingresado)
        
        if pelicula_seleccionada:
            if not pelicula_seleccionada.disponibilidad:
                print(f"{ROJO}Lo sentimos, esta película no se encuentra disponible actualmente.{RESET}")
            else:
                print(f"\nPelícula seleccionada: {pelicula_seleccionada.nombre}")
                print(f"El costo del boleto es: ${pelicula_seleccionada.costo:.2f}")
                
                try:
                    monto_ingresado = float(input("Ingrese el monto con el que va a pagar: "))
                    
                    if monto_ingresado >= pelicula_seleccionada.costo:
                        cambio = monto_ingresado - pelicula_seleccionada.costo
                        
                        # Registramos la venta en el CSV mediante el gestor
                        cine.registrar_venta(pelicula_seleccionada)
                        
                        print(f"\n{VERDE}¡Compra exitosa! Disfrute su función.{RESET}")
                        if cambio > 0:
                            print(f"Su cambio es: ${cambio:.2f}")
                    else:
                        print(f"\n{ROJO}Monto insuficiente. La compra ha sido cancelada.{RESET}")
                
                except ValueError:
                    print(f"\n{ROJO}Error: Debe ingresar un valor numérico válido para el monto.{RESET}")
        else:
            print(f"\n{ROJO}No se encontró ninguna película con el ID ingresado.{RESET}")

    input("\nPresione Enter para continuar...")