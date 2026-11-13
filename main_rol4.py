# Archivo: main_rol4.py
# Modulo correspondiente al ROL 4: Gestion del Inventario de la Dulceria (Administrador)
# Permite agregar productos, modificar precios, actualizar stock y eliminar productos.
# Todas las modificaciones se realizan sobre la estructura en memoria (diccionario de objetos Snack).
# El guardado en archivo (stock.csv) se realiza unicamente al finalizar el programa.

import os
import atexit
from modelo_snack import Snack
from gestor_snacks import (
    generar_id_hash,
    cargar_snacks_desde_csv,
    guardar_snacks_en_csv
)

# Constantes para estilos y colores ANSI en consola
AZUL = "\033[94m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
NEGRITA = "\033[1m"

# Variable global a nivel de modulo para mantener el diccionario de objetos Snack en memoria
_inventario_snacks = None


def obtener_inventario():
    """
    Retorna el diccionario de snacks cargado en memoria.
    Si aun no ha sido cargado desde stock.csv, lo inicializa y carga.
    Clave: ID Hash (str) -> Valor: Objeto de tipo Snack.
    """
    global _inventario_snacks
    if _inventario_snacks is None:
        _inventario_snacks = cargar_snacks_desde_csv("stock.csv")
    return _inventario_snacks


def guardar_inventario_final():
    """
    Guarda el estado final del diccionario de snacks en el archivo stock.csv.
    Esta funcion esta registrada para ejecutarse al cerrar el programa,
    cumpliendo con la instruccion de persistir solo al finalizar.
    """
    global _inventario_snacks
    if _inventario_snacks is not None:
        guardar_snacks_en_csv(_inventario_snacks, "stock.csv")
        print(f"\n{VERDE}[INFO] Inventario de dulceria guardado exitosamente en stock.csv.{RESET}")


# Registrar guardado automatico al finalizar el proceso de Python
atexit.register(guardar_inventario_final)


def limpiar_pantalla():
    """Limpia la terminal segun el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Pausa la ejecucion para permitir la lectura del usuario."""
    input(f"\n{AMARILLO}Presione ENTER para continuar...{RESET}")


def listar_inventario_completo(diccionario_snacks):
    """
    Muestra en pantalla una tabla con todos los snacks registrados en el diccionario,
    incluyendo agotados, precios y cantidades.
    """
    print(f"\n{AZUL}{NEGRITA}" + "=" * 85 + f"{RESET}")
    print(f"{CYAN}{NEGRITA}{'INVENTARIO GENERAL DE DULCERÍA (VISTA ADMINISTRADOR)':^85}{RESET}")
    print(f"{AZUL}{NEGRITA}" + "=" * 85 + f"{RESET}")

    if not diccionario_snacks:
        print(f"{ROJO}No hay ningun producto registrado en el inventario.{RESET}")
        print(f"{AZUL}" + "-" * 85 + f"{RESET}")
        return

    # Encabezado de columnas
    encabezado = f"{'ID':<10} | {'PRODUCTO':<25} | {'PRECIO':<10} | {'STOCK':<8} | {'DESCRIPCIÓN'}"
    print(f"{NEGRITA}{encabezado}{RESET}")
    print(f"{AZUL}" + "-" * 85 + f"{RESET}")

    for id_hash, snack in diccionario_snacks.items():
        cant = snack.get_cantidad()
        color_stock = VERDE if cant > 5 else (AMARILLO if cant > 0 else ROJO)
        stock_str = f"{color_stock}{cant:>5} uds{RESET}"
        precio_str = f"${snack.get_precio():.2f}"
        
        # Recortar descripcion si es muy larga para la tabla
        desc = snack.get_descripcion()
        if len(desc) > 30:
            desc = desc[:27] + "..."

        print(f"{AMARILLO}{snack.get_id_snack():<10}{RESET} | "
              f"{NEGRITA}{snack.get_nombre():<25}{RESET} | "
              f"{VERDE}{precio_str:<10}{RESET} | "
              f"{stock_str:<17} | "
              f"{desc}")

    print(f"{AZUL}{NEGRITA}" + "=" * 85 + f"{RESET}")


