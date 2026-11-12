# Reparto de caudal en una bifurcación de canales rectangulares

Trabajo 01 — Flujo en superficie libre (MIH-626), Escuela de Posgrado, Universidad Nacional de San Cristóbal de Huamanga (UNSCH). Estructura n.º 8: confluencia o bifurcación de canales. **Grupo 7.**

- **Autores:** Brigmar Prado Taquire, Giomar Rubenney Quispe Ozaita, Luis Jhonatan Zamora Guillen.
- **Docente:** MSc. Iván Arturo Ayala Bizarro.
- **Contacto:** giomar.quispe.16@unsch.edu.pe
- **Repositorio:** https://github.com/Quioz/Prueba-collab
- **Fecha de esta versión:** noviembre de 2026 (versión final para entrega).

## Qué contiene

Se resuelve por Newton–Raphson el reparto de un caudal de 12 m³/s entre dos ramales rectangulares (b₁ = 3 m, b₂ = 2 m) de un canal principal de 4 m, con dos formulaciones (I: flujo plano ideal con tapa rígida; II: energía por ramal con nivel común), se calcula su sensibilidad y se contrasta con simulaciones HEC-RAS 2D para θ = 30°, 45°, 60°, 90° y 120°. El caso es **sintético**: no hay obra ni levantamiento reales.

## Resultado principal

- **2D (SWE-EM, celda de 0.25 m, paquete v3):** φ = Q₂/Q₀ = 0.374, 0.358, 0.350, 0.340 y 0.313 para θ = 30°, 45°, 60°, 90° y 120°. El reparto **decrece** con el ángulo. Las cinco corridas cumplen el control de calidad (error de volumen ≤ 0.009 %, cierre de caudal ≤ 0.009 %, reparto estable en los últimos 600 s).
- **Formulación I:** crece de 0.406 a 0.785; queda contradicha a ángulos grandes (+150 % a 120°).
- **Formulación II:** φ = 0.4216 para todo θ; sobrestima Q₂ entre +13 y +35 % frente al 2D SWE-EM, y queda a +2 o +3 % hasta 60° frente al conjunto exploratorio SWE-ELM (celda de 0.125 m). No reproduce la tendencia con el ángulo. Es casi insensible a la pérdida local K (φ de 0.4232 a 0.4142 para K entre 0 y 2.4).
- **El 2D no es una referencia convergida:** la resistencia efectiva cae al refinar (n_eff/n = 0.93, 0.86 y 0.72 para celdas de 0.50, 0.25 y 0.125 m en ramales rectos aislados) y φ a 30° pasa de 0.389 a 0.374 y a 0.343. Refinar solo el nudo no cambia el resultado. La corrección lineal de n (0.0174 y 0.0212) **no** cumple la tolerancia de ±0.01 m.

## Cambios respecto de la versión anterior (borrador)

| Tema | Borrador | Versión final |
|---|---|---|
| Ecuaciones 2D | Onda difusiva | SWE-EM (SWE-ELM solo como conjunto exploratorio) |
| Configuración 2D | Corridas no equivalentes entre ángulos (v1 del generador) | Paquete v3: misma configuración en los cinco ángulos, nivel fijo en las salidas, hidrograma mantenido 7200 s |
| Malla | Una malla por ángulo (0.46–0.53 m) | 0.25 m en los cinco ángulos; 0.50, 0.125 m y refinamientos del nudo en 30° y 120° |
| Caudales | Rásteres de calado y velocidad máximos | Caudales de las líneas de borde, promedio de los últimos 600 s |
| Verificación del 2D | No había | Ramales rectos aislados, n_eff y prueba de corrección de n |
| Conclusión sobre el ángulo | No se interpretaba | El 2D decrece con θ; la Formulación I crece; la II es constante |
| Comparación 1D–2D | Contra la Formulación II con la configuración simulada | Contra el 2D de la v3 (la configuración ya es la nominal) |

Las subsecciones de configuración simulada, nivel en la unión, sesgo, identificabilidad y descomposición del borrador se retiraron porque dependían de las corridas anteriores.

## Estructura

| Carpeta | Contenido |
|---|---|
| `datos/` | `datos_entrada.json` (caso sintético), `resultados_2d_v3.csv` (φ de las cinco corridas y control de calidad), `mallas_EM.csv` (30° y 120°, mallas y refinamientos), `mallas_ELM.csv` (conjunto exploratorio), `elasticidades_fase4.csv` y `resultados_fase4.csv` (conjunto exploratorio inicial). |
| `codigo/` | `newton_bifurcacion.py` (Formulaciones I y II), `figuras_final.py` (figuras de reparto y malla), `figuras_articulo.py` (figuras de sensibilidad del conjunto inicial). |
| `figuras/` | Figuras del artículo (PNG, 300 dpi para las generadas por código) y el logotipo de la Escuela de Posgrado. |
| `secciones/`, `referencias/`, `water_like.sty`, `Art_MIH-626.tex` | Fuente LaTeX del artículo (estilo emulado de Water; no es la clase oficial de MDPI). |

