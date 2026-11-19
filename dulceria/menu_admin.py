# Archivo: dulceria/menu_admin.py
# Interfaz de Administracion de Inventario de Dulceria (Rol 4).
# Persiste cada modificacion en tiempo real sobre datos/stock.csv.

import math
from config import (
    MAX_LEN_DESCRIPCION_SNACK,
    MAX_LEN_NOMBRE_SNACK,
    MIN_LEN_NOMBRE_SNACK,
    PRECIO_MAX_SNACK,
    PRECIO_MIN_SNACK,
    RUTA_STOCK,
    STOCK_MAX_SNACK,
    STOCK_MIN_SNACK
)
from dulceria.gestor_inventario import (
    cargar_snacks_desde_csv,
    generar_id_hash,
    generar_id_unico,
    guardar_snacks_en_csv
)
from dulceria.snack import Snack
# Importa la clase Colores unificada desde nucleo/colores.py
from nucleo.colores import Colores
from nucleo.consola import (
    confirmar_accion,
    limpiar_pantalla,
    pausar
)


def obtener_inventario(ruta_csv=RUTA_STOCK):
    """Carga y retorna el inventario actualizado directamente desde stock.csv."""
    return cargar_snacks_desde_csv(ruta_csv)


def listar_inventario_completo(diccionario_snacks):
    """Muestra en pantalla una tabla alineada con todos los snacks del inventario."""
    print(f"\n{Colores.AZUL}{Colores.NEGRITA}" + "=" * 85 + f"{Colores.RESET}")
    print(f"{Colores.CYAN}{Colores.NEGRITA}{'INVENTARIO GENERAL DE DULCERÍA (VISTA ADMINISTRADOR)':^85}{Colores.RESET}")
    print(f"{Colores.AZUL}{Colores.NEGRITA}" + "=" * 85 + f"{Colores.RESET}")

    if not diccionario_snacks:
        print(f"{Colores.ROJO}No hay ningún producto registrado en el inventario.{Colores.RESET}")
        print(f"{Colores.AZUL}" + "-" * 85 + f"{Colores.RESET}")
        return

    encabezado = f"{'ID':<10} | {'PRODUCTO':<25} | {'PRECIO':<10} | {'STOCK':<9} | {'DESCRIPCIÓN'}"
    print(f"{Colores.NEGRITA}{encabezado}{Colores.RESET}")
    print(f"{Colores.AZUL}" + "-" * 85 + f"{Colores.RESET}")

    for snack in diccionario_snacks.values():
        cant = snack.get_cantidad()
        color_stock = Colores.VERDE if cant > 5 else (Colores.AMARILLO if cant > 0 else Colores.ROJO)
        # Se formatea y alinea antes de envolver en ANSI para evitar desalineacion visual
        stock_texto = f"{cant:>5} uds"
        stock_str = f"{color_stock}{stock_texto:<9}{Colores.RESET}"
        precio_str = f"${snack.get_precio():.2f}"

        nombre_mostrar = snack.get_nombre()
        if len(nombre_mostrar) > 25:
            nombre_mostrar = nombre_mostrar[:22] + "..."

        desc = snack.get_descripcion()
        if len(desc) > 30:
            desc = desc[:27] + "..."

        print(
            f"{Colores.AMARILLO}{snack.get_id_snack():<10}{Colores.RESET} | "
            f"{Colores.NEGRITA}{nombre_mostrar:<25}{Colores.RESET} | "
            f"{Colores.VERDE}{precio_str:<10}{Colores.RESET} | "
            f"{stock_str} | "
            f"{desc}"
        )

    print(f"{Colores.AZUL}{Colores.NEGRITA}" + "=" * 85 + f"{Colores.RESET}")


