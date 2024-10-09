
import streamlit as st

def app():
    st.image("imagenes/logo.png", use_column_width=True)
    st.markdown("<h2 style='text-align: center;'>Enfermedad de Parkinson</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
    """<p style="font-size:20px; text-align: justify">
            La enfermedad de Parkinson es un trastorno progresivo que afecta al sistema nervioso y a las partes del cuerpo controladas por los nervios. Los síntomas comienzan lentamente. El primer síntoma puede ser un temblor apenas perceptible en una sola mano. Los temblores son comunes, pero el trastorno también puede causar rigidez o lentitud de movimiento.
            </p>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## Random Forest - Prediccion de Parkinson")
    st.markdown(
    """<p style="font-size:20px; text-align: justify">
            Esta aplicación web te ayudará a predecir si una persona tiene riesgo de ser paciente de la enfermedad de Parkinson o tiene la enfermedad en un nivel menor o agudo. Esta aplicación ayuda a predecir las causas de dichos escenarios patológicos en el futuro analizando los valores de varias características utilizando el Clasificador de Bosques Aleatorios.
        </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='text-align: center; color: blue;'>Sintomas de Parkinson</h3>", unsafe_allow_html=True)
        st.image("imagenes/parkinson.png", width=300)

    with col2:
        st.markdown("<h3 style='text-align: center; color: blue;'>Random - Forest</h3>", unsafe_allow_html=True)
        st.image("imagenes/randon_forest.png", width=400)
