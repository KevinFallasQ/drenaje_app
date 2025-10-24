import streamlit as st
import math

st.set_page_config(page_title="Espaciamiento entre Drenes", layout="wide")
st.title("🌾 Aplicación de Espaciamiento entre Drenes")
st.subheader("Métodos: Donnan, Hooghoudt, Ernst, Dagan y Glover–Dumm")

# ======================================================
# PARÁMETROS GENERALES
# ======================================================
st.markdown("### Parámetros generales")
K = st.number_input("Conductividad hidráulica K (m/día)", value=1.2, min_value=0.0001, step=0.01, format="%.3f")
R = st.number_input("Recarga R (m/día)", value=0.01, min_value=0.0001, step=0.001, format="%.3f")
PZ = st.number_input("Profundidad de la zanja (m)", value=1.5, min_value=0.01, step=0.01, format="%.3f")
NFd = st.number_input("Altura del nivel freático deseado (m)", value=1.0, min_value=0.01, step=0.01, format="%.3f")
prof_capa_imp = st.number_input("Profundidad de la capa impermeable (m)", value=4.8, min_value=0.01, step=0.01, format="%.3f")
tipo_drenaje = st.selectbox("Tipo de drenaje", ["Zanja", "Tubería"])

# ======================================================
# PARÁMETROS SEGÚN TIPO DE DRENAJE
# ======================================================
if tipo_drenaje == "Zanja":
    st.markdown("### Parámetros de la zanja")
    b = st.number_input("Ancho de solera b (m)", value=0.5, min_value=0.01, step=0.01, format="%.3f")
    y = st.number_input("Tirante de agua y (m)", value=0.2, min_value=0.01, step=0.01, format="%.3f")
    Z = st.number_input("Talud Z (horizontal/vertical)", value=1.0, min_value=0.01, step=0.01, format="%.3f")
    p = b + 2 * y * math.sqrt(1 + Z**2)
    Do = prof_capa_imp - PZ + y
    h = prof_capa_imp - NFd - Do
    u = p

else:  # Tubería
    st.markdown("### Parámetros de la tubería")
    r = st.number_input("Radio del tubo drenante r (m)", value=0.1, min_value=0.01, step=0.01)
    b = st.number_input("Ancho de solera b de la zanja (m)", value=0.5, min_value=0.01, step=0.01, format="%.3f")
    p = math.pi * r
    Do = prof_capa_imp - PZ + r
    h = prof_capa_imp - NFd - Do
    u = b + 4 * r
    y = r
# Profundidad total deseada
H = prof_capa_imp - NFd

# ======================================================
# MÉTODO DONNAN
# ======================================================
st.markdown("## Método Donnan")
try:
    L_donnan = math.sqrt((4 * K * (H**2 - Do**2)) / R)
    st.success(f"✅ Espaciamiento Donnan: {L_donnan:.2f} m")
except Exception as e:
    st.error(f"❌ Error en el cálculo de Donnan: {e}")

# ======================================================
# MÉTODO HOOGHOUDT
# ======================================================
st.markdown("## Método Hooghoudt")
try:
    Lh = 5.0  # valor inicial de L (m)
    for _ in range(200):  # iterar hasta converger
        d = Do / (((8 * Do) / (math.pi * Lh)) * math.log(Do / p) + 1)
        L_new = math.sqrt((8 * K * d * h + 4 * K * h**2) / R)
        if abs(L_new - Lh) < 1e-3:
            break
        Lh = L_new
    L_hooghoudt = L_new
    st.success(f"✅ Espaciamiento Hooghoudt: {L_hooghoudt:.2f} m")
except Exception as e:
    st.error(f"❌ Error en el cálculo de Hooghoudt: {e}")


# ======================================================
# MÉTODO ERNST
# ======================================================
st.markdown("## Método Ernst")
try:
    
    D1 = Do + h / 2
    A = R / (8 * K * D1)
    B = (R / (math.pi * K)) * math.log(Do / u)
    C = R * (y + h) / K - h

    discriminant = B**2 - 4 * A * C

    if discriminant < 0:
        st.error("❌ Discriminante negativo en la fórmula de Ernst. No hay solución real.")
    else:       
        L_pos = (-B + math.sqrt(discriminant)) / (2 * A)
        L_neg = (-B - math.sqrt(discriminant)) / (2 * A)

        # Seleccionar la raíz positiva (físicamente válida)
        L_ernst = L_pos if L_pos > 0 else L_neg

        if L_ernst > 0:
            st.success(f"✅ Espaciamiento Ernst: {L_ernst:.2f} m")
        else:
            st.error("❌ Resultado negativo para L. Verifica los parámetros.")
except Exception as e:
    st.error(f"❌ Error en el cálculo de Ernst: {e}")