Los proyectos de HEC-RAS (`modelo2d/`), los paquetes v3 del generador de geometría y los cuadernos de las Fases I–IV se conservan en el repositorio general del trabajo; **suban a `modelo2d/` los proyectos de las corridas v3** (30° y 120° en todas las mallas, 45°, 60° y 90° en 0.25 m, ramales aislados) y los resultados del conjunto SWE-ELM.

## Software y versiones

| Componente | Versión |
|---|---|
| Python | 3.13 (probado con 3.13.16) |
| NumPy / pandas / Matplotlib | 2.5.3 / 3.0.5 / 3.11.2 |
| HEC-RAS | 6.6/7.0, SI, SWE-EM |
| LaTeX | pdflatex (MiKTeX 23.12), paquetes `natbib`, `mathpazo`, `babel` (spanish) |

Los *scripts* imprimen las versiones al ejecutarse. La semilla del Monte Carlo es `20261103`; el resto de cálculos es determinista.

## Cómo reproducir

```bash
pip install numpy pandas matplotlib
python codigo/newton_bifurcacion.py     # historial de Newton, φ_II = 0.4216 y φ_I por ángulo
python codigo/figuras_final.py          # figuras de reparto y dependencia de malla
python codigo/figuras_articulo.py       # figuras de sensibilidad (conjunto exploratorio inicial)
```

Artículo: compilar `Art_MIH-626.tex` con **pdflatex** dos veces. No usa bibtex ni biber (bibliografía en `referencias/referencias.tex`). En TeXstudio basta el compilador pdflatex.

### Origen de cada figura

| Figura | Origen |
|---|---|
| `fig_phi_theta.png`, `fig_malla.png` | `codigo/figuras_final.py`, a partir de `datos/resultados_2d_v3.csv`, `mallas_EM.csv` y `mallas_ELM.csv`. |
| `fig_elasticidad.png` | `codigo/figuras_articulo.py`, a partir de `datos/elasticidades_fase4.csv` (conjunto exploratorio inicial). |
| `fig_reparto.png`, `fig_error_q2.png`, `fig_nivel.png`, `fig_descomposicion.png` | Conjunto exploratorio inicial; ya no se usan en el artículo. |
| `1.png` | Reproducida de Milne-Thomson (1962), §10.8; no es obra propia. |
| `2.png` | Esquema isométrico, elaboración propia (ilustrativo, no a escala). |
| `3.png` | Cuaderno de la Fase I (redes de flujo, λ = 1, μ = 0.5). |
| Tablas de resultados 2D | Archivos HDF de los planos (resumen de cálculo y series de caudal de las líneas de borde). |

## Limitaciones conocidas

- Con SWE-EM, φ no converge al refinar la malla; 45°, 60° y 90° solo se corrieron con celda de 0.25 m. No corresponde aplicar GCI porque las diferencias crecen.
- La resistencia efectiva del 2D difiere de la nominal y depende de la malla; la corrección lineal de n no cumple ±0.01 m.
- El conjunto SWE-ELM (tres mallas, cinco ángulos) usa un paquete anterior, midió caudales en secciones transversales y no pasó la verificación en ramales diagonales; es exploratorio.
- La pérdida de carga en el nudo (≈ 0.04 m a 30° y ≈ 0.22 m a 120°; K efectivo ≈ 0.4–0.5 y ≈ 2.4) es aproximada; su atribución a la separación del flujo es una hipótesis.
- Las elasticidades y la incertidumbre paramétrica (σ_φ ≈ 0.035) provienen del conjunto exploratorio inicial y de desviaciones postuladas por el grupo.
- En 90° el cálculo informa una celda aislada con error de nivel de 0.62 m junto a la punta de la divisoria, sin efecto sobre el volumen ni los caudales.
- No hay validación con datos observados. El benchmark de la red de ocho canales no se reproduce.

## Pendientes del grupo

- Contribución de los autores, financiamiento y conflictos de interés (marcadores en la sección de declaraciones).
- Verificar las referencias Gümgüm (2025, 2026) y Hsu et al. (2002).
- Confirmar con el docente los umbrales de aceptación (10 % y 20 % en Q₂).
- Confirmar la licencia y subir al repositorio las carpetas actualizadas.

## Licencia

*Por confirmar por el grupo.* Propuesta: código bajo MIT y texto, datos y figuras propios bajo CC BY 4.0. La figura `1.png` y la bibliografía conservan sus derechos originales.

## Uso de inteligencia artificial

Se usó un asistente de IA para organizar la redacción, desarrollar el código, analizar los resultados HDF y preparar el generador de geometría; el detalle está en el Anexo A del artículo. Los autores son responsables de verificar ecuaciones, resultados y referencias. Las simulaciones de HEC-RAS las ejecutaron los integrantes del grupo.