def localizar_snack(diccionario_snacks):
    """Busca y selecciona un snack por ID exacto, hash o coincidencia parcial."""
    criterio = input(f"\n{Colores.AMARILLO}Ingrese el ID o nombre del producto a gestionar: {Colores.RESET}").strip()
    if not criterio:
        print(f"{Colores.ROJO}Debe ingresar un valor válido.{Colores.RESET}")
        return None

    # 1. Comprueba primero coincidencia exacta con ID en mayusculas
    criterio_upper = criterio.upper()
    if criterio_upper in diccionario_snacks:
        return criterio_upper

    # 2. Busqueda por clave hash exacta validando tambien el nombre
    posible_hash = generar_id_hash(criterio)
    if posible_hash in diccionario_snacks:
        if diccionario_snacks[posible_hash].get_nombre().strip().lower() == criterio.lower():
            return posible_hash

    # 3. Busqueda por coincidencia parcial en nombre o ID
    coincidencias = []
    criterio_lower = criterio.lower()
    for id_clave, snack in diccionario_snacks.items():
        if criterio_lower in snack.get_nombre().lower() or criterio_lower == id_clave.lower():
            coincidencias.append(id_clave)

    if len(coincidencias) == 1:
        return coincidencias[0]
    if len(coincidencias) > 1:
        print(f"\n{Colores.AMARILLO}Se encontraron múltiples coincidencias:{Colores.RESET}")
        for i, id_c in enumerate(coincidencias, start=1):
            snk = diccionario_snacks[id_c]
            print(f"  [{i}] ID: {id_c} - {snk.get_nombre()} (${snk.get_precio():.2f})")

        seleccion = input("Seleccione el número correspondiente (o 'c' para cancelar): ").strip()
        if seleccion.lower() == "c":
            return None
        try:
            indice = int(seleccion) - 1
            if 0 <= indice < len(coincidencias):
                return coincidencias[indice]
            print(f"{Colores.ROJO}Índice fuera de rango.{Colores.RESET}")
            return None
        except ValueError:
            print(f"{Colores.ROJO}Opción inválida.{Colores.RESET}")
            return None

    print(f"{Colores.ROJO}No se encontró ningún producto que coincida con '{criterio}'.{Colores.RESET}")
    return None


