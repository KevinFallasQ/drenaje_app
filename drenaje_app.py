
import streamlit as st
import math

st.set_page_config(page_title="Espaciamiento entre Drenes", layout="wide")
st.title("🌾 Aplicación de Espaciamiento entre Drenes – Régimen Permanente")
st.subheader("Métodos: Donnan, Hooghoudt, Ernst, Dagan")

# Parámetros generales
st.markdown("### Parámetros generales")
K = st.number_input("Conductividad hidráulica K (m/día)", value=1.2, min_value=0.0001, step=0.1)
R = st.number_input("Recarga R (m/día)", value=0.01, min_value=0.0001, step=0.001)
NF = st.number_input("Altura del nivel freático (m)", value=1.5, min_value=0.1, step=0.1)
NFd= st.number_input("Altura del nivel freático deseado (m)", value=1, min_value=0.1, step=0.1)

prof_capa_imp = st.number_input("Profundidad de la capa impermeable (m)", value=4.8, min_value=0.1, step=0.1)

tipo_drenaje = st.selectbox("Tipo de drenaje", ["Zanja", "Tubería"])

# Parámetros específicos
if tipo_drenaje == "Zanja":
    st.markdown("### Parámetros de la zanja")
    b = st.number_input("Ancho de solera b (m)", value=0.5, min_value=0.1, step=0.1)
    y = st.number_input("Tirante de agua y (m)", value=0.2, min_value=0.01, step=0.01)
    Z = st.number_input("Talud Z (horizontal/vertical)", value=1.0, min_value=0.1, step=0.1)
    p = b + 2 * y* math.sqrt(1 + Z**2)
    Do = prof_capa_imp - NF + y
    h = prof_capa_imp - NFd - Do
    H = prof_capa_imp - NFd
    u = p
else:
    st.markdown("### Parámetros de la tubería")
    r = st.number_input("Radio del tubo drenante r (m)", value=0.1, min_value=0.01, step=0.01)
    p = math.pi * r
    Do = prof_capa_imp - NF + r
    u = b + 4*r
# Método Donnan
try:
    L_donnan = math.sqrt((4 * K * (H**2 - Do**2)) / R)
    st.success(f"✅ Espaciamiento Donnan: {L_donnan:.2f} m")
except:
    st.error("❌ Error en el cálculo de Donnan. Verifica los parámetros.")

# Método Hooghoudt
L_hooghoudt = 10
try:
    d = Do/(((8*Do)/(math.pi*L_hooghoudt))*math.log(Do/p)+1)
    L_hooghoudt = math.sqrt((8 * K * d*h + 4*K*h**2) / R)
    st.success(f"✅ Espaciamiento Hooghoudt: {L_hooghoudt:.2f} m")
except:
    st.error("❌ Error en el cálculo de Hooghoudt. Verifica los parámetros.")

# Método Ernst
st.markdown("### Parámetros para Ernst")
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

        # Solo aceptamos soluciones positivas
        L2 = L2_pos if L2_pos > 0 else L2_neg

        if L2 > 0:
            L_ernst = math.sqrt(L2)
            st.success(f"✅ Espaciamiento Ernst: {L_ernst:.2f} m")
        else:
            st.error("❌ Resultado negativo en L². Verifica los parámetros ingresados.")

except Exception as e:
    st.error(f"❌ Error en el cálculo de Ernst: {e}")

# Método Dagan
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
            st.error("❌ Resultado negativo en la raíz cuadrada de L². Verifica los parámetros.")
    else:
        st.error("❌ Discriminante negativo en la fórmula de Dagan. No hay solución real.")
except:
    st.error("❌ Error en el cálculo de Dagan. Verifica los parámetros.")

   
   





