# 🎬 Sistema Automatizado de Gestión de Cine

Aplicación de consola desarrollada en **Python** con arquitectura modular y programación orientada a objetos (POO) para administrar las operaciones de un cine: compra de entradas en **boletería**, venta directa en **dulcería**, administración de **inventario** y **cartelera/salas**, y **reportes financieros** con persistencia en archivos `.csv`.

---

## 👥 Integrantes

- **Jesús Herrada**
- **Samuel Reyna**
- **Greilys Hernández**
- **Jorge Naranjo**
- **Edgar Martínez**

---

## 🎯 Alcance del Sistema

- Enfocado en la gestión operativa de **una sola sede de cine**.
- No contempla gestión de personal.
- El flujo de cobro en consola es **simulado** (no procesa pagos reales ni impuestos).

---

## ✨ Funcionalidades Implementadas

### Perfil Usuario (Cliente)
- **Dulcería (`dulceria/menu_cliente.py`):**
  - Al ingresar muestra directamente la lista numerada de snacks disponibles, resaltando producto, precio y disponibilidad con código de color.
  - Selección directa por número para consultar la ficha detallada del producto (nombre, descripción, precio unitario y stock).
  - Validación de cantidad a comprar, resumen detallado del producto y total al pagar, actualización segura en `datos/stock.csv` (con reversión automática si falla el guardado en disco) y registro en `datos/reporte_ventas.csv`.
- **Boletería (`boleteria/menu_boleteria.py`):**
  - Cartelera numerada con formato (`2D`, `3D`, `IMAX`), clasificación, duración formateada (`HH:MM:SS`), horario, sala, precio base y estado/butacas disponibles.
  - Ficha detallada de la función seleccionada con sinopsis y hora estimada de finalización.
  - Venta con **3 clases de entradas**: *General (Adulto)* (`100%`), *Mayor de edad (+60)* (`-20%`) y *Niño (hasta 12 años)* (`-30%`), más modalidad **Mixta** para distribuir varias clases en una compra (hasta `10` butacas por transacción).

### Perfil Administrador
> Acceso protegido por contraseña definida en `config.py` (por defecto: `2026`), con máximo `3` intentos, límite de `20` caracteres y opción de cancelación rápida (`0` o `C`).

- **Gestión de Inventario de Dulcería — Rol 4 (`dulceria/menu_admin.py`):**
  - CRUD completo: alta de productos con generación automática de ID hash único (`000`–`999`), modificación de precios, actualización de stock (fijar total, sumar o restar unidades) y eliminación con confirmación interactiva.
  - Consulta del inventario completo en tabla alineada con semáforo de stock por color.
  - Selección ágil por ID exacto (prioritario), número de orden en lista, búsqueda O(1) por clave hash o coincidencia parcial.
- **Gestión de Cartelera y Sala (`boleteria/menu_admin.py`):**
  - Consulta tabular completa de películas, formatos, clasificaciones, salas, horarios, hora estimada de fin, precios y butacas libres.
  - Registro de nuevas películas (`PEL-XX`) con asignación opcional de sala/horario y soporte para múltiples funciones de un mismo título.
  - Asignación o cambio de sala y horario configurando automáticamente la capacidad física de la sala y validando solapamientos horarios (`validar_solapamiento`) según la duración.
  - Modificación completa de datos de película (costo base, formato, clasificación, butacas —exigiendo sala asignada—, título, duración con revalidación de cruces, descripción y fecha de estreno) y eliminación con confirmación.
- **Control, Métricas y Reportes (`finanzas/reportes.py`):**
  - Recaudación acumulada (general, solo boletos y solo dulces).
  - Rankings de productos más y menos vendidos (general, dulce y película), con soporte para empates y normalización de nombres históricos entre formatos.
  - Resumen de operaciones (total de transacciones, unidades despachadas y recaudación) e historial tabular completo de ventas.

### Núcleo y Robustez Técnica (`nucleo/`)
- **Estilos centralizados (`nucleo/colores.py`):** clase `Colores` unificada para los códigos ANSI en terminal.
- **Validadores de entrada (`nucleo/consola.py`):** `pedir_entero`, `pedir_flotante` (acepta coma decimal y valida `math.isfinite` contra `nan`/`inf`), `pedir_opcion_menu`, `pedir_horario_valido` (estandarizado a `HH:MM AM/PM`), `pedir_texto_no_vacio`, `confirmar_accion` y `conversor_de_minutos`.
- **Persistencia segura (`guardar_csv_seguro` y `append_csv_seguro`):** captura errores de bloqueo de archivo (`PermissionError`/`OSError`, por ejemplo si el CSV está abierto en Excel) permitiendo cerrar el archivo y reintentar sin perder datos ni cerrar la aplicación.

