import streamlit as st
from DataLoader import DataLoader
from DataEvaluator import DataEvaluator
from GraphicGenerator import GraphicGenerator
from LogisticRegressor import LogisticRegressor
from PIL import Image
import base64

# Cargar la imagen
image = Image.open('imagenes/logo.png')

# Mostrar la imagen como título
st.image(image, use_column_width=400)

background_color = "#160E2A" 

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {background_color};
    }}
    </style>
    
    """,
    unsafe_allow_html=True
)



if __name__ == '__main__':

    st.markdown('<h1 style="text-align: center; color: #81B0D5;">REGRESION LOGISTICA</h1>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: justify">La regresión logística es un modelo estadístico utilizado para predecir la probabilidad de ocurrencia de un evento binario basado en variables predictoras. Se utiliza ampliamente en problemas de clasificación, donde se busca asignar una categoría a una observación en función de sus características.</div>', unsafe_allow_html=True)

    # Cargar Datos
    st.header('Importar Datos')
    dataLoader = DataLoader()
    dataLoader.check_labels()
    dataLoader.check_separator()
    file = dataLoader.load_file()

    if file is not None:
        df = dataLoader.load_data(file)

        # Evaluacion de Datos
        st.header('Evaluación de Datos')
        st.write('Se eliminaron las columnas y filas no numéricas con valores faltantes.')
        dataEvaluator = DataEvaluator(df)
        dataEvaluator.show_head()
        dataEvaluator.show_dimensions()
        dataEvaluator.show_columns()

        # Generar Graficos
        st.header('GRAFICOS')
        plotGenerator = GraphicGenerator(df)

        checked_pairplot = st.checkbox('Graficos de Dispersión en Matriz')
        checked_scatterPlot = st.checkbox('Gráfico de dispersión')
        checked_correlationPlot = st.checkbox('Correlación')
        checked_logisticRegPlot = st.checkbox('Regresión Logística')

        if checked_pairplot:
            plotGenerator.pairplot()
            st.markdown('<hr/>', unsafe_allow_html=True)

        if checked_scatterPlot:
            plotGenerator.scatterplot()
            st.markdown('<hr/>', unsafe_allow_html=True)

        if checked_correlationPlot:
            plotGenerator.correlationPlot()
            st.markdown('<hr/>', unsafe_allow_html=True)

        if checked_logisticRegPlot:
            plotGenerator.logisticRegressionPlot()
            st.markdown('<hr/>', unsafe_allow_html=True)

        # Regresion Logistica
        st.header('Regresión Logistica')
        regressor = LogisticRegressor(df)
        regressor.logistic()
        st.markdown('<hr/>', unsafe_allow_html=True)
