# Reparto de caudal en una bifurcación de canales rectangulares

Trabajo 01 — Flujo en superficie libre (MIH-626), Escuela de Posgrado, Universidad Nacional de San Cristóbal de Huamanga (UNSCH). Estructura n.º 8: confluencia o bifurcación de canales. **Grupo 7.**

- **Autores:** Brigmar Prado Taquire, Giomar Rubenney Quispe Ozaita, Luis Jhonatan Zamora Guillen.
- **Docente:** MSc. Iván Arturo Ayala Bizarro.
- **Contacto:** giomar.quispe.16@unsch.edu.pe
- **Repositorio:** https://github.com/Quioz/Prueba-collab
- **Fecha de esta versión:** noviembre de 2026 (borrador para revisión).

## Qué contiene

Se resuelve por Newton–Raphson el reparto de un caudal de 12 m³/s entre dos ramales rectangulares (b₁ = 3 m, b₂ = 2 m) de un canal principal de 4 m, con dos formulaciones (I: flujo plano ideal con tapa rígida; II: energía por ramal con nivel común), se calcula su sensibilidad y se contrasta con simulaciones HEC-RAS 2D para θ = 30°, 45°, 60°, 90° y 120°. El caso es **sintético**: no hay obra ni levantamiento reales.

**Resultado principal:** con la configuración efectivamente simulada, la Formulación II reproduce Q₂ con error ≤ 6.5 % (calados de salida del 2D) o ≤ 8.5 % (calado normal, 30°–90°); la Formulación I no es aceptable (de −0.1 % a +152 %).

## Estructura (según la estructura mínima exigida)

| Carpeta | Contenido |
|---|---|
| `datos/` | `datos_entrada.json` (caso sintético), `resultados_fase4.csv` y `elasticidades_fase4.csv` (valores del cuaderno de la Fase IV), `Balance de masa.xlsx`. Procedencia: datos sintéticos definidos por el grupo; resultados 2D de HEC-RAS 7.0.1 (corridas de octubre de 2026). |
| `codigo/` | `newton_bifurcacion.py` (Formulaciones I y II), `figuras_articulo.py` (figuras), cuadernos de las Fases I–IV y `Codigo_Calculo_de_Datos_de_salida_Python.ipynb` (caudales por sección desde los rásteres de HEC-RAS). |
| `modelo2d/` | Proyectos de HEC-RAS en estado ejecutable: `HEC_RAS_45G/` y `HEC_RAS_90G/` (`.g01`, `.p0x`, `.u01`, `.hdf`). Para 30°, 60° y 120° solo se dispone de los resultados (CSV y libro), no del proyecto. Paquetes del generador de geometría versión 2 en `generador_2d_v2/` (aún sin simular). |
| `figuras/` | Figuras del artículo (PNG, 300 dpi para las generadas por código) y el logotipo de la Escuela de Posgrado. |
| `secciones/`, `referencias/`, `water_like.sty`, `Art_MIH-626.tex` | Fuente LaTeX del artículo (estilo emulado de Water; no es la clase oficial de MDPI). |

## Software y versiones

| Componente | Versión |
|---|---|
| Python | 3.13 (probado con 3.13.16) |
| NumPy / pandas / Matplotlib / openpyxl | 2.5.3 / 3.0.5 / 3.11.2 / 3.1.5 |
| HEC-RAS | 7.0.1 (junio de 2026), SI, onda difusiva |
| LaTeX | pdflatex (MiKTeX 23.12), paquetes `natbib`, `mathpazo`, `babel` (spanish) |

Los *scripts* imprimen las versiones al ejecutarse. La semilla del Monte Carlo es `20261103`; el resto de cálculos es determinista.

## Cómo reproducir

```bash
pip install numpy pandas matplotlib openpyxl
python codigo/newton_bifurcacion.py     # historial de Newton, φ_II = 0.4216 y φ_I por ángulo
python codigo/figuras_articulo.py       # regenera las figuras generadas por código
```

Artículo: compilar `Art_MIH-626.tex` con **pdflatex** dos veces. No usa bibtex ni biber (bibliografía en `referencias/referencias.tex`). En TeXstudio basta el compilador pdflatex.

### Origen de cada figura

| Figura | Origen |
|---|---|
| `fig_reparto.png`, `fig_error_q2.png`, `fig_elasticidad.png`, `fig_nivel.png`, `fig_descomposicion.png` | `codigo/figuras_articulo.py`, a partir de `datos/*.csv` (valores del cuaderno de la Fase IV). |
| `1.png` | Reproducida de Milne-Thomson (1962), §10.8; no es obra propia. |
| `2.png` | Esquema isométrico, elaboración propia (ilustrativo, no a escala). |
| `3.png` | Cuaderno de la Fase I (redes de flujo, λ = 1, μ = 0.5). |
| Tablas de resultados | Cuaderno de la Fase IV (`bifurcacion_fase4_comparacion_hecras.ipynb`) y archivos HDF de los planos. |

## Limitaciones conocidas

- Una sola malla por ángulo (≈ 0.46–0.53 m): no hay estudio de independencia de malla.
- Ecuaciones 2D de onda difusiva; no se probaron las ecuaciones completas.
- Caudales derivados de rásteres de calado y velocidad máximos de un hidrograma triangular, con supuesto cuasipermanente no verificado; salidas de calado normal.
- Las corridas usaron la versión 1 del generador de geometría y no son equivalentes entre ángulos (rugosidad, pendiente, paso de tiempo), por lo que no se interpreta el efecto del ángulo.
- La hoja `Balance de masa.xlsx` tiene dos anomalías (error de 0.22 % a 30° y columna de porcentaje de 60° igual a los m³); el artículo da los valores corregidos.
- No hay validación con datos observados.

## Licencia

*Por confirmar por el grupo.* Propuesta: código bajo MIT y texto, datos y figuras propios bajo CC BY 4.0. La figura `1.png` y la bibliografía conservan sus derechos originales.

## Uso de inteligencia artificial

Se usó un asistente de IA para organizar la redacción, desarrollar el código y auditar resultados; el detalle está en el Anexo A del artículo. Los autores son responsables de verificar ecuaciones, resultados y referencias.
