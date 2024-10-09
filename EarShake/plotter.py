import streamlit as st
import plotly.express as px
import datetime as dt
import requests
import pandas as pd

from YearOnYear import YearOnYear
yoy_obj = YearOnYear()
from loader import GetDataFromAPI
loader_obj = GetDataFromAPI()

today = dt.date.today()

class Plot:

    def __init__(self) -> None:
        pass

    def plot_iteractive_map(self, dataframe, option):
        if option == 'Terreno':
            mapbox_style = 'stamen-terrain'
        if option == 'Claro':
            mapbox_style = 'carto-positron'
        if option == 'Oscuro':
            mapbox_style = 'carto-darkmatter'
        fig = px.density_mapbox(dataframe, lat='Latitude', lon='Longitude', z='mag', radius=10,
                        center=dict(lat=0, lon=180), zoom=0.5,
                        mapbox_style= mapbox_style,height=700 ,color_continuous_scale=px.colors.sequential.Plasma,
                        hover_name='place')
        st.plotly_chart(fig, use_container_width=True)
    

    def plot_histogram(self, dataframe, option):
        st.subheader('Histograma')
        # fig = px.bar(dataframe, x='city/state', y='mag', hover_name='city/state')
        if option == 'Normal':
            fig = px.histogram(dataframe, x='ciudad/estado')
            st.plotly_chart(fig, use_container_width=True)
        if option == 'Apilado':
            if dataframe['place'].value_counts().head(1).values[0] > 1:
                fig = px.histogram(dataframe, x='ciudad/estado',color='mag')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning('Muy pocos datos para un histograma apilado')
        st.markdown('---')

        st.subheader('Estadísticas año tras año')
        btn = st.button('Ver estadísticas año tras año')  
        # col1, col2 = st.colums(2)
        if btn:
            response1 = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-3-3&endtime=2023-1-1&minmagnitude=5')
            final1 = loader_obj.load_clean_data(response1)
            col1, col2 = st.columns(2)
            
            yoy_obj.plot_yoy_bar(final1)
            
            yoy_obj.plot_yoy_line(final1)

            yoy_obj.plot_yoy_animated_graph(final1)

            with col1:
                yoy_obj.plot_pie_total(final1)


    def plot_country(self, dataframe, choice):
        
        try:
            url = 'https://api.opencagedata.com/geocode/v1/geojson?q={}&key=028fc01b3e044c1693027b167e31b1b5&pretty=1'.format(choice)
            response = requests.get(url)
        except:
            st.warning('Los datos no pudieron ser cargados')
        lat = response.json()['features'][0]['geometry']['coordinates'][0]
        lon = response.json()['features'][0]['geometry']['coordinates'][1]
        curr_name = response.json()['features'][0]['properties']['annotations']['currency']['name']
        smallest_denomination =  response.json()['features'][0]['properties']['annotations']['currency']['smallest_denomination']
        drive = response.json()['features'][0]['properties']['annotations']['roadinfo']['drive_on']
        speed_in = response.json()['features'][0]['properties']['annotations']['roadinfo']['speed_in']
        timezone = response.json()['features'][0]['properties']['annotations']['timezone']['name']
        GMT_relative = response.json()['features'][0]['properties']['annotations']['timezone']['offset_string']

        new_df = pd.DataFrame({'Longitude': [lat], 'Latitude': [lon], 'Currency': [curr_name], 'Denominación más pequeña': [smallest_denomination],
                        'Driving Side': [drive], 'Speed Unit':[speed_in], 'Zona horaria':timezone, 'Relative to GMT':GMT_relative, 'Country':choice})
        
        st.subheader('Algunas estadísticas sobre {}'.format(choice))
        col1, col2 = st.columns(2)
        with col1:
            st.metric('Moneda ', curr_name)
            st.metric('Lado de conducción', drive)
            st.metric('Zona horaria',timezone )
        with col2:
            st.metric('Denominación más pequeña', smallest_denomination)
            st.metric('Velocidad medida en', speed_in)
            st.metric('Relativo a GMT', GMT_relative)

        custom_marker_symbol = "star-diamond"
        fig = px.scatter_geo(new_df, lat='Latitude', lon='Longitude', title='{} en el Mapa Mundial'.format(choice), height=550, hover_name='Country')   

        fig.update_traces(marker=dict(symbol=custom_marker_symbol,size=15))
        fig.update_layout(geo=dict(showcountries=True))

        longitude = float(new_df['Longitude'])
        latitude = float(new_df['Latitude'])
        fig.update_geos(
            visible=True, resolution=50, showcountries=True, countrycolor='gray',projection_type="mollweide", projection_scale=2, center=dict(lat = latitude, lon=longitude),
            scope="world")

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('---')

        yoy_obj.plot_country_bar_chart(dataframe, choice)

        yoy_obj.plot_country_bar_chart_month(dataframe, choice)

        yoy_obj.plot_country_pie_chart_overall(dataframe, choice)

        yoy_obj.plot_country_pie_chart_month(dataframe, choice)