---

## 🏗️ Arquitectura del Proyecto

El proyecto está organizado por dominios funcionales, sin dependencias externas:

```text
Proyecto-Gestor-Mercado-Cine/
├── main.py                       # Punto de entrada y navegación de perfiles (Usuario / Administrador)
├── config.py                     # Rutas absolutas, reglas/límites de negocio, tarifas y contraseña
├── boleteria/
│   ├── __init__.py
│   ├── pelicula.py               # Clase Pelicula (formato, clasificación, hora_fin, validaciones y getters/setters)
│   ├── gestor_cartelera.py       # Clase GestorCartelera (persistencia CSV, solapamientos y registro de ventas)
│   ├── menu_boleteria.py         # Interfaz de taquilla para cliente (clases de boletos y promo lunes)
│   └── menu_admin.py             # Panel de administración de cartelera y salas (Rol 5)
├── dulceria/
│   ├── __init__.py
│   ├── snack.py                  # Clase Snack (atributos privados, validaciones y getters/setters)
│   ├── gestor_inventario.py      # Persistencia en stock.csv, IDs hash, catálogo y buscador
│   ├── menu_cliente.py           # Interfaz directa de dulcería para clientes (Rol 2)
│   └── menu_admin.py             # Panel de administración de inventario (Rol 4)
├── finanzas/
│   ├── __init__.py
│   ├── pagos.py                  # Pasarela de pago simulada y registro seguro en reporte_ventas.csv
│   └── reportes.py               # Módulo de auditoría, métricas, rankings e historial (Rol 6)
├── nucleo/
│   ├── __init__.py
│   ├── colores.py                # Clase Colores unificada para formato ANSI en terminal
│   └── consola.py                # Utilidades de consola, validadores estrictos y guardado CSV seguro
└── datos/
    ├── cartelera.csv             # Películas, formatos, clasificaciones, salas, horarios y butacas
    ├── stock.csv                 # Inventario actual de la dulcería
    └── reporte_ventas.csv        # Historial acumulado de ventas (boletos y dulces)
```

---

## ▶️ Ejecución

Desde la raíz del proyecto, ejecuta el programa principal:

```bash
python main.py
```

> Los archivos de datos se resuelven mediante rutas absolutas a partir de `config.py`, por lo que `main.py` puede ejecutarse desde cualquier directorio.

---

## ⚙️ Configuración y Reglas de Negocio (`config.py`)

| Parámetro | Valor por defecto | Descripción |
| :--- | :---: | :--- |
| `PASSWORD_ADMIN` | `'2026'` | Contraseña de acceso al panel de administrador |
| `SALAS_DISPONIBLES` | `Sala 1`, `Sala 2`, `Sala 3`, `Sala IMAX` | Salas configuradas en el complejo |
| `CAPACIDADES_POR_SALA` | `30`, `40`, `35`, `50` (`30` por defecto) | Capacidad máxima de butacas por sala |
| `FORMATOS_VALIDOS` | `2D`, `3D`, `IMAX` | Formatos de proyección permitidos |
| `CLASIFICACIONES_VALIDAS` | `A`, `B`, `C`, `PG-13`, `+18` | Clasificaciones por edad admitidas |
| `LIMITE_BOLETOS_POR_COMPRA` | `10` | Máximo de entradas permitidas por transacción |
| `TARIFAS_CLASES` | General `1.00`, Mayor `0.80`, Niño `0.70` | Multiplicadores por clase de boleto |
| `DESCUENTO_LUNES` | `0.15` | Descuento especial aplicado los lunes (`15%`) |
| `MIN_LEN_NOMBRE_SNACK` / `MAX_LEN_NOMBRE_SNACK` | `2` / `40` | Longitud permitida para nombres de snacks |
| `MAX_LEN_DESCRIPCION_SNACK` | `120` | Longitud máxima de descripción de snacks |
| `PRECIO_MIN_SNACK` / `PRECIO_MAX_SNACK` | `$0.01` / `$1000.00` | Rango válido de precios en dulcería |
| `STOCK_MIN_SNACK` / `STOCK_MAX_SNACK` | `0` / `10000` | Rango válido de unidades en inventario |

---

## 💾 Estructura de los Archivos CSV (`datos/`)

- **`datos/cartelera.csv`**: `id,nombre,descripcion,duracion,costo,fecha_de_estreno,horario,sala,disponibilidad,clasificacion,formato`
- **`datos/stock.csv`**: `id_hash,nombre,descripcion,precio,cantidad`
- **`datos/reporte_ventas.csv`**: `tipo,nombre_item,cantidad,total_pagado`
