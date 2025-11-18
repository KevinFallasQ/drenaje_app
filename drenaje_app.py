# streamlit_app.py
import streamlit as st
import math

st.set_page_config(page_title="Espaciamiento entre Drenes", layout="wide")
st.title("🌾 Espaciamiento entre Drenes")
st.markdown("Aplicación para calcular espaciamientos por distintos métodos (sin visualización gráfica).")

# ----------------------------------------
# Selección de régimen y método
# ----------------------------------------
st.markdown("## 1) Selección del régimen y método")
regimen = st.radio("Seleccione el régimen:", ("Permanente", "No permanente"))

if regimen == "Permanente":
    metodo = st.selectbox("Seleccione el método:", ("Donnan", "Hooghoudt", "Ernst", "Dagan"))
else:  # No permanente
    metodo = st.selectbox("Seleccione el método:", ("Glover–Dumm",))

st.markdown("---")

# ----------------------------------------
# Parámetros generales (visibles siempre)
# ----------------------------------------
st.markdown("## 2) Parámetros generales")
K = st.number_input("Conductividad hidráulica K (m/día)", value=1.20, min_value=1e-6, step=0.01, format="%.3f")
R = st.number_input("Recarga R (m/día)", value=0.01, min_value=1e-6, step=0.001, format="%.4f")
tipo_drenaje = st.selectbox("Tipo de drenaje", ("Zanja", "Tubería"))

st.markdown("---")

# ----------------------------------------
# Parámetros según tipo de dren
# ----------------------------------------
st.markdown("## 3) Parámetros geométricos del dren y del suelo")

# Profundidad de la zanja y nivel freático deseado (para régimen permanente)
PZ = st.number_input("Profundidad de la zanja PZ (m) — (régimen permanente)", value=1.50, min_value=0.01, step=0.01, format="%.3f")
NFd = st.number_input("Altura del nivel freático deseado NFd (m) — (régimen permanente)", value=1.00, min_value=0.00, step=0.01, format="%.3f")
prof_capa_imp = st.number_input("Profundidad de la capa impermeable (m)", value=4.80, min_value=0.01, step=0.01, format="%.3f")

# Parámetros específicos para zanja o tubería (usados por los métodos de régimen permanente)
if tipo_drenaje == "Zanja":
    st.markdown("### Parámetros para Zanja")
    b = st.number_input("Ancho de solera b (m)", value=0.50, min_value=0.01, step=0.01, format="%.3f")
    y = st.number_input("Tirante de agua y (m)", value=0.20, min_value=0.00, step=0.01, format="%.3f")
    Z = st.number_input("Talud Z (horizontal/vertical)", value=1.0, min_value=0.0, step=0.01, format="%.3f")
    # perímetro hidráulico equivalente (aproximación)
    p_perm = b + 2 * y * math.sqrt(1 + Z**2)
    Do_perm = prof_capa_imp - PZ + y
    h_perm = prof_capa_imp - NFd - Do_perm
    u_perm = p_perm
else:
    st.markdown("### Parámetros para Tubería")
    r = st.number_input("Radio del tubo drenante r (m)", value=0.10, min_value=0.01, step=0.01, format="%.3f")
    b = st.number_input("Ancho de solera b de la zanja (m) — (para cálculo geométrico) (m)", value=0.50, min_value=0.01, step=0.01, format="%.3f")
    p_perm = math.pi * r
    Do_perm = prof_capa_imp - PZ + r
    h_perm = prof_capa_imp - NFd - Do_perm
    u_perm = b + 4 * r
    y = r

