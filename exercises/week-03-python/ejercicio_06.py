
clientes = [
    
{
    "nombre": "Acerinox",
    "consumo_anual_kwh": 10_500_000,
    "sector": "metalúrgico"
},
{
    "nombre": "Mercadona",
    "consumo_anual_kwh": 300_000,
    "sector": "retail"
},
{
    "nombre": "Cemex",
    "consumo_anual_kwh": 5_000_000,
    "sector": "construcción"
},
]   

for cliente in clientes:
    if cliente["consumo_anual_kwh"] > 10_000_000:
        precio_kwh = 0.135
        categoria = "Industrial Intensivo"
    elif cliente["consumo_anual_kwh"] > 1_000_000:
        precio_kwh = 0.155  # Gran Industrial
        categoria = "Gran Industrial"
    elif cliente["consumo_anual_kwh"] > 100_000:
        precio_kwh = 0.185  # Mediano Industrial
        categoria = "Mediano Industrial"
    else:
        precio_kwh = 0.220  # Pequeño Comercial
        categoria = "Pequeño Comercial"
    coste_anual = cliente["consumo_anual_kwh"] * precio_kwh
    print(f"{cliente['nombre']} | {cliente['consumo_anual_kwh']} | {categoria} | {coste_anual}")

