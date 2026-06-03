import mysql.connector

class Conexion:
    def __init__(self,
                 host: str = "localhost",
                 user: str = "root",
                 password: str = "",
                 database: str = "monopoli"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexion = None
        self.cursor = None

    def conectar(self):
        self.conexion = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            autocommit=False
        )
        self.cursor = self.conexion.cursor()

    def desconectar(self):
        if self.cursor:
            try:
                self.cursor.close()
            except Exception:
                pass
        if self.conexion:
            try:
                self.conexion.close()
            except Exception:
                pass
