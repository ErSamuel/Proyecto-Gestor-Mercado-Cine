# Archivo: main.py
# Punto de entrada principal del Sistema Gestor de Cine (Paso 2 - Organizacion por Mecanica).
import time
from boleteria.menu_boleteria import ejecutar_menu_boleteria
from boleteria.menu_admin import iniciar_modulo_cartelera_admin
from dulceria.menu_admin import iniciar_modulo_inventario
from dulceria.menu_cliente import iniciar_dulceria_cliente
from finanzas.reportes import ejecutar_menu_metricas
# Importa la clase Colores unificada desde su archivo dedicado
from nucleo.colores import Colores
from nucleo.consola import (
    habilitar_ansi,
    limpiar_pantalla,
    mostrar_encabezado,
    pausar
)
from config import PASSWORD_ADMIN 

def mostrar_menu():
    """Muestra el menu principal de seleccion de perfil."""
    print(f"{Colores.AZUL}{Colores.NEGRITA}=========================================================")
    print("|| ----------Bienvenido Al Menú de Navegación Del Sistema ------------||")
    print(f"========================================================={Colores.RESET}")
    print(f"{Colores.NEGRITA} {Colores.AMARILLO} Seleccione su tipo de usuario:{Colores.RESET}\n")
    print(f"  {Colores.VERDE}[1]{Colores.RESET} Usuario")
    print(f"  {Colores.VERDE}[2]{Colores.RESET} Administrador")
    print(f"  {Colores.ROJO}[3]{Colores.RESET} Salir\n")
    print(f"{Colores.AZUL}---------------------------------------------------------{Colores.RESET}")


def menu_usuario():
    """Imprime las opciones disponibles para el perfil Usuario."""
    print(f"  {Colores.VERDE}[1]{Colores.RESET} Dulcería")
    print(f"  {Colores.VERDE}[2]{Colores.RESET} Boletería")
    print(f"  {Colores.ROJO}[3]{Colores.RESET} Volver al menú principal\n")


def menu_admin():
    """Imprime las opciones disponibles para el perfil Administrador."""
    print(f"  {Colores.VERDE}[1]{Colores.RESET} Gestionar el inventario de la dulcería")
    print(f"  {Colores.VERDE}[2]{Colores.RESET} Gestionar la cartelera de películas")
    print(f"  {Colores.VERDE}[3]{Colores.RESET} Control y reportes")
    print(f"  {Colores.ROJO}[4]{Colores.RESET} Volver al menú principal\n")


def main():
    """Orquestador principal del sistema."""
    habilitar_ansi()

    while True:
        limpiar_pantalla()
        mostrar_menu()

        opcion = input("Ingrese una opción (1-3): ").strip()
        if len(opcion) != 1:
            print(f"{Colores.ROJO}\nLimite de caracteres superados. Intente una opcion valida. {Colores.RESET}\n")
            pausar()
            continue
        match opcion: 
            case "1": #menu para usuarios
                while True:
                    limpiar_pantalla()
                    mostrar_encabezado("MENÚ DE USUARIO", ancho=45)
                    menu_usuario()
                    opcion_usuario = input("Ingrese una de las opciones para continuar: ").strip()
                    if len(opcion_usuario) !=1:
                        print(f"{Colores.ROJO}\nLimite de caracteres superados. Intente una opcion valida. {Colores.RESET}\n")
                        pausar()
                        continue
                    if opcion_usuario == "1":
                        iniciar_dulceria_cliente()
                    elif opcion_usuario == "2":
                        ejecutar_menu_boleteria()
                    elif opcion_usuario == "3":
                        print(f"\n{Colores.AMARILLO}Saliendo al menú principal...{Colores.RESET}")
                        break
                    else:
                        print(f"\n{Colores.ROJO}Opción inválida{Colores.RESET}, por favor ingrese una opción entre 1 y 3.")
                        pausar()
            case "2": #menu administradores - se requiere contrasena
                intentos = 0
                while True:
                    limpiar_pantalla()
                    if(intentos==3):
                        print("\nNumero de intentos 3 -> volviendo al menu principal.\n")
                        pausar()
                        break
                    else:
                        MAX_LENT = 20
                        password = input("\nIngrese su contraseña: ")
                        if len(password) > MAX_LENT: #verifica que la contrasena no supere un maximo de tamano permitido
                            print(f"\n{Colores.ROJO}La contraseña no puede superar los {MAX_LENT} caracteres.{Colores.RESET}")
                            intentos += 1
                            pausar()
                            continue
                        if password == PASSWORD_ADMIN:
                            while True:
                                limpiar_pantalla()
                                print(f"\n{Colores.AMARILLO}{Colores.NEGRITA}------ Ha Ingresado Como Administrador Del Sistema --------{Colores.RESET}\n")
                                menu_admin()
                                opcion_admin = input("Ingrese una de las opciones para continuar: ").strip()
                                if opcion_admin == "1":
                                    iniciar_modulo_inventario()
                                elif opcion_admin == "2":
                                    # Rol 5: Gestion de Cartelera y Salas
                                    iniciar_modulo_cartelera_admin()
                                elif opcion_admin == "3":
                                    # Rol 6 reconectado hacia finanzas/reportes.py
                                    ejecutar_menu_metricas()
                                elif opcion_admin == "4":
                                    print(f"\n{Colores.AMARILLO}Saliendo al menú principal.{Colores.RESET}")
                                    break
                                else:
                                    print(f"\n{Colores.ROJO}La opción que ha ingresado no es correcta. Intente nuevamente.{Colores.RESET}")
                                    pausar()
                            break
                        else:
                            print("\nContraseña incorrecta intente nuevamente: ")
                            time.sleep(2)
                            intentos +=1
            case "3":
                limpiar_pantalla()
                print(f"{Colores.AMARILLO}Saliendo del programa. Gracias por preferir nuestros servicios, ¡le esperamos nuevamente!{Colores.RESET}")
                break
            case _:
                print(f"\n{Colores.ROJO}Opción inválida. Por favor, ingrese una opción entre 1 y 3.{Colores.RESET}")
                pausar()


if __name__ == "__main__":
    main()
