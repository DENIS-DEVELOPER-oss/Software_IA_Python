import pandas as pd
import datetime as dt
import requests
import numpy as np
from pandas import json_normalize
import datetime
import streamlit as st
from datetime import date

from loader import GetDataFromAPI
loader_obj = GetDataFromAPI()
from calculate import Calculate
calc_obj =  Calculate()
from plotter import Plot
plotter_obj = Plot()

today = dt.date.today()
week_ago = today - dt.timedelta(days=7)
yesterday = today - dt.timedelta(days=1)
first_day_month = today.replace(day=1)
year = date(date.today().year, 1, 1)



st.sidebar.image('imagenes/logo.png', use_column_width=True)

option = st.sidebar.radio('Select', ['Descripcion','VerTerremoto'])

if option == 'VerTerremoto':
    st.sidebar.markdown('*Visualización de terremotos en un mapa interactivo*')
    st.header('VerTerremoto')
    st.markdown('---')

    city_date_option = st.sidebar.selectbox('Visualizar activado', ['Fecha', 'ciudad/estado'])
    if city_date_option == 'Fecha':
        date_option = st.sidebar.selectbox('Elija Fechas', ['Hoy', 'Esta semana', 'Este mes', 'Este año', 'Intervalo de fechas personalizado'])

        if date_option == 'Hoy':
            response = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={}&endtime={}&minmagnitude=5'.format(yesterday, today))
            final = loader_obj.load_clean_data(response)
            calc_obj.get_statistics(final)
            st.subheader('Mapa interactivo')
            map_option = st.selectbox('Elegir estilo de mapa', ['Terreno', 'Claro', 'Oscuro'])
            if map_option == 'Terreno':
                plotter_obj.plot_iteractive_map(final, map_option)
            if map_option == 'Claro':
                plotter_obj.plot_iteractive_map(final, map_option)
            if map_option == 'Oscuro':
                plotter_obj.plot_iteractive_map(final, map_option)
            st.markdown('---')
            histogram_option = st.selectbox('Elegir estilo de histograma', ['Normal', 'Apilado'])
            if histogram_option == 'Normal':
                plotter_obj.plot_histogram(final, histogram_option)
            if histogram_option == 'Apilado':
                plotter_obj.plot_histogram(final, histogram_option)

        if date_option == 'Esta semana':
            response = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={}&endtime={}&minmagnitude=5'.format(week_ago, today))
            final = loader_obj.load_clean_data(response)
            calc_obj.get_statistics(final)
            mag_slider = st.slider('Filtrar por magnitud', min_value= float(final['mag'].min()), max_value=float(final['mag'].max()))
            final = final[final['mag'] > mag_slider]
            st.subheader('Mapa interactivo')
            map_option = st.selectbox('Elegir estilo de mapa', ['Terreno', 'Claro', 'Oscuro'])
            if map_option == 'Terreno':
                plotter_obj.plot_iteractive_map(final, map_option)
            if map_option == 'Claro':
                plotter_obj.plot_iteractive_map(final, map_option)
            if map_option == 'Oscuro':
                plotter_obj.plot_iteractive_map(final, map_option)
            st.markdown('---')
            histogram_option = st.selectbox('Elegir estilo de histograma', ['Normal', 'Apilado'])
            if histogram_option == 'Normal':
                plotter_obj.plot_histogram(final, histogram_option)
            if histogram_option == 'Apilado':
                plotter_obj.plot_histogram(final, histogram_option)
        

        if date_option == 'Este mes':
            try:
                response = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={}&endtime={}&minmagnitude=5'.format(first_day_month, today))
                final = loader_obj.load_clean_data(response)
                calc_obj.get_statistics(final)
                mag_slider = st.slider('Filtrar por magnitud', min_value= float(final['mag'].min()), max_value= float(final['mag'].max()))
                final = final[final['mag'] > mag_slider]
            except:
                st.warning('Seleccione la opción \'Hoy\' ya que es el primer día del mes.')
            st.subheader('Mapa interactivo')
            map_option = st.selectbox('Elegir estilo de mapa', ['Terreno', 'Claro', 'Oscuro'])
            if map_option == 'Terreno':
                plotter_obj.plot_iteractive_map(final, map_option)
            if map_option == 'Claro':
                plotter_obj.plot_iteractive_map(final, map_option)
            if map_option == 'Oscuro':
                plotter_obj.plot_iteractive_map(final, map_option)
            st.markdown('---')
            histogram_option = st.selectbox('Elegir estilo de histograma', ['Normal', 'Apilado'])
            if histogram_option == 'Normal':
                plotter_obj.plot_histogram(final, histogram_option)
            if histogram_option == 'Apilado':
                plotter_obj.plot_histogram(final, histogram_option)


        if date_option == 'Este año':
            response = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={}&endtime={}&minmagnitude=5'.format(year, today))
            final = loader_obj.load_clean_data(response)
            calc_obj.get_statistics(final)
            mag_slider = st.slider('Filtrar por magnitud', min_value= float(final['mag'].min()), max_value= float(final['mag'].max()))
            final = final[final['mag'] > mag_slider]
            st.subheader('Mapa interactivo')
            map_option = st.selectbox('Elegir estilo de mapa', ['Terreno', 'Claro', 'Oscuro'])
            if map_option == 'Terreno':
                plotter_obj.plot_iteractive_map(final, map_option)
            if map_option == 'Claro':
                plotter_obj.plot_iteractive_map(final, map_option)
            if map_option == 'Oscuro':
                plotter_obj.plot_iteractive_map(final, map_option)
            st.markdown('---')
            histogram_option = st.selectbox('Elegir estilo de histograma', ['Normal', 'Apilado'])
            if histogram_option == 'Normal':
                plotter_obj.plot_histogram(final, histogram_option)
            if histogram_option == 'Apilado':
                plotter_obj.plot_histogram(final, histogram_option)


        if date_option == 'Intervalo de fechas personalizado':
            st.sidebar.markdown("<p style='color: orange;'>Note: Si selecciona una amplia gama de fechas que abarcan varios años, es posible que no se muestren los datos.</p>", unsafe_allow_html=True)
            start_date = st.date_input('Elija la fecha de inicio', max_value=today)
            end_date = st.date_input('Elija la fecha de finalización', min_value=start_date, max_value=today)
            if end_date <= start_date:
                st.warning('Elija una fecha de finalización posterior a la fecha de inicio.')
 
            try: 
                response = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={}&endtime={}&minmagnitude=5'.format(start_date, end_date))
                final = loader_obj.load_clean_data(response)
                calc_obj.get_statistics(final)
                mag_slider = st.slider('Filtrar por magnitud', min_value= float(final['mag'].min()), max_value= float(final['mag'].max()))
                final = final[final['mag'] > mag_slider]
                st.subheader('Mapa interactivo')
                map_option = st.selectbox('Elegir estilo de mapa', ['Terreno', 'Claro', 'Oscuro'])
                if map_option == 'Terreno':
                    plotter_obj.plot_iteractive_map(final, map_option)
                if map_option == 'Claro':
                    plotter_obj.plot_iteractive_map(final, map_option)
                if map_option == 'Oscuro':
                    plotter_obj.plot_iteractive_map(final, map_option)
                st.markdown('---')
                histogram_option = st.selectbox('Elegir estilo de histograma', ['Normal', 'Apilado'])
                if histogram_option == 'Normal':
                    plotter_obj.plot_histogram(final, histogram_option)
                if histogram_option == 'Apilado':
                    plotter_obj.plot_histogram(final, histogram_option)
            except:
                st.error('Los datos para el intervalo de fechas seleccionado no están disponibles.')
    


    if city_date_option == 'ciudad/estado':
        response = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=1-1-2015&endtime={}&minmagnitude=5'.format(today))
        final = loader_obj.load_clean_data(response)
        chosen_country = st.sidebar.selectbox('Choose the City/Country', sorted(list(final['ciudad/estado'].dropna().unique())))
        plotter_obj.plot_country(final, chosen_country)
            
