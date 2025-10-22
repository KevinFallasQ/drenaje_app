import streamlit as st
import math

st.set_page_config(page_title="Espaciamiento entre Drenes", layout="wide")
st.title("🌾 Aplicación de Espaciamiento entre Drenes")
st.subheader("Métodos: Donnan, Hooghoudt, Ernst, Dagan y Glover–Dumm")

# ======================================================
# PARÁMETROS GENERALES
# ======================================================
st.markdown("### Parámetros generales")
K = st.number_input("Conductividad hidráulica K (m/día)", value=1.2, min_value=0.0001, step=0.1)
R = st.number_input("Recarga R (m/día)", value=0.01, min_value=0.0001, step=0.001)
PZ = st.number_input("Profundidad de la zanja (m)", value=1.5, min_value=0.1, step=0.1)
NFd = st.number_input("Altura del nivel freático deseado (m)", value=1.0, min_value=0.1, step=0.1)
prof_capa_imp = st.number_input("Profundidad de la capa impermeable (m)", value=4.8, min_value=0.1, step=0.1)
tipo_drenaje = st.selectbox("Tipo de drenaje", ["Zanja", "Tubería"])

# ======================================================
# PARÁMETROS SEGÚN TIPO DE DRENAJE
# ======================================================
if tipo_drenaje == "Zanja":
    st.markdown("### Parámetros de la zanja")
    b = st.number_input("Ancho de solera b (m)", value=0.5, min_value=0.1, step=0.1)
    y = st.number_input("Tirante de agua y (m)", value=0.2, min_value=0.01, step=0.01)
    Z = st.number_input("Talud Z (horizontal/vertical)", value=1.0, min_value=0.1, step=0.1)
    p = b + 2 * y * math.sqrt(1 + Z**2)
    Do = prof_capa_imp - PZ + y
    h = prof_capa_imp - NFd - Do
    u = p

else:  # Tubería
    st.markdown("### Parámetros de la tubería")
    r = st.number_input("Radio del tubo drenante r (m)", value=0.1, min_value=0.01, step=0.01)
    p = math.pi * r
    Do = prof_capa_imp - PZ + r
    h = prof_capa_imp - NFd - Do
    u = 4 * r

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
    Lh = 10.0  # Valor inicial para la iteración
    d = Do / (((8 * Do) / (math.pi * Lh)) * math.log(Do / p) + 1)
    L_hooghoudt = math.sqrt((8 * K * d * h + 4 * K * h**2) / R)
    st.success(f"✅ Espaciamiento Hooghoudt: {L_hooghoudt:.2f} m")
except Exception as e:
    st.error(f"❌ Error en el cálculo de Hooghoudt: {e}")

# ======================================================
# MÉTODO ERNST
# ======================================================
st.markdown("## Método Ernst (dos estratos)")
K1 = st.number_input("Conductividad hidráulica estrato superior K₁ (m/día)", value=0.8, min_value=0.0001, step=0.1)
K2 = st.number_input("Conductividad hidráulica estrato inferior K₂ (m/día)", value=2.0, min_value=0.0001, step=0.1)
d1 = st.number_input("Espesor del estrato superior d₁ (m)", value=1.0, min_value=0.1, step=0.1)
d2 = st.number_input("Espesor del estrato inferior d₂ (m)", value=1.0, min_value=0.1, step=0.1)

try:
    D1 = Do + h / 2
    A = R / (8 * K * D1)
    B = (R / (math.pi * K)) * math.log(Do / u)
    C = R * (y + h) / K - h
    discriminant = B**2 - 4 * A * C

    if discriminant < 0:
        st.error("❌ Discriminante negativo en la fórmula de Ernst. No hay solución real.")
    else:
        L2_pos = (-B + math.sqrt(discriminant)) / (2 * A)
        L2_neg = (-B - math.sqrt(discriminant)) / (2 * A)
        L2 = L2_pos if L2_pos > 0 else L2_neg

        if L2 > 0:
            L_ernst = math.sqrt(L2)
            st.success(f"✅ Espaciamiento Ernst: {L_ernst:.2f} m")
        else:
            st.error("❌ Resultado negativo en L². Verifica los parámetros.")
except Exception as e:
    st.error(f"❌ Error en el cálculo de Ernst: {e}")

# ======================================================
# MÉTODO DAGAN
# ======================================================
st.markdown("## Método Dagan")
try:
    A = R / (2 * Do)
    beta = (2 / math.pi) * math.log(2 * math.cosh(p / Do) - 2)
    B = -R * beta
    C = -4 * h * K
    discriminant = B**2 - 4 * A * C

    if discriminant >= 0:
        L2 = (-B + math.sqrt(discriminant)) / (2 * A)
        if L2 > 0:
            L_dagan = math.sqrt(L2)
            st.success(f"✅ Espaciamiento Dagan: {L_dagan:.2f} m")
        else:
            st.error("❌ Resultado negativo en L².")
    else:
        st.error("❌ Discriminante negativo en Dagan.")
