# Archivo: nucleo/consola.py
# Utilidades compartidas de interfaz en consola con validaciones estrictas y guardado CSV a prueba de bloqueos (PermissionError).

import csv
from datetime import datetime
import math
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
    input(f"\n{Colores.AMARILLO}{mensaje}{Colores.RESET}")


def confirmar_accion(mensaje):
    """
    Solicita confirmacion (s/n) en un bucle seguro.
    Ante entradas invalidas (como '0', letras o vacio), informa el error
    y vuelve a preguntar sin cancelar la operacion ni aceptar cualquier cosa.
    """
    while True:
        respuesta = input(f"{Colores.AMARILLO}{mensaje} (s/n): {Colores.RESET}").strip().lower()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print(f"{Colores.ROJO}Opción inválida. Por favor ingrese estrictamente 's' para sí o 'n' para no.{Colores.RESET}")


def mostrar_encabezado(titulo, ancho=57):
    """Imprime un banner uniforme centrado al ancho especificado."""
    borde = "=" * ancho
    print(f"\n{Colores.AZUL}{Colores.NEGRITA}{borde}")
    print(f"{titulo:^{ancho}}")
    print(f"{borde}{Colores.RESET}\n")


def conversor_de_minutos(minutos: float | int) -> str:
    """Convierte minutos a formato digital hh:mm:ss."""
    total_segundos = max(0, int(round(minutos * 60)))
    horas = total_segundos // 3600
    mins = (total_segundos % 3600) // 60
    segs = total_segundos % 60
    return f"{horas:02d}:{mins:02d}:{segs:02d}"


# =========================================================================
# VALIDADORES DE ENTRADA ROBUSTOS (A PRUEBA DE ENTRADAS ERRÓNEAS O '0')
# =========================================================================

def pedir_entero(mensaje, minimo=None, maximo=None, permitir_cancelar=False):
    """
    Solicita un numero entero validando limites estrictos.
    Rechaza letras, entradas vacias y valores fuera de rango en un bucle continuo.
    """
    while True:
        entrada = input(mensaje).strip()
        if permitir_cancelar and entrada.lower() in ("c", "cancelar"):
            return None
        try:
            valor = int(entrada)
            if minimo is not None and valor < minimo:
                print(f"{Colores.ROJO}Error: El valor no puede ser menor a {minimo}.{Colores.RESET}")
                continue
            if maximo is not None and valor > maximo:
                print(f"{Colores.ROJO}Error: El valor no puede ser mayor a {maximo}.{Colores.RESET}")
                continue
            return valor
        except ValueError:
            print(f"{Colores.ROJO}Error: Debe ingresar un número entero válido.{Colores.RESET}")


def pedir_flotante(mensaje, minimo=None, maximo=None, permitir_cancelar=False):
    """
    Solicita un numero decimal (precio) validando que sea finito y este en rango.
    Rechaza '0' si el minimo es mayor a cero, letras, negativos, nan e inf.
    """
    while True:
        entrada = input(mensaje).strip()
        if permitir_cancelar and entrada.lower() in ("c", "cancelar", "0"):
            return None
        try:
            entrada_normalizada = entrada.replace(",", ".")
            valor = float(entrada_normalizada)
            if not math.isfinite(valor):
                print(f"{Colores.ROJO}Error: Debe ingresar un valor numérico válido (no infinito ni indefinido).{Colores.RESET}")
                continue
            if minimo is not None and valor < minimo:
                print(f"{Colores.ROJO}Error: El valor debe ser mayor o igual a {minimo:.2f}.{Colores.RESET}")
                continue
            if maximo is not None and valor > maximo:
                print(f"{Colores.ROJO}Error: El valor no puede ser mayor a {maximo:.2f}.{Colores.RESET}")
                continue
            return round(valor, 2)
        except ValueError:
            print(f"{Colores.ROJO}Error: Debe ingresar un valor numérico válido (ej. 5.50).{Colores.RESET}")


# =========================================================================
# GESTOR DE PERSISTENCIA CSV A PRUEBA DE BLOQUEOS (EXCEL / PERMISSIONERROR)
# =========================================================================