def agregar_nuevo_dulce(diccionario_snacks, ruta_csv=RUTA_STOCK):
    """Agrega un nuevo dulce validando limites y guardando en tiempo real en stock.csv."""
    print(f"\n{Colores.CYAN}{Colores.NEGRITA}--- AGREGAR NUEVO PRODUCTO AL INVENTARIO ---{Colores.RESET}")

    nombre = input(f"Nombre del dulce/snack ({MIN_LEN_NOMBRE_SNACK}-{MAX_LEN_NOMBRE_SNACK} caracteres): ").strip()
    if len(nombre) < MIN_LEN_NOMBRE_SNACK:
        print(f"{Colores.ROJO}Error: El nombre debe tener al menos {MIN_LEN_NOMBRE_SNACK} caracteres.{Colores.RESET}")
        return
    if len(nombre) > MAX_LEN_NOMBRE_SNACK:
        print(f"{Colores.ROJO}Error: El nombre no puede superar {MAX_LEN_NOMBRE_SNACK} caracteres.{Colores.RESET}")
        return

    for snack_existente in diccionario_snacks.values():
        if snack_existente.get_nombre().strip().lower() == nombre.lower():
            print(f"{Colores.ROJO}Error: Ya existe un producto con el mismo nombre ({snack_existente.get_id_snack()}):{Colores.RESET}")
            print(f"Producto existente: {snack_existente.get_nombre()}")
            print(f"{Colores.AMARILLO}Si desea actualizarlo, utilice las opciones de modificar precio o stock.{Colores.RESET}")
            return

    id_generado = generar_id_unico(nombre, diccionario_snacks)

    descripcion = input(f"Descripción del producto (máx. {MAX_LEN_DESCRIPCION_SNACK} caracteres): ").strip()
    if not descripcion:
        descripcion = "Sin descripción adicional"
    elif len(descripcion) > MAX_LEN_DESCRIPCION_SNACK:
        print(f"{Colores.ROJO}Error: La descripción no puede superar {MAX_LEN_DESCRIPCION_SNACK} caracteres.{Colores.RESET}")
        return

    try:
        precio_input = input(f"Precio en dólares (${PRECIO_MIN_SNACK:.2f} - ${PRECIO_MAX_SNACK:.2f}): ").strip()
        precio = float(precio_input)
        if not math.isfinite(precio) or precio < PRECIO_MIN_SNACK or precio > PRECIO_MAX_SNACK:
            print(f"{Colores.ROJO}Error: El precio debe estar entre ${PRECIO_MIN_SNACK:.2f} y ${PRECIO_MAX_SNACK:.2f}.{Colores.RESET}")
            return
        precio = round(precio, 2)
    except ValueError:
        print(f"{Colores.ROJO}Error: Ingrese un valor numérico válido para el precio.{Colores.RESET}")
        return

    try:
        cantidad_input = input(f"Cantidad inicial en stock ({STOCK_MIN_SNACK}-{STOCK_MAX_SNACK}): ").strip()
        cantidad = int(cantidad_input)
        if cantidad < STOCK_MIN_SNACK or cantidad > STOCK_MAX_SNACK:
            print(f"{Colores.ROJO}Error: La cantidad debe estar entre {STOCK_MIN_SNACK} y {STOCK_MAX_SNACK} unidades.{Colores.RESET}")
            return
    except ValueError:
        print(f"{Colores.ROJO}Error: Ingrese un número entero válido para la cantidad.{Colores.RESET}")
        return

    nuevo_snack = Snack(id_generado, nombre, descripcion, precio, cantidad)
    diccionario_snacks[id_generado] = nuevo_snack
    guardar_snacks_en_csv(diccionario_snacks, ruta_csv)

    print(f"\n{Colores.VERDE}{Colores.NEGRITA}¡Producto agregado y guardado exitosamente en stock.csv!{Colores.RESET}")
    print(f"ID Asignado: {Colores.AMARILLO}{id_generado}{Colores.RESET} | {nombre} | Stock: {cantidad} | Precio: ${precio:.2f}")


def modificar_precio_dulce(diccionario_snacks, ruta_csv=RUTA_STOCK):
    """Modifica el precio de un dulce existente y guarda de inmediato en stock.csv."""
    print(f"\n{Colores.CYAN}{Colores.NEGRITA}--- MODIFICAR PRECIO DE PRODUCTO ---{Colores.RESET}")
    id_snack = localizar_snack(diccionario_snacks)
    if not id_snack:
        return

    snack = diccionario_snacks[id_snack]
    print(f"\nProducto: {Colores.NEGRITA}{snack.get_nombre()}{Colores.RESET} (ID: {snack.get_id_snack()})")
    print(f"Precio actual: {Colores.VERDE}${snack.get_precio():.2f}{Colores.RESET}")

    try:
        nuevo_precio_str = input(f"\nIngrese el nuevo precio (${PRECIO_MIN_SNACK:.2f} - ${PRECIO_MAX_SNACK:.2f}): ").strip()
        nuevo_precio = float(nuevo_precio_str)
        if not math.isfinite(nuevo_precio) or nuevo_precio < PRECIO_MIN_SNACK or nuevo_precio > PRECIO_MAX_SNACK:
            print(f"{Colores.ROJO}Error: El precio debe estar entre ${PRECIO_MIN_SNACK:.2f} y ${PRECIO_MAX_SNACK:.2f}.{Colores.RESET}")
            return

        nuevo_precio = round(nuevo_precio, 2)
        snack.set_precio(nuevo_precio)
        guardar_snacks_en_csv(diccionario_snacks, ruta_csv)
        print(f"\n{Colores.VERDE}{Colores.NEGRITA}¡Precio actualizado y guardado exitosamente a ${nuevo_precio:.2f}!{Colores.RESET}")
    except ValueError:
        print(f"{Colores.ROJO}Error: Ingrese un valor numérico válido.{Colores.RESET}")


