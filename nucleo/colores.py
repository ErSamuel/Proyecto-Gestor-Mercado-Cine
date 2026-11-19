# Archivo: nucleo/colores.py
# Define la clase Colores para centralizar e importar los codigos de estilo ANSI en todo el proyecto.


class Colores:
    """
    Contenedor unificado de codigos de escape ANSI para dar estilo a la consola.
    Permite importar la paleta desde cualquier modulo mediante:
        from nucleo.colores import Colores
    """

    # Codigos de color ANSI estandar para terminal
    AZUL = "\033[94m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    ROJO = "\033[91m"
    CYAN = "\033[96m"

    # Codigos de formato y reinicio de estilo
    NEGRITA = "\033[1m"
    RESET = "\033[0m"

    @classmethod
    def pintar(cls, texto, color, negrita=False):
        """
        Envuelve una cadena de texto con el color indicado (y negrita opcional),
        cerrando siempre con Colores.RESET para evitar fugas de estilo.
        """
        prefijo = f"{cls.NEGRITA}{color}" if negrita else color
        return f"{prefijo}{texto}{cls.RESET}"
