# Hito 1 · GitHub profesional · primeros 3 PR

**Fecha:** 19 nov 2026

## Qué he aprendido

- **Flujo completo:** parto de `main` actualizado (`git pull`), creo una
  rama nueva (`git switch -c`), hago el cambio, lo guardo con `add` y
  `commit`, lo subo con `push`, abro un Pull Request, lo reviso y lo
  fusiono con `main`.
- **`push` y PR son cosas distintas.** El `push` sube mi rama a GitHub.
  El PR es la petición de revisión: ahí leo el diff, comento y decido si
  lo fusiono. El merge incorpora los cambios a `main`.
- **Los cambios pueden ser manuales o con ayuda de Claude Code**, ya sea
  para aclarar el código (docstring, renombrar una variable) o para
  mejorar el programa (una pregunta nueva en el árbol de decisión). En
  ambos casos reviso el diff antes de fusionar.
- **Sin entorno virtual, Python se ejecuta con `py`** (por ejemplo
  `py recorrer.py`), no con `python`.
- **Un `push` sin `commit` sube una rama vacía.** Si GitHub dice que
  `main` y mi rama son idénticas, es que falta el commit.

## Hecho

- 3 PR fusionados en `playbook-energy-lead`: README, `recorrer.py`
  (renombrado de variable con Claude Code) y `arbol.py` (nueva pregunta
  de comprador en la rama Bridge Power).

## Pendiente

- Protección de rama en `main`: en un repo privado requiere plan de pago
  de GitHub.
- Probar un worktree una vez.