# ----------------------------------------
# Parámetros para Glover–Dumm (régimen no permanente)
# ----------------------------------------
if regimen == "No permanente":
    st.markdown("## 4) Parámetros — Glover–Dumm (régimen no permanente)")
    K_gd = st.number_input("Conductividad hidráulica K (m/día) [Glover–Dumm]", value=0.90, min_value=1e-6, step=0.01, format="%.3f")
    S = st.number_input("Porosidad drenable S (adimensional)", value=0.05, min_value=0.0001, step=0.005, format="%.3f")
    t = st.number_input("Tiempo de drenaje t (días)", value=3.0, min_value=0.01, step=0.1, format="%.2f")
    hi = st.number_input("Altura inicial del nivel freático h₀ (m)", value=0.650, min_value=0.0, step=0.01, format="%.3f")
    hf = st.number_input("Altura final deseada del nivel freático hₜ (m)", value=1.10, min_value=0.0, step=0.01, format="%.3f")
    PZ_gd = st.number_input("Profundidad de la zanja PZ (m) — (Glover–Dumm)", value=1.50, min_value=0.01, step=0.01, format="%.3f")
    prof_capa_imp_gd = st.number_input("Profundidad de la capa impermeable (m) — (Glover–Dumm)", value=4.80, min_value=0.01, step=0.01, format="%.3f")

    st.markdown("### Parámetros geométricos (Glover–Dumm)")
    r_gd = st.number_input("Radio del tubo drenante r (m) — (Glover–Dumm)", value=0.10, min_value=0.01, step=0.01, format="%.3f")
    b_gd = st.number_input("Ancho de solera b de la zanja (m) — (Glover–Dumm)", value=0.50, min_value=0.01, step=0.01, format="%.3f")

    # geométricos para gd
    p_gd = math.pi * r_gd
    Do_gd = prof_capa_imp_gd - PZ_gd + r_gd
    ho = PZ_gd - r_gd - hi
    ht = PZ_gd - r_gd - hf

st.markdown("---")

# ----------------------------------------
# Funciones de cálculo (métodos)
# ----------------------------------------
def calculo_donnan(K, R, H, Do):
    # H: profundidad total deseada (prof_capa_imp - NFd)
    if R <= 0:
        raise ValueError("R debe ser mayor que 0")
    val = (4 * K * (H**2 - Do**2)) / R
    if val <= 0:
        raise ValueError("Expresión dentro de sqrt no positiva para Donnan.")
    return math.sqrt(val)

def calculo_hooghoudt(K, R, Do, h, p, iter_max=500, tol=1e-4):
    # Iteración para Hooghoudt (valor inicial L)
    Lh = 5.0
    for _ in range(iter_max):
        # evitar log de <=0
        if Do <= p:
            raise ValueError("Para Hooghoudt: Do debe ser mayor que p (perímetro equivalente) para evitar log no definido.")
        denom = ((8 * Do) / (math.pi * Lh)) * math.log(Do / p) + 1
        if denom == 0:
            raise ValueError("Denominator cero en Hooghoudt.")
        d = Do / denom
        L_new = math.sqrt((8 * K * d * h + 4 * K * h**2) / R)
        if math.isnan(L_new) or L_new <= 0:
            raise ValueError("Resultado no físico en Hooghoudt (NaN o <=0). Revisa parámetros.")
        if abs(L_new - Lh) < tol:
            return L_new
        Lh = L_new
    return Lh

def calculo_ernst(K, R, Do, h, y, u):
    # Fórmula cuadrática proporcionada en tu ejemplo
    D1 = Do + h / 2
    A = R / (8 * K * D1) if (8*K*D1) != 0 else float("inf")
    # Evitar log no definido
    if Do <= u:
        raise ValueError("Para Ernst: Do debe ser mayor que u (evita log de <=1 o negativo).")
    B = (R / (math.pi * K)) * math.log(Do / u)
    C = R * (y + h) / K - h
    discriminant = B**2 - 4 * A * C
    if discriminant < 0:
        raise ValueError("Discriminante negativo en Ernst — no hay solución real.")
    L_pos = (-B + math.sqrt(discriminant)) / (2 * A)
    L_neg = (-B - math.sqrt(discriminant)) / (2 * A)
    L = L_pos if L_pos > 0 else L_neg
    if L <= 0 or math.isnan(L):
        raise ValueError("Resultado no físico (Ernst).")
    return L

