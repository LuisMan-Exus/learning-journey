nombre_cliente = input("Cual es el nombre del cliente?")
consumo_anual_kwh = int(input("Cual es el consumo anual del cliente en kWh?"))
if consumo_anual_kwh > 10_000_000:
    precio_kwh = 0.135
    categoría = "Industrial Intensivo"
elif consumo_anual_kwh > 1_000_000:
    precio_kwh = 0.155  # Gran Industrial
    categoría = "Gran Industrial"
elif consumo_anual_kwh > 100_000:
    precio_kwh = 0.185  # Mediano Industrial
    categoría = "Mediano Industrial"
else:
    precio_kwh = 0.220  # Pequeño Comercial
    categoría = "Pequeño Comercial"
coste_anual = consumo_anual_kwh * precio_kwh
print(f"{nombre_cliente} | {consumo_anual_kwh} | {categoría} | {coste_anual}")


