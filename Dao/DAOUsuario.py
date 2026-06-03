from Dao.conexiones import Conexion
from seguridad import Seguridad

class DAOUsuario:
    def obtener_usuario(self, rut: str):
        conexion = Conexion()
        try:
            conexion.conectar()
            sql = "SELECT rut, password_hash FROM Usuarios WHERE rut = %s"
            conexion.cursor.execute(sql, (rut,))
            fila = conexion.cursor.fetchone()
            return fila if fila else None
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
        finally:
            conexion.desconectar()

    def crear_usuario(self, rut: str, password: str):
        if self.obtener_usuario(rut):
            print("El usuario ya existe.")
            return False

        contraseña_hash = Seguridad.encriptar_clave(password)
        conexion = Conexion()
        try:
            conexion.conectar()
            sql = "INSERT INTO Usuarios (rut, password_hash) VALUES (%s, %s)"
            conexion.cursor.execute(sql, (rut, contraseña_hash))
            conexion.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return False
        finally:
            conexion.desconectar()

    def validar_usuario(self, rut: str, password: str):
        fila = self.obtener_usuario(rut)
        if not fila:
            return False
        _, password_hash = fila
        return Seguridad.validar_clave(password, password_hash)
