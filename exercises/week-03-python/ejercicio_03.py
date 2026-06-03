consumo_anual_kWh = 50000000    
if consumo_anual_kWh > 10_000_000:
    precio_kWh = 0.135 # Industrial Intensivo
elif consumo_anual_kWh <= 10_000_000 and consumo_anual_kWh >= 1_000_000:
    precio_kWh = 0.155 # Gran Industrial
elif consumo_anual_kWh < 1_000_000 and consumo_anual_kWh >= 100_000:
    precio_kWh = 0.185 # Mediano Industrial
else:
    precio_kWh = 0.220 # Pequeño Comercial 
coste_anual = consumo_anual_kWh * precio_kWh

print(f"Consumo anual: {consumo_anual_kWh} kWh")
print(f"Precio por kWh: {precio_kWh} €/kWh")
print(f"Gasto anual: {coste_anual} €")



