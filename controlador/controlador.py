# controlador/controlador.py
from modelo.conexion import ConexionDB

class ControladorDB:
    def __init__(self, host, user, password, database):
        # Inicializamos la conexión a la base de datos usando la clase ConexionDB
        self.conexion = ConexionDB(host, user, password, database)
        self.conexion.conectar()  # Establece la conexión inmediatamente al crear el controlador

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos."""
        self.conexion.cerrar()

    def insertar_datos(self, consulta, parametros):
        """Ejecuta una consulta de inserción de datos."""
        try:
            self.conexion.ejecutar_consulta(consulta, parametros)
        except Exception as e:
            print(f"Error al insertar datos: {e}")

    def modificar_datos(self, consulta, parametros):
        """Ejecuta una consulta para modificar datos."""
        try:
            self.conexion.ejecutar_consulta(consulta, parametros)
        except Exception as e:
            print(f"Error al modificar datos: {e}")

    def obtener_datos(self, consulta, parametros=()):
        """Obtiene los datos de una consulta."""
        try:
            return self.conexion.obtener_resultados(consulta, parametros)
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return None
