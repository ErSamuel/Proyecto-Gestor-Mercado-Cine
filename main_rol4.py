# Archivo: main_rol4.py
# Modulo correspondiente al ROL 4: Gestion del Inventario de la Dulceria (Administrador)
# Permite agregar productos, modificar precios, actualizar stock y eliminar productos.
# Cada modificacion se persiste inmediatamente en stock.csv para mantener sincronia en tiempo real con el Cliente.

import math
import os
from modelo_snack import Snack
from gestor_snacks import (
    RUTA_STOCK_DEFECTO,
    generar_id_hash,
    generar_id_unico,
    cargar_snacks_desde_csv,
    guardar_snacks_en_csv
)

# Limites de validacion para prevenir desbordamiento de tabla, memoria y valores invalidos (NaN/Inf)
MIN_LEN_NOMBRE = 2
MAX_LEN_NOMBRE = 40
MAX_LEN_DESCRIPCION = 120
PRECIO_MIN = 0.01
PRECIO_MAX = 1000.00
STOCK_MIN = 0
STOCK_MAX = 10000

# Constantes para estilos y colores ANSI en consola
AZUL = "\033[94m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
NEGRITA = "\033[1m"


def obtener_inventario():
    """
    Carga y retorna el inventario actualizado directamente desde stock.csv.
    Evita usar una cache obsoleta que ignore compras recientes de clientes.
    Clave: ID Hash (str) -> Valor: Objeto de tipo Snack.
    """
    return cargar_snacks_desde_csv(RUTA_STOCK_DEFECTO)


