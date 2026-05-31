import requests

url = "https://teehee.dev/api/joke"
r = requests.get(url)
print(r)
data = r.json()
print(data)
print(type(data))
pregunta = data['question']
respuesta = data['answer']
print(pregunta)
print(respuesta)