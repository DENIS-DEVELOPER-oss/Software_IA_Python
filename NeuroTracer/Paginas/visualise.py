
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import tree
import streamlit as st


# Importar funciones necesarias de web_functions
from web_functions import train_model

def app(df, X, y):

    warnings.filterwarnings('ignore')
    st.set_option('deprecation.showPyplotGlobalUse', False)


    st.title("Visualizar la Predicción del Parkinson")

  
    if st.checkbox("Mostrar el mapa de calor de correlación"):
        st.subheader("Mapa de Calor de Correlación")

        fig = plt.figure(figsize = (10, 6))
        ax = sns.heatmap(df.iloc[:, 1:].corr(), annot = True)  
        bottom, top = ax.get_ylim()                            
        ax.set_ylim(bottom + 0.5, top - 0.5)                    
        st.pyplot(fig)
        if st.button("Interpretacion-"):
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
            <hr style="border:2px solid blue"> 
            """, unsafe_allow_html=True)

    if st.checkbox("Mostrar Gráfico de Dispersión"):
        st.subheader("Gráficos de Dispersión y de conteo")
        figure, axis = plt.subplots(2, 2,figsize=(15,10))

        sns.scatterplot(ax=axis[0,0],data=df,x='AVFF',y='MAVFF',hue='status')
        axis[0, 0].set_title("Dispersión de la Minoría Sobremuestreada")
  
        sns.countplot(ax=axis[0, 1],x="status", data=df)
        axis[0, 1].set_title("Conteo de la Minoría Sobremuestreada")
  
        sns.scatterplot(ax=axis[1, 0],data=df,x='AVFF',y='MAVFF',hue='status')
        axis[1, 0].set_title("Dispersión de la Mayoría Submuestreada")
  
        sns.countplot(ax=axis[1, 1],x="status", data=df)
        axis[1, 1].set_title("Conteo de la Mayoría Submuestreada")
        st.pyplot()
        if st.button("-Interpretacion"):
            st.markdown(
            """
                <div style="text-align: justify">
                    Estos gráficos se utilizan para visualizar la relación entre la frecuencia fundamental vocal media (AVFF) y la frecuencia fundamental vocal máxima (MAVFF) en dos contextos diferentes: sobremuestreo de la minoría y submuestreo de la mayoría. Los gráficos de dispersión muestran cómo se distribuyen estos dos atributos en función del estado de la enfermedad de Parkinson (presente o ausente), mientras que los gráficos de conteo muestran el número de observaciones para cada estado de la enfermedad en los dos contextos.
                </div>
            """,
                unsafe_allow_html=True
                        )
        st.markdown("""
            <hr style="border:2px solid blue"> 
            """, unsafe_allow_html=True)           
    if st.checkbox("Mostrar Boxplot"):
        st.subheader("Boxplot")
        fig, ax = plt.subplots(figsize=(15,5))
        df.boxplot(['AVFF', 'MAVFF', 'MIVFF','HNR'],ax=ax)
        st.pyplot()
        if st.button("Interpretacion"):
            st.markdown(
            """
                <div style="text-align: justify">
Este gráfico muestra la distribución de varias variables ('AVFF', 'MAVFF', 'MIVFF','HNR') en el conjunto de datos. Los gráficos de caja pueden proporcionar información sobre la mediana, los cuartiles, los valores atípicos y la simetría de los datos.                </div>
            """,
                unsafe_allow_html=True
                        )
        st.markdown("""
            <hr style="border:1px solid blue"> 
            """, unsafe_allow_html=True)
    if st.checkbox("Mostrar Resultados de Muestra"):
        st.subheader("Resultados de Muestra")
        safe = (df['status'] == 0).sum()
        prone = (df['status'] == 1).sum()
        data = [safe,prone]
        labels = ['Seguro', 'Propenso']
        colors = sns.color_palette('pastel')[0:7]
        plt.pie(data, labels = labels, colors = colors, autopct='%.0f%%')
        st.pyplot()
        if st.button(".Interpretacion."):
            st.markdown(
            """
                <div style="text-align: justify">
Este gráfico de pastel muestra la proporción de observaciones que son 'Seguras' (no tienen la enfermedad de Parkinson) y 'Propensas' (tienen la enfermedad de Parkinson o están en riesgo de tenerla). Esto proporciona una visión general de cómo están balanceados los datos.                </div>
            """,
                unsafe_allow_html=True
                        )
        st.markdown("""
            <hr style="border:1px solid blue"> 
            """, unsafe_allow_html=True)
    if st.checkbox("Graficar Árbol de Decisión"):
        st.header("Árbol de decisión")
        model, score = train_model(X, y)
        dot_data = tree.export_graphviz(
            decision_tree=model, max_depth=3, out_file=None, filled=True, rounded=True,
            feature_names=X.columns, class_names=['0', '1']
        )
        st.graphviz_chart(dot_data)
        if st.button("Interpretacion."):
            
            st.markdown(
            """
                <div style="text-align: justify">
Este gráfico visualiza el árbol de decisión del modelo de aprendizaje automático entrenado para predecir el estado de la enfermedad de Parkinson. Cada nodo en el árbol representa una decisión basada en los atributos, lo que ayuda a entender el proceso de toma de decisiones del modelo.                </div>
            """,
                unsafe_allow_html=True
                        )


