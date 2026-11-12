"""Figuras de la versión final: reparto φ(θ) y dependencia de malla. Uso: python codigo/figuras_final.py (desde la raíz)."""
import os, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":"serif","font.size":9,"axes.grid":True,"grid.alpha":.25,"axes.spines.top":False,"axes.spines.right":False})
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); F=lambda n:os.path.join(R,"figuras",n)
d=pd.read_csv(os.path.join(R,"datos","resultados_2d_v3.csv")); m=pd.read_csv(os.path.join(R,"datos","mallas_EM.csv")); e=pd.read_csv(os.path.join(R,"datos","mallas_ELM.csv"))
fig,ax=plt.subplots(figsize=(5.8,3.5))
ax.plot(d.theta,d.phi_I,"s--",c="#b2182b",label="Formulación I")
ax.plot(d.theta,d.phi_II,"^--",c="#2166ac",label="Formulación II (θ no interviene)")
ax.plot(d.theta,d.phi_EM_025,"o-",c="#111111",lw=1.8,label="HEC-RAS 2D, SWE-EM, celda 0.25 m")
u=m[m.malla=="uniforme"]
for c,mk,l in ((0.5,"v","SWE-EM, celda 0.50 m"),(0.125,"D","SWE-EM, celda 0.125 m")):
    s=u[u.celda_m==c]; ax.plot(s.theta,s.phi,mk,mfc="white",c="#111111",ms=6,ls="none",label=l)
s=e[e.celda_m==0.125]; ax.plot(s.theta,s.phi,"x:",c="#777777",label="SWE-ELM, celda 0.125 m (exploratorio)")
ax.set_xlabel("Ángulo de bifurcación θ (°)"); ax.set_ylabel("Fracción al ramal 2, φ = Q₂/Q₀"); ax.set_xticks(d.theta); ax.set_ylim(.25,.85)
ax.legend(fontsize=7,frameon=False,loc="upper left"); fig.tight_layout(); fig.savefig(F("fig_phi_theta.png"),dpi=300); plt.close(fig)
fig,(a,b)=plt.subplots(1,2,figsize=(6.4,3.0),sharey=True)
for t,c in ((30,"#1b7837"),(120,"#762a83")):
    s=u[u.theta==t].sort_values("celda_m"); a.plot(s.celda_m,s.phi,"o-",c=c,label=f"{t}° uniforme")
    n=m[(m.theta==t)&(m.malla=="nudo")]; a.plot(0.25*np.ones(len(n)),n.phi,"s",mfc="white",c=c,label=f"{t}° con refinamiento del nudo")
a.axhline(0.4216,c="#2166ac",ls="--",lw=1); a.set_xscale("log"); a.set_xticks([.125,.25,.5]); a.set_xticklabels(["0.125","0.25","0.5"]); a.set_xlabel("Celda base (m)"); a.set_ylabel("φ"); a.set_ylim(.27,.50); a.set_title("(a) SWE-EM",fontsize=9); a.minorticks_off(); a.legend(fontsize=6.5,frameon=False,loc="upper left")
for t,c in zip((30,45,60,90,120),("#1b7837","#4393c3","#fdae61","#d6604d","#762a83")):
    s=e[e.theta==t].sort_values("celda_m"); b.plot(s.celda_m,s.phi,"o-",c=c,label=f"{t}°")
b.axhline(0.4216,c="#2166ac",ls="--",lw=1); b.set_xscale("log"); b.set_xticks([.125,.25,.5]); b.set_xticklabels(["0.125","0.25","0.5"]); b.set_xlabel("Celda (m)"); b.set_title("(b) SWE-ELM (exploratorio)",fontsize=9); b.minorticks_off(); b.legend(fontsize=6.5,frameon=False,ncol=2,loc="lower right")
fig.tight_layout(); fig.savefig(F("fig_malla.png"),dpi=300); plt.close(fig); print("ok")
