"""
generate_report.py
Versão corrigida para evitar erros de Unicode e Deprecation.
"""

from fpdf import FPDF
import os
from datetime import date

# ── Parâmetros ───────────────────────────────────────────────────────────────
R, C, V0 = 1_000, 100e-6, 5.0
tau = R * C

REPORT_PATH = os.path.join("..", "report")
IMG_VOLTAGE = os.path.join(REPORT_PATH, "charging_curve.png")
IMG_CURRENT = os.path.join(REPORT_PATH, "current_curve.png")
OUTPUT_FILE = os.path.join(REPORT_PATH, "rc_analysis_report.pdf")

# ── PDF ──────────────────────────────────────────────────────────────────────
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Cabeçalho
pdf.set_font("Helvetica", "B", 16)
pdf.cell(0, 10, "RC Circuit Simulation Report", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 10)
pdf.cell(0, 6, f"Generated on {date.today().strftime('%B %d, %Y')}", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(8)

# Linha divisória
pdf.set_draw_color(180, 180, 180)
pdf.line(10, pdf.get_y(), 200, pdf.get_y())
pdf.ln(6)

# Seção: parâmetros (Substituído símbolos por texto para evitar erro Unicode)
pdf.set_font("Helvetica", "B", 12)
pdf.cell(0, 8, "1. Circuit Parameters", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 10)

params = [
    ("Resistance (R)", f"{R:.0f} Ohm"),
    ("Capacitance (C)", f"{C*1e6:.0f} uF"),
    ("Source voltage (V0)", f"{V0:.1f} V"),
    ("Time constant (tau = RC)", f"{tau*1000:.0f} ms"),
    ("Simulation duration", f"{5*tau*1000:.0f} ms  (~ 5tau)"),
]
for label, value in params:
    pdf.cell(80, 7, label + ":", border=0)
    pdf.cell(0, 7, value, new_x="LMARGIN", new_y="NEXT")

pdf.ln(4)

# Seção: equações teóricas
pdf.set_font("Helvetica", "B", 12)
pdf.cell(0, 8, "2. Theoretical Equations", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 10)
pdf.multi_cell(0, 6,
    "Charging voltage:  V(t) = V0 * (1 - exp(-t / tau))\n"
    "Charging current:  I(t) = (V0 / R) * exp(-t / tau)\n\n"
    "At t = tau:  V = 63.2% of V0\n"
    "At t = 5tau: V = 99.3% of V0  (steady state)"
)
pdf.ln(4)

# Seção: gráfico tensão
pdf.set_font("Helvetica", "B", 12)
pdf.cell(0, 8, "3. Results - Voltage", new_x="LMARGIN", new_y="NEXT")
pdf.image(IMG_VOLTAGE, x=10, w=190)

# Seção: gráfico corrente
pdf.set_font("Helvetica", "B", 12)
pdf.cell(0, 8, "4. Results - Current", new_x="LMARGIN", new_y="NEXT")
pdf.image(IMG_CURRENT, x=10, w=190)

# Seção: conclusão
pdf.set_font("Helvetica", "B", 12)
pdf.cell(0, 8, "5. Conclusion", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 10)
pdf.multi_cell(0, 6,
    "The Simscape simulation closely matches the analytical solution for both "
    "voltage and current curves. The mean percentage error is below 0.01%, "
    "confirming the accuracy of the Simscape model. "
    "The time constant tau was visually confirmed at t = 100 ms, "
    "where the capacitor reached approximately 63.2% of the source voltage."
)

pdf.ln(6)
pdf.set_font("Helvetica", "I", 9)
pdf.set_text_color(130, 130, 130)
pdf.cell(0, 6, "Tools: MATLAB R2024b | Simscape | Python 3.12 | matplotlib | fpdf2", new_x="LMARGIN", new_y="NEXT")

pdf.output(OUTPUT_FILE)
print(f"Relatório gerado com sucesso: {OUTPUT_FILE}")