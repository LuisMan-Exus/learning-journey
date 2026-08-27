# Semana 5 — Pandas y series temporales

**Proyecto:** `spot-pvpc-analyzer`
**Qué construí:** una herramienta que descarga de la API de REE el precio spot
(cuartohorario) y el PVPC (horario) de un día, los alinea, y calcula la
diferencia hora a hora.

---

## El problema de fondo

Dos series de precios que no encajaban: el spot da 96 valores al día (uno cada
15 minutos, desde la reforma de octubre 2025) y el PVPC da 24 (uno por hora).
Restarlos directamente no tiene sentido: el valor nº 5 de una lista no
corresponde al nº 5 de la otra.

La solución fue promediar el spot a resolución horaria y comparar hora contra
hora. No es un apaño: es lo que hace el propio sistema eléctrico para los
contadores que registran por horas.

---

## Conceptos clave

### 1. Vectorización: por qué no se usan bucles en pandas

Escribí esto:

```python
df["diferencia"] = df["pvpc"] - df["spot"]
```

En vez de un `for` que recorriera las 24 filas. La diferencia no es solo
estética, es de velocidad, y por tres motivos:

**Python es lento por naturaleza.** Cada vuelta de un `for` obliga a Python a
comprobar tipos, buscar métodos y crear objetos nuevos. Son cientos de
instrucciones de máquina para restar dos números.

**Los datos están juntos en memoria.** Una lista normal de Python guarda
punteros a números dispersos por la memoria. Pandas los guarda pegados unos a
otros, lo que permite a la CPU traerse bloques enteros a su memoria rápida.

**La CPU puede restar varios a la vez.** Con los datos contiguos, el
procesador aplica una misma operación a 4 u 8 números en un solo ciclo.

**La idea clave:** pandas no elimina el bucle, lo *delega* a código compilado
en C, donde es barato. Python solo da las órdenes. Por eso, cada vez que
fuerzas a pandas a volver a Python fila por fila (con `iterrows()` o un `for`),
pierdes toda la ventaja.

---

### 2. El índice: la pieza que hace que todo funcione

Cuando escribí `set_index("datetime")`, no moví una columna de sitio. Declaré
una **clave**: le dije a pandas "la identidad de cada fila es su marca de
tiempo".

A partir de ahí, pandas cambia cómo opera. Esto:

```python
pd.concat([df_pvpc, df_spot_horario], axis=1)
```

no es "pegar dos tablas". Es casar cada fila con la que tiene la misma
etiqueta. Es lo mismo que un `JOIN` en una base de datos.

**Por qué esto es importante y no solo cómodo:** si a una serie le falta una
hora, en un sistema sin alineación todas las filas posteriores se desplazan y
el resultado sale mal *pero plausible*. Con alineación por etiqueta, el dato
que falta produce un hueco visible.

Es la diferencia entre **fallar de forma evidente** y **mentir en silencio**.

---

### 3. Split-Apply-Combine: el patrón detrás de `resample`

```python
df_spot.resample("h").mean()
```

Esto hace tres cosas:

1. **Partir** — agrupa los 96 cuartos según a qué hora pertenecen.
2. **Aplicar** — calcula la media de cada grupo.
3. **Recombinar** — junta los 24 resultados en una tabla nueva.

Lo interesante es que este patrón es el mismo en `groupby`, `pivot_table` y
`rolling`. No son cuatro cosas que memorizar, es una con distintos criterios de
agrupación. `resample` es simplemente el caso en que agrupas por tiempo.

**La trampa que me pilló:** `.mean()` ignora los datos que faltan por defecto.
Si una hora tenía 3 cuartos en vez de 4, calculaba la media de esos 3 sin
avisar. El resultado parecía normal (solo unos decimales raros lo delataban).

Lección general: **los valores por defecto de una librería asumen el caso de
uso más común, que no tiene por qué ser el tuyo.**

---

### 4. NaN: qué es un dato que falta

`NaN` no es cero ni una casilla vacía. Es un valor especial con dos
comportamientos que conviene conocer:

**Se contagia.** Cualquier cuenta con un NaN da NaN. Por eso, cuando el spot de
las 01:00 quedó vacío, la diferencia también quedó vacía automáticamente, sin
que yo lo programara. El contagio es intencionado: significa "este resultado no
es fiable porque depende de un dato que no tengo".

**No es igual a sí mismo.** `NaN == NaN` da falso. Un valor desconocido no es
igual a otro valor desconocido. Por eso hay que usar `.isna()` en vez de
comparar con `==`.

**La decisión de diseño que tomé:** si falta un solo cuarto de hora, invalido la
hora entera en vez de promediar con datos parciales. Prefiero un resultado
ausente y evidente a uno presente y sutilmente sesgado.

---

### 5. Por qué se escribe `df = df.algo()`

Los métodos de pandas no modifican la tabla original: devuelven una copia nueva.
Si no la guardas con el `=`, se pierde.

Al principio parece redundante, pero tiene ventajas:

- **Puedes leer cualquier línea y saber qué hay en `df`** sin rastrear todo el
  historial anterior.
