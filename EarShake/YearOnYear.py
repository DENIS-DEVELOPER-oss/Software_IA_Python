import streamlit as st
import plotly.express as px
import pandas as pd


from loader import GetDataFromAPI
loader_obj = GetDataFromAPI()



class YearOnYear:

    def __init__(self) -> None:
        pass

    def plot_yoy_bar(self, dataframe):
        temp_df = dataframe.groupby('Año')['mag'].count().reset_index()
        temp_df.rename(columns={'mag':'Cantidad'}, inplace=True)
        fig = px.bar(temp_df, x='Año', y='Cantidad', color='Cantidad')
        fig.update_layout(xaxis=dict(dtick='1 year'), xaxis_title='Año', yaxis_title='Cantidad', title='Terremotos por año - Gráfico de barras')
        st.plotly_chart(fig,use_container_width=True)
    
    def plot_yoy_line(self, dataframe):
        temp_df = dataframe.groupby('Año')['mag'].count().reset_index()
        temp_df.rename(columns={'mag':'Cantidad'}, inplace=True)
        fig = px.line(temp_df, x='Año', y='Cantidad', markers='o')
        fig.update_layout(xaxis=dict(dtick='1 year'), xaxis_title='Año', yaxis_title='Cantidadt',yaxis=dict(range=[1100,2500]),title='Terremotos por año - Gráfico de líneas')
        st.plotly_chart(fig,use_container_width=True)

    def plot_yoy_animated_graph(self, dataframe):
        dataframe = dataframe.sort_values(by='Año')
        fig = px.density_mapbox(dataframe, lat='Latitude', lon='Longitude', z='mag', radius=10,
                        center=dict(lat=0, lon=180), zoom=0.5,
                        mapbox_style= 'stamen-terrain',height=700 ,color_continuous_scale=px.colors.sequential.Plasma, animation_frame='Año', title='Gráfico animado')
        st.plotly_chart(fig,use_container_width=True)
    
    def plot_pie_total(self, dataframe):
        temp_df = dataframe.groupby('Año')['mag'].count().reset_index()
        temp_df.rename(columns={'mag':'Cantidad'}, inplace=True)
        fig = px.pie(temp_df, values='Cantidad', names='Año', title='Conteo de terremotos en los últimos 10 años - Gráfico circular', labels='Año')
        st.plotly_chart(fig)
    

    def plot_country_bar_chart(self, dataframe, choice):
        temp_df = dataframe[dataframe['ciudad/estado'] == choice].groupby('Año')['mag'].count().reset_index()
        temp_df.rename(columns={'mag':'Cantidad'}, inplace=True)
        fig = px.bar(temp_df, x='Año', y='Cantidad', color='Cantidad')
        fig.update_layout(xaxis=dict(dtick='1 year'), xaxis_title='Año', yaxis_title='Cantidad', title='Terremotos en {} por año - Gráfico de barras'.format(choice))
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_country_bar_chart_month(self, dataframe, choice):
        temp_df = dataframe[dataframe['ciudad/estado'] == choice].groupby(dataframe['Fecha'].dt.month_name())['mag'].count().sort_values(ascending=False).reset_index()
        temp_df.rename(columns={'mag':'Cantidad', 'Fecha':'Mes'}, inplace=True)
        fig = px.bar(temp_df, x='Mes', y='Cantidad', color='Cantidad')
        fig.update_layout(xaxis_title='Mes', yaxis_title='Cantidad', title='Terremotos en {} por mes - Gráfico de barras'.format(choice))
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_country_pie_chart_overall(self, dataframe, choice):
        temp_df = dataframe[dataframe['ciudad/estado'] == choice].groupby('Año')['mag'].count().reset_index()
        temp_df.rename(columns={'mag':'Cantidad'}, inplace=True)
        fig = px.pie(temp_df, values='Cantidad', names='Año', title='Todos los terremotos por año - Gráfico circular')
        st.plotly_chart(fig)

    def plot_country_pie_chart_month(self, dataframe, choice):
        temp_df = dataframe[dataframe['ciudad/estado'] == choice].groupby(dataframe['Fecha'].dt.month_name())['mag'].count().sort_values(ascending=False).reset_index()
        temp_df.rename(columns={'mag':'Cantidad', 'Fecha':'Mes'}, inplace=True)
        fig = px.pie(temp_df, values='Cantidad', names='Mes', title='Todos los terremotos por mes - Gráfico circular')
        st.plotly_chart(fig)


    
    
