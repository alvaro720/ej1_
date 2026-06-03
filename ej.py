from servicio_indicadores import ServicioIndicadores
from Dao.DAOIndicador import DAOIndicador
from Dao.DAOUsuario import DAOUsuario
from datetime import datetime
from typing import List, Optional

INDICADORES_DISPONIBLES = ["uf", "dolar", "euro", "ipc", "utm", "ivp"]


def pedir_opcion(menu: str, opciones: List[str]) -> str:
    while True:
        print(menu)
        for idx, opcion in enumerate(opciones, 1):
            print(f"{idx}. {opcion}")
        seleccion = input("Elija una opción: ").strip()
        if seleccion.isdigit() and 1 <= int(seleccion) <= len(opciones):
            return opciones[int(seleccion) - 1]
        print("Opción inválida. Intente nuevamente.\n")


def pedir_fecha() -> Optional[str]:
    fecha = input("Ingrese fecha (YYYY-MM-DD) o ENTER para hoy: ").strip()
    if not fecha:
        return None
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return fecha
    except ValueError:
        print("Formato de fecha inválido. Debe ser YYYY-MM-DD.")
        return pedir_fecha()


def login_o_registro(dao_usuario: DAOUsuario) -> Optional[str]:
    accion = pedir_opcion("¿Qué desea hacer?", ["Iniciar sesión", "Registrar usuario"])
    rut = input("RUT: ").strip()
    if not rut:
        print("El RUT no puede estar vacío.")
        return None

    if accion == "Registrar usuario":
        password = input("Contraseña: ").strip()
        confirmar = input("Confirmar contraseña: ").strip()
        if password != confirmar:
            print("Las contraseñas no coinciden.")
            return None
        if dao_usuario.crear_usuario(rut, password):
            print("Usuario registrado correctamente. Inicie sesión ahora.")
        else:
            print("No se pudo registrar el usuario.")
        return None

    password = input("Contraseña: ").strip()
    if dao_usuario.validar_usuario(rut, password):
        print("Inicio de sesión exitoso.\n")
        return rut

    print("RUT o contraseña incorrectos.")
    return None


def main():
    print("=== Sistema de Indicadores Económicos ===")
    servicio = ServicioIndicadores()
    dao_indicador = DAOIndicador()
    dao_usuario = DAOUsuario()

    usuario = None
    while not usuario:
        usuario = login_o_registro(dao_usuario)

    indicador = pedir_opcion("Seleccione el indicador a consultar:", INDICADORES_DISPONIBLES)
    fecha = pedir_fecha()

    indicador_obj = servicio.obtener_indicador(indicador, fecha)
    if indicador_obj:
        indicador_obj.usuario = usuario
        print("\nResultado de la consulta:")
        print(indicador_obj)

        if dao_indicador.registrar(indicador_obj):
            print("✅ Guardado en base de datos monopoli")
        else:
            print("❌ No se pudo guardar en la base de datos")
    else:
        print("❌ No se pudo obtener el indicador. Verifique la conexión o la fecha.")


if __name__ == "__main__":
    main()