def localizar_snack(diccionario_snacks):
    """
    Funcion auxiliar para buscar y seleccionar un snack por ID o coincidencia de nombre.
    Retorna la clave (id_hash) del snack seleccionado o None si se cancela.
    """
    criterio = input(f"\n{AMARILLO}Ingrese el ID o nombre del producto a gestionar: {RESET}").strip()
    if not criterio:
        print(f"{ROJO}Debe ingresar un valor valido.{RESET}")
        return None

    # 1. Busqueda por clave hash exacta o ID directo
    posible_hash = generar_id_hash(criterio)
    if posible_hash in diccionario_snacks:
        return posible_hash
    
    # Comprobar coincidencia exacta con mayusculas del ID (ej. SNK-743)
    criterio_upper = criterio.upper()
    if criterio_upper in diccionario_snacks:
        return criterio_upper

    # 2. Busqueda por coincidencia parcial en nombre o ID
    coincidencias = []
    criterio_lower = criterio.lower()
    for id_clave, snack in diccionario_snacks.items():
        if (criterio_lower in snack.get_nombre().lower() or 
                criterio_lower == id_clave.lower()):
            coincidencias.append(id_clave)

    if len(coincidencias) == 1:
        return coincidencias[0]
    elif len(coincidencias) > 1:
        print(f"\n{AMARILLO}Se encontraron multiples coincidencias:{RESET}")
        for i, id_c in enumerate(coincidencias, start=1):
            snk = diccionario_snacks[id_c]
            print(f"  [{i}] ID: {id_c} - {snk.get_nombre()} (${snk.get_precio():.2f})")
        
        seleccion = input("Seleccione el numero correspondiente (o 'c' para cancelar): ").strip()
        if seleccion.lower() == 'c':
            return None
        try:
            indice = int(seleccion) - 1
            if 0 <= indice < len(coincidencias):
                return coincidencias[indice]
            else:
                print(f"{ROJO}Indice fuera de rango.{RESET}")
                return None
        except ValueError:
            print(f"{ROJO}Opcion invalida.{RESET}")
            return None

    print(f"{ROJO}No se encontro ningun producto que coincida con '{criterio}'.{RESET}")
    return None


# =========================================================================
# ASIGNACIONES ESPECIFICAS DEL ROL 4: ADMINISTRACION DEL INVENTARIO
# =========================================================================

def agregar_nuevo_dulce(diccionario_snacks):
    """
    Paso 1 del Rol 4: Agregar un nuevo dulce/snack al sistema.
    Crea el objeto Snack con su ID hash generado y lo inserta en el diccionario.
    """
    print(f"\n{CYAN}{NEGRITA}--- AGREGAR NUEVO PRODUCTO AL INVENTARIO ---{RESET}")
    
    nombre = input("Nombre del dulce/snack: ").strip()
    if not nombre:
        print(f"{ROJO}Error: El nombre no puede estar vacio.{RESET}")
        return

    # Comprobar si ya existe un producto con el mismo nombre o hash
    id_generado = generar_id_hash(nombre)
    if id_generado in diccionario_snacks:
        snack_existente = diccionario_snacks[id_generado]
        print(f"{ROJO}Error: Ya existe un producto con un identificador identico ({id_generado}):{RESET}")
        print(f"Producto existente: {snack_existente.get_nombre()}")
        print(f"{AMARILLO}Si desea actualizarlo, utilice las opciones de modificar precio o stock.{RESET}")
        return

    descripcion = input("Descripcion del producto: ").strip()
    if not descripcion:
        descripcion = "Sin descripcion adicional"

    # Validacion del precio
    try:
        precio_input = input("Precio en dolares ($): ").strip()
        precio = float(precio_input)
        if precio < 0:
            print(f"{ROJO}Error: El precio no puede ser negativo.{RESET}")
            return
    except ValueError:
        print(f"{ROJO}Error: Ingrese un valor numerico valido para el precio.{RESET}")
        return

    # Validacion de la cantidad inicial
    try:
        cantidad_input = input("Cantidad inicial en stock: ").strip()
        cantidad = int(cantidad_input)
        if cantidad < 0:
            print(f"{ROJO}Error: La cantidad no puede ser negativa.{RESET}")
            return
    except ValueError:
        print(f"{ROJO}Error: Ingrese un numero entero valido para la cantidad.{RESET}")
        return

    # Creacion del nuevo objeto de la clase Snack
    nuevo_snack = Snack(
        id_snack=id_generado,
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        cantidad=cantidad
    )

    # Insercion directa en la estructura en memoria (diccionario de tipo Snack)
    diccionario_snacks[id_generado] = nuevo_snack

    print(f"\n{VERDE}{NEGRITA}¡Producto agregado exitosamente a la estructura en memoria!{RESET}")
    print(f"ID Asignado: {AMARILLO}{id_generado}{RESET} | {nombre} | Stock: {cantidad} | Precio: ${precio:.2f}")


