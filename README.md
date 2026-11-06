# Contrataciones · Sanidad GVA (Intersindical Salut Orihuela)

Filtra las contrataciones por categoría, departamento, turno, tipo de nombramiento, breve y jornada
y devuelve nombre y puesto. Misma línea que BolsaSanGVA, TuNomina y Eleccions.

## Abrirla
Doble clic en `index.html` (funciona sin servidor). Código de acceso: el mismo que las otras apps.

## Publicar en GitHub Pages
1. Crea el repositorio `Contrataciones` y sube todos los archivos de esta carpeta.
2. Settings → Pages → Deploy from a branch → `main` / root.
3. Quedará en https://intersindicalorihuela.github.io/Contrataciones/

## Actualización mensual
```
pip install openpyxl
python convert.py Contrataciones.xlsx
```
Regenera `index.html` (lee las hojas por cabecera; se ignora "Observaciones"). Sube el `index.html` nuevo.
`template.html` es el diseño y `convert.py` le inyecta los datos: no hace falta tocarlos.

## Regla de contrato corto
- Con fecha de fin: corto si (Fin − Inicio + 1) ≤ 5 días.
- Sin fecha de fin y con inicio en los últimos 5 días del mes de corte: **indeterminado**.
- Sin fecha de fin y con más de 5 días ya transcurridos hasta el corte: no corto.
El corte es el fin de mes del último dato del Excel (editable en la app).
