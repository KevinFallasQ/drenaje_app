import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Drenaje Subsuperficial", layout="wide")
st.title("🌾 Aplicación de Drenaje Subsuperficial – v5")
st.subheader("Cálculo de espaciamiento y visualización de flujo")

# Botón para reiniciar la app
if st.button("🔄 Reiniciar valores"):
    st.experimental_rerun()

# Selección del método
metodo = st.selectbox(
    "Selecciona el método de cálculo:",
    ["Hooghoudt", "Donnan", "Ernst", "Glover-Dumm (No Permanente)"],
    help="Elige el método que quieras usar para calcular el espaciamiento entre drenes."
)

# Parámetros básicos
st.markdown("### Parámetros básicos")
K = st.number_input(
    "Conductividad hidráulica K (m/día)",
    value=1.0, min_value=0.0001, step=0.1,
    help="Facilidad con la que el agua se mueve a través del suelo."
)
D = st.number_input(
    "Profundidad del dren D (m)",
    value=1.5, min_value=0.1, step=0.1,
    help="Profundidad a la que se colocarán los drenes."
)

L = None

if metodo != "Glover-Dumm (No Permanente)":
    h = st.number_input(
        "Altura del nivel freático sobre el dren h (m)",
        value=0.75, min_value=0.1, step=0.05,
        help="Distancia entre el dren y el nivel freático en condiciones de régimen permanente."
    )
    R = st.number_input(
        "Recarga o infiltración R (m/día)",
        value=0.005, min_value=0.0001, step=0.001,
        help="Cantidad de agua que ingresa al suelo diariamente (precipitación o riego)."
    )

# Métodos permanentes
if metodo == "Hooghoudt":
    De = st.number_input(
        "Profundidad equivalente De (m)",
        value=1.5, min_value=0.1, step=0.1,
        help="Profundidad equivalente considerando el efecto de estratos más permeables."
    )
    L = math.sqrt((8 * K * (De + h) * h) / R)
    st.success(f"✅ Espaciamiento recomendado (Hooghoudt): {L:.2f} m")

elif metodo == "Donnan":
    L = math.sqrt((4 * K * D * h) / R)
    st.success(f"✅ Espaciamiento recomendado (Donnan): {L:.2f} m")

elif metodo == "Ernst":
    K1 = st.number_input(
        "Conductividad hidráulica estrato superior K1 (m/día)",
        value=0.5, min_value=0.0001, step=0.1,
        help="Conductividad del estrato más cercano a la superficie."
    )
    K2 = st.number_input(
        "Conductividad hidráulica estrato inferior K2 (m/día)",
        value=2.0, min_value=0.0001, step=0.1,
        help="Conductividad del estrato inferior."
    )
    d1 = st.number_input(
        "Espesor del estrato superior d1 (m)",
        value=0.5, min_value=0.1, step=0.1
    )
    d2 = st.number_input(
        "Espesor del estrato inferior d2 (m)",
        value=1.0, min_value=0.1, step=0.1
    )
    
    K_equiv = (K1 * d1 + K2 * d2) / (d1 + d2)
    L = math.sqrt((8 * K_equiv * (d1 + d2) * h) / R)
    st.success(f"✅ Espaciamiento recomendado (Ernst): {L:.2f} m")

# Método no permanente: Glover-Dumm
elif metodo == "Glover-Dumm (No Permanente)":
    h0 = st.number_input(
        "Altura inicial del nivel freático h₀ (m)",
        value=0.8, min_value=0.1, step=0.05,
        help="Nivel freático inicial antes del drenaje."
    )
    ht = st.number_input(
        "Altura final del nivel freático hₜ (m)",
        value=0.4, min_value=0.05, step=0.05,
        help="Nivel freático deseado después del drenaje."
    )
    t = st.number_input(
        "Tiempo de drenaje t (días)",
        value=5.0, min_value=0.1, step=0.5,
        help="Tiempo en días para que el nivel freático baje de h₀ a hₜ."
    )
    f = math.pi**2 / 4  # constante ≈ 2.47

    if h0 > ht:
        L = math.sqrt((4 * K * D * t / f) * math.log(h0 / ht))
        st.success(f"✅ Espaciamiento recomendado (Glover-Dumm, No Permanente): {L:.2f} m")
    else:
        st.error("❌ h₀ debe ser mayor que hₜ (el nivel freático debe descender).")

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
