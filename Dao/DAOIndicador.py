from Dao.conexiones import Conexion
from indicadorEconomico import IndicadorEconomico

class DAOIndicador:

    def registrar(self, indicador: IndicadorEconomico):
        conexion = Conexion()
        try:
            conexion.conectar()
            sql = """
                INSERT INTO IndicadorEconomico 
                (nombre, fecha, valor, fuente, fecha_consulta, usuario)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                indicador.nombre,
                indicador.fecha,
                indicador.valor,
                indicador.fuente,
                indicador.fecha_consulta,
                indicador.usuario
            )
            conexion.cursor.execute(sql, params)
            conexion.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False
        finally:
            conexion.desconectar()