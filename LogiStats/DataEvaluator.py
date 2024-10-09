import streamlit as st
import numpy as np
import pandas as pd

class DataEvaluator:
    def __init__(self, df):
        self.df = df

    def show_head(self):
        # Displaying the header and the first lines of the dataframe
        st.write('El encabezado y las primeras líneas del conjunto de datos son:')
        st.dataframe(self.df.head(10))

    def show_dimensions(self):
        # Displaying the dataframe dimensions
        dimensions = 'Las dimensiones del conjunto de datos son ' + str(self.df.shape[0]) + ' filas y ' + str(
            self.df.shape[1]) + ' columnas.'
        st.write(dimensions)

    def show_columns(self):
        # Displaying column names
        columns_names = ', '.join(list(self.df.columns))
        st.write('las columnas son: ' + columns_names + '.')
