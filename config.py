# Archivo: config.py
# Configuracion centralizada del Sistema Gestor de Cine (Paso 2).
# Unica fuente de verdad para rutas absolutas y reglas/limites de negocio.

import os

# Directorio raiz del proyecto reorganizado (independiente del directorio de trabajo CWD)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Carpeta dedicada exclusivamente a los archivos de persistencia CSV
DATA_DIR = os.path.join(BASE_DIR, "datos")

# Rutas absolutas hacia los archivos CSV unificados
RUTA_CARTELERA = os.path.join(DATA_DIR, "cartelera.csv")
RUTA_STOCK = os.path.join(DATA_DIR, "stock.csv")
RUTA_REPORTE_VENTAS = os.path.join(DATA_DIR, "reporte_ventas.csv")

# Reglas de negocio para Boleteria y Cartelera (Rol 5)
CAPACIDAD_SALA_DEFECTO = 30
LIMITE_BOLETOS_POR_COMPRA = 10
SALAS_DISPONIBLES = ("Sala 1", "Sala 2", "Sala 3", "Sala IMAX")
FORMATOS_VALIDOS = ("2D", "3D", "IMAX")
CLASIFICACIONES_VALIDAS = ("A", "B", "C", "PG-13", "+18")
CAPACIDADES_POR_SALA = {
    "Sala 1": 30,
    "Sala 2": 40,
    "Sala 3": 35,
    "Sala IMAX": 50
}

# Clases de boletos y promociones
TARIFAS_CLASES = {
    "General": 1.00,        # Tarifa completa
    "Mayor de edad": 0.80,  # 20% de descuento (tercera edad)
    "Niño": 0.70            # 30% de descuento (infantil)
}
DESCUENTO_LUNES = 0.15      # 15% de descuento especial los lunes

# Reglas de validacion y limites de seguridad para Inventario de Dulceria (Rol 4)
MIN_LEN_NOMBRE_SNACK = 2
MAX_LEN_NOMBRE_SNACK = 40
MAX_LEN_DESCRIPCION_SNACK = 120
PRECIO_MIN_SNACK = 0.01
PRECIO_MAX_SNACK = 1000.00
STOCK_MIN_SNACK = 0
STOCK_MAX_SNACK = 10000
PASSWORD_ADMIN = '2026'