# 🌾 Aplicación de Drenaje Subsuperficial – v5

Esta aplicación permite calcular el **espaciamiento entre drenes** y visualizar el **perfil del nivel freático** en régimen permanente y no permanente.  

## Métodos disponibles:
- Hooghoudt
- Donnan
- Ernst
- Glover-Dumm (No Permanente)

## Cómo usar:
1. Selecciona el método deseado.
2. Ingresa los parámetros del suelo y drenaje.
3. La app mostrará el espaciamiento recomendado y un gráfico con el flujo.
4. Si deseas reiniciar los valores, haz clic en **"🔄 Reiniciar valores"**.

## Requisitos
- La app está lista para ejecutarse en [Streamlit Cloud](https://streamlit.io/cloud) o localmente.
- Librerías necesarias: `streamlit`, `numpy`, `matplotlib`.

## Cómo ejecutar localmente:
```bash
pip install -r requirements.txt
streamlit run drenaje_app.py