def actualizar_stock_dulce(diccionario_snacks, ruta_csv=RUTA_STOCK):
    """Actualiza el stock de un dulce existente y guarda inmediatamente en stock.csv."""
    print(f"\n{Colores.CYAN}{Colores.NEGRITA}--- ACTUALIZAR STOCK DE PRODUCTO ---{Colores.RESET}")
    id_snack = localizar_snack(diccionario_snacks)
    if not id_snack:
        return

    snack = diccionario_snacks[id_snack]
    cantidad_actual = snack.get_cantidad()
    print(f"\nProducto: {Colores.NEGRITA}{snack.get_nombre()}{Colores.RESET} (ID: {snack.get_id_snack()})")
    print(f"Stock actual: {Colores.AMARILLO}{cantidad_actual} unidades{Colores.RESET}")

    print("\nOpciones de actualización:")
    print(f"  [1] Establecer una cantidad total fija ({STOCK_MIN_SNACK}-{STOCK_MAX_SNACK})")
    print("  [2] Añadir unidades al stock (+)")
    print("  [3] Restar unidades del stock (-)")
    sub_opcion = input("Seleccione una modalidad (1-3): ").strip()

    try:
        if sub_opcion == "1":
            nueva_cant = int(input("Ingrese la nueva cantidad total: ").strip())
            if nueva_cant < STOCK_MIN_SNACK or nueva_cant > STOCK_MAX_SNACK:
                print(f"{Colores.ROJO}Error: La cantidad debe estar entre {STOCK_MIN_SNACK} y {STOCK_MAX_SNACK} unidades.{Colores.RESET}")
                return
            snack.set_cantidad(nueva_cant)
            guardar_snacks_en_csv(diccionario_snacks, ruta_csv)
            print(f"\n{Colores.VERDE}¡Stock actualizado y guardado en {nueva_cant} unidades con éxito!{Colores.RESET}")

        elif sub_opcion == "2":
            adicionales = int(input("Cantidad de unidades que ingresan: ").strip())
            if adicionales <= 0:
                print(f"{Colores.ROJO}Error: Debe ingresar una cantidad mayor a cero.{Colores.RESET}")
                return
            nueva_cant = cantidad_actual + adicionales
            if nueva_cant > STOCK_MAX_SNACK:
                print(f"{Colores.ROJO}Error: El stock resultante ({nueva_cant}) supera el límite máximo de {STOCK_MAX_SNACK} unidades.{Colores.RESET}")
                return
            snack.set_cantidad(nueva_cant)
            guardar_snacks_en_csv(diccionario_snacks, ruta_csv)
            print(f"\n{Colores.VERDE}¡Se sumaron {adicionales} uds! Nuevo stock guardado: {nueva_cant} unidades.{Colores.RESET}")

        elif sub_opcion == "3":
            a_restar = int(input("Cantidad de unidades a descontar: ").strip())
            if a_restar <= 0:
                print(f"{Colores.ROJO}Error: Debe ingresar una cantidad mayor a cero.{Colores.RESET}")
                return
            if a_restar > cantidad_actual:
                print(f"{Colores.ROJO}Error: No se pueden descontar {a_restar} uds porque solo hay {cantidad_actual}.{Colores.RESET}")
                return
            nueva_cant = cantidad_actual - a_restar
            snack.set_cantidad(nueva_cant)
            guardar_snacks_en_csv(diccionario_snacks, ruta_csv)
            print(f"\n{Colores.VERDE}¡Se descontaron {a_restar} uds! Nuevo stock guardado: {nueva_cant} unidades.{Colores.RESET}")

        else:
            print(f"{Colores.ROJO}Modalidad no válida.{Colores.RESET}")
    except ValueError:
        print(f"{Colores.ROJO}Error: Debe ingresar un número entero válido.{Colores.RESET}")


