import streamlit as st

class Calculate:

    def __init__(self) -> None:
            pass;

    def get_statistics(self, dataframe):
        # Obteniendo los datos estadísticos del DataFrame
        maximum = dataframe['mag'].max()
        most_prone_city = dataframe['ciudad/estado'].value_counts().head(1).index[0]
        least_prone_city = dataframe['ciudad/estado'].value_counts().tail(1).index[0]
        most_prone_place = dataframe['place'].value_counts().head(1).index[0]
        least_prone_place = dataframe['place'].value_counts().tail(1).index[0]

        # Presentando las estadísticas en la interfaz de usuario
        st.markdown("<h3 style='color: #FFDB58; text-align: center;'>ESTADISTICAS</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Máximo en la escala de Richter:', maximum)
        with col2:
            st.metric('País más propenso: ', most_prone_city)
        with col3:
            st.metric('País menos propenso:', least_prone_city)
        col4, col5 = st.columns(2)
        with col4:  
            st.metric('Lugar más propenso:', most_prone_place)
        with col5:
            st.metric('Lugar menos propenso:', least_prone_place)
        st.markdown('---')

