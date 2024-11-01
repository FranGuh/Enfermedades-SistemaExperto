import mysql.connector

class ConexionDB:
    def __init__(self, host, user, password, database):
        self.conn = None
        self.cursor = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def conectar(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor()
            print("Conexión a la base de datos establecida")
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def cerrar(self):
        if self.conn:
            self.conn.close()
            print("Conexión a la base de datos cerrada")

    def ejecutar_consulta(self, consulta, parametros=()):
        if self.cursor:
            try:
                self.cursor.execute(consulta, parametros)
                self.conn.commit()
            except mysql.connector.Error as e:
                print(f"Error al ejecutar la consulta: {e}")
        else:
            print("No hay conexión activa a la base de datos.")

    def obtener_resultados(self, consulta, parametros=()):
        if self.cursor:
            try:
                self.cursor.execute(consulta, parametros)
                return self.cursor.fetchall()
            except mysql.connector.Error as e:
                print(f"Error al obtener resultados: {e}")
        else:
            print("No hay conexión activa a la base de datos.")
