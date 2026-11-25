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

**1. Descargar los datos desde SanGVA**

Abre `marcador_contrataciones.html` y arrastra el enlace **Extractor Contrataciones** a tu barra de
marcadores. En la pantalla de SanGVA "Contratados por categoría": elige la CATEGORÍA, pulsa el
marcador y espera (si sale el captcha, resuélvelo y pulsa Obtener Listado). Descarga
`CATEGORIA.xlsx` por cada categoría y cierra la tirada con la siguiente.

**2. Mezclar con el Excel maestro**

Abre `GeneradorContrataciones.html`, sube el `Contrataciones.xlsx` del mes anterior y todos los
archivos recién descargados. Revisa las hojas de destino de cada categoría (se recuerdan de una
vez a la siguiente) y pulsa **Generar Excel actualizado**: añade solo las filas nuevas sin
duplicar nada y conserva las hojas de notas tal cual.

**3. Publicar en GitHub**

Sube el Excel resultante a la carpeta `data/` del repositorio con el nombre `data/Contrataciones.xlsx`.
El workflow `.github/workflows/actualizar-contrataciones.yml` regenera y publica `index.html` solo:

```
pip install openpyxl
python convert.py data/Contrataciones.xlsx
```

`template.html` es el diseño y `convert.py` le inyecta los datos: no hace falta tocarlos.

## Regla de contrato corto
- Con fecha de fin: corto si (Fin − Inicio + 1) ≤ 5 días.
- Sin fecha de fin y con inicio en los últimos 5 días del mes de corte: **indeterminado**.
- Sin fecha de fin y con más de 5 días ya transcurridos hasta el corte: no corto.
El corte es el fin de mes del último dato del Excel (editable en la app).
