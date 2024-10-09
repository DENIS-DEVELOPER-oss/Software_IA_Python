import streamlit as st
from web_functions import predict

def app(df, X, y):
    st.title("Página de Predicción")

    st.markdown(
        """
            <p style="font-size:25px">
                Esta aplicación utiliza el <b style="color:green">Clasificador de Árbol de Decisión</b> para predecir el Nivel de Estrés.
            </p>
        """, unsafe_allow_html=True)
 
    st.subheader("Seleccionar Valores:")

    # Tomar la entrada de las características del usuario
    sr = st.slider("Tasa de Ronquidos (eventos/hora)", int(df["sr"].min()), int(df["sr"].max()))
    rr = st.slider("Tasa de Respiración (respiraciones/minuto)", int(df["rr"].min()), int(df["rr"].max()))
    bt = st.slider("Temperatura Corporal (en °F)", int(df["bt"].min()), int(df["bt"].max()))
    lm = st.slider("Movimiento de Extremidades", float(df["lm"].min()), float(df["lm"].max()))
    bo = st.slider("Oxígeno en Sangre (%)", float(df["bo"].min()), float(df["bo"].max()))
    rem = st.slider("Movimiento Rápido de Ojos", float(df["rem"].min()), float(df["rem"].max()))
    sh = st.slider("Horas de Sueño (horas)", float(df["sh"].min()), float(df["sh"].max()))
    hr = st.slider("Ritmo Cardíaco (latidos/minuto) ", float(df["hr"].min()), float(df["hr"].max()))
    
    # Crear una lista para almacenar todas las características
    features = [sr, rr, bt, lm, bo, rem, sh, hr]

    # Crear un botón para hacer la predicción
    if st.button("Predecir"):
        # Obtener la predicción y la precisión del modelo
        prediction, score = predict(X, y, features)
        st.info("Nivel de estrés detectado...")

        # Imprimir el resultado según la predicción
        if prediction == 1:
            st.success("La persona tiene un nivel de estrés bajo 🙂")
        elif prediction == 2:
            st.warning("La persona tiene un nivel de estrés medio 😐")
        elif prediction == 3:
            st.error("La persona tiene un nivel de estrés alto! 😞")
        elif prediction == 4:
            st.error("La persona tiene un nivel de estrés muy alto!! 😫")
        else:
            st.success("La persona está libre de estrés y tranquila 😄")

        # Imprimir la precisión del modelo
        st.write("El modelo  tiene una precisión del ", (score * 100), "%")

