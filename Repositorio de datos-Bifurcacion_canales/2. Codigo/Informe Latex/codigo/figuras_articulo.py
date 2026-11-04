"""Genera las figuras del artículo a partir de datos/*.csv (valores del cuaderno de la Fase IV).
Uso:  python codigo/figuras_articulo.py   (desde la raíz del proyecto)
Requiere: numpy, pandas, matplotlib. Sin aleatoriedad (no hay semilla que fijar aquí)."""
import sys, os
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
print("Python", sys.version.split()[0], "| NumPy", np.__version__, "| pandas", pd.__version__, "| Matplotlib", matplotlib.__version__)
plt.rcParams.update({"font.family":"serif","font.size":9,"axes.grid":True,"grid.alpha":.25,"axes.spines.top":False,"axes.spines.right":False})
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = pd.read_csv(os.path.join(R,"datos","resultados_fase4.csv")); e = pd.read_csv(os.path.join(R,"datos","elasticidades_fase4.csv"))
F = lambda n: os.path.join(R,"figuras",n)
C = {"2D":"#111111","I":"#b2182b","IIn":"#999999","IIs":"#2166ac","IIc":"#4daf4a"}

# 1. reparto
fig, ax = plt.subplots(figsize=(5.6,3.3))
ax.errorbar(d.theta, d.phi_2D_libro, yerr=0.0078, fmt="o-", c=C["2D"], capsize=3, label="HEC-RAS 2D (±0.0078)")
ax.plot(d.theta, d.phi_I, "s--", c=C["I"], label="Formulación I (potencial ideal)")
ax.plot(d.theta, d.phi_II_nominal, "^:", c=C["IIn"], label="Formulación II, datos nominales")
ax.plot(d.theta, d.phi_II_simulada, "D-", c=C["IIs"], label="Formulación II, configuración simulada")
m = d.phi_II_normal.notna(); ax.plot(d.theta[m], d.phi_II_normal[m], "v-", c=C["IIc"], label="Formulación II, calado normal")
ax.set_xlabel("Ángulo de bifurcación θ (°)"); ax.set_ylabel("Fracción al ramal 2, φ = Q₂/Q₀"); ax.set_xticks(d.theta); ax.set_ylim(.25,.85)
ax.legend(fontsize=7, frameon=False, loc="upper left"); fig.tight_layout(); fig.savefig(F("fig_reparto.png"), dpi=300); plt.close(fig)

# 2. error Q2
fig, ax = plt.subplots(figsize=(5.6,3.3)); x = np.arange(5); w = .2
for i,(c,l,k) in enumerate([("eps_I","Form. I","I"),("eps_IInom","II nominal","IIn"),("eps_IIsim","II simulada","IIs"),("eps_IInorm","II calado normal","IIc")]):
    ax.bar(x+(i-1.5)*w, d[c].fillna(0), w, color=C[k], label=l)
for y in (10,-10): ax.axhline(y, c="k", lw=.8, ls="--")
for y in (20,-20): ax.axhline(y, c="k", lw=.8, ls=":")
ax.set_yscale("symlog", linthresh=10); ax.set_ylim(-30,200); ax.set_xticks(x); ax.set_xticklabels(d.theta)
ax.set_xlabel("Ángulo de bifurcación θ (°)"); ax.set_ylabel("ε(Q₂) = (1D − 2D)/2D (%)"); ax.legend(fontsize=7, frameon=False, ncol=2)
fig.tight_layout(); fig.savefig(F("fig_error_q2.png"), dpi=300); plt.close(fig)

# 3. elasticidades
fig, ax = plt.subplots(figsize=(5.2,4.0)); M = e.drop(columns="parametro").values.astype(float)
im = ax.imshow(M, cmap="RdBu_r", vmin=-1.3, vmax=1.3, aspect="auto"); ax.set_xticks(range(5)); ax.set_xticklabels(e.columns[1:]); ax.set_yticks(range(len(e))); ax.set_yticklabels(e.parametro)
for i in range(M.shape[0]):
    for j in range(M.shape[1]): ax.text(j,i,"n/d" if np.isnan(M[i,j]) else f"{M[i,j]:+.2f}", ha="center", va="center", fontsize=7)
ax.grid(False); ax.set_xlabel("θ (°) — configuración simulada"); fig.colorbar(im, label="Elasticidad E(φ, p)"); fig.tight_layout(); fig.savefig(F("fig_elasticidad.png"), dpi=300); plt.close(fig)

# 4. nivel
fig, ax = plt.subplots(figsize=(5.2,3.0)); ax.axhspan(-.10,.10,color="#d9f0d3",label="Aceptable (|Δy| ≤ 0.10 m)"); ax.axhspan(.10,.20,color="#fee391"); ax.axhspan(-.20,-.10,color="#fee391",label="Marginal (≤ 0.20 m)")
ax.plot(d.theta, d.dyJ_Pb2y, "o-", c=C["IIs"], label="Perímetro P = b + 2y"); ax.plot(d.theta, d.dyJ_Ry, "s-", c=C["I"], label="Pared ancha R ≈ y")
ax.set_xticks(d.theta); ax.set_xlabel("Ángulo de bifurcación θ (°)"); ax.set_ylabel("Δy_J = y_J,1D − y_J,2D (m)"); ax.legend(fontsize=7, frameon=False, loc="lower left"); ax.set_ylim(-.2,.2)
fig.tight_layout(); fig.savefig(F("fig_nivel.png"), dpi=300); plt.close(fig)

# 5. descomposición
fig, ax = plt.subplots(figsize=(5.6,3.2)); w=.2
for i,(c,l,col) in enumerate([("paso1","Paso 1: n₁, S₂ simulados","#92c5de"),("paso2","Paso 2: calados de salida del 2D","#f4a582"),("resto","Sesgo restante","#252525")]):
    ax.bar(x+(i-1)*w*1.2, d[c], w*1.2, color=col, label=l)
ax.axhline(0,c="k",lw=.6); ax.set_xticks(x); ax.set_xticklabels(d.theta); ax.set_xlabel("Ángulo de bifurcación θ (°)"); ax.set_ylabel("Δφ"); ax.legend(fontsize=7, frameon=False)
fig.tight_layout(); fig.savefig(F("fig_descomposicion.png"), dpi=300); plt.close(fig)
print("Figuras escritas en", F(""))
