# Semana 2 — Fundamentos de Git

Notas tomadas tras varias sesiones prácticas en mayo 2026. Pensadas para mi yo de dentro de 3 meses, que se habrá olvidado de la mitad.

---

## La idea más importante: ¿qué es Git?

Git es un sistema que vigila una carpeta de mi ordenador y guarda **fotos completas** de su contenido cada vez que se lo pido. Esas fotos forman un histórico que puedo revisar, comparar, y recuperar.

No es "track changes" como Word. Cada foto es íntegra: contiene el estado entero de la carpeta en ese momento.

**Git ≠ GitHub.** Git es la herramienta que vive en mi ordenador (funciona sin internet). GitHub es un sitio web donde puedo subir mis repos para tenerlos en la nube. Puedo usar Git sin GitHub. Al revés, no.

---

## Las tres zonas: el viaje de un cambio

Cuando modifico un archivo, el cambio pasa por tres "zonas" antes de quedar archivado:

1. **Working directory** — mi carpeta normal de Windows, donde edito día a día.
2. **Staging area** — la "sala de espera". Aquí le digo a Git "estos cambios sí los quiero archivar en el próximo commit".
3. **Repository** — el archivo histórico. Cuando hago commit, los cambios pasan de staging al repo y quedan archivados (dentro de la carpeta oculta `.git/`).

Movimientos entre zonas:
- `git add <archivo>` → working → staging
- `git commit -m "mensaje"` → staging → repository

---

## Las ramas: el concepto que más me costó

Una rama **no es una copia del proyecto**. Es solo un **nombre que apunta a un commit concreto**. Como una pegatina con un nombre escrito, pegada en el lomo de uno de los expedientes de una estantería.

Cuando estoy en la rama `main` y hago un commit nuevo:
1. Se crea un commit nuevo (una foto nueva)
2. La pegatina "main" se despega del commit viejo
3. La pegatina "main" se pega al commit nuevo

La pegatina avanza conmigo. Por eso `main` siempre apunta al último commit de esa rama.

Cuando creo una rama nueva con `git switch -c experimento`, pego una segunda pegatina al mismo commit donde estaba. Si hago commits con esa pegatina "activa", solo esa avanza. La otra se queda atrás.

**El "momento mágico":** cuando cambio de rama con `git switch`, Git reescribe los archivos de mi carpeta de Windows para que reflejen el commit donde está pegada la otra etiqueta. **Mi carpeta de Windows no es la "verdad" — los expedientes archivados en `.git/` son la verdad.** Mi carpeta es solo una ventana al expediente actual.

---

## Comandos que ya domino

### Diagnóstico
- `git status` — "Oye Git, ¿qué ves?" Me dice en qué rama estoy, qué hay modificado, qué hay en staging. **Lo uso 50 veces al día.**
- `git diff` — Muestra línea a línea qué cambió. `+` líneas nuevas, `-` borradas.
- `git log` — Histórico de commits.
  - `git log --oneline` — un commit por línea
  - `git log --all --oneline --graph` — incluye ramas no actuales y dibuja un grafo
  - `git log -1 --format=fuller <hash>` — info completa de un commit concreto

### Archivar
- `git add <archivo>` — preparar para commit
- `git commit -m "mensaje"` — archivar lo de staging

Convención: mensaje en **imperativo presente y en inglés**: "Add login feature", no "Added".

### Ramas
- `git branch` — listar ramas (asterisco = donde estoy)
- `git switch -c <nombre>` — crear rama Y moverme a ella
- `git switch <nombre>` — moverme a una rama existente
- `git branch -d <nombre>` — borrar una rama ya fusionada

### Combinar ramas
- `git merge <otra_rama>` — traer cambios de otra rama a la actual. **Me sitúo en la que va a RECIBIR los cambios.**

### Comunicar con GitHub
- `git push` — subir mis commits a GitHub
- `git pull` — bajar cambios de GitHub a local (aún poco usado)

---

## Tipos de merge

### Fast-forward
La rama destino no se movió desde que la otra salió de ella. Git solo **desplaza la pegatina** de la destino hasta donde está la otra. No crea commit nuevo. Línea recta en el grafo.

### Merge commit
Las dos ramas avanzaron **en paralelo**. Git **crea un commit nuevo con dos padres** que une las dos historias. Forma un diamante: