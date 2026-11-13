
# menu principal
import os
#importar el modulo para el rol 2
from main_rol2 import iniciar_programa
#importar el modulo para el rol 3
from main_rol3 import iniciar_modulo_boleteria

#variables globales
# Colores ANSI
AZUL = "\033[94m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
RESET = "\033[0m"
NEGRITA = "\033[1m"
#funcion para limpiar la pantalla
def limpiar_pantalla():
  os.system("cls" if os.name == "nt" else "clear")

def mostrar_menu():
  
  print(f"{AZUL}{NEGRITA}=========================================")
  print(f"|| -------------- Menu De Navegacion ------------------||")
  print(f"========================================================={RESET}")
  print(f"{NEGRITA}Seleccione su tipo de usuario:{RESET}\n")
  print(f"  {VERDE}[1]{RESET} USUARIO)")
  print(f"  {AZUL}[2]{RESET} ADMINISTRADOR")
  print(f"  {ROJO}[3]{RESET} Salir\n")
  print(f"{AZUL}-----------------------------------------------------{RESET}")

def menu_usuario():
  print(f"1: {VERDE} DULCERIA {RESET}\n")
  print(f"2. {AMARILLO} BOLETERIA {RESET} \n")
  print(f"3. {ROJO}  SALIR {RESET}\n")

def menu_admin():
   print(f"\n1. {AZUL} Gestionar El Inventario De La Dulceria. {RESET} \n")
   print(f"\n2. {AZUL} Gestionar La Cartelera De Peliculas. {RESET} \n")
   print(f"\n3. {AZUL} Control y Reportes. {RESET} \n")
   print(f"\n4. {ROJO} Salir al menu principal. {RESET} \n")
#funcion principal del codigo - punto de partida
def main():
  while True:
    limpiar_pantalla()
    mostrar_menu()

    opcion = input("Ingrese una opcion (1-3): ").strip()

    match opcion:
        case '1':
            while True:
                print(f"\n{AZUL} ------ BIENVENIDO  ------- {RESET}\n")
                menu_usuario()
                opcion_usuario = input("Ingrese una de las opciones para continuar: ").strip()
                limpiar_pantalla()
                if opcion_usuario == '1': #mostrar la informacion para la dulceria
                    iniciar_programa()
                elif opcion_usuario == '2':
                   #boleteria (rol3)
                   iniciar_modulo_boleteria()
                elif opcion_usuario =='3':
                    print("\nSaliendo al Menu Principal ...\n")
                    break
                else:
                   print(f"{ROJO} \nOpcion invalida {RESET}, por favor ingrese una opcion nuevamente.")
                limpiar_pantalla()
        case '2':
          while True:
             print(f"\n{AMARILLO} ------ Ha Ingresado Como Administrador Del Sistema -------- {RESET}")
             limpiar_pantalla()
             menu_admin()
             opcion_admin = input("\nIngrese una de las opciones para continuar: ").strip()
             if opcion_admin == '1': 
                pass
             elif opcion_admin == '2':
                pass 
             elif opcion_admin == '3':
                pass
             elif opcion_admin == '4':
                print(f"{AMARILLO} Saliendo al menu principal.{RESET}")
                break
             else:
                print("\nLa opcion que ha ingresado no es correcta. Intente nuevamente.\n ")

        case '3':
          print(f"{AMARILLO} Saliendo del programa, Gracias por preferir nuestro servicios, le esperamos nuevamente !{RESET}")
          break
            
if __name__ == "__main__":
  main()