- **Nadie te cambia los datos por detrás.** Si dos variables apuntaran al mismo
  objeto y una lo modificara, la otra cambiaría sin avisar. Es una fuente de
  errores muy difícil de encontrar.
- **Puedes encadenar** operaciones: `df.a().b().c()`.

El coste es memoria (cada paso crea una copia), pero la claridad casi siempre lo
compensa.

---

### 6. Diseñar funciones: qué me enseñó `extraer_serie`

Empecé con este código duplicado dos veces:

```python
bruto = datos["included"][0]["attributes"]["values"]
df = pd.DataFrame(bruto)
# ... 5 líneas más
```

Y lo convertí en una función. El proceso fue: **mirar qué cambia entre las dos
copias y qué se queda igual.** Lo que cambia se convierte en parámetros. Eso es
literalmente lo que significa "hacer una abstracción".

**Regla práctica:** código repetido = función que falta.

#### Una mejora pendiente

La función quedó con cinco parámetros:

```python
def extraer_serie(datos, posicion, nombre, fecha, frecuencia):
```

Cinco es demasiado, y es una señal. Fijándose bien, `posicion`, `nombre` y
`frecuencia` no son tres cosas sueltas: son las tres propiedades de **un
indicador**. Falta un concepto sin nombrar.

Se arreglaría así:

```python
@dataclass
class Indicador:
    posicion: int
    nombre: str
    frecuencia: str

PVPC = Indicador(posicion=0, nombre="pvpc_eur_mwh", frecuencia="1h")
SPOT = Indicador(posicion=1, nombre="spot_medio_eur_mwh", frecuencia="15min")

def extraer_serie(datos: dict, indicador: Indicador, fecha: str):
```

Dos ventajas: la firma baja de 5 parámetros a 3, y el código **empieza a hablar
el idioma del negocio**. Ya no dices "posición 1 con frecuencia 15min", dices
"SPOT". Si REE añade un indicador nuevo, añades una línea sin tocar la función.

*(Pendiente para cuando toque `dataclass` en Semana 6.)*

---

### 7. Validar en la puerta de entrada

Puse las comprobaciones de fecha al principio, antes de llamar a nada:

```python
if fecha_dt < limite:
    raise ValueError("No existen datos para esta fecha")
elif fecha_dt.date() > hoy:
    raise ValueError("No se pueden pedir fechas futuras")
```

La idea: **valida una sola vez, en el punto donde los datos entran al sistema.**
A partir de ahí, el resto del código puede dar por hecho que son válidos. Como
una fortaleza con una sola puerta: controlas quién entra, y dentro te mueves
libre.

La alternativa (comprobar en cada función) infla el código con verificaciones
repetidas.

También es **fallar pronto**: un error que salta en la línea 3 diciendo "fecha
fuera de rango" es mucho más útil que uno que salta 40 líneas después diciendo
"no se puede restar un valor nulo".

---

## Método aplicado

1. **SPEC primero** — cerrada antes de escribir una línea, con reconocimiento
   real contra la API para no suponer nada.
2. **Reconocimiento** — probé los endpoints en el navegador antes de codificar.
   Descubrí así que `time_trunc` es obligatorio y que el spot llega
   cuartohorario aunque pidas `hour`.
3. **Construcción por piezas** — una función cada vez, verificando antes de
   pasar a la siguiente.
4. **Verificación con caso de fallo fabricado** — borré una fila a propósito
   para comprobar que la detección de huecos funcionaba de verdad. Sin esa
   prueba, habría dado por bueno algo que nunca se había ejercitado.
5. **Documentación final** — README con instalación, uso y decisiones de diseño.

---

## Errores que cometí y qué aprendí de ellos

| Error | Lección |
|---|---|
| `f"{2026-07-14}"` | Dentro de las llaves de un f-string va **código**, no texto. La fecha va en una variable, entre comillas. |
| Quitar `time_trunc` de la petición | No suponer cómo se comporta una API. Probar el endpoint aislado antes de codificar. |
| `.mean(min_count=4)` | No todos los objetos de pandas aceptan los mismos parámetros aunque el método se llame igual. |
| `reindex` antes de crear la rejilla | Leer el error literalmente: "variable no asociada a un valor" = está usada antes de existir. |
| Entrar en el REPL de Python sin querer | `python` a secas abre la consola interactiva. `python main.py` ejecuta el archivo. Se sale con `exit()`. |

---

## Higiene resuelta esta semana

- **Proyectos movidos fuera de OneDrive** a `C:\Users\lm\dev\`. La ruta
  corporativa era tan larga que superaba el límite de 260 caracteres de Windows
  y bloqueaba la instalación de numpy.
- **Entorno virtual por proyecto**: cada uno empieza vacío a propósito, para que
  las versiones de un proyecto no rompan otro.

---

## Pendiente

- Convertir los 5 parámetros de `extraer_serie` en un objeto `Indicador`
  (Semana 6).
- Generar `requirements.txt` para poder reconstruir el entorno de un tirón.
- Días con cambio de hora (23h / 25h) — declarado fuera de alcance en la V1.
