# Archivo: boleteria/menu_admin.py
# Modulo de Administracion de Cartelera y Salas (Rol 5).
# Permite crear peliculas sin obligar la asignacion inmediata de sala,
# gestionar horarios, modificar tarifas y eliminar funciones con robustez.

from boleteria.gestor_cartelera import GestorCartelera
from config import (
    CAPACIDADES_POR_SALA,
    CLASIFICACIONES_VALIDAS,
    FORMATOS_VALIDOS,
    RUTA_CARTELERA,
    SALAS_DISPONIBLES
)
from nucleo.colores import Colores
from nucleo.consola import (
    confirmar_accion,
    limpiar_pantalla,
    mostrar_encabezado,
    pausar
)


def listar_cartelera_admin(gestor):
    """Muestra la tabla completa de peliculas con salas, horarios, butacas y formatos."""
    peliculas = gestor.listar_todas()
    print(f"\n{Colores.AZUL}{Colores.NEGRITA}" + "=" * 110 + f"{Colores.RESET}")
    print(f"{Colores.CYAN}{Colores.NEGRITA}{'CARTELERA GENERAL Y SALAS (VISTA ADMINISTRADOR)':^110}{Colores.RESET}")
    print(f"{Colores.AZUL}{Colores.NEGRITA}" + "=" * 110 + f"{Colores.RESET}")

    if not peliculas:
        print(f"{Colores.ROJO}No hay ninguna película registrada en la cartelera.{Colores.RESET}")
        print(f"{Colores.AZUL}" + "-" * 110 + f"{Colores.RESET}")
        return

    encabezado = f"{'ID':<8} | {'TÍTULO':<25} | {'FMT':<5} | {'EDAD':<5} | {'SALA':<12} | {'HORARIO':<11} | {'FIN EST.':<10} | {'PRECIO':<7} | {'ESTADO/BUTACAS'}"
    print(f"{Colores.NEGRITA}{encabezado}{Colores.RESET}")
    print(f"{Colores.AZUL}" + "-" * 110 + f"{Colores.RESET}")

    for p in peliculas:
        cant_butacas = p.disponibilidad
        if p.sala.lower() in ("sin asignar", "por definir"):
            sala_str = f"{Colores.AMARILLO}{p.sala:<12}{Colores.RESET}"
            estado_str = f"{Colores.AMARILLO}[Sin función]{Colores.RESET}"
        else:
            sala_str = f"{Colores.AZUL}{p.sala:<12}{Colores.RESET}"
            if cant_butacas > 10:
                estado_str = f"{Colores.VERDE}{cant_butacas:>3} libres{Colores.RESET}"
            elif cant_butacas > 0:
                estado_str = f"{Colores.AMARILLO}{cant_butacas:>3} libres{Colores.RESET}"
            else:
                estado_str = f"{Colores.ROJO}  0 (Agotada){Colores.RESET}"

        precio_str = f"${p.costo:.2f}"
        titulo_str = p.nombre
        if len(titulo_str) > 25:
            titulo_str = titulo_str[:22] + "..."

        print(
            f"{Colores.AMARILLO}{p.id:<8}{Colores.RESET} | "
            f"{Colores.NEGRITA}{titulo_str:<25}{Colores.RESET} | "
            f"{Colores.CYAN}{p.formato:<5}{Colores.RESET} | "
            f"[{p.clasificacion:<3}] | "
            f"{sala_str} | "
            f"{p.horario:<11} | "
            f"{p.hora_fin:<10} | "
            f"{Colores.VERDE}{precio_str:<7}{Colores.RESET} | "
            f"{estado_str}"
        )

    print(f"{Colores.AZUL}{Colores.NEGRITA}" + "=" * 110 + f"{Colores.RESET}")


