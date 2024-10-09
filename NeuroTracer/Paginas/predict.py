
import streamlit as st
from web_functions import predict

def app(df, X, y):

    st.title("Página de Predicción")

    st.markdown(
        """
            <p style="font-size:25px">
                Esta aplicación utiliza el <b style="color:green">Clasificador Random Forest</b> para la Predicción de la enfermedad de Parkinson.
            </p>
        """, unsafe_allow_html=True)
    with st.expander("Ver detalles de los atributos"):
        st.markdown("""MDVP:Fo(Hz) - Frecuencia fundamental vocal media 
MDVP:Fhi(Hz) - Frecuencia fundamental vocal máxima
MDVP:Flo(Hz) - Frecuencia fundamental vocal mínima\n
MDVP:Jitter(%),MDVP:Jitter(Abs),MDVP:RAP,MDVP:PPQ,Jitter:DDP - Varios
medidas de variación en la frecuencia fundamental\n
MDVP:Shimmer,MDVP:Shimmer(dB),Shimmer:APQ3,Shimmer:APQ5,MDVP:APQ,Shimmer:DDA - Varios medidas de variación en amplitud\n
NHR,HNR - Dos medidas de la relación entre el ruido y los componentes tonales en la voz\n
status - Estado de salud del sujeto (uno) - Parkinson, (cero) - saludable\n
RPDE,D2 - Dos medidas de complejidad dinámica no lineal\n
DFA - Exponente de escalado fractal de la señal\n
spread1,spread2,PPE - Tres medidas no lineales de variación de la frecuencia fundamental""")

    st.subheader("Seleccionar Valores:")

    # Tomar la entrada de características del usuario.
    col1, col2 = st.columns(2)
    with col1:
        avff = st.slider("Frecuencia fundamental vocal media", int(df["AVFF"].min()), int(df["AVFF"].max()))
        mavff = st.slider("Frecuencia fundamental vocal máxima", int(df["MAVFF"].min()), int(df["MAVFF"].max()))
    with col2:
        mivff = st.slider("Frecuencia fundamental vocal mínima", int(df["MIVFF"].min()), int(df["MIVFF"].max()))
        jitddp = st.slider("Jitter:DDP", float(df["Jitter:DDP"].min()), float(df["Jitter:DDP"].max()))

    col3, col4 = st.columns(2)
    with col3:
        mdvpjit = st.slider("Programa Multidimensional de Voz:Jitter(%)", float(df["MDVP:Jitter(%)"].min()), float(df["MDVP:Jitter(%)"].max()))
        mdvprap = st.slider("MDVP:RAP", float(df["MDVP:RAP"].min()), float(df["MDVP:RAP"].max()))
    with col4:
        mdvpapq = st.slider("MDVP:APQ", float(df["MDVP:APQ"].min()), float(df["MDVP:APQ"].max()))
        mdvpppq = st.slider("MDVP:PPQ", float(df["MDVP:PPQ"].min()), float(df["MDVP:PPQ"].max()))

    col5, col6 = st.columns(2)
    with col5:
        mdvpshim = st.slider("MDVP:Shimmer", float(df["MDVP:Shimmer"].min()), float(df["MDVP:Shimmer"].max()))
        shimdda = st.slider("Shimmer:DDA", float(df["Shimmer:DDA"].min()), float(df["Shimmer:DDA"].max()))
    with col6:
        shimapq3 = st.slider("Shimmer:APQ3", float(df["Shimmer:APQ3"].min()), float(df["Shimmer:APQ3"].max()))
        shimapq5 = st.slider("Shimmer:APQ5", float(df["Shimmer:APQ5"].min()), float(df["Shimmer:APQ5"].max()))

    col7, col8 = st.columns(2)
    with col7:
        nhr = st.slider("NHR", float(df["NHR"].min()), float(df["NHR"].max()))
        hnr = st.slider("HNR", float(df["HNR"].min()), float(df["HNR"].max()))
    with col8:
        rpde = st.slider("RPDE", float(df["RPDE"].min()), float(df["RPDE"].max()))
        dfa = st.slider("DFA", float(df["DFA"].min()), float(df["DFA"].max()))

    col9, col10 = st.columns(2)
    with col9:
        d2 = st.slider("D2", float(df["D2"].min()), float(df["D2"].max()))
    with col10:
        ppe = st.slider("PPE", float(df["PPE"].min()), float(df["PPE"].max()))


    # Crear una lista para almacenar todas las características
    features = [avff, mavff, mivff, jitddp, mdvpjit, mdvprap,mdvpapq,mdvpppq,mdvpshim,shimdda,shimapq3,shimapq5,nhr,hnr,rpde,dfa,d2,ppe]

    # Crear un botón para predecir
    if st.button("Predecir"):
        # Obtener la predicción y el puntaje del modelo
        prediction, score = predict(X, y, features)
        st.success("Predicción realizada con éxito")

        # Imprimir la salida según la predicción
        if (prediction == 1):
            st.warning("La persona tiene la enfermedad de Parkinson o está propensa a contraerla")
        else:
            st.info("La persona está a salvo de la enfermedad de Parkinson")

        # Imprimir el puntaje del modelo
        st.write("El modelo tiene una precisión del ", (score*100),"%")
