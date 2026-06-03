import requests
from indicadorEconomico import IndicadorEconomico

class ServicioIndicadores:
    BASE_URL = "https://mindicador.cl/api"
    INDICADORES_VALIDOS = {"uf", "dolar", "euro", "ipc", "utm", "ivp"}

    @staticmethod
    def obtener_indicador(indicador: str, fecha: str = None):
        if indicador.lower() not in ServicioIndicadores.INDICADORES_VALIDOS:
            print(f"Indicador no soportado: {indicador}")
            return None

        try:
            url = f"{ServicioIndicadores.BASE_URL}/{indicador.lower()}"
            if fecha:
                url += f"/{fecha}"

            respuesta = requests.get(url, timeout=10)
            respuesta.raise_for_status()
            data = respuesta.json()

            if not data or "serie" not in data or not data["serie"]:
                print(f"No se encontró información para {indicador}.")
                return None

            item = data["serie"][0]
            valor = float(item["valor"])
            fecha_data = item["fecha"][:10]

            return IndicadorEconomico(
                nombre=data.get("nombre", indicador.upper()),
                fecha=fecha_data,
                valor=valor
            )
        except requests.exceptions.RequestException as e:
            print(f"Error de red al consultar {indicador}: {e}")
            return None
        except ValueError as e:
            print(f"Error al procesar los datos de {indicador}: {e}")
            return None
        except Exception as e:
            print(f"Error consultando {indicador}: {e}")
            return None

    @staticmethod
    def obtener_periodo(indicador: str, fecha_inicio: str, fecha_fin: str):
        if indicador.lower() not in ServicioIndicadores.INDICADORES_VALIDOS:
            print(f"Indicador no soportado: {indicador}")
            return []

        try:
            url = f"{ServicioIndicadores.BASE_URL}/{indicador.lower()}/{fecha_inicio}/{fecha_fin}"
            respuesta = requests.get(url, timeout=10)
            respuesta.raise_for_status()
            data = respuesta.json()

            resultados = []
            for item in data.get("serie", []):
                valor = float(item["valor"])
                fecha_data = item["fecha"][:10]
                resultados.append(IndicadorEconomico(
                    nombre=data.get("nombre", indicador.upper()),
                    fecha=fecha_data,
                    valor=valor
                ))
            return resultados
        except requests.exceptions.RequestException as e:
            print(f"Error de red al consultar periodo para {indicador}: {e}")
            return []
        except Exception as e:
            print(f"Error consultando periodo para {indicador}: {e}")
            return []
