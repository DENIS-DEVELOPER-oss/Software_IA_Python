import streamlit as st
from web_functions import load_data
from Paginas import home, data, predict, visualise



Tabs = {
    "Descripcion": home,
    "Info de Datos": data,
    "Predicción": predict,
    "Visualización": visualise
    
}

# Crear una barra lateral
st.sidebar.image("imagenes/logo1.png", use_column_width=True)

st.sidebar.markdown("""
    <h1 style="color:blue; font-family:Barlow; text-align:center;">NEURO TRACER</h1>
    """, unsafe_allow_html=True)
st.sidebar.markdown("""
    <p style="text-align: justify">
            En esta seccion podras navegar entre las diferentes pestañas de la aplicacion, de manera muy sencilla.
    </p>
    """, unsafe_allow_html=True)
st.sidebar.markdown("---")

pagina = st.sidebar.radio("SECCIONES", list(Tabs.keys()))

df, X, y = load_data()

if pagina in ["Predicción", "Visualización"]:
    Tabs[pagina].app(df, X, y)
elif (pagina == "Info de Datos"):
    Tabs[pagina].app(df)
else:
    Tabs[pagina].app()
