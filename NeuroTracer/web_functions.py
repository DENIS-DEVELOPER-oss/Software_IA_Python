
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import streamlit as st

@st.cache_data()
def load_data():


    # Cargar el conjunto de datos de Parkinson en un DataFrame.
    df = pd.read_csv('data_modelo/Parkinson.csv')
    # Renombrar los nombres de las columnas en el DataFrame.
    df.rename(columns = {"MDVP:Fo(Hz)": "AVFF",}, inplace = True)
    df.rename(columns = {"MDVP:Fhi(Hz)": "MAVFF",}, inplace = True)
    df.rename(columns = {"MDVP:Flo(Hz)": "MIVFF",}, inplace = True)

    # Realizar la división de características y objetivo
    X = df[["AVFF", "MAVFF", "MIVFF","Jitter:DDP","MDVP:Jitter(%)","MDVP:RAP","MDVP:APQ","MDVP:PPQ","MDVP:Shimmer","Shimmer:DDA","Shimmer:APQ3","Shimmer:APQ5","NHR","HNR","RPDE","DFA","D2","PPE"]]
    y = df['status']

    return df, X, y

@st.cache_data()
def train_model(X, y):
    """Esta función entrena el modelo y devuelve el modelo y la puntuación del modelo"""
    # Crear el modelo
    model = DecisionTreeClassifier(
            ccp_alpha=0.0, class_weight=None, criterion='entropy',
            max_depth=4, max_features=None, max_leaf_nodes=None,
            min_impurity_decrease=0.0, min_samples_leaf=1, 
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            random_state=42, splitter='best'
        )
    # Ajustar los datos en el modelo
    model.fit(X, y)
    # Obtener la puntuación del modelo
    score = model.score(X, y)

    # Devolver los valores
    return model, score

def predict(X, y, features):
    # Obtener el modelo y la puntuación del modelo
    model, score = train_model(X, y)
    # Predecir el valor
    prediction = model.predict(np.array(features).reshape(1, -1))
    return prediction, score

