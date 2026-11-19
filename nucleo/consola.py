# Archivo: nucleo/consola.py
# Utilidades compartidas de interfaz en consola (limpieza, pausas, confirmaciones y encabezados).
# Los colores se importan desde la clase centralizada nucleo.colores.Colores.

import os
from nucleo.colores import Colores


def habilitar_ansi():
    """Habilita el procesamiento de secuencias de escape ANSI en consolas Windows."""
    os.system("")


def limpiar_pantalla():
    """Limpia la terminal segun el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar(mensaje="Presione Enter para continuar..."):
    """Pausa la ejecucion para permitir leer mensajes o resultados en pantalla."""
    # Utiliza Colores.AMARILLO y Colores.RESET desde la clase Colores
    input(f"\n{Colores.AMARILLO}{mensaje}{Colores.RESET}")


def confirmar_accion(mensaje):
    """
    Solicita confirmacion (s/n) en un bucle seguro.
    Ante entradas invalidas informa el error y vuelve a preguntar sin cancelar la operacion.
    Retorna True si el usuario confirma ('s'/'si'/'sí') o False si cancela ('n'/'no').
    """
    while True:
        respuesta = input(f"{Colores.AMARILLO}{mensaje} (s/n): {Colores.RESET}").strip().lower()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print(f"{Colores.ROJO}Opción inválida. Por favor ingrese 's' para sí o 'n' para no.{Colores.RESET}")


def mostrar_encabezado(titulo, ancho=57):
    """Imprime un banner uniforme centrado al ancho especificado."""
    borde = "=" * ancho
    print(f"\n{Colores.AZUL}{Colores.NEGRITA}{borde}")
    print(f"{titulo:^{ancho}}")
    print(f"{borde}{Colores.RESET}\n")
