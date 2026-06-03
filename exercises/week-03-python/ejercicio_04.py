clientes = [
    ("Cementos Cosmos", 80_000_000),
    ("Acerinox", 25_000_000),
    ("Ybarra", 2_500_000),
    ("Lácteos Pascual", 750_000),
    ("Panadería local", 45_000),
]
for cliente, consumo_anual_kWh in clientes:
    if consumo_anual_kWh > 10_000_000:
        precio_kWh = 0.135
        Categoría = "Industrial Intensivo"
    elif consumo_anual_kWh > 1_000_000:
        precio_kWh = 0.155 # Gran Industrial
        Categoría = "Gran Industrial"
    elif consumo_anual_kWh > 100_000:
        precio_kWh = 0.185 # Mediano Industrial
        Categoría = "Mediano Industrial"
    else:
        precio_kWh = 0.220 # Pequeño Comercial 
        Categoría = "Pequeño Comercial"
    coste_anual = consumo_anual_kWh * precio_kWh

    print(f"{cliente} & {consumo_anual_kWh} & {Categoría} & {coste_anual}")
    