def modificar_precio_dulce(diccionario_snacks):
    """
    Paso 2 del Rol 4: Modificar el precio de un dulce existente.
    Utiliza el setter 'set_precio' definido en la clase Snack.
    """
    print(f"\n{CYAN}{NEGRITA}--- MODIFICAR PRECIO DE PRODUCTO ---{RESET}")
    id_snack = localizar_snack(diccionario_snacks)
    if not id_snack:
        return

    snack = diccionario_snacks[id_snack]
    print(f"\nProducto: {NEGRITA}{snack.get_nombre()}{RESET} (ID: {snack.get_id_snack()})")
    print(f"Precio actual: {VERDE}${snack.get_precio():.2f}{RESET}")

    try:
        nuevo_precio_str = input("\nIngrese el nuevo precio ($): ").strip()
        nuevo_precio = float(nuevo_precio_str)
        if nuevo_precio < 0:
            print(f"{ROJO}Error: El precio no puede ser menor a cero.{RESET}")
            return

        # Modificacion sobre la estructura mediante el setter
        snack.set_precio(nuevo_precio)
        print(f"\n{VERDE}{NEGRITA}¡Precio actualizado exitosamente a ${nuevo_precio:.2f}!{RESET}")

    except ValueError:
        print(f"{ROJO}Error: Ingrese un valor numerico valido.{RESET}")


def actualizar_stock_dulce(diccionario_snacks):
    """
    Paso 3 del Rol 4: Actualizar las existencias en inventario.
    Permite fijar una nueva cantidad o sumar/restar unidades.
    Utiliza el setter 'set_cantidad' de la clase Snack.
    """
    print(f"\n{CYAN}{NEGRITA}--- ACTUALIZAR STOCK DE PRODUCTO ---{RESET}")
    id_snack = localizar_snack(diccionario_snacks)
    if not id_snack:
        return

    snack = diccionario_snacks[id_snack]
    cantidad_actual = snack.get_cantidad()
    print(f"\nProducto: {NEGRITA}{snack.get_nombre()}{RESET} (ID: {snack.get_id_snack()})")
    print(f"Stock actual: {AMARILLO}{cantidad_actual} unidades{RESET}")

    print("\nOpciones de actualizacion:")
    print("  [1] Establecer una cantidad total fija")
    print("  [2] Añadir unidades al stock (+)")
    print("  [3] Restar unidades del stock (-)")
    sub_opcion = input("Seleccione una modalidad (1-3): ").strip()

    try:
        if sub_opcion == "1":
            nueva_cant = int(input("Ingrese la nueva cantidad total: ").strip())
            if nueva_cant < 0:
                print(f"{ROJO}Error: La cantidad no puede ser negativa.{RESET}")
                return
            snack.set_cantidad(nueva_cant)
            print(f"\n{VERDE}¡Stock actualizado a {nueva_cant} unidades con exito!{RESET}")

        elif sub_opcion == "2":
            adicionales = int(input("Cantidad de unidades que ingresan: ").strip())
            if adicionales <= 0:
                print(f"{ROJO}Error: Debe ingresar una cantidad mayor a cero.{RESET}")
                return
            nueva_cant = cantidad_actual + adicionales
            snack.set_cantidad(nueva_cant)
            print(f"\n{VERDE}¡Se sumaron {adicionales} uds! Nuevo stock: {nueva_cant} unidades.{RESET}")

        elif sub_opcion == "3":
            a_restar = int(input("Cantidad de unidades a descontar: ").strip())
            if a_restar <= 0:
                print(f"{ROJO}Error: Debe ingresar una cantidad mayor a cero.{RESET}")
                return
            if a_restar > cantidad_actual:
                print(f"{ROJO}Error: No se pueden descontar {a_restar} uds porque solo hay {cantidad_actual}.{RESET}")
                return
            nueva_cant = cantidad_actual - a_restar
            snack.set_cantidad(nueva_cant)
            print(f"\n{VERDE}¡Se descontaron {a_restar} uds! Nuevo stock: {nueva_cant} unidades.{RESET}")

        else:
            print(f"{ROJO}Modalidad no valida.{RESET}")

    except ValueError:
        print(f"{ROJO}Error: Debe ingresar un numero entero valido.{RESET}")