def localizar_pelicula(gestor):
    """
    Muestra el listado numerado de peliculas registradas y permite seleccionar
    directamente por su numero de orden (ej. '1', '7'), por su ID ('PEL-01')
    o por coincidencia en el titulo.
    """
    peliculas = gestor.listar_todas()
    if not peliculas:
        print(f"\n{Colores.ROJO}No hay ninguna película registrada en el sistema.{Colores.RESET}")
        return None

    print(f"\n{Colores.CYAN}{Colores.NEGRITA}--- PELÍCULAS DISPONIBLES EN EL SISTEMA ---{Colores.RESET}")
    for idx, p in enumerate(peliculas, start=1):
        if p.sala.lower() in ("sin asignar", "por definir"):
            info_sala = f"{Colores.AMARILLO}Sin sala asignada{Colores.RESET}"
        else:
            info_sala = f"{Colores.AZUL}{p.sala}{Colores.RESET} ({p.horario}) | {p.disponibilidad} butacas"

        print(
            f"  {Colores.VERDE}[{idx}]{Colores.RESET} {Colores.AMARILLO}{p.id:<8}{Colores.RESET} | "
            f"{Colores.NEGRITA}{p.nombre:<26}{Colores.RESET} [{p.formato}] ({p.clasificacion}) | {info_sala}"
        )
    print(f"  {Colores.ROJO}[0] Cancelar operación{Colores.RESET}")

    criterio = input(f"\n{Colores.AMARILLO}Seleccione el número (1-{len(peliculas)}), ID o título de la película: {Colores.RESET}").strip()
    if not criterio or criterio == "0":
        print(f"{Colores.AMARILLO}Operación cancelada.{Colores.RESET}")
        return None

    # 1. Seleccion directa por numero de orden en la lista mostrada (ej. '7')
    try:
        numero_sel = int(criterio)
        if 1 <= numero_sel <= len(peliculas):
            return peliculas[numero_sel - 1]
    except ValueError:
        pass

    # 2. Busqueda directa por ID (ej. 'PEL-01')
    criterio_upper = criterio.upper()
    pelicula = gestor.buscar_por_id(criterio_upper)
    if pelicula:
        return pelicula

    # 3. Busqueda por coincidencia parcial en nombre o ID
    coincidencias = []
    criterio_lower = criterio.lower()
    for p in peliculas:
        if criterio_lower in p.nombre.lower() or criterio_lower in p.id.lower():
            coincidencias.append(p)

    if len(coincidencias) == 1:
        return coincidencias[0]
    elif len(coincidencias) > 1:
        print(f"\n{Colores.AMARILLO}Se encontraron múltiples coincidencias:{Colores.RESET}")
        for i, item in enumerate(coincidencias, start=1):
            sala_info = f"{item.sala} - {item.horario}" if item.sala != "Sin asignar" else "Sin sala asignada"
            print(f"  [{i}] {item.id} - {item.nombre} [{item.formato}] ({sala_info})")

        seleccion = input("Seleccione el número de la película (o 'c' para cancelar): ").strip()
        if seleccion.lower() in ("c", "0"):
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

    print(f"{Colores.ROJO}No se encontró ninguna película que coincida con '{criterio}'.{Colores.RESET}")
    return None


