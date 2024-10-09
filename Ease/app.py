import streamlit as st
from web_functions import load_data
from Paginas import home, data, predict, visualise

Tabs = {
    "Inicio": home,
    "Información de Datos": data,
    "Predicción": predict,
    "Visualización": visualise
    
}

# Crear una barra lateral
st.sidebar.image("imagenes/logo1.png", use_column_width=200)
st.sidebar.markdown("<h1 style='text-align: center; color: red;'>EASE</h1>", unsafe_allow_html=True)
st.sidebar.markdown(
    """
    <div style='text-align: justify;'>
        Aquí puedes encontrar diferentes opciones de navegación para explorar la aplicación. 
        Puedes seleccionar entre las distintas páginas disponibles y analizar los datos, realizar predicciones y visualizar los resultados.
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown("---")
st.sidebar.title("Navegación")

pagina = st.sidebar.radio("Páginas", list(Tabs.keys()))

# Cargando el conjunto de datos.
df, X, y = load_data()

# Llamar a la función de la página seleccionada para ejecutar
if pagina in ["Predicción", "Visualización"]:
    Tabs[pagina].app(df, X, y)
elif (pagina == "Información de Datos"):
    Tabs[pagina].app(df)
else:
    Tabs[pagina].app()