# ======================================================
# MÉTODO DAGAN
# ======================================================
st.markdown("## Método Dagan")
try:
    A = R / (2 * Do)
    beta = (2 / math.pi) * math.log(2 * math.cosh(p / Do) - 2)
    B = R * beta
    C = -4 * h * K
   
 
    discriminant = B**2 - 4 * A * C

    if discriminant < 0:
        st.error("❌ Discriminante negativo en la fórmula de Dagan. No hay solución real.")
    else:       
        L_pos = (-B + math.sqrt(discriminant)) / (2 * A)
        L_neg = (-B - math.sqrt(discriminant)) / (2 * A)

        # Seleccionar la raíz positiva (físicamente válida)
        L_dagan = L_pos if L_pos > 0 else L_neg

        if L_dagan > 0:
            st.success(f"✅ Espaciamiento Dagan: {L_dagan:.2f} m")
        else:
            st.error("❌ Resultado negativo para L. Verifica los parámetros.")
except Exception as e:
    st.error(f"❌ Error en el cálculo de Dagan: {e}")
# ======================================================
# MÉTODO GLOVER-DUMM (RÉGIMEN NO PERMANENTE)
# ======================================================
st.markdown("## Régimen No Permanente (Glover–Dumm)")

# Parámetros de entrada
K_gd = st.number_input("Conductividad hidráulica K (m/día) [Glover–Dumm]", value=1.20, min_value=0.0001, step=0.01, format="%.2f")
S = st.number_input("Porosidad drenable S (adimensional)", value=0.05, min_value=0.001, step=0.01, format="%.2f")
t = st.number_input("Tiempo de drenaje t (días)", value=10.0, min_value=0.1, step=0.1, format="%.2f")
hi = st.number_input("Altura inicial del nivel freático h₀ (m)", value=1.50, min_value=0.1, step=0.1, format="%.2f")
hf = st.number_input("Altura final deseada del nivel freático hₜ (m)", value=0.80, min_value=0.1, step=0.1, format="%.2f")
PZ_gd = st.number_input("Profundidad de la zanja (m)", value=1.50, min_value=0.01, step=0.01, format="%.2f")
prof_capa_imp_gd = st.number_input("Profundidad de la capa impermeable (m)", value=4.80, min_value=0.01, step=0.01, format="%.2f")

st.markdown("### Parámetros de la tubería")
r_gd = st.number_input("Radio del tubo drenante r (m)", value=0.10, min_value=0.01, step=0.01, format="%.2f")
b_gd = st.number_input("Ancho de solera b de la zanja (m)", value=0.50, min_value=0.01, step=0.01, format="%.2f")

# =======================
# Cálculos geométricos
# =======================
p = math.pi * r_gd  # perímetro hidráulico equivalente
Do = prof_capa_imp_gd - PZ_gd + r_gd  # profundidad desde la capa impermeable hasta el tubo
ho = PZ_gd - r_gd - hi  # altura inicial sobre el dren
ht = PZ_gd - r_gd - hf  # altura final sobre el dren

# =======================
# Cálculo iterativo de L
# =======================
try:
    Lh = 5.0  # valor inicial de L (m)
    for _ in range(200):  # iterar hasta convergencia
        # Cálculo de d usando Hooghoudt
        d = Do / (((8 * Do) / (math.pi * Lh)) * math.log(Do / p) + 1)
        
        # Fórmula de Glover–Dumm
        L_new = math.sqrt((math.pi**2 * K_gd * t * (d + (ho + ht) / 4)) / (S * math.log(1.16 * (ho / ht))))
        
        # Criterio de convergencia
        if abs(L_new - Lh) < 1e-4:
            break
        Lh = L_new
    
    L_gd = L_new
    st.success(f"✅ Espaciamiento Glover–Dumm: {L_gd:.2f} m")

except Exception as e:
    st.error(f"❌ Error en el cálculo de Glover–Dumm: {e}")



   

# ======================================================
# VISUALIZACIÓN DEL PERFIL DEL NIVEL FREÁTICO ENTRE DRENES
# ======================================================
import matplotlib.pyplot as plt
import numpy as np

st.markdown("## 💧 Visualización del sistema de drenaje subsuperficial")

# Visualización del perfil y flujo
if L:
    x = np.linspace(0, L, 200)
    h_max = h if metodo != "Glover-Dumm (No Permanente)" else h0
    y_freatico = -D + h_max * (1 - (2*x/L - 1)**2)

    X, Y = np.meshgrid(np.linspace(0, L, 40), np.linspace(-D, 0, 20))
    U = -(X - L/2)
    V = -0.3 * (Y + D)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.axhline(0, color="black", linewidth=1.2, label="Terreno")
    ax.plot(x, y_freatico, color="blue", linewidth=2, label="Nivel freático inicial")

    # Nivel final Glover-Dumm
    if metodo == "Glover-Dumm (No Permanente)":
        y_final = -D + ht * (1 - (2*x/L - 1)**2)
        ax.plot(x, y_final, color="cyan", linestyle="--", label="Nivel freático final")

    ax.axhline(-D, color="brown", linestyle="--", label=f"Drenes a {D} m")
    ax.scatter([0, L], [-D, -D], color="brown", s=80)
    ax.streamplot(X, Y, U, V, color="skyblue", linewidth=1, density=1.1, arrowsize=1)

    ax.set_xlim(-0.5, L + 0.5)
    ax.set_ylim(-D - 0.5, h_max + 0.5)
    ax.set_xlabel("Distancia entre drenes (m)")
    ax.set_ylabel("Altura (m)")
    ax.set_title("Perfil del drenaje subsuperficial")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.4)

    st.pyplot(fig)














