import requests

url = "https://apidatos.ree.es/es/datos/mercados/precios-mercados-tiempo-real"

parametros = {
    "start_date": "2026-06-09T00:00",
    "end_date": "2026-06-09T23:59",
    "time_trunc": "hour",
}

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

respuesta = requests.get(url, params=parametros, headers=headers)

print(f"Código de estado: {respuesta.status_code}")

if respuesta.status_code == 200:
    datos = respuesta.json()
    print(f"Indicador Recibido: {datos['data']['type']}")
    print(f"Numero de indicadores en `included` : {len(datos['included'])}")  
else:
    print(f"Error: la API devolvió el código {respuesta.status_code}")
    # Aquí querríamos parar el programa
    exit(1)


