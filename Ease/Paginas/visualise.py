import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import tree
import streamlit as st

from web_functions import train_model

def app(df, X, y):

    warnings.filterwarnings('ignore')
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.title("Visualizar el Nivel de Estrés")

    # Crear una casilla de verificación para mostrar el mapa de calor de correlación
    if st.checkbox("Mostrar el mapa de calor de correlación"):
        st.subheader("Mapa de calor de correlación")
        fig = plt.figure(figsize=(10, 6))
        ax = sns.heatmap(df.iloc[:, 1:].corr(), annot=True)   
        bottom, top = ax.get_ylim()                            
        ax.set_ylim(bottom + 0.5, top - 0.5)                   
        st.pyplot(fig)
        if st.button("Interpretacion...."):
            st.markdown(
            """
                <div style="text-align: justify">
                    Este gráfico muestra las correlaciones entre todas las variables numéricas del conjunto de datos. 
                    Cada celda en el gráfico corresponde al coeficiente de correlación entre dos variables. Los colores 
                    más cálidos (más cerca del rojo) indican una correlación positiva fuerte, mientras que los colores 
                    más fríos (más cerca del azul) indican una correlación negativa fuerte. Este gráfico puede ayudar a 
                    identificar qué variables están más correlacionadas entre sí, lo cual es útil para entender las relaciones 
                    entre las variables.
                </div>
            """,
                unsafe_allow_html=True
                        )
        st.markdown("""
            <hr style="border:1px solid red"> 
            """, unsafe_allow_html=True)

    if st.checkbox("Mostrar Gráficas de Dispersión"):
        st.subheader("Gráficas de Dispersión")

        figure, axis = plt.subplots(2, 2, figsize=(15, 10))

        sns.scatterplot(ax=axis[0, 0], data=df, x='bt', y='rr')
        axis[0, 0].set_title("Temperatura Corporal vs Tasa de Respiración")

        sns.scatterplot(ax=axis[0, 1], data=df, x='sr', y='lm')
        axis[0, 1].set_title("Tasa de Ronquidos vs Movimiento de Extremidades")

        sns.scatterplot(ax=axis[1, 0], data=df, x='bo', y='bt')
        axis[1, 0].set_title("Oxígeno en Sangre vs Temperatura Corporal")

        sns.scatterplot(ax=axis[1, 1], data=df, x='sh', y='hr')
        axis[1, 1].set_title("Horas de Sueño vs Ritmo Cardíaco")
        st.pyplot()
        if st.button("Interpretacion-"):
           st.markdown(
            """
            <div style="text-align: justify">\n
            - Temperatura Corporal vs Tasa de Respiración: Este gráfico de dispersión muestra la relación entre la temperatura corporal y la tasa de respiración. Permite observar si hay alguna tendencia o patrón en los datos que relacione estos dos atributos.\n
            - Tasa de Ronquidos vs Movimiento de Extremidades: Aquí, se representa la relación entre la tasa de ronquidos y el movimiento de extremidades. El gráfico permite analizar si existe alguna conexión entre ambos atributos.\n
            - Oxígeno en Sangre vs Temperatura Corporal: Esta gráfica muestra cómo se relaciona el oxígeno en sangre con la temperatura corporal. Ayuda a identificar si hay alguna asociación significativa entre estas dos variables.\n
            - Horas de Sueño vs Ritmo Cardíaco: Este gráfico ilustra la relación entre las horas de sueño y el ritmo cardíaco. Permite identificar posibles correlaciones o patrones entre estos atributos.\n
            </div>
            """,
        unsafe_allow_html=True
        )

        st.markdown("""
            <hr style="border:1px solid red"> 
            """, unsafe_allow_html=True)

    if st.checkbox("Mostrar Diagramas de Caja"):
        st.subheader("Diagramas de Caja")
        
        fig, ax = plt.subplots(figsize=(15, 5))
        df.boxplot(['sr', 'rr', 'bt', 'rem', 'bo', 'sh'], ax=ax)
        st.pyplot()
        if st.button("Interpretacion."):
            st.markdown(
            """
                <div style="text-align: justify">
Los diagramas de caja proporcionan una representación visual de la distribución de los datos en cada atributo. La caja representa el rango intercuartílico, que muestra el 50% central de los datos. La línea dentro de la caja representa la mediana, y los puntos fuera de la caja son valores atípicos. Este gráfico es útil para detectar valores atípicos y tener una idea de cómo se distribuyen los datos en cada atributo.                </div>
            """,
                unsafe_allow_html=True
                        )
        st.markdown("""
            <hr style="border:1px solid red"> 
            """, unsafe_allow_html=True)

    if st.checkbox("Mostrar Resultados"):
        st.subheader("Resultados")
        seguro = (df['sl'] == 0).sum()
        bajo = (df['sl'] == 1).sum()
        medio = (df['sl'] == 2).sum()
        alto = (df['sl'] == 3).sum()
        muy_alto = (df['sl'] == 4).sum()
        data = [seguro, bajo, medio, alto, muy_alto]
        etiquetas = ['Seguro', 'Bajo', 'Medio', 'Alto', 'Muy Alto']
        colores = sns.color_palette('pastel')[0:7]
        plt.pie(data, labels=etiquetas, colors=colores, autopct='%.0f%%')
        st.pyplot()
        if st.button("Interpretacion.."):
            st.markdown(
            """
                <div style="text-align: justify">
Este gráfico de pastel muestra la distribución de los resultados de ejemplo en diferentes niveles de estrés. Cada porción del pastel representa el porcentaje de personas en cada nivel de estrés (Seguro, Bajo, Medio, Alto y Muy Alto) dentro del conjunto de datos. Es una representación visual rápida para tener una idea de la proporción de personas en cada categoría de estrés.
                </div>
            """,
                unsafe_allow_html=True
                        )
        st.markdown("""
            <hr style="border:1px solid red"> 
            """, unsafe_allow_html=True)

    

    
    