def calculo_dagan(K, R, Do, h, p):
    # Implementación basada en el bloque original
    A = R / (2 * Do) if Do != 0 else float("inf")
    # cálculo beta: evitar cosh demasiado grande; usar la expresión original con precaución
    # Si p/Do es grande, cosh puede crecer — revisar dominio
    try:
        beta = (2 / math.pi) * math.log(2 * math.cosh(p / Do) - 2)
    except Exception:
        raise ValueError("Error calculando beta en Dagan (argumento de log inválido). Revise p y Do.")
    B = R * beta
    C = -4 * h * K
    discriminant = B**2 - 4 * A * C
    if discriminant < 0:
        raise ValueError("Discriminante negativo en Dagan — no hay solución real.")
    L_pos = (-B + math.sqrt(discriminant)) / (2 * A)
    L_neg = (-B - math.sqrt(discriminant)) / (2 * A)
    L = L_pos if L_pos > 0 else L_neg
    if L <= 0 or math.isnan(L):
        raise ValueError("Resultado no físico (Dagan).")
    return L

def calculo_glover_dumm(K_gd, S, t, d, ho, ht):
    # Fórmula de Glover–Dumm proporcionada en tu código original
    if S <= 0:
        raise ValueError("S debe ser mayor que 0")
    ratio = ho / ht if ht != 0 else float("inf")
    if ratio <= 0:
        raise ValueError("Relación ho/ht inválida para logaritmo en Glover–Dumm.")
    val = (math.pi**2 * K_gd * t * (d + (ho + ht) / 4)) / (S * math.log(1.16 * ratio))
    if val <= 0:
        raise ValueError("Expresión dentro de sqrt no positiva para Glover–Dumm.")
    return math.sqrt(val)

# ----------------------------------------
# Cálculo y salida de resultados
# ----------------------------------------
st.markdown("## 5) Resultados")

results = {}

try:
    if regimen == "Permanente":
        # H: profundidad total deseada
        H = prof_capa_imp - NFd

        if metodo == "Donnan":
            L = calculo_donnan(K, R, H, Do_perm)
            results["Donnan"] = L

        elif metodo == "Hooghoudt":
            L = calculo_hooghoudt(K, R, Do_perm, h_perm, p_perm)
            results["Hooghoudt"] = L

        elif metodo == "Ernst":
            L = calculo_ernst(K, R, Do_perm, h_perm, y, u_perm)
            results["Ernst"] = L

        elif metodo == "Dagan":
            L = calculo_dagan(K, R, Do_perm, h_perm, p_perm)
            results["Dagan"] = L

    else:
        # No permanente -> Glover–Dumm
        # Primero calcular d (usando Hooghoudt como en tu flujo original)
        # usar Do_gd y p_gd
        if Do_gd <= p_gd:
            raise ValueError("Para Glover–Dumm: Do debe ser mayor que p para calcular d correctamente.")
        # calcular d con la expresión de Hooghoudt simplificada (itera L inicial)
        L_temp = 5.0
        for _ in range(200):
            denom = ((8 * Do_gd) / (math.pi * L_temp)) * math.log(Do_gd / p_gd) + 1
            if denom == 0:
                raise ValueError("Denominator cero al calcular d para Glover–Dumm.")
            d = Do_gd / denom
            # calcular L_new con fórmula de Glover–Dumm
            try:
                L_new = calculo_glover_dumm(K_gd, S, t, d, ho, ht)
            except Exception as e:
                raise
            if abs(L_new - L_temp) < 1e-4:
                break
            L_temp = L_new
        results["Glover–Dumm"] = L_new

except Exception as e:
    st.error(f"❌ Error en los cálculos: {e}")
    results = {}

# Mostrar resultados de forma clara
if results:
    for name, val in results.items():
        st.success(f"✅ Espaciamiento {name}: {val:.2f} m")
else:
    st.info("Aún no hay resultados válidos. Revise los parámetros o mensajes de error arriba.")

st.markdown("---")
st.caption("Notas: Las fórmulas empleadas son las provistas en la versión inicial. Revise unidades y dominio de las funciones (logs, raíces).")





