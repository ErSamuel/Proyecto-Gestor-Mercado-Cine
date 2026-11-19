# menu principal
import os
# importar el modulo para el rol 2
from main_rol2 import iniciar_programa
# importar el modulo de peliculas / boleteria
from main_peliculas import ejecutar_menu_boleteria
# importar el modulo para el rol 4 (Gestion de Inventario de Dulceria)
from main_rol4 import iniciar_modulo_inventario

# variables globales
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


def pausar():
  """Pausa la ejecución para que el usuario pueda leer los mensajes antes de limpiar."""
  input(f"\n{AMARILLO}Presione Enter para continuar...{RESET}")


def mostrar_menu():
  # Banner alineado exactamente a 57 caracteres de ancho
  print(f"{AZUL}{NEGRITA}=========================================================")
  print("|| ---------------- Menú de Navegación ----------------||")
  print(f"========================================================={RESET}")
  print(f"{NEGRITA}Seleccione su tipo de usuario:{RESET}\n")
  print(f"  {VERDE}[1]{RESET} Usuario")
  print(f"  {VERDE}[2]{RESET} Administrador")
  print(f"  {ROJO}[3]{RESET} Salir\n")
  print(f"{AZUL}---------------------------------------------------------{RESET}")


def menu_usuario():
  # Formato uniforme y tabulacion consistente en opciones de Usuario
  print(f"  {VERDE}[1]{RESET} Dulcería")
  print(f"  {VERDE}[2]{RESET} Boletería")
  print(f"  {ROJO}[3]{RESET} Volver al menú principal\n")


def menu_admin():
  # Formato uniforme y colores consistentes (acciones en verde, salida en rojo)
  print(f"  {VERDE}[1]{RESET} Gestionar el inventario de la dulcería")
  print(f"  {VERDE}[2]{RESET} Gestionar la cartelera de películas")
  print(f"  {VERDE}[3]{RESET} Control y reportes")
  print(f"  {ROJO}[4]{RESET} Volver al menú principal\n")


# funcion principal del codigo - punto de partida
def main():
  # Habilita secuencias de escape ANSI en consolas de Windows
  os.system("")

  while True:
    limpiar_pantalla()
    mostrar_menu()

    opcion = input("Ingrese una opción (1-3): ").strip()
    match opcion:
        case '1':
            while True:
                # Limpia la pantalla al comienzo del ciclo para no borrar mensajes previos sin pausa
                limpiar_pantalla()
                print(f"\n{AZUL}{NEGRITA}=========================================")
                print("            MENÚ DE USUARIO              ")
                print(f"========================================={RESET}\n")
                menu_usuario()
                opcion_usuario = input("Ingrese una de las opciones para continuar: ").strip()
                if opcion_usuario == '1':  # mostrar la informacion para la dulceria
                    iniciar_programa()
                elif opcion_usuario == '2':
                    # boleteria
                    ejecutar_menu_boleteria()
                elif opcion_usuario == '3':
                    print(f"\n{AMARILLO}Saliendo al menú principal...{RESET}")
                    break
                else:
                    # Pausa para que el usuario pueda leer el error antes de limpiar la pantalla
                    print(f"\n{ROJO}Opción inválida{RESET}, por favor ingrese una opción entre 1 y 3.")
                    pausar()
        case '2':
          while True:
             # Limpia la pantalla antes de imprimir el banner para que sea visible
             limpiar_pantalla()
             print(f"\n{AMARILLO}{NEGRITA}------ Ha Ingresado Como Administrador Del Sistema --------{RESET}\n")
             menu_admin()
             opcion_admin = input("Ingrese una de las opciones para continuar: ").strip()
             if opcion_admin == '1':
                # Rol 4: Gestion del Inventario de la Dulceria
                iniciar_modulo_inventario()
             elif opcion_admin == '2':
                # Aviso informativo mientras se implementa el Rol 5 en bloques posteriores
                print(f"\n{AMARILLO}[INFO] El módulo 'Gestión de Cartelera' (Rol 5) aún está pendiente de implementación.{RESET}")
                pausar()
             elif opcion_admin == '3':
                # Aviso informativo mientras se implementa el Rol 6 en bloques posteriores
                print(f"\n{AMARILLO}[INFO] El módulo 'Control y Reportes' (Rol 6) aún está pendiente de implementación.{RESET}")
                pausar()
             elif opcion_admin == '4':
                print(f"\n{AMARILLO}Saliendo al menú principal.{RESET}")
                break
             else:
                # Pausa tras el error para que no desaparezca al redibujar el menu
                print(f"\n{ROJO}La opción que ha ingresado no es correcta. Intente nuevamente.{RESET}")
                pausar()

        case '3':
          limpiar_pantalla()
          # La persistencia ya se realiza en tiempo real en cada operacion
          print(f"{AMARILLO}Saliendo del programa. Gracias por preferir nuestros servicios, ¡le esperamos nuevamente!{RESET}")
          break

        case _:
          # Captura opciones invalidas del menu principal que antes se ignoraban en silencio
          print(f"\n{ROJO}Opción inválida. Por favor, ingrese una opción entre 1 y 3.{RESET}")
          pausar()


if __name__ == "__main__":
  main()