def eliminar_dulce(diccionario_snacks, ruta_csv=RUTA_STOCK):
    """Elimina un dulce del inventario usando confirmar_accion() y guarda en stock.csv."""
    print(f"\n{Colores.CYAN}{Colores.NEGRITA}--- ELIMINAR PRODUCTO DEL INVENTARIO ---{Colores.RESET}")
    id_snack = localizar_snack(diccionario_snacks)
    if not id_snack:
        return

    snack = diccionario_snacks[id_snack]
    print(f"\n{Colores.ROJO}Producto a eliminar:{Colores.RESET}")
    print(f"  ID: {snack.get_id_snack()}")
    print(f"  Nombre: {snack.get_nombre()}")
    print(f"  Precio: ${snack.get_precio():.2f}")
    print(f"  Stock actual: {snack.get_cantidad()} uds\n")

    if confirmar_accion("¿Está seguro de eliminar este producto del sistema?"):
        del diccionario_snacks[id_snack]
        guardar_snacks_en_csv(diccionario_snacks, ruta_csv)
        print(f"\n{Colores.VERDE}{Colores.NEGRITA}¡Producto '{snack.get_nombre()}' eliminado y cambios guardados!{Colores.RESET}")
    else:
        print(f"\n{Colores.AMARILLO}Operación de eliminación cancelada.{Colores.RESET}")


def menu_gestion_inventario():
    """Imprime el submenu del Rol 4 con colores unificados (verde acciones, rojo volver)."""
    print(f"\n{Colores.AZUL}{Colores.NEGRITA}=====================================================")
    print("||      ROL 4: GESTIÓN DE INVENTARIO DE DULCERÍA   ||")
    print(f"====================================================={Colores.RESET}")
    print(f"{Colores.NEGRITA}Seleccione una operación:{Colores.RESET}\n")
    print(f"  {Colores.VERDE}[1]{Colores.RESET} Agregar nuevo dulce / snack")
    print(f"  {Colores.VERDE}[2]{Colores.RESET} Modificar precio de un producto")
    print(f"  {Colores.VERDE}[3]{Colores.RESET} Actualizar stock (cantidad disponible)")
    print(f"  {Colores.VERDE}[4]{Colores.RESET} Eliminar producto que ya no se venda")
    print(f"  {Colores.VERDE}[5]{Colores.RESET} Consultar inventario completo")
    print(f"  {Colores.ROJO}[6]{Colores.RESET} Volver al menú de administrador\n")
    print(f"{Colores.AZUL}-----------------------------------------------------{Colores.RESET}")


def iniciar_modulo_inventario(diccionario_externo=None, ruta_csv=RUTA_STOCK):
    """Punto de entrada del Rol 4 sincronizado contra disco en cada operacion."""
    usar_disco = diccionario_externo is None

    while True:
        diccionario_snacks = obtener_inventario(ruta_csv) if usar_disco else diccionario_externo
        limpiar_pantalla()
        menu_gestion_inventario()
        opcion = input("Ingrese una opción (1-6): ").strip()

        if opcion == "1":
            limpiar_pantalla()
            agregar_nuevo_dulce(diccionario_snacks, ruta_csv=ruta_csv)
            pausar()
        elif opcion == "2":
            limpiar_pantalla()
            modificar_precio_dulce(diccionario_snacks, ruta_csv=ruta_csv)
            pausar()
        elif opcion == "3":
            limpiar_pantalla()
            actualizar_stock_dulce(diccionario_snacks, ruta_csv=ruta_csv)
            pausar()
        elif opcion == "4":
            limpiar_pantalla()
            eliminar_dulce(diccionario_snacks, ruta_csv=ruta_csv)
            pausar()
        elif opcion == "5":
            limpiar_pantalla()
            listar_inventario_completo(diccionario_snacks)
            pausar()
        elif opcion == "6":
            print(f"\n{Colores.AMARILLO}Regresando al menú de administrador...{Colores.RESET}")
            break
        else:
            print(f"\n{Colores.ROJO}Opción inválida. Intente nuevamente.{Colores.RESET}")
            pausar()
