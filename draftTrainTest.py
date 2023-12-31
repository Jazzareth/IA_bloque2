# -*- coding: utf-8 -*-
"""script 4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jntaR37LCJHWJlmRCX-13GTo1KqqvjbR
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Carga los datos desde un archivo CSV
data = pd.read_csv('dummies_data.csv')

# Separar las características (X) y las etiquetas (y)
X = data.drop('etiqueta', axis=1)  # etiqueta se modifica a las columnas que tenemos
y = data['etiqueta']

# Número de particiones (k) para k-fold cross-validation
k = 5

# Crear un objeto KFold
kf = KFold(n_splits=k, shuffle=True, random_state=42)

# Inicializa una lista para almacenar las puntuaciones de rendimiento
scores = []

# Iterar sobre las particiones
for train_index, test_index in kf.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    # Aquí se entrena el modelo en X_train e y_train

    # evaluar el modelo en X_test

    # Aquí se modifica cuándo elegimos el modelo que usaremos
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Calcular accuracy
    accuracy = accuracy_score(y_test, y_pred)
    scores.append(accuracy)

# Imprimir las puntuaciones
for i, score in enumerate(scores):
    print(f'Fold {i+1}: Accuracy = {score:.2f}')

# Calcula el promedio de las puntuaciones
average_score = np.mean(scores)
print(f'Promedio de Accuracy: {average_score:.2f}')
