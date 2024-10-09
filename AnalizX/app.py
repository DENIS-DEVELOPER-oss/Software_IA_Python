import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import numpy as np
import io
from PIL import Image
import base64
image = Image.open("imagenes/logo.png")

st.set_page_config(
    page_title="AnalizX",
    page_icon="📊"
)

st.header("")
st.image(image)
st.markdown("<p style='text-align: justify;'>AnalizX es una  aplicación de análisis de datos que te permite explorar, visualizar y analizar tus conjuntos de datos de manera intuitiva y eficiente. Con AnalizX, puedes cargar archivos CSV, obtener una vista previa de los datos, realizar análisis descriptivos, identificar y manejar valores nulos, convertir datos no numéricos en numéricos, y generar visualizaciones impactantes como gráficos de barras, diagramas de caja, violín, dispersión y líneas. Descubre patrones, tendencias y relaciones ocultas en tus datos, y obtén información valiosa para tomar decisiones informadas y realizar análisis en profundidad. AnalizX es la herramienta perfecta para potenciar tus capacidades de análisis de datos.</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Elige un archivo CSV", type='csv')
generate = st.button('Analizar')


def get_base64_of_image(image_path):
    with open(image_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode("utf-8")
    return encoded_string

background_image = "imagenes/fondo.jpg"
encoded_image = get_base64_of_image(background_image)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('data:image/png;base64,{encoded_image}');
        background-size: cover;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
if 'load_state' not in st.session_state:
    st.session_state.load_state = False

if generate or st.session_state.load_state:
    st.session_state.load_state = True

    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)

        st.subheader("VISTA PREVIA DE LOS DATOS")
        col1, col2, col3 = st.columns([1, 10, 1])

        with col2:
            st.dataframe(dataframe)


        st.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([10, 3, 10])

        with col1:
            st.subheader("Descripción de los datos")
            st.markdown("<p style='text-align: justify;'>En esta seccion se proporciona información esencial sobre la estructura y el contenido del DataFrame, incluyendo el nombre de las columnas, el tipo de datos de cada columna y la cantidad de valores no nulos en cada una de ellas. Esto es útil para comprender la composición y la calidad de los datos contenidos en el DataFrame</p>", unsafe_allow_html=True)
        with col2:
            st.write("")

        with col3:
            buffer = io.StringIO()
            dataframe.info(buf=buffer)
            s = buffer.getvalue()

            st.text(s)

        st.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

        st.subheader('Proporción de valores nulos')
        st.markdown("<p style='text-align: justify;'>Esta sección proporciona una manera conveniente de manejar los valores nulos en el conjunto de datos cargado, ofreciendo opciones para rellenarlos con medidas estadísticas o eliminar las filas que los contienen. Esto permite realizar una limpieza inicial de los datos antes de realizar análisis o visualizaciones.</p>", unsafe_allow_html=True)
        st.markdown("")
        def null_ratio(df):
            data = [(col, dataframe[col].isnull().sum() / len(dataframe) * 100)
                    for col in dataframe.columns if dataframe[col].isnull().sum() > 0]

            columns = ['columna', 'proporción']
            missing_data = pd.DataFrame(data, columns=columns)

            fig = px.bar(missing_data, x='columna', y='proporción')
            st.write(fig)

        null_ratio(dataframe)

        st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

        st.subheader("Convertir datos no numéricos a numéricos")
        col = st.selectbox("Selecciona una columna para convertir", dataframe.columns)
        if col:
            dataframe[col] = pd.to_numeric(dataframe[col], errors='coerce')
            Convert = st.button('Convertir')
            if Convert:
                if (dataframe[col].dtype == np.float64 or dataframe[col].dtype == np.int64):
                    st.success('Columna convertida a tipo de datos numéricos')

        st.subheader("Valores nulos")
        col = st.selectbox("Selecciona una columna para imputar o eliminar", dataframe.columns[dataframe.isna().any()].tolist())
        if col:
            option = st.selectbox("Selecciona un tipo de visualización", ["Media", "Moda", "Mediana", "Eliminar valores nulos"])
            if (option == "Media" and (dataframe[col].dtype == np.float64 or dataframe[col].dtype == np.int64)):
                dataframe[col].fillna(dataframe[col].mean(), inplace=True)

            elif option == "Moda" and dataframe.dtypes[col] == 'object':
                dataframe[col].fillna(dataframe[col].mode()[0], inplace=True)

            elif option == 'Mediana' and (dataframe[col].dtype == np.float64 or dataframe[col].dtype == np.int64):
                dataframe[col].fillna(dataframe[col].median(), inplace=True)

            elif option == "Eliminar valores nulos":
                dataframe.dropna(subset=[col], inplace=True)

            Fill = st.button('Completar')
            if Fill:
                if (dataframe.dtypes[col] == 'object' and option == 'Media' or option == 'Mediana'):
                    st.error('Elige otro método')

                elif option == "Eliminar valores nulos":
                    st.success('Valores nulos eliminados')
                    null_df = dataframe.isnull().sum()
                    columns = ['Cantidad de valores nulos']
                    missing_data = pd.DataFrame(null_df, columns=columns)
                    st.write(missing_data.T)

                else:
                    st.success('Columna completada')
                    null_df = dataframe.isnull().sum()
                    columns = ['Cantidad de valores nulos']
                    missing_data = pd.DataFrame(null_df, columns=columns)
                    st.write(missing_data.T)

        st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

        st.subheader("Gráficas")
        st.markdown("<p style='text-align: justify;'>Estas seccion es para poder explorar visualmente los datos cargados seleccionando columnas y generando diferentes tipos de gráficas interactivas. Esto facilita el análisis y la comprensión de los datos de manera visual.</p>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])

        categ = [col for col in dataframe.columns if dataframe.dtypes[col] == 'object']

        box_1 = col1.selectbox('Selecciona la columna 1', categ)
        box_2 = col2.selectbox('Selecciona la columna 2', categ)
        box_3 = col3.selectbox('Selecciona la columna 3', categ)

        col4, col5, col6 = st.columns([1, 1, 1])

        numer = [col for col in dataframe.columns if (dataframe[col].dtype == np.float64 or dataframe[col].dtype == np.int64)]

        box_4 = col4.selectbox('Selecciona la columna 4', numer)
        box_5 = col5.selectbox('Selecciona la columna 5', numer)
        box_6 = col6.selectbox('Selecciona la columna 6', numer)

        graphs = st.container()

        with graphs:
            col1, col2, col3 = st.columns([1, 1, 1])

            fig1 = px.pie(dataframe, values=box_4, names=box_1, hole=0.5)
            fig1.update_layout(
                showlegend=False,
                margin=dict(l=1, r=1, t=1, b=1),
                height=200,
                yaxis_scaleanchor="x",
            )
            col1.plotly_chart(fig1, use_container_width=True)

            fig2 = px.pie(dataframe, values=box_5, names=box_2, hole=0.5)
            fig2.update_layout(
                showlegend=False,
                margin=dict(l=1, r=1, t=1, b=1),
                height=200,
                yaxis_scaleanchor="x",
            )
            col2.plotly_chart(fig2, use_container_width=True)

            fig3 = px.pie(dataframe, values=box_6, names=box_3, hole=0.5)
            fig3.update_layout(
                showlegend=False,
                margin=dict(l=1, r=1, t=1, b=1),
                height=200,
                yaxis_scaleanchor="x",
            )
            col3.plotly_chart(fig3, use_container_width=True)

        st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        option = st.selectbox("Selecciona un tipo de visualización", ["Gráfico de barras", "Diagrama de caja", "Violin plot", "Gráfico de dispersión", "Gráfico de línea"])

        if option == "Gráfico de barras":
            col1, col2 = st.columns([1, 1])
            x = col1.selectbox("Selecciona una columna para el eje x", categ)
            y = col2.selectbox("Selecciona una columna para el eje y", numer)
            fig = px.bar(dataframe, x=x, y=y, title='Gráfico de barras para {} y {}'.format(x, y))
            st.write(fig)

        elif option == "Diagrama de caja":
            col1, col2 = st.columns([1, 1])
            x = col1.selectbox("Selecciona una columna para el eje x", categ)
            y = col2.selectbox("Selecciona una columna para el eje y", numer)
            fig = px.box(dataframe, x=x, y=y, title='Diagrama de caja para {} y {}'.format(x, y))
            st.write(fig)

        elif option == "Violin plot":
            col1, col2 = st.columns([1, 1])
            x = col1.selectbox("Selecciona una columna para el eje x", categ)
            y = col2.selectbox("Selecciona una columna para el eje y", numer)
            fig = px.violin(dataframe, x=x, y=y, box=True, points="all", title='Violin plot para {} y {}'.format(x, y))
            st.write(fig)

        elif option == "Gráfico de dispersión":
            col1, col2 = st.columns([1, 1])
            x = col1.selectbox("Selecciona una columna para el eje x", categ)
            y = col2.selectbox("Selecciona una columna para el eje y", numer)
            fig = px.scatter(dataframe, x=x, y=y, title='Gráfico de dispersión para {} y {}'.format(x, y))
            st.write(fig)

        elif option == "Gráfico de línea":
            col1, col2 = st.columns([1, 1])
            x = col1.selectbox("Selecciona una columna para el eje x", categ)
            y = col2.selectbox("Selecciona una columna para el eje y", numer)
            fig = px.line(dataframe, x=x, y=y, title='Gráfico de línea para {} y {}'.format(x, y))
            st.write(fig)

