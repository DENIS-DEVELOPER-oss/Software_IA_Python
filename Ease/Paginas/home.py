import streamlit as st

def app():
    
    st.image("imagenes/logo.png", use_column_width=True)
    st.markdown(
        """<p style="font-size:20px; text-align: justify">
El estrés es una respuesta física y mental del cuerpo ante situaciones que percibe como desafiantes o amenazantes. Es una reacción natural y adaptativa que nos permite enfrentar situaciones difíciles y peligrosas. Cuando una persona se encuentra bajo estrés, el cuerpo libera hormonas como el cortisol y la adrenalina, lo que provoca cambios fisiológicos como aumento del ritmo cardíaco, la respiración y la presión arterial.
El estrés puede ser tanto positivo como negativo. El estrés positivo, conocido como estrés agudo, puede brindar motivación y energía para enfrentar desafíos y superar obstáculos.            </p>
        """, unsafe_allow_html=True)
    
    st.markdown("---")


    st.title("Nivel de Estrés - Arboles de Desicion")
    st.markdown(
    """<p style="font-size:20px; text-align: justify">
Esta aplicación web te ayudará a predecir si una persona está experimentando estrés. 
    Utiliza un Clasificador de Árboles de Decisión para analizar los valores de varias características 
    y determinar si una persona tiene un nivel bajo, medio, alto o muy alto de estrés. Tambien de ayudara a predecir los niveles de estrés futuros basados en las características proporcionadas. 
       </p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='text-align: center; color: red;'>Estrés</h3>", unsafe_allow_html=True)
        st.image("imagenes/estres.jpg", width=300)

    with col2:
        st.markdown("<h3 style='color: red;'>Arboles de Desición</h3>", unsafe_allow_html=True)
        st.image("imagenes/aboles_desicion.jpg", width=200)