def agregar_nueva_pelicula(gestor):
    """
    Paso simplificado del Rol 5: Agrega una pelicula al catalogo.
    NO obliga a colocarla en sala de inmediato; puede quedar guardada lista para asignarse luego.
    """
    print(f"\n{Colores.CYAN}{Colores.NEGRITA}--- AGREGAR NUEVA PELÍCULA AL CATÁLOGO ---{Colores.RESET}")

    nombre = input("Título de la película: ").strip()
    if not nombre:
        print(f"{Colores.ROJO}Error: El título no puede estar vacío.{Colores.RESET}")
        return

    # Duracion en minutos con valor por defecto
    entrada_dur = input("Duración en minutos [120]: ").strip()
    try:
        duracion = int(entrada_dur) if entrada_dur else 120
        if duracion <= 0:
            duracion = 120
    except ValueError:
        duracion = 120

    # Precio base del boleto con valor por defecto
    entrada_costo = input("Precio base del boleto ($) [5.00]: ").strip()
    try:
        costo = float(entrada_costo) if entrada_costo else 5.00
        if costo < 0:
            costo = 5.00
    except ValueError:
        costo = 5.00

    # Formato de proyeccion
    print(f"\nFormatos disponibles: {', '.join(FORMATOS_VALIDOS)}")
    fmt_in = input("Formato [2D]: ").strip().upper()
    formato = fmt_in if fmt_in in FORMATOS_VALIDOS else "2D"

    # Clasificacion
    print(f"Clasificaciones: {', '.join(CLASIFICACIONES_VALIDAS)}")
    clasif_in = input("Clasificación de edad [A]: ").strip().upper()
    clasificacion = clasif_in if clasif_in in CLASIFICACIONES_VALIDAS else "A"

    descripcion = input("Descripción o sinopsis breve (opcional): ").strip()
    if not descripcion:
        descripcion = "Sin descripción adicional"

    fecha_estreno = input("Fecha de estreno (opcional) [En cartelera]: ").strip()
    if not fecha_estreno:
        fecha_estreno = "En cartelera"

    # Pregunta opcional de asignacion de sala
    asignar_sala = input(f"\n{Colores.AMARILLO}¿Desea asignar sala y horario ahora mismo? (s/n) [n]: {Colores.RESET}").strip().lower()

    if asignar_sala in ("s", "si", "sí"):
        print("\nSalas disponibles:")
        for i, s in enumerate(SALAS_DISPONIBLES, start=1):
            cap = CAPACIDADES_POR_SALA.get(s, 30)
            print(f"  [{i}] {s} (Capacidad: {cap} butacas)")
        opcion_sala = input(f"Seleccione sala (1-{len(SALAS_DISPONIBLES)}): ").strip()
        try:
            idx_sala = int(opcion_sala) - 1
            if 0 <= idx_sala < len(SALAS_DISPONIBLES):
                sala = SALAS_DISPONIBLES[idx_sala]
            else:
                sala = "Sala 1"
        except ValueError:
            sala = "Sala 1"

        horario = input("Horario de inicio (ej. '04:00 PM', '18:30'): ").strip()
        if not horario:
            horario = "04:00 PM"

        disponibilidad = CAPACIDADES_POR_SALA.get(sala, 30)
    else:
        sala = "Sin asignar"
        horario = "Por definir"
        disponibilidad = 0

    # Generar ID consecutivo tipo PEL-XX
    num_peliculas = len(gestor.listar_todas()) + 1
    id_personalizado = f"PEL-{num_peliculas:02d}"
    while gestor.buscar_por_id(id_personalizado) is not None:
        num_peliculas += 1
        id_personalizado = f"PEL-{num_peliculas:02d}"

    nueva = gestor.agregar_y_guardar_pelicula(
        nombre=nombre,
        descripcion=descripcion,
        duracion=duracion,
        costo=costo,
        fecha_de_estreno=fecha_estreno,
        horario=horario,
        sala=sala,
        disponibilidad=disponibilidad,
        clasificacion=clasificacion,
        formato=formato,
        id_personalizado=id_personalizado
    )

    if nueva:
        print(f"\n{Colores.VERDE}{Colores.NEGRITA}¡Película '{nombre}' guardada exitosamente en el catálogo!{Colores.RESET}")
        print(f"ID asignado: {Colores.AMARILLO}{nueva.id}{Colores.RESET} | Sala: {nueva.sala} | Horario: {nueva.horario} | Formato: {nueva.formato}")


