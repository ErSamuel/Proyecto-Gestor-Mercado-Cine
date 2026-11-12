
# menu principal
import os


def limpiar_pantalla():
  os.system("cls" if os.name == "nt" else "clear")

def mostrar_menu():
  # Colores ANSI
  AZUL = "\033[94m"
  VERDE = "\033[92m"
  AMARILLO = "\033[93m"
  ROJO = "\033[91m"
  RESET = "\033[0m"
  NEGRITA = "\033[1m"

  print(f"{AZUL}{NEGRITA}=========================================")
  print(f"|| -------------- Menu De Navegacion ------------------||")
  print(f"========================================================={RESET}")
  print(f"{NEGRITA}Seleccione su tipo de usuario:{RESET}\n")
  print(f"  {VERDE}[1]{RESET} User  (Usuario estandar)")
  print(f"  {AMARILLO}[2]{RESET} Seller (Vendedor)")
  print(f"  {AZUL}[3]{RESET} Admin  (Administrador)")
  print(f"  {ROJO}[4]{RESET} Salir\n")
  print(f"{AZUL}-----------------------------------------------------{RESET}")


def main():
  while True:
    limpiar_pantalla()
    mostrar_menu()

    opcion = input("Ingrese una opcion (1-4): ").strip()

    if opcion == "1":
      print("\nHas seleccionado la vista de: **User**")
      input("\nPresiona Enter para continuar...")
    elif opcion == "2":
      print("\nHas seleccionado la vista de: **Seller**")
      input("\nPresiona Enter para continuar...")
    elif opcion == "3":
      print("\nHas seleccionado la vista de: **Admin**")
      input("\nPresiona Enter para continuar...")
    elif opcion == "4":
      print("\nHasta luego! Saliendo del sistema...")
      break
    else:
      print("\nOpcion invalida. Por favor, elige un numero del 1 al 4.")
      input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
  main()