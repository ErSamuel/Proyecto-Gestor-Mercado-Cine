# Archivo: boleteria/menu_admin.py
# Modulo de Administracion de Cartelera y Salas (Rol 5).
# Disenado con validaciones estrictas y a prueba de errores de usuario (sin defaults silenciosos ante '0').

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
    pausar,
    pedir_entero,
    pedir_flotante,
    pedir_horario_valido,
    pedir_opcion_menu,
    pedir_texto_no_vacio
)


def listar_cartelera_admin(gestor):
    """Muestra la tabla completa de peliculas con salas, horarios, butacas y formatos."""
    peliculas = gestor.listar_todas()
    print(f"\n{Colores.AZUL}{Colores.NEGRITA}" + "=" * 114 + f"{Colores.RESET}")
    print(f"{Colores.CYAN}{Colores.NEGRITA}{'CARTELERA GENERAL Y SALAS (VISTA ADMINISTRADOR)':^114}{Colores.RESET}")
    print(f"{Colores.AZUL}{Colores.NEGRITA}" + "=" * 114 + f"{Colores.RESET}")

    if not peliculas:
        print(f"{Colores.ROJO}No hay ninguna película registrada en la cartelera.{Colores.RESET}")
        print(f"{Colores.AZUL}" + "-" * 114 + f"{Colores.RESET}")
        return

    encabezado = f"{'ID':<8} | {'TÍTULO':<25} | {'FMT':<5} | {'EDAD':<7} | {'SALA':<12} | {'HORARIO':<11} | {'FIN EST.':<10} | {'PRECIO':<7} | {'ESTADO/BUTACAS'}"
    print(f"{Colores.NEGRITA}{encabezado}{Colores.RESET}")
    print(f"{Colores.AZUL}" + "-" * 114 + f"{Colores.RESET}")

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

        edad_formateada = f"[{p.clasificacion}]"

        print(
            f"{Colores.AMARILLO}{p.id:<8}{Colores.RESET} | "
            f"{Colores.NEGRITA}{titulo_str:<25}{Colores.RESET} | "
            f"{Colores.CYAN}{p.formato:<5}{Colores.RESET} | "
            f"{edad_formateada:<7} | "
            f"{sala_str} | "
            f"{p.horario:<11} | "
            f"{p.hora_fin:<10} | "
            f"{Colores.VERDE}{precio_str:<7}{Colores.RESET} | "
            f"{estado_str}"
        )

    print(f"{Colores.AZUL}{Colores.NEGRITA}" + "=" * 114 + f"{Colores.RESET}")


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
    Paso robusto del Rol 5: Agrega una pelicula al catalogo.
    Valida estrictamente duracion, precio y opciones numericas sin aceptar '0' ni basura.
    Permite opcionalmente programarla en sala o dejarla en catalogo.
    """
    print(f"\n{Colores.CYAN}{Colores.NEGRITA}--- AGREGAR NUEVA PELÍCULA AL CATÁLOGO ---{Colores.RESET}")

    # 1. Titulo de la pelicula
    nombre = pedir_texto_no_vacio("Título de la película: ", min_len=2, max_len=60)
    
    # Validar si ya existe otra función con ese mismo nombre e informar
    if any(p.nombre.strip().lower() == nombre.lower() for p in gestor.listar_todas()):
        print(f"{Colores.AMARILLO}[AVISO] Ya existe al menos una función registrada para '{nombre}'. Se registrará como una función adicional.{Colores.RESET}")

    # 2. Duracion en minutos (30 a 360 min)
    duracion = pedir_entero("Duración en minutos (30 a 360): ", minimo=30, maximo=360)

    # 3. Precio base del boleto (mayor a $0.00)
    costo = pedir_flotante("Precio base del boleto ($) (mínimo $0.50): ", minimo=0.50, maximo=100.00)

    # 4. Formato de proyeccion (seleccion numerica obligatoria)
    print("\nFormatos de proyección disponibles:")
    for i, f in enumerate(FORMATOS_VALIDOS, start=1):
        print(f"  [{i}] {f}")
    opc_fmt = pedir_opcion_menu(f"Seleccione formato (1-{len(FORMATOS_VALIDOS)}): ", total_opciones=len(FORMATOS_VALIDOS))
    formato = FORMATOS_VALIDOS[opc_fmt - 1]

    # 5. Clasificacion por edad (seleccion numerica obligatoria)
    print("\nClasificaciones por edad:")
    for i, c in enumerate(CLASIFICACIONES_VALIDAS, start=1):
        print(f"  [{i}] {c}")
    opc_clasif = pedir_opcion_menu(f"Seleccione clasificación (1-{len(CLASIFICACIONES_VALIDAS)}): ", total_opciones=len(CLASIFICACIONES_VALIDAS))
    clasificacion = CLASIFICACIONES_VALIDAS[opc_clasif - 1]

    # 6. Descripcion o sinopsis (texto libre)
    descripcion = input("Descripción o sinopsis breve (opcional): ").strip()
    if not descripcion:
        descripcion = "Sin descripción adicional"
    elif len(descripcion) > 150:
        descripcion = descripcion[:147] + "..."

    # 7. Fecha de estreno
    fecha_estreno = input("Fecha de estreno (opcional) [En cartelera]: ").strip()
    if not fecha_estreno:
        fecha_estreno = "En cartelera"
    elif len(fecha_estreno) > 40:
        fecha_estreno = fecha_estreno[:40]

    # 8. Asignacion opcional de sala
    asignar_sala = confirmar_accion("¿Desea asignar sala y horario ahora mismo?")

    if asignar_sala:
        while True:
            print("\nSalas disponibles:")
            for i, s in enumerate(SALAS_DISPONIBLES, start=1):
                cap = CAPACIDADES_POR_SALA.get(s, 30)
                print(f"  [{i}] {s} (Capacidad: {cap} butacas)")
            print("  [0] Cancelar asignación de sala por ahora")
            opc_sala = pedir_opcion_menu(f"Seleccione sala (1-{len(SALAS_DISPONIBLES)}, o 0 para cancelar): ", total_opciones=len(SALAS_DISPONIBLES), permitir_cero=True)
            if opc_sala == 0:
                sala = "Sin asignar"
                horario = "Por definir"
                disponibilidad = 0
                break

            cand_sala = SALAS_DISPONIBLES[opc_sala - 1]
            cand_horario = pedir_horario_valido("Horario de inicio de la función (ej. '04:00 PM', '18:30'): ", permitir_cancelar=True)
            if not cand_horario:
                sala = "Sin asignar"
                horario = "Por definir"
                disponibilidad = 0
                break

            solapa, motivo = gestor.validar_solapamiento(cand_sala, cand_horario, duracion)
            if solapa:
                print(f"{Colores.ROJO}Error de solapamiento: {motivo}{Colores.RESET}")
                print(f"{Colores.AMARILLO}Por favor elija otra sala u otro horario.{Colores.RESET}")
            else:
                sala = cand_sala
                horario = cand_horario
                disponibilidad = CAPACIDADES_POR_SALA.get(sala, 30)
                break
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
    Valida solapamientos de horario en la misma sala segun la duracion de la pelicula.
    Configura automaticamente las butacas disponibles segun la capacidad de la sala.
    """
    print(f"\n{Colores.CYAN}{Colores.NEGRITA}--- ASIGNAR O CAMBIAR SALA Y HORARIO ---{Colores.RESET}")
    pelicula = localizar_pelicula(gestor)
    if not pelicula:
        return

    print(f"\nPelícula seleccionada: {Colores.NEGRITA}{pelicula.nombre}{Colores.RESET} [{pelicula.formato}]")
    print(f"Estado actual: Sala: {pelicula.sala} | Horario: {pelicula.horario} | Butacas: {pelicula.disponibilidad}")

    print("\nSalas disponibles en el complejo:")
    for i, s in enumerate(SALAS_DISPONIBLES, start=1):
        cap = CAPACIDADES_POR_SALA.get(s, 30)
        print(f"  [{i}] {s} (Capacidad: {cap} butacas)")

    print(f"  [0] Mantener sala actual ({pelicula.sala})")
    sel_sala = pedir_opcion_menu(f"Seleccione sala (1-{len(SALAS_DISPONIBLES)}, o 0 para mantener): ", total_opciones=len(SALAS_DISPONIBLES), permitir_cero=True)
    nueva_sala = SALAS_DISPONIBLES[sel_sala - 1] if sel_sala > 0 else pelicula.sala

    nuevo_horario = pedir_horario_valido(f"Nuevo horario de inicio (actual: '{pelicula.horario}', o '0' para mantener): ", permitir_cancelar=True)
    if not nuevo_horario:
        nuevo_horario = pelicula.horario

    # Si la sala no es 'Sin asignar' y el horario no es 'Por definir', validar solapamiento
    if nueva_sala.strip().lower() not in ("sin asignar", "por definir") and nuevo_horario.strip().lower() not in ("por definir", "sin asignar"):
        solapa, motivo = gestor.validar_solapamiento(nueva_sala, nuevo_horario, pelicula.duracion, excluir_id=pelicula.id)
        if solapa:
            print(f"\n{Colores.ROJO}Error de solapamiento: {motivo}{Colores.RESET}")
            print(f"{Colores.AMARILLO}No se aplicaron cambios de sala/horario.{Colores.RESET}")
            return

    pelicula.set_sala(nueva_sala)
    pelicula.set_horario(nuevo_horario)

    # Si se asigno a una sala fisica real, se actualizan las butacas a la capacidad de esa sala
    if nueva_sala.strip().lower() not in ("sin asignar", "por definir"):
        pelicula.set_disponibilidad(CAPACIDADES_POR_SALA.get(nueva_sala, 30))
    else:
        pelicula.set_disponibilidad(0)

    gestor.guardar_catalogo_en_csv()

    print(f"\n{Colores.VERDE}{Colores.NEGRITA}¡Función actualizada con éxito!{Colores.RESET}")
    print(f"Sala: {Colores.AZUL}{pelicula.sala}{Colores.RESET} | Horario: {pelicula.horario} (Fin est.: {pelicula.hora_fin}) | Butacas: {pelicula.disponibilidad}")


def modificar_datos_pelicula(gestor):
    """Permite ajustar todos los datos de una pelicula con validaciones estrictas y completas."""
    print(f"\n{Colores.CYAN}{Colores.NEGRITA}--- MODIFICAR DATOS / TARIFAS DE PELÍCULA ---{Colores.RESET}")
    pelicula = localizar_pelicula(gestor)
    if not pelicula:
        return

    print(f"\nPelícula: {Colores.NEGRITA}{pelicula.nombre}{Colores.RESET} ({pelicula.id})")
    print(f"1. Costo base del boleto: ${pelicula.costo:.2f}")
    print(f"2. Formato de proyección: {pelicula.formato}")
    print(f"3. Clasificación de edad: [{pelicula.clasificacion}]")
    print(f"4. Butacas disponibles: {pelicula.disponibilidad} (Sala: {pelicula.sala})")
    print(f"5. Título de la película: {pelicula.nombre}")
    print(f"6. Duración: {pelicula.duracion} min (Fin est.: {pelicula.hora_fin})")
    print(f"7. Descripción / Sinopsis: {pelicula.descripcion[:40]}...")
    print(f"8. Fecha de estreno: {pelicula.fecha_de_estreno}")

    opcion = pedir_opcion_menu("\n¿Qué dato desea modificar? (1-8, o 0 para cancelar): ", total_opciones=8, permitir_cero=True)
    if opcion == 0:
        print(f"{Colores.AMARILLO}Modificación cancelada.{Colores.RESET}")
        return

    if opcion == 1:
        nuevo_costo = pedir_flotante("Ingrese nuevo costo base ($) (mínimo $0.50): ", minimo=0.50, maximo=100.00)
        pelicula.set_costo(nuevo_costo)
        gestor.guardar_catalogo_en_csv()
        print(f"{Colores.VERDE}¡Costo actualizado exitosamente a ${nuevo_costo:.2f}!{Colores.RESET}")

    elif opcion == 2:
        print("\nFormatos disponibles:")
        for i, f in enumerate(FORMATOS_VALIDOS, start=1):
            print(f"  [{i}] {f}")
        opc_f = pedir_opcion_menu(f"Seleccione nuevo formato (1-{len(FORMATOS_VALIDOS)}): ", total_opciones=len(FORMATOS_VALIDOS))
        nuevo_fmt = FORMATOS_VALIDOS[opc_f - 1]
        pelicula.set_formato(nuevo_fmt)
        gestor.guardar_catalogo_en_csv()
        print(f"{Colores.VERDE}¡Formato actualizado a {nuevo_fmt}!{Colores.RESET}")

    elif opcion == 3:
        print("\nClasificaciones por edad:")
        for i, c in enumerate(CLASIFICACIONES_VALIDAS, start=1):
            print(f"  [{i}] {c}")
        opc_c = pedir_opcion_menu(f"Seleccione clasificación (1-{len(CLASIFICACIONES_VALIDAS)}): ", total_opciones=len(CLASIFICACIONES_VALIDAS))
        nueva_clasif = CLASIFICACIONES_VALIDAS[opc_c - 1]
        pelicula.set_clasificacion(nueva_clasif)
        gestor.guardar_catalogo_en_csv()
        print(f"{Colores.VERDE}¡Clasificación actualizada a [{nueva_clasif}]!{Colores.RESET}")

    elif opcion == 4:
        # Validacion de sala fisica obligatoria
        if pelicula.sala.strip().lower() in ("sin asignar", "por definir"):
            print(f"{Colores.ROJO}[AVISO] La película no tiene una sala asignada. Asigne primero una sala física (opción 3 del menú de cartelera) para poder gestionar sus butacas.{Colores.RESET}")
            return
        capacidad_max = CAPACIDADES_POR_SALA.get(pelicula.sala, 50)
        nuevas_butacas = pedir_entero(f"Ingrese nueva cantidad de butacas (0 a {capacidad_max}): ", minimo=0, maximo=capacidad_max)
        pelicula.set_disponibilidad(nuevas_butacas)
        gestor.guardar_catalogo_en_csv()
        print(f"{Colores.VERDE}¡Butacas actualizadas a {nuevas_butacas}!{Colores.RESET}")

    elif opcion == 5:
        nuevo_nombre = pedir_texto_no_vacio("Nuevo título de la película: ", min_len=2, max_len=60)
        if any(p.nombre.strip().lower() == nuevo_nombre.lower() and p.id != pelicula.id for p in gestor.listar_todas()):
            print(f"{Colores.AMARILLO}[AVISO] Ya existe otra función registrada con el título '{nuevo_nombre}'. Se mantendrá como función adicional.{Colores.RESET}")
        pelicula.nombre = nuevo_nombre
        gestor.guardar_catalogo_en_csv()
        print(f"{Colores.VERDE}¡Título actualizado a '{nuevo_nombre}'!{Colores.RESET}")

    elif opcion == 6:
        nueva_duracion = pedir_entero("Nueva duración en minutos (30 a 360): ", minimo=30, maximo=360)
        if pelicula.sala.strip().lower() not in ("sin asignar", "por definir") and pelicula.horario.strip().lower() not in ("por definir", "sin asignar"):
            solapa, motivo = gestor.validar_solapamiento(pelicula.sala, pelicula.horario, nueva_duracion, excluir_id=pelicula.id)
            if solapa:
                print(f"{Colores.ROJO}Error: La nueva duración generaría un conflicto de sala: {motivo}{Colores.RESET}")
                return
        pelicula.set_duracion(nueva_duracion)
        gestor.guardar_catalogo_en_csv()
        print(f"{Colores.VERDE}¡Duración actualizada a {nueva_duracion} minutos (Nueva hora fin: {pelicula.hora_fin})!{Colores.RESET}")

    elif opcion == 7:
        nueva_desc = input("Nueva descripción o sinopsis breve (máximo 150 caracteres, vacío para mantener): ").strip()
        if nueva_desc:
            if len(nueva_desc) > 150:
                nueva_desc = nueva_desc[:147] + "..."
            pelicula.descripcion = nueva_desc
            gestor.guardar_catalogo_en_csv()
            print(f"{Colores.VERDE}¡Descripción actualizada exitosamente!{Colores.RESET}")
        else:
            print(f"{Colores.AMARILLO}Descripción sin cambios.{Colores.RESET}")

    elif opcion == 8:
        nueva_fecha = input("Nueva fecha de estreno (máximo 40 caracteres, vacío para mantener): ").strip()
        if nueva_fecha:
            if len(nueva_fecha) > 40:
                nueva_fecha = nueva_fecha[:40]
            pelicula.fecha_de_estreno = nueva_fecha
            gestor.guardar_catalogo_en_csv()
            print(f"{Colores.VERDE}¡Fecha de estreno actualizada exitosamente!{Colores.RESET}")
        else:
            print(f"{Colores.AMARILLO}Fecha de estreno sin cambios.{Colores.RESET}")


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
    print(f"  {Colores.CYAN}[4]{Colores.RESET} Modificar datos base (precio, formato, butacas, título, etc.)")
    print(f"  {Colores.ROJO}[5]{Colores.RESET} Eliminar película de cartelera")
    print(f"  {Colores.NEGRITA}[6]{Colores.RESET} Volver al menú de administrador\n")
    print(f"{Colores.AZUL}---------------------------------------------------------{Colores.RESET}")


def iniciar_modulo_cartelera_admin(ruta_csv=RUTA_CARTELERA):
    """Punto de entrada principal para el Rol 5 (Administrador de Cartelera)."""
    gestor = GestorCartelera(ruta_csv=ruta_csv)

    while True:
        gestor.cargar_desde_csv()
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
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    iniciar_modulo_cartelera_admin()
