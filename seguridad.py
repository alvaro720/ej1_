import bcrypt

class Seguridad:
    @staticmethod
    def encriptar_clave(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def validar_clave(password_plana: str, password_encriptada: str) -> bool:
        return bcrypt.checkpw(password_plana.encode('utf-8'), password_encriptada.encode('utf-8'))