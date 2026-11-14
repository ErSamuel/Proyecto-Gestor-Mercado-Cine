# Archivo: main_rol2.py
# Punto de entrada para probar e integrar el Rol 2 (Estructura y Busqueda de Snacks)
import os
from pagos import procesar_pago, registrar_en_reporte
from gestor_snacks import (
    cargar_snacks_desde_csv,
    guardar_snacks_en_csv,
    mostrar_catalogo_snacks,
    buscar_snack
)
#variables globales
# Colores ANSI
AZUL = "\033[94m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
RESET = "\033[0m"
NEGRITA = "\033[1m"

# funcion para limpiar la pantalla
def limpiar_pantalla():
  os.system("cls" if os.name == "nt" else "clear")

def menu_snacks_usuario(diccionario_snacks):
    """Submenú del Rol 2 para consultar, buscar y comprar snacks."""
    while True:
        print(f"\n{AZUL}--- MENU DE DULCERIA ---{RESET}\n")
        print(f"{ROJO} 1. {RESET} Ver todos los snacks disponibles")
        print(f" {ROJO} 2. {RESET} Buscar un snack especifico (por nombre o ID)")
        print(f" {ROJO} 3. {RESET} Comprar un snack")  
        print(f" {ROJO} 4. {RESET} Volver al menu anterior")
        
        opcion = input("\nSelecciona una opcion (1-4): ").strip()
        limpiar_pantalla()
        if opcion == "1":
            mostrar_catalogo_snacks(diccionario_snacks)
        elif opcion == "2":
            buscar_snack(diccionario_snacks)
        elif opcion == "3":
            # --- FLUJO DE COMPRA DE DULCES CORREGIDO ---
            print("\n--- COMPRA DE SNACKS ---")
            mostrar_catalogo_snacks(diccionario_snacks)
            
            id_elegido = input("\nIngrese el ID del snack que desea comprar: ").strip()
            
            # Buscamos el snack en el diccionario
            snack = diccionario_snacks.get(id_elegido)
            
            if not snack:
                print("\nError: El ID ingresado no existe en la dulcería.")
            else:
                # Usamos los GETTERS de la clase Snack
                print(f"\nSnack seleccionado: {snack.get_nombre()}")
                print(f"Costo unitario: ${snack.get_precio():.2f} | Stock disponible: {snack.get_cantidad()}")
                
                try:
                    cantidad = int(input("¿Cuántas unidades desea comprar?: "))
                    if cantidad <= 0:
                        print("\nLa cantidad debe ser mayor a cero.")
                    elif cantidad > snack.get_cantidad():  # Usamos get_cantidad()
                        print(f"\nLo sentimos, solo hay {snack.get_cantidad()} unidades disponibles.")
                    else:
                        total = cantidad * snack.get_precio()  # Usamos get_precio()
                        print(f"Total a pagar: ${total:.2f}")
                        
                        confirmar = input("¿Desea proceder al pago? (s/n): ").strip().lower()
                        if confirmar in ('s', 'si'):
                            # 1. Usamos la pasarela de pago compartida
                            if procesar_pago(total):
                                
                                # 2. Descontamos el stock usando set_cantidad() y get_cantidad()
                                stock_actualizado = snack.get_cantidad() - cantidad
                                snack.set_cantidad(stock_actualizado)
                                
                                # 3. Sincronizamos el stock actualizado en el archivo stock.csv
                                guardar_snacks_en_csv(diccionario_snacks, "stock.csv")
                                
                                # 4. Registramos la venta en el reporte general unificado
                                registrar_en_reporte("Dulce", snack.get_nombre(), cantidad, total)
                                
                                print("\n¡Compra de dulces exitosa! Registrada en el reporte de métricas.")
                        else:
                            print("\nCompra de dulces cancelada.")
                except ValueError:
                    print("\nDebe ingresar un número entero válido para la cantidad.")
            
            input("\nPresione Enter para continuar...")
            
        elif opcion == "4":
            print("Regresando al menu anterior...")
            break
        else:
            print("Opcion no valida. Por favor, intente de nuevo.")

def iniciar_programa():
    # 1. Al iniciar el programa se carga automaticamente stock.csv en el diccionario
    diccionario_snacks = cargar_snacks_desde_csv("stock.csv")

    # Sincroniza los IDs hash generados con el archivo CSV
    guardar_snacks_en_csv(diccionario_snacks, "stock.csv")

    # 2. Ejecuta el menu correspondiente al Rol 2
    menu_snacks_usuario(diccionario_snacks)


if __name__ == "__main__":
    iniciar_programa()