def guardar_csv_seguro(ruta_archivo, campos, filas):
    """
    Escribe un archivo CSV de forma segura ante bloqueos de Windows (PermissionError).
    Si el archivo esta bloqueado (por ejemplo, abierto en Microsoft Excel),
    solicita al usuario cerrarlo y presionar Enter para reintentar,
    evitando que el programa aborte con un traceback no controlado.
    """
    carpeta = os.path.dirname(os.path.abspath(ruta_archivo))
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)

    while True:
        try:
            with open(ruta_archivo, mode="w", newline="", encoding="utf-8") as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=campos)
                escritor.writeheader()
                for fila in filas:
                    escritor.writerow(fila)
            return True
        except (PermissionError, OSError) as err:
            nombre = os.path.basename(ruta_archivo)
            print(f"\n{Colores.ROJO}[ERROR DE ACCESO / BLOQUEO] No se pudo guardar en '{nombre}': {err}{Colores.RESET}")
            print(f"{Colores.AMARILLO}El archivo parece estar abierto en Excel u otro programa.{Colores.RESET}")
            resp = input(f"{Colores.AMARILLO}Por favor ciérrelo y presione ENTER para reintentar (o '0' para cancelar sin guardar): {Colores.RESET}").strip().lower()
            if resp in ("0", "c", "cancelar"):
                print(f"{Colores.ROJO}Operación de guardado en disco cancelada.{Colores.RESET}")
                return False


def append_csv_seguro(ruta_archivo, campos, fila):
    """
    Agrega una fila al final de un CSV de forma segura ante bloqueos de archivo.
    """
    carpeta = os.path.dirname(os.path.abspath(ruta_archivo))
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)

    necesita_cabecera = (not os.path.exists(ruta_archivo)) or (os.path.getsize(ruta_archivo) == 0)
    while True:
        try:
            with open(ruta_archivo, mode="a", newline="", encoding="utf-8") as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=campos)
                if necesita_cabecera:
                    escritor.writeheader()
                    necesita_cabecera = False
                escritor.writerow(fila)
            return True
        except (PermissionError, OSError) as err:
            nombre = os.path.basename(ruta_archivo)
            print(f"\n{Colores.ROJO}[ERROR DE ACCESO / BLOQUEO] No se pudo registrar en '{nombre}': {err}{Colores.RESET}")
            print(f"{Colores.AMARILLO}El archivo probablemente esté abierto en Excel u otro visor.{Colores.RESET}")
            resp = input(f"{Colores.AMARILLO}Por favor ciérrelo y presione ENTER para reintentar (o '0' para cancelar): {Colores.RESET}").strip().lower()
            if resp in ("0", "c", "cancelar"):
                return False


def pedir_opcion_menu(mensaje, total_opciones, permitir_cero=False):
    """
    Obliga a elegir un numero dentro del rango de opciones del menu.
    Rechaza '0' (salvo que permitir_cero sea True), letras y opciones fuera de rango.
    """
    min_val = 0 if permitir_cero else 1
    while True:
        entrada = input(mensaje).strip()
        try:
            opcion = int(entrada)
            if min_val <= opcion <= total_opciones:
                return opcion
            print(f"{Colores.ROJO}Error: Opción inválida. Seleccione un número entre {min_val} y {total_opciones}.{Colores.RESET}")
        except ValueError:
            print(f"{Colores.ROJO}Error: Ingrese solo el número correspondiente a la opción.{Colores.RESET}")


def pedir_horario_valido(mensaje, permitir_cancelar=False):
    """
    Valida que el horario ingresado corresponda a una hora real y la formatea
    estandarizada en formato 'HH:MM AM/PM'.
    Rechaza estrictamente '0', letras arbitrarias o formatos no horarios.
    """
    formatos_aceptados = (
        "%I:%M %p", "%H:%M", "%I:%M%p", "%I %p", "%I%p"
    )
    while True:
        entrada = input(mensaje).strip()
        if permitir_cancelar and entrada.lower() in ("c", "cancelar", "0"):
            return None

        entrada_upper = entrada.upper()
        # Intentar parsear con cada patron aceptado
        for fmt in formatos_aceptados:
            try:
                dt = datetime.strptime(entrada_upper, fmt)
                # Formato final uniforme: ej. '04:00 PM'
                return dt.strftime("%I:%M %p")
            except ValueError:
                continue

        print(
            f"{Colores.ROJO}Error: Horario inválido. Ingrese una hora reconocible "
            f"(ej. '04:00 PM', '18:30', '5 pm').{Colores.RESET}"
        )


def pedir_texto_no_vacio(mensaje, min_len=2, max_len=60):
    """
    Solicita un texto asegurando que no este vacio, no sea puramente espacios
    y cumpla con una longitud minima y maxima.
    """
    while True:
        entrada = input(mensaje).strip()
        if len(entrada) < min_len:
            print(f"{Colores.ROJO}Error: El campo debe tener al menos {min_len} caracteres.{Colores.RESET}")
            continue
        if len(entrada) > max_len:
            print(f"{Colores.ROJO}Error: El campo no puede exceder {max_len} caracteres.{Colores.RESET}")
            continue
        return entrada