def asignar_o_cambiar_sala_y_horario(gestor):
    """
    Permite asignar una pelicula a una sala fisica o cambiar el horario de una funcion.
    Configura automaticamente las butacas disponibles segun la capacidad de la sala.
    """
    print(f"\n{Colores.CYAN}{Colores.NEGRITA}--- ASIGNAR O CAMBIAR SALA Y HORARIO ---{Colores.RESET}")
    pelicula = localizar_pelicula(gestor)
    if not pelicula:
        return

    print(f"\nPelícula: {Colores.NEGRITA}{pelicula.nombre}{Colores.RESET} [{pelicula.formato}]")
    print(f"Estado actual: Sala: {pelicula.sala} | Horario: {pelicula.horario} | Butacas: {pelicula.disponibilidad}")

    print("\nSalas disponibles en el complejo:")
    for i, s in enumerate(SALAS_DISPONIBLES, start=1):
        cap = CAPACIDADES_POR_SALA.get(s, 30)
        print(f"  [{i}] {s} (Capacidad: {cap} butacas)")

    sel_sala = input(f"Seleccione sala (1-{len(SALAS_DISPONIBLES)}, o ENTER para mantener actual): ").strip()
    if sel_sala:
        try:
            idx = int(sel_sala) - 1
            if 0 <= idx < len(SALAS_DISPONIBLES):
                nueva_sala = SALAS_DISPONIBLES[idx]
                pelicula.set_sala(nueva_sala)
                # Al reasignar sala, inicializamos las butacas a la capacidad total de esa sala
                pelicula.set_disponibilidad(CAPACIDADES_POR_SALA.get(nueva_sala, 30))
        except ValueError:
            pass

    nuevo_horario = input(f"Horario de inicio (actual: '{pelicula.horario}', o ENTER para mantener): ").strip()
    if nuevo_horario:
        pelicula.set_horario(nuevo_horario)

    gestor.guardar_catalogo_en_csv()

    print(f"\n{Colores.VERDE}{Colores.NEGRITA}¡Función actualizada con éxito!{Colores.RESET}")
    print(f"Sala: {Colores.AZUL}{pelicula.sala}{Colores.RESET} | Horario: {pelicula.horario} (Fin est.: {pelicula.hora_fin}) | Butacas: {pelicula.disponibilidad}")


def modificar_datos_pelicula(gestor):
    """Permite ajustar precio base, formato o clasificacion de una pelicula."""
    print(f"\n{Colores.CYAN}{Colores.NEGRITA}--- MODIFICAR DATOS / TARIFAS DE PELÍCULA ---{Colores.RESET}")
    pelicula = localizar_pelicula(gestor)
    if not pelicula:
        return

    print(f"\nPelícula: {Colores.NEGRITA}{pelicula.nombre}{Colores.RESET} ({pelicula.id})")
    print(f"1. Costo base del boleto: ${pelicula.costo:.2f}")
    print(f"2. Formato de proyección: {pelicula.formato}")
    print(f"3. Clasificación de edad: [{pelicula.clasificacion}]")
    print(f"4. Butacas disponibles: {pelicula.disponibilidad}")

    opcion = input("\n¿Qué dato desea modificar? (1-4, o '0' para cancelar): ").strip()

    if opcion == "1":
        try:
            nuevo_costo = float(input("Ingrese nuevo costo base ($): ").strip())
            if nuevo_costo >= 0:
                pelicula.set_costo(nuevo_costo)
                gestor.guardar_catalogo_en_csv()
                print(f"{Colores.VERDE}¡Costo actualizado a ${nuevo_costo:.2f}!{Colores.RESET}")
            else:
                print(f"{Colores.ROJO}El costo no puede ser negativo.{Colores.RESET}")
        except ValueError:
            print(f"{Colores.ROJO}Valor numérico inválido.{Colores.RESET}")

    elif opcion == "2":
        print(f"\nFormatos: {', '.join(FORMATOS_VALIDOS)}")
        nuevo_fmt = input("Ingrese nuevo formato: ").strip().upper()
        if nuevo_fmt in FORMATOS_VALIDOS:
            pelicula.set_formato(nuevo_fmt)
            gestor.guardar_catalogo_en_csv()
            print(f"{Colores.VERDE}¡Formato actualizado a {nuevo_fmt}!{Colores.RESET}")

    elif opcion == "3":
        nueva_clasif = input(f"Ingrese clasificación ({', '.join(CLASIFICACIONES_VALIDAS)}): ").strip().upper()
        if nueva_clasif in CLASIFICACIONES_VALIDAS:
            pelicula.set_clasificacion(nueva_clasif)
            gestor.guardar_catalogo_en_csv()
            print(f"{Colores.VERDE}¡Clasificación actualizada a [{nueva_clasif}]!{Colores.RESET}")

    elif opcion == "4":
        try:
            nuevas_butacas = int(input("Ingrese nueva cantidad de butacas: ").strip())
            if nuevas_butacas >= 0:
                pelicula.set_disponibilidad(nuevas_butacas)
                gestor.guardar_catalogo_en_csv()
                print(f"{Colores.VERDE}¡Butacas actualizadas a {nuevas_butacas}!{Colores.RESET}")
        except ValueError:
            print(f"{Colores.ROJO}Número entero inválido.{Colores.RESET}")