def guardar_inventario_final():
    """
    Funcion mantenida por compatibilidad de importacion con main.py.
    Dado que ahora cada cambio del Administrador se guarda de inmediato en stock.csv,
    no sobrescribe el disco al salir para no borrar ventas realizadas por los clientes.
    """
    return None


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
        # Se formatea y alinea el texto antes de envolverlo con codigos ANSI para no romper columnas
        stock_texto = f"{cant:>5} uds"
        stock_str = f"{color_stock}{stock_texto:<9}{RESET}"
        precio_str = f"${snack.get_precio():.2f}"

        # Recortar nombre si supera el ancho de columna de 25 caracteres
        nombre_mostrar = snack.get_nombre()
        if len(nombre_mostrar) > 25:
            nombre_mostrar = nombre_mostrar[:22] + "..."

        # Recortar descripcion si es muy larga para la tabla
        desc = snack.get_descripcion()
        if len(desc) > 30:
            desc = desc[:27] + "..."

        print(f"{AMARILLO}{snack.get_id_snack():<10}{RESET} | "
              f"{NEGRITA}{nombre_mostrar:<25}{RESET} | "
              f"{VERDE}{precio_str:<10}{RESET} | "
              f"{stock_str} | "
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

    # 1. Comprueba primero coincidencia exacta con el ID en mayusculas (ej. SNK-743)
    criterio_upper = criterio.upper()
    if criterio_upper in diccionario_snacks:
        return criterio_upper

    # 2. Busqueda por clave hash exacta si coincide tambien el nombre del producto
    posible_hash = generar_id_hash(criterio)
    if posible_hash in diccionario_snacks:
        if diccionario_snacks[posible_hash].get_nombre().strip().lower() == criterio.lower():
            return posible_hash

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
    Crea el objeto Snack con su ID hash unico y lo guarda inmediatamente en stock.csv.
    """
    print(f"\n{CYAN}{NEGRITA}--- AGREGAR NUEVO PRODUCTO AL INVENTARIO ---{RESET}")

    nombre = input(f"Nombre del dulce/snack ({MIN_LEN_NOMBRE}-{MAX_LEN_NOMBRE} caracteres): ").strip()
    if len(nombre) < MIN_LEN_NOMBRE:
        print(f"{ROJO}Error: El nombre debe tener al menos {MIN_LEN_NOMBRE} caracteres.{RESET}")
        return
    if len(nombre) > MAX_LEN_NOMBRE:
        print(f"{ROJO}Error: El nombre no puede superar {MAX_LEN_NOMBRE} caracteres.{RESET}")
        return

    # Comprobar por nombre exacto si ya existe un producto igual en el inventario
    for snack_existente in diccionario_snacks.values():
        if snack_existente.get_nombre().strip().lower() == nombre.lower():
            print(f"{ROJO}Error: Ya existe un producto con el mismo nombre ({snack_existente.get_id_snack()}):{RESET}")
            print(f"Producto existente: {snack_existente.get_nombre()}")
            print(f"{AMARILLO}Si desea actualizarlo, utilice las opciones de modificar precio o stock.{RESET}")
            return

    # Asigna un ID hash garantizando que no colisione con otro producto distinto
    id_generado = generar_id_unico(nombre, diccionario_snacks)

    descripcion = input(f"Descripcion del producto (max. {MAX_LEN_DESCRIPCION} caracteres): ").strip()
    if not descripcion:
        descripcion = "Sin descripcion adicional"
    elif len(descripcion) > MAX_LEN_DESCRIPCION:
        print(f"{ROJO}Error: La descripcion no puede superar {MAX_LEN_DESCRIPCION} caracteres.{RESET}")
        return

    # Validacion del precio (finito y dentro del rango permitido)
    try:
        precio_input = input(f"Precio en dolares (${PRECIO_MIN:.2f} - ${PRECIO_MAX:.2f}): ").strip()
        precio = float(precio_input)
        if not math.isfinite(precio) or precio < PRECIO_MIN or precio > PRECIO_MAX:
            print(f"{ROJO}Error: El precio debe ser un numero valido entre ${PRECIO_MIN:.2f} y ${PRECIO_MAX:.2f}.{RESET}")
            return
        precio = round(precio, 2)
    except ValueError:
        print(f"{ROJO}Error: Ingrese un valor numerico valido para el precio.{RESET}")
        return

    # Validacion de la cantidad inicial dentro del limite permitido
    try:
        cantidad_input = input(f"Cantidad inicial en stock ({STOCK_MIN}-{STOCK_MAX}): ").strip()
        cantidad = int(cantidad_input)
        if cantidad < STOCK_MIN or cantidad > STOCK_MAX:
            print(f"{ROJO}Error: La cantidad debe estar entre {STOCK_MIN} y {STOCK_MAX} unidades.{RESET}")
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

    # Insercion en diccionario y persistencia inmediata en stock.csv
    diccionario_snacks[id_generado] = nuevo_snack
    guardar_snacks_en_csv(diccionario_snacks, RUTA_STOCK_DEFECTO)

    print(f"\n{VERDE}{NEGRITA}¡Producto agregado y guardado exitosamente en stock.csv!{RESET}")
    print(f"ID Asignado: {AMARILLO}{id_generado}{RESET} | {nombre} | Stock: {cantidad} | Precio: ${precio:.2f}")


def modificar_precio_dulce(diccionario_snacks):
    """
    Paso 2 del Rol 4: Modificar el precio de un dulce existente.
    Utiliza el setter 'set_precio' y guarda el cambio de inmediato en stock.csv.
    """
    print(f"\n{CYAN}{NEGRITA}--- MODIFICAR PRECIO DE PRODUCTO ---{RESET}")
    id_snack = localizar_snack(diccionario_snacks)
    if not id_snack:
        return

    snack = diccionario_snacks[id_snack]
    print(f"\nProducto: {NEGRITA}{snack.get_nombre()}{RESET} (ID: {snack.get_id_snack()})")
    print(f"Precio actual: {VERDE}${snack.get_precio():.2f}{RESET}")

    try:
        nuevo_precio_str = input(f"\nIngrese el nuevo precio (${PRECIO_MIN:.2f} - ${PRECIO_MAX:.2f}): ").strip()
        nuevo_precio = float(nuevo_precio_str)
        # Rechaza NaN, Inf y valores fuera del rango permitido
        if not math.isfinite(nuevo_precio) or nuevo_precio < PRECIO_MIN or nuevo_precio > PRECIO_MAX:
            print(f"{ROJO}Error: El precio debe estar entre ${PRECIO_MIN:.2f} y ${PRECIO_MAX:.2f}.{RESET}")
            return

        nuevo_precio = round(nuevo_precio, 2)
        # Modificacion sobre la estructura mediante el setter y guardado inmediato
        snack.set_precio(nuevo_precio)
        guardar_snacks_en_csv(diccionario_snacks, RUTA_STOCK_DEFECTO)
        print(f"\n{VERDE}{NEGRITA}¡Precio actualizado y guardado exitosamente a ${nuevo_precio:.2f}!{RESET}")

    except ValueError:
        print(f"{ROJO}Error: Ingrese un valor numerico valido.{RESET}")


def actualizar_stock_dulce(diccionario_snacks):
    """
    Paso 3 del Rol 4: Actualizar las existencias en inventario.
    Permite fijar una nueva cantidad o sumar/restar unidades y guarda al instante.
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
    print(f"  [1] Establecer una cantidad total fija ({STOCK_MIN}-{STOCK_MAX})")
    print("  [2] Añadir unidades al stock (+)")
    print("  [3] Restar unidades del stock (-)")
    sub_opcion = input("Seleccione una modalidad (1-3): ").strip()

    try:
        if sub_opcion == "1":
            nueva_cant = int(input("Ingrese la nueva cantidad total: ").strip())
            if nueva_cant < STOCK_MIN or nueva_cant > STOCK_MAX:
                print(f"{ROJO}Error: La cantidad debe estar entre {STOCK_MIN} y {STOCK_MAX} unidades.{RESET}")
                return
            snack.set_cantidad(nueva_cant)
            guardar_snacks_en_csv(diccionario_snacks, RUTA_STOCK_DEFECTO)
            print(f"\n{VERDE}¡Stock actualizado y guardado en {nueva_cant} unidades con exito!{RESET}")

        elif sub_opcion == "2":
            adicionales = int(input("Cantidad de unidades que ingresan: ").strip())
            if adicionales <= 0:
                print(f"{ROJO}Error: Debe ingresar una cantidad mayor a cero.{RESET}")
                return
            nueva_cant = cantidad_actual + adicionales
            if nueva_cant > STOCK_MAX:
                print(f"{ROJO}Error: El stock resultante ({nueva_cant}) supera el limite maximo de {STOCK_MAX} unidades.{RESET}")
                return
            snack.set_cantidad(nueva_cant)
            guardar_snacks_en_csv(diccionario_snacks, RUTA_STOCK_DEFECTO)
            print(f"\n{VERDE}¡Se sumaron {adicionales} uds! Nuevo stock guardado: {nueva_cant} unidades.{RESET}")

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
            guardar_snacks_en_csv(diccionario_snacks, RUTA_STOCK_DEFECTO)
            print(f"\n{VERDE}¡Se descontaron {a_restar} uds! Nuevo stock guardado: {nueva_cant} unidades.{RESET}")

        else:
            print(f"{ROJO}Modalidad no valida.{RESET}")

    except ValueError:
        print(f"{ROJO}Error: Debe ingresar un numero entero valido.{RESET}")


def eliminar_dulce(diccionario_snacks):
    """
    Paso 4 del Rol 4: Eliminar productos que ya no se comercialicen.
    Elimina la clave del diccionario y persiste inmediatamente en stock.csv.
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

    # Bucle de confirmacion para aceptar 's'/'si' o 'n'/'no' y re-preguntar ante entradas invalidas
    while True:
        confirmacion = input(f"\n{AMARILLO}¿Esta seguro de eliminar este producto del sistema? (s/n): {RESET}").strip().lower()
        if confirmacion in ("s", "si", "sí"):
            # Remocion directa del diccionario y persistencia inmediata
            del diccionario_snacks[id_snack]
            guardar_snacks_en_csv(diccionario_snacks, RUTA_STOCK_DEFECTO)
            print(f"\n{VERDE}{NEGRITA}¡Producto '{snack.get_nombre()}' eliminado y cambios guardados!{RESET}")
            break
        elif confirmacion in ("n", "no"):
            print(f"\n{AMARILLO}Operacion de eliminacion cancelada.{RESET}")
            break
        else:
            print(f"{ROJO}Opcion invalida. Por favor ingrese 's' para confirmar o 'n' para cancelar.{RESET}")


# =========================================================================
# MENU PRINCIPAL DEL ROL 4: GESTION DE INVENTARIO
# =========================================================================

def menu_gestion_inventario():
    """Imprime las opciones del submenu de administracion de inventario."""
    print(f"\n{AZUL}{NEGRITA}=====================================================")
    print("||      ROL 4: GESTIÓN DE INVENTARIO DE DULCERÍA   ||")
    print(f"====================================================={RESET}")
    print(f"{NEGRITA}Seleccione una operacion:{RESET}\n")
    # Colores unificados: opciones de accion en verde y unicamente 'Volver' en rojo
    print(f"  {VERDE}[1]{RESET} Agregar nuevo dulce / snack")
    print(f"  {VERDE}[2]{RESET} Modificar precio de un producto")
    print(f"  {VERDE}[3]{RESET} Actualizar stock (cantidad disponible)")
    print(f"  {VERDE}[4]{RESET} Eliminar producto que ya no se venda")
    print(f"  {VERDE}[5]{RESET} Consultar inventario completo")
    print(f"  {ROJO}[6]{RESET} Volver al menu de administrador\n")
    print(f"{AZUL}-----------------------------------------------------{RESET}")


def iniciar_modulo_inventario(diccionario_externo=None):
    """
    Punto de entrada para el Rol 4.
    Recarga el inventario desde stock.csv para reflejar siempre el estado real en disco.
    """
    usar_disco = diccionario_externo is None

    while True:
        # Recarga en cada iteracion si trabaja contra disco para reflejar compras simultaneas
        diccionario_snacks = obtener_inventario() if usar_disco else diccionario_externo
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
    # Habilita secuencias ANSI en consola Windows al probar el modulo directamente
    os.system("")
    iniciar_modulo_inventario()

