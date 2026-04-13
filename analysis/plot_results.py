import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# ── Parâmetros do circuito ──────────────────────────────────────────────────
R   = 1_000      # Ohm
C   = 100e-6     # F
V0  = 5.0        # V
tau = R * C      # s

# ── Caminhos ────────────────────────────────────────────────────────────────
DATA_PATH   = os.path.join("..", "data", "simulation_output.csv")
OUTPUT_PATH = os.path.join("..", "report")
os.makedirs(OUTPUT_PATH, exist_ok=True)

# ── Carregar dados ───────────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
t        = df["time_s"].values
V_sim    = df["voltage_V"].values
I_sim    = df["current_A"].values

# ── Curvas teóricas ──────────────────────────────────────────────────────────
V_theory = V0 * (1 - np.exp(-t / tau))
I_theory = (V0 / R) * np.exp(-t / tau)

# ── Erro percentual médio ────────────────────────────────────────────────────
error_pct = np.mean(np.abs(V_sim - V_theory) / V0 * 100)
print(f"Erro percentual médio (tensão): {error_pct:.4f}%")

# ── Estilo dos gráficos ──────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "figure.dpi": 150,
})

# ── Gráfico 1: Tensão ────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 4.5))

ax.plot(t, V_theory, "--", color="#378ADD", linewidth=1.8,
        label="Theoretical  V(t) = V₀·(1 − e^(−t/τ))")
ax.plot(t, V_sim,    "-",  color="#1D9E75", linewidth=2.0,
        label="Simscape simulation")

# Marcador em t = tau
ax.axvline(x=tau, color="#BA7517", linewidth=1, linestyle=":")
ax.axhline(y=V0 * 0.632, color="#BA7517", linewidth=1, linestyle=":")
ax.annotate(f"t = τ = {tau*1000:.0f} ms\nV = 63.2% V₀",
            xy=(tau, V0 * 0.632), xytext=(tau + 0.01, V0 * 0.45),
            fontsize=9, color="#854F0B",
            arrowprops=dict(arrowstyle="->", color="#854F0B", lw=1))

ax.set_xlabel("Time (s)")
ax.set_ylabel("Voltage (V)")
ax.set_title(f"RC Circuit — Capacitor Charging Curve  |  R={R}Ω  C={C*1e6:.0f}µF  τ={tau*1000:.0f}ms",
             fontsize=11)
ax.legend(fontsize=9)
ax.set_ylim(0, V0 * 1.15)
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f V"))

# Anotação de erro
ax.text(0.98, 0.08,
        f"Mean error: {error_pct:.4f}%",
        transform=ax.transAxes, ha="right", fontsize=9,
        color="gray")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "charging_curve.png"))
print("Gráfico de tensão salvo.")
plt.close()

# ── Gráfico 2: Corrente ──────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 4.5))

ax.plot(t, I_theory * 1000, "--", color="#378ADD", linewidth=1.8,
        label="Theoretical  I(t) = (V₀/R)·e^(−t/τ)")
ax.plot(t, I_sim * 1000,    "-",  color="#D85A30", linewidth=2.0,
        label="Simscape simulation")

ax.set_xlabel("Time (s)")
ax.set_ylabel("Current (mA)")
ax.set_title("RC Circuit — Charging Current", fontsize=11)
ax.legend(fontsize=9)
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.2f mA"))

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "current_curve.png"))
print("Gráfico de corrente salvo.")
plt.close()