def eliminar_pelicula_cartelera(gestor):
    """Paso del Rol 5: Eliminar una pelicula de la cartelera."""
    print(f"\n{Colores.CYAN}{Colores.NEGRITA}--- ELIMINAR PELÍCULA DE CARTELERA ---{Colores.RESET}")
    pelicula = localizar_pelicula(gestor)
    if not pelicula:
        return

    print(f"\n{Colores.ROJO}Película a eliminar:{Colores.RESET}")
    print(f"  ID: {pelicula.id} | {pelicula.nombre} [{pelicula.formato}]")
    print(f"  Sala: {pelicula.sala} | Horario: {pelicula.horario}")

    if confirmar_accion("¿Está seguro de eliminar esta película del sistema?"):
        eliminada = gestor.eliminar_pelicula(pelicula.id)
        if eliminada:
            print(f"\n{Colores.VERDE}{Colores.NEGRITA}¡Película '{eliminada.nombre}' eliminada con éxito!{Colores.RESET}")
    else:
        print(f"\n{Colores.AMARILLO}Operación cancelada.{Colores.RESET}")


def menu_gestion_cartelera():
    """Imprime las opciones del submenu de administracion de cartelera."""
    print(f"\n{Colores.AZUL}{Colores.NEGRITA}=========================================================")
    print("||       ROL 5: GESTIÓN DE CARTELERA Y SALAS           ||")
    print(f"========================================================={Colores.RESET}")
    print(f"{Colores.NEGRITA}Seleccione una operación:{Colores.RESET}\n")
    print(f"  {Colores.VERDE}[1]{Colores.RESET} Consultar cartelera y salas completa")
    print(f"  {Colores.VERDE}[2]{Colores.RESET} Agregar película al catálogo (creación rápida)")
    print(f"  {Colores.AMARILLO}[3]{Colores.RESET} Asignar o cambiar sala y horario de función")
    print(f"  {Colores.CYAN}[4]{Colores.RESET} Modificar datos base (precio, formato, butacas)")
    print(f"  {Colores.ROJO}[5]{Colores.RESET} Eliminar película de cartelera")
    print(f"  {Colores.NEGRITA}[6]{Colores.RESET} Volver al menú de administrador\n")
    print(f"{Colores.AZUL}---------------------------------------------------------{Colores.RESET}")


def iniciar_modulo_cartelera_admin(ruta_csv=RUTA_CARTELERA):
    """Punto de entrada principal para el Rol 5 (Administrador de Cartelera)."""
    gestor = GestorCartelera(ruta_csv=ruta_csv)

    while True:
        limpiar_pantalla()
        menu_gestion_cartelera()
        opcion = input("Ingrese una opción (1-6): ").strip()

        if opcion == "1":
            limpiar_pantalla()
            listar_cartelera_admin(gestor)
            pausar()
        elif opcion == "2":
            limpiar_pantalla()
            agregar_nueva_pelicula(gestor)
            pausar()
        elif opcion == "3":
            limpiar_pantalla()
            asignar_o_cambiar_sala_y_horario(gestor)
            pausar()
        elif opcion == "4":
            limpiar_pantalla()
            modificar_datos_pelicula(gestor)
            pausar()
        elif opcion == "5":
            limpiar_pantalla()
            eliminar_pelicula_cartelera(gestor)
            pausar()
        elif opcion == "6":
            print(f"\n{Colores.AMARILLO}Regresando al menú de administrador...{Colores.RESET}")
            break
        else:
            print(f"\n{Colores.ROJO}Opción inválida. Intente nuevamente.{Colores.RESET}")
            pausar()


if __name__ == "__main__":
    iniciar_modulo_cartelera_admin()
