
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import streamlit as st


@st.cache_data()
def load_data():
    df = pd.read_csv('data_modelo/Stress.csv')

    df.rename(columns = {"t": "bt",}, inplace = True)
    
    
    X = df[["sr","rr","bt","lm","bo","rem","sh","hr"]]
    y = df['sl']

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
    return model, score

def predict(X, y, features):
    # Obtener el modelo y la puntuación del modelo
    model, score = train_model(X, y)
    # Predecir el valor
    prediction = model.predict(np.array(features).reshape(1, -1))

    return prediction, score