def eliminar_dulce(diccionario_snacks):
    """
    Paso 4 del Rol 4: Eliminar productos que ya no se comercialicen.
    Elimina la clave y el objeto correspondiente del diccionario.
    """
    print(f"\n{CYAN}{NEGRITA}--- ELIMINAR PRODUCTO DEL INVENTARIO ---{RESET}")
    id_snack = localizar_snack(diccionario_snacks)
    if not id_snack:
        return

    snack = diccionario_snacks[id_snack]
    print(f"\n{ROJO}Producto a eliminar:{RESET}")
    print(f"  ID: {snack.get_id_snack()}")
    print(f"  Nombre: {snack.get_nombre()}")
    print(f"  Precio: ${snack.get_precio():.2f}")
    print(f"  Stock actual: {snack.get_cantidad()} uds")

    confirmacion = input(f"\n{AMARILLO}¿Esta seguro de eliminar este producto del sistema? (s/n): {RESET}").strip().lower()
    if confirmacion == "s":
        # Remocion directa del diccionario
        del diccionario_snacks[id_snack]
        print(f"\n{VERDE}{NEGRITA}¡Producto '{snack.get_nombre()}' eliminado exitosamente de la estructura!{RESET}")
    else:
        print(f"\n{AMARILLO}Operacion de eliminacion cancelada.{RESET}")


# =========================================================================
# MENU PRINCIPAL DEL ROL 4: GESTION DE INVENTARIO
# =========================================================================

def menu_gestion_inventario():
    """Imprime las opciones del submenu de administracion de inventario."""
    print(f"\n{AZUL}{NEGRITA}=====================================================")
    print(f"||      ROL 4: GESTIÓN DE INVENTARIO DE DULCERÍA   ||")
    print(f"====================================================={RESET}")
    print(f"{NEGRITA}Seleccione una operacion:{RESET}\n")
    print(f"  {VERDE}[1]{RESET} Agregar nuevo dulce / snack")
    print(f"  {AZUL}[2]{RESET} Modificar precio de un producto")
    print(f"  {AMARILLO}[3]{RESET} Actualizar stock (cantidad disponible)")
    print(f"  {ROJO}[4]{RESET} Eliminar producto que ya no se venda")
    print(f"  {CYAN}[5]{RESET} Consultar inventario completo")
    print(f"  {NEGRITA}[6]{RESET} Volver al menu de administrador\n")
    print(f"{AZUL}-----------------------------------------------------{RESET}")


def iniciar_modulo_inventario(diccionario_externo=None):
    """
    Punto de entrada para el Rol 4.
    Permite operar sobre el inventario en memoria.
    Si se le pasa un diccionario externo lo utiliza; de lo contrario usa el interno.
    """
    # Obtenemos la referencia a la estructura en memoria
    diccionario_snacks = diccionario_externo if diccionario_externo is not None else obtener_inventario()

    while True:
        limpiar_pantalla()
        menu_gestion_inventario()
        opcion = input("Ingrese una opcion (1-6): ").strip()

        if opcion == "1":
            limpiar_pantalla()
            agregar_nuevo_dulce(diccionario_snacks)
            pausar()
        elif opcion == "2":
            limpiar_pantalla()
            modificar_precio_dulce(diccionario_snacks)
            pausar()
        elif opcion == "3":
            limpiar_pantalla()
            actualizar_stock_dulce(diccionario_snacks)
            pausar()
        elif opcion == "4":
            limpiar_pantalla()
            eliminar_dulce(diccionario_snacks)
            pausar()
        elif opcion == "5":
            limpiar_pantalla()
            listar_inventario_completo(diccionario_snacks)
            pausar()
        elif opcion == "6":
            print(f"\n{AMARILLO}Regresando al menu de administrador...{RESET}")
            break
        else:
            print(f"\n{ROJO}Opcion invalida. Intente nuevamente.{RESET}")
            pausar()


if __name__ == "__main__":
    # Permite probar este modulo de forma independiente
    iniciar_modulo_inventario()