if option == 'Descripcion':
    st.image('imagenes/planeta.png', width=700)
    st.title('Exploración Interactiva de Terremotos')

    st.markdown("<h2 style='color: #FFDB58;'>Descripcion EarShake:</h2>", unsafe_allow_html=True)

    st.write("Bienvenido a EarShake, una emocionante aplicación de visualización de terremotos de manera interactiva. Con EarShake, podrás explorar y descubrir datos fascinantes sobre terremotos de todo el mundo, y sumergirte en la ciencia detrás de estos impactantes fenómenos naturales.")
    st.markdown('---')
    st.markdown("<h2 style='color: #FFDB58;'>FUNCIONES:</h2>", unsafe_allow_html=True)

    st.markdown("<h3 style='color: #00BFFF;'>VerTerremoto: Descubre terremotos en un mapa interactivo</h3>", unsafe_allow_html=True)
    st.write("En esta seccion  puedes explorar terremotos ocurridos en diferentes intervalos de tiempo, desde el día actual hasta eventos sísmicos históricos. Visualiza la ubicación exacta de cada terremoto en un mapa interactivo y obtén detalles clave sobre su magnitud y localización.")

    st.subheader('Visualización por Ciudad/Estado')
    st.write("Si deseas obtener información específica sobre terremotos en una ubicación concreta, la opción de Visualización por Ciudad/Estado te permitirá seleccionar una ciudad o estado para ver los terremotos que han ocurrido en esa región.")

    st.subheader('Estilos de Visualización Personalizados')
    st.markdown(
    """
    <p style='text-align: justify;'>EarShake ofrece una variedad de estilos de visualización, como el mapa de terreno, luces o tonos oscuros, para que puedas personalizar tu experiencia y adaptarla a tus preferencias.</p>
    """,
    unsafe_allow_html=True
    )

    st.subheader('Filtrado por Magnitud')
    st.markdown(
    """
    <p style='text-align: justify;'>Ajusta el filtro de magnitud para enfocarte en terremotos de interés específico y analizar cómo varía la distribución de la actividad sísmica.</p>
    """,
    unsafe_allow_html=True
)

    st.markdown('---')

