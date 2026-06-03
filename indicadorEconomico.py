from datetime import datetime

class IndicadorEconomico:
    def __init__(self, nombre: str, fecha: str, valor: float, fuente: str = "mindicador.cl"):
        self.nombre = nombre
        self.fecha = fecha
        self.valor = valor
        self.fuente = fuente
        self.fecha_consulta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.usuario = None

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "fecha": self.fecha,
            "valor": self.valor,
            "fuente": self.fuente,
            "fecha_consulta": self.fecha_consulta,
            "usuario": self.usuario,
        }

    def __str__(self):
        base = f"{self.nombre} | Fecha valor: {self.fecha} | Valor: {self.valor:,.2f}"
        if self.usuario:
            base += f" | Usuario: {self.usuario}"
        base += f" | Fuente: {self.fuente}"
        return base
