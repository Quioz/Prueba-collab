"""Newton–Raphson para la bifurcación de canales: Formulación I (potencial ideal) y II (energía por ramal).
Uso: python codigo/newton_bifurcacion.py   (desde la raíz). Lee datos/datos_entrada.json. Sin aleatoriedad."""
import json, os, sys, numpy as np
print("Python", sys.version.split()[0], "| NumPy", np.__version__)
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(R, "datos", "datos_entrada.json")))
g, Q0 = D["g"], D["Q0"]; r1, r2 = D["ramal1"], D["ramal2"]

def Sf(Q, y, b, n):                      # pendiente de fricción de Manning, sección rectangular
    A = b*y; Rh = A/(b+2*y); return (n*Q/(A*Rh**(2/3)))**2

def G(Q, H, r, zJ=None):                 # residuo de energía del ramal, ec. (2)
    yJ = H - r["zJ"]; zd = r["zJ"] - r["S"]*r["L"]; AJ = r["b"]*yJ; Ad = r["b"]*r["yd"]
    return (H + (1-r["K"])*Q**2/(2*g*AJ**2) - (zd + r["yd"]) - Q**2/(2*g*Ad**2)
            - 0.5*r["L"]*(Sf(Q, yJ, r["b"], r["n"]) + Sf(Q, r["yd"], r["b"], r["n"])))

def F2(X, r1=r1, r2=r2, yref=1.60):
    Q1, Q2, H = X
    return np.array([(Q0-Q1-Q2)/Q0, G(Q1, H, r1)/yref, G(Q2, H, r2)/yref])

def jac(F, X, h=1e-7):                   # jacobiano por diferencias centrales (comprobación del analítico)
    J = np.zeros((len(X), len(X)))
    for j in range(len(X)):
        d = h*max(abs(X[j]), 1.0); e = np.zeros(len(X)); e[j] = d
        J[:, j] = (F(X+e) - F(X-e))/(2*d)
    return J

def newton(F, X0, tol=1e-12, itmax=50, verbose=True):
    X = np.array(X0, float); hist = []
    for k in range(itmax):
        f = F(X); nf = np.linalg.norm(f, np.inf); hist.append((k, *X, nf))
        if nf < tol: break
        dX = np.linalg.solve(jac(F, X), -f); a = 1.0
        while np.linalg.norm(F(X + a*dX), np.inf) >= nf and a > 1e-4: a *= 0.5
        X = X + a*dX
    if verbose:
        print(f"{'it':>3} {'Q1':>10} {'Q2':>10} {'H_J':>10} {'||F||inf':>11}")
        for h in hist: print(f"{h[0]:3d} {h[1]:10.6f} {h[2]:10.6f} {h[3]:10.6f} {h[4]:11.3e}")
    return X, hist

# Punto inicial: reparto por conductancias y H_J 0.05 m sobre el mayor nivel terminal
cond = lambda r: r["b"]*r["yd"]*((r["b"]*r["yd"]/(r["b"]+2*r["yd"]))**(2/3))/r["n"]/np.sqrt(max(r["S"], 1e-6))
c1, c2 = cond(r1), cond(r2)
Hmax = max(r1["zJ"]-r1["S"]*r1["L"]+r1["yd"], r2["zJ"]-r2["S"]*r2["L"]+r2["yd"])
X0 = [Q0*c1/(c1+c2), Q0*c2/(c1+c2), Hmax+0.05]
print("Formulación II, caso nominal"); X, _ = newton(F2, X0)
print(f"Q1 = {X[0]:.4f}  Q2 = {X[1]:.4f}  H_J = {X[2]:.4f}  phi = {X[1]/Q0:.4f}")

# Formulación I: ec. (1) con lambda = b1/b0, mu = b2/b0
lam, mu = r1["b"]/D["b0"], r2["b"]/D["b0"]
print("\nFormulación I")
for al in (30, 45, 60, 90, 120):
    e = 1 - 180/al
    F1 = lambda u: np.array([lam*u[0] + mu*u[1] - 1, lam*u[0]**e - mu*u[1]**e - 1])
    u, _ = newton(F1, [1.2, 0.6], verbose=False)
    print(f"alpha = {al:3d}  phi_I = {mu*u[1]:.4f}")
