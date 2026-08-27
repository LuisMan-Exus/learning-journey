## 1. Mision 
El Tariff Scraper consulta la API pública de REE (apidatos.ree.es) para
obtener el precio horario del mercado eléctrico español (PVPC) del día anterior, lo convierte
a €/kWh y lo guarda de forma estructurada con fecha y fuente.

MVP deliberadamente acotado: un indicador (PVPC), una fuente (REE), salida a CSV.
Extensible después a más indicadores, fuentes y formatos.

## 2. Qué hace
- Consulta la API de REE
- Convierte los datos de €/MWh a €/kWh
- Crea un archo CSV con la informacion para poder consultarlo y exportar


## 3. Requisitos

- Python 3.x
- Librerías_ requests (vienen incluidas)

## 4. Instalacion
uv venv
..venv\Scripts\activate
uv pip install requests

## 5. Uso
python scraper.py

## 6. Ourputs
Genera un archivo `pvpc_AAAA-MM-DD.csv` con los precios horarios del día anterior.

## Notas y limitaciones

- Dato horaria del PVPC en €/kWh, no el capturado por el consumidor
- No obtiene la diferencia entre el precio de mercado y el precio final




 