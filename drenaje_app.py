import streamlit as st
import math

# ======================================================
# CONFIGURACIÓN GENERAL DE LA APP
# ======================================================
st.set_page_config(page_title="Espaciamiento entre Drenes", layout="wide")
st.title("🌾 Aplicación Modular para Calcular Espaciamiento entre Drenes")

st.markdown("""
**Clasificación principal:**
- Permanente – Homogéneo  
- Permanente – 2 estratos  
- No Permanente – 1 estrato  
""")

# ======================================================
# =============== MÓDULOS (FUNCIONES) ==================
# ======================================================

# ---------- MÉTODOS PERMANENTE – HOMOGÉNEO ----------

def metodo_donnan(K, R, H, Do):
    """Método Donnan — Régimen permanente homogéneo"""
    return math.sqrt((4 * K * (H**2 - Do**2)) / R)

def metodo_hooghoudt(K, R, Do, p, h):
    """Método Hooghoudt clásico — Iterativo"""
    Lh = 5.0
    for _ in range(200):
        d = Do / (((8 * Do) / (math.pi * Lh)) * math.log(Do / p) + 1)
        L_new = math.sqrt((8 * K * d * h + 4 * K * h**2) / R)
        if abs(L_new - Lh) < 1e-3:
            break
        Lh = L_new
    return L_new

def metodo_dagan(K, R, Do, p, h):
    """Método Dagan — Permanente homogéneo"""
    A = R / (2 * Do)
    beta = (2 / math.pi) * math.log(2 * math.cosh(p / Do) - 2)
    B = R * beta
    C = -4 * h * K

    disc = B**2 - 4*A*C
    if disc < 0:
        return None
    L1 = (-B + math.sqrt(disc)) / (2*A)
    L2 = (-B - math.sqrt(disc)) / (2*A)
    return L1 if L1 > 0 else L2


def metodo_ernst_homogeneo(K, R, Do, u, y, h):
    """Método Ernst — 1 Estratos """
    D1 = Do + h / 2
    A = R / (8 * K * D1)
    B = (R / (math.pi * K)) * math.log(Do / u)
    C = R * (y + h) / K - h

    disc = B**2 - 4*A*C
    if disc < 0:
        return None

    L1 = (-B + math.sqrt(disc)) / (2*A)
    L2 = (-B - math.sqrt(disc)) / (2*A)
    return L1 if L1 > 0 else L2

# ---------- MÉTODOS PERMANENTE – 2 ESTRATOS ----------
def metodo_dagan_dos_estratos(K1, K2, R, Do, p, h):
    """Método Dagan — Permanente 2 estratos"""
    c = 1/(1-(R/K1))
    A = cR / (2 * Do)
    beta = (2 / math.pi) * math.log(2 * math.cosh(p / Do) - 2)
    B = cR * beta
    C = -4 * h * K2

    disc = B**2 - 4*A*C
    if disc < 0:
        return None
    L1 = (-B + math.sqrt(disc)) / (2*A)
    L2 = (-B - math.sqrt(disc)) / (2*A)
    return L1 if L1 > 0 else L2




def metodo_ernst_dos_estratos(K1, K2, R, Do, u, y, h):
    """Método Ernst — 2 Estratos o K vertical != K horizontal"""
    D1 = Do + h / 2
    A = R / (8 * K * D1)
    B = (R / (math.pi * K)) * math.log(Do / u)
    C = R * (y + h) / K - h

    disc = B**2 - 4*A*C
    if disc < 0:
        return None

    L1 = (-B + math.sqrt(disc)) / (2*A)
    L2 = (-B - math.sqrt(disc)) / (2*A)
    return L1 if L1 > 0 else L2


# Placeholder para métodos avanzados
def metodo_hooghoudt_modificado():
    return None

def metodo_kirkham():
    return None

def metodo_dagan_modificado():
    return None


# ---------- MÉTODOS NO PERMANENTE – 1 ESTRATO ----------

def metodo_glover_dumm(K, S, t, ho, ht, Do, p):
    """Método Glover–Dumm — No permanente 1 estrato"""
    Lh = 5.0
    for _ in range(200):
        d = Do / (((8 * Do) / (math.pi * Lh)) * math.log(Do / p) + 1)
        L_new = math.sqrt((math.pi**2 * K * t * (d + (ho + ht)/4)) /
                          (S * math.log(1.16 * (ho / ht))))
        if abs(L_new - Lh) < 1e-4:
            break
        Lh = L_new
    return L_new


# ======================================================
# INTERFAZ PRINCIPAL
# ======================================================

st.sidebar.header("⚙ Configuración")

# --- Selección de categoría principal ---
categoria = st.sidebar.selectbox(
    "Seleccione el tipo de régimen",
    [
        "Permanente – Homogéneo",
        "Permanente – 2 estratos",
        "No Permanente – 1 estrato"
    ]
)

# --- Selección del tipo de dren ---
tipo_dren = st.sidebar.selectbox("Tipo de drenaje", ["Zanja", "Tubería"])

st.markdown(f"### Tipo de Régimen: **{categoria}**")
st.markdown(f"### Tipo de Drenaje: **{tipo_dren}**")

# ======================================================
# PARÁMETROS GENERALES DEL TERRENO
# ======================================================

st.markdown("## Parámetros generales del suelo")

K = st.number_input("Conductividad hidráulica K (m/día)", value=1.2, min_value=0.0001, step=0.01)
R = st.number_input("Recarga R (m/día)", value=0.01, min_value=0.0001, step=0.001)
PZ = st.number_input("Profundidad de la zanja (m)", value=1.5)
NFd = st.number_input("Nivel freático deseado (m)", value=1.0)
prof_capa_imp = st.number_input("Profundidad capa impermeable (m)", value=4.8)

# Parámetros geométricos según dren
if tipo_dren == "Zanja":
    st.markdown("### Parámetros de la zanja")
    b = st.number_input("Ancho de solera b (m)", value=0.5)
    y = st.number_input("Tirante de agua y (m)", value=0.2)
    Z = st.number_input("Talud Z (horizontal/vertical)", value=1.0)

    p = b + 2 * y * math.sqrt(1 + Z**2)
    Do = prof_capa_imp - PZ + y
    u = p
    h = prof_capa_imp - NFd - Do

else:  # Tubería
    st.markdown("### Parámetros de la tubería")
    r = st.number_input("Radio r (m)", value=0.1)
    b = st.number_input("Ancho solera zanja (m)", value=0.5)

    p = math.pi * r
    Do = prof_capa_imp - PZ + r
    y = r
    u = b + 4 * r
    h = prof_capa_imp - NFd - Do

H = prof_capa_imp - NFd

# ======================================================
# SELECCIÓN Y CÁLCULO DE MÉTODOS
# ======================================================

# ------------- 1) PERMANENTE HOMOGÉNEO ----------------
if categoria == "Permanente – Homogéneo":
    metodo = st.selectbox("Seleccione el método", ["Donnan", "Hooghoudt", "Dagan", "Ernst"])

    if metodo == "Donnan":
        L = metodo_donnan(K, R, H, Do)

    elif metodo == "Hooghoudt":
        L = metodo_hooghoudt(K, R, Do, p, h)

    elif metodo == "Dagan":
        L = metodo_dagan(K, R, Do, p, h)

    elif metodo == "Ernst":
        L = metodo_ernst_homogeneo(K, R, Do, p, h)
    
    if L is None:
        st.error("❌ No fue posible calcular el espaciamiento (discriminante negativo).")
    else:
        st.success(f"✅ Espaciamiento ({metodo}): **{L:.2f} m**")


# ------------- 2) PERMANENTE 2 ESTRATOS ----------------
elif categoria == "Permanente – 2 estratos":
    metodo = st.selectbox("Seleccione el método", ["Ernst"])
    K1 = st.number_input("Conductividad hidráulica K₁ (m/día) — Estrato superior", value=1.0)
    K2 = st.number_input("Conductividad hidráulica K₂ (m/día) — Estrato inferior", value=0.5)

    
    
    if metodo == "Dagan":
        L = metodo_dagan_dos_estratos(K1, K2, R, Do, u, y, h)
    
    elif metodo == "Ernst":
        L = metodo_ernst_dos_estratos(K1, K2, R, Do, u, y, h)

        if L is None:
            st.error("❌ No hay solución real en Ernst (discriminante < 0).")
        else:
            st.success(f"✅ Espaciamiento Ernst: **{L:.2f} m**")


# ------------- 3) NO PERMANENTE 1 ESTRATO ---------------
else:
    metodo = st.selectbox("Seleccione el método", ["Glover–Dumm"])

    if metodo == "Glover–Dumm":
        st.markdown("### Parámetros adicionales (No permanente)")
        S = st.number_input("Porosidad drenable S", value=0.05)
        t = st.number_input("Tiempo de drenaje t (días)", value=10.0)
        hi = st.number_input("Nivel inicial h₀ (m)", value=1.5)
        hf = st.number_input("Nivel final hₜ (m)", value=0.8)

        ho = PZ - y - hi
        ht = PZ - y - hf

        L = metodo_glover_dumm(K, S, t, ho, ht, Do, p)
        st.success(f"✅ Espaciamiento Glover–Dumm: **{L:.2f} m**")