except Exception as e:
    st.error(f"❌ Error en el cálculo de Dagan: {e}")

# ======================================================
# MÉTODO GLOVER-DUMM (RÉGIMEN NO PERMANENTE)
# ======================================================
st.markdown("## Régimen No Permanente (Glover–Dumm)")
K_gd = st.number_input("Conductividad hidráulica K (m/día) [Glover–Dumm]", value=1.2, min_value=0.0001, step=0.1)
S = st.number_input("Almacenamiento específico S (adimensional)", value=0.05, min_value=0.001, step=0.01)
t = st.number_input("Tiempo de drenaje t (días)", value=10.0, min_value=0.1, step=1.0)
h0 = st.number_input("Altura inicial del nivel freático h₀ (m)", value=1.5, min_value=0.1, step=0.1)
ht = st.number_input("Altura final del nivel freático hₜ (m)", value=0.8, min_value=0.1, step=0.1)

try:
    if ht >= h0:
        st.error("⚠️ La altura final (hₜ) debe ser menor que la inicial (h₀).")
    else:
        L_gd = math.sqrt((4 * K_gd * t / (math.pi * S)) * math.log(h0 / ht))
        st.success(f"✅ Espaciamiento Glover–Dumm: {L_gd:.2f} m")
except Exception as e:
    st.error(f"❌ Error en el cálculo de Glover–Dumm: {e}")

   
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# ======================================================
# VISUALIZACIÓN DEL PERFIL DEL NIVEL FREÁTICO ENTRE DRENES
# ======================================================
st.markdown("## 💧 Visualización del perfil del nivel freático entre drenes")

# Seleccionar el método que se quiere graficar
metodo = st.selectbox(
    "Selecciona el método para graficar el perfil",
    ["Donnan", "Hooghoudt", "Ernst", "Dagan", "Glover–Dumm"]
)

# Asignar el espaciamiento correspondiente según el método elegido
if metodo == "Donnan" and "L_donnan" in locals():
    L_plot = L_donnan
elif metodo == "Hooghoudt" and "L_hooghoudt" in locals():
    L_plot = L_hooghoudt
elif metodo == "Ernst" and "L_ernst" in locals():
    L_plot = L_ernst
elif metodo == "Dagan" and "L_dagan" in locals():
    L_plot = L_dagan
elif metodo == "Glover–Dumm" and "L_gd" in locals():
    L_plot = L_gd
else:
    L_plot = None

if L_plot:
    # Definir el dominio completo entre dos drenes
    x = np.linspace(0, L_plot, 200)
    
    # Altura máxima del nivel freático (NF - NFd)
    h0 = NF - NFd
    
    # Perfil parabólico (simétrico entre dos drenes)
    h = h0 * (1 - ((x - L_plot/2) / (L_plot/2))**2)

    # Crear el gráfico
    fig, ax = plt.subplots(figsize=(9, 4))
    
    # Curva del nivel freático
    ax.plot(x, h, color="blue", linewidth=2.5, label="Nivel freático (perfil parabólico)")
    
    # Líneas de los drenes (extremos del espaciamiento)
    ax.axhline(y=0, color="saddlebrown", linestyle="--", linewidth=2, label="Nivel del dren")
    ax.axvline(x=0, color="gray", linestyle="--", linewidth=1)
    ax.axvline(x=L_plot, color="gray", linestyle="--", linewidth=1)
    
    # Línea del nivel freático deseado (NFd)
    ax.axhline(y=h0, color="green", linestyle="--", linewidth=2, label="Nivel freático deseado (NFd)")

    # Etiquetas y estilo
    ax.set_xlabel("Distancia entre drenes (m)")
    ax.set_ylabel("Altura sobre el dren (m)")
    ax.set_title(f"Perfil completo del nivel freático – Método {metodo}")
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend()
    ax.set_ylim(bottom=-0.1)

    # Mostrar el gráfico
    st.pyplot(fig)

    # ==============================================
    # OPCIÓN PARA DESCARGAR EL GRÁFICO COMO IMAGEN
    # ==============================================
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
    buffer.seek(0)

    st.download_button(
        label="📥 Descargar gráfico como PNG",
        data=buffer,
        file_name=f"perfil_nivel_freatico_completo_{metodo}.png",
        mime="image/png"
    )

else:
    st.warning("⚠️ Calcula primero el espaciamiento con el método seleccionado para visualizar el perfil completo.")





