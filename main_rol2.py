# Archivo: main_rol2.py
# Punto de entrada para probar e integrar el Rol 2 (Estructura y Busqueda de Snacks)

from gestor_snacks import (
    cargar_snacks_desde_csv,
    guardar_snacks_en_csv,
    mostrar_catalogo_snacks,
    buscar_snack
)


def menu_snacks_usuario(diccionario_snacks):
    """Submenu del Rol 2 para que el cliente consulte y busque snacks."""
    while True:
        print("\n--- MENU DE DULCERIA (CONSULTA DE USUARIO) ---")
        print("1. Ver todos los snacks disponibles")
        print("2. Buscar un snack especifico (por nombre o ID)")
        print("3. Volver al menu anterior")

        opcion = input("Seleccione una opcion (1-3): ").strip()

        if opcion == "1":
            mostrar_catalogo_snacks(diccionario_snacks)
        elif opcion == "2":
            buscar_snack(diccionario_snacks)
        elif opcion == "3":
            print("Regresando al menu principal...")
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
