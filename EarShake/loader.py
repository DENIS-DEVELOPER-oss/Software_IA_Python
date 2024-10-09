import pandas as pd
from pandas import json_normalize

class GetDataFromAPI:

    def __init__(self) -> None:
        pass
        
    def convert_unix_datetime(self, series):
        # Convierte las fechas en formato Unix a formato datetime de pandas.
        return pd.to_datetime(series, unit='ms')
    
    def load_clean_data(self, data):
        # Extrae y limpia los datos del archivo JSON obtenidos de la API.
        properties = pd.DataFrame(data.json()['features'])['properties']
        geometry = pd.DataFrame(data.json()['features'])['geometry']
        json_normalized_properties = json_normalize(properties)
        json_normalized_geometry = json_normalize(geometry)
        json_normalized_properties = json_normalized_properties[['mag', 'place','time']]
        
        # Convierte la columna de tiempo de formato Unix a formato datetime de pandas y realiza transformaciones adicionales.
        json_normalized_properties['time'] = json_normalized_properties['time'].apply(self.convert_unix_datetime)
        json_normalized_properties['time'] = json_normalized_properties['time'].astype('str')
        json_normalized_properties['Time'] = json_normalized_properties['time'].str.split(' ').str.get(1)
        json_normalized_properties['Fecha'] = json_normalized_properties['time'].str.split(' ').str.get(0)
        json_normalized_properties.drop(columns='time', inplace=True)
        json_normalized_properties['Fecha'] = pd.to_datetime(json_normalized_properties['Fecha'])
        json_normalized_properties['Año'] = json_normalized_properties['Fecha'].dt.year
        
        # Realiza transformaciones en la geometría de los datos.
        json_normalized_geometry['Latitude'] = json_normalized_geometry['coordinates'].str.get(0)
        json_normalized_geometry['Longitude'] = json_normalized_geometry['coordinates'].str.get(1)
        json_normalized_geometry.drop(columns=['type','coordinates'], inplace=True)
        
        # Concatena los datos procesados de propiedades y geometría.
        final = pd.concat([json_normalized_properties, json_normalized_geometry], axis=1)
        final['ciudad/estado'] = final['place'].str.split(',').str.get(1)
        final['place'] = final['place'].str.split(',').str.get(0)
        final.rename(columns={'Latitude':'Longitude', 'Longitude':'Latitude'}, inplace=True)
        final['ciudad/estado'] = final['ciudad/estado'].str.strip()
        return final
