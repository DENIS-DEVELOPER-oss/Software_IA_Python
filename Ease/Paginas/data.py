import streamlit as st


def app(df):

    st.title("Información de Datos")
    st.markdown("""
         <div style='text-align: justify'>
        En esta sección de la aplicación, se proporciona una interfaz interactiva para que los usuarios exploren un conjunto de datos. Esta interfaz permite a los usuarios visualizar el conjunto de datos que se utilizo para poder realizar el clasificador, obtener un resumen estadístico, ver los nombres y tipos de datos de las columnas, y seleccionar y visualizar los datos de una columna específica. Todo se presenta en un formato de tres columnas para una navegación fácil e intuitiva.
        </div>
        """, unsafe_allow_html=True)
    st.subheader("Ver Datos")
    with st.expander("Ver datos"):
        st.dataframe(df)

    st.subheader("Descripción de las Columnas:")

    if st.checkbox("Ver Resumen"):
        st.dataframe(df.describe())

    # Crear múltiples casillas de verificación en fila
    col_nombre, col_tipo, col_data = st.columns(3)

    # Mostrar nombre de todas las columnas del dataframe
    with col_nombre:
        if st.checkbox("Nombres de las Columnas"):
            st.dataframe(df.columns)

    # Mostrar tipo de datos de todas las columnas 
    with col_tipo:
        if st.checkbox("Tipos de Datos de las Columnas"):
            tipos = df.dtypes.apply(lambda x: x.name)
            st.dataframe(tipos)
    
    # Mostrar datos para cada columna
    with col_data: 
        if st.checkbox("Datos de las Columnas"):
            col = st.selectbox("Nombre de la Columna", list(df.columns))
            st.dataframe(df[col])

