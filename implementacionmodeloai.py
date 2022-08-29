# -*- coding: utf-8 -*-
"""ImplementacionModeloAI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cPQakNX0_sgt99vzORA03boKxgKpH8gl
"""

# Importamos las librerias
import pandas as pd
import numpy as np
from math import sqrt
from collections import Counter

# Ponemos los nombres de las columnas e importamos los datos
columns = ["Classification", "Alcohol","Malic acid","Ash","Alcalinity of ash", "Magnesium", "Total phenols", "Flavanoids", "Nonflavanoid phenols"
 	,"Proanthocyanins", "Color intensity", "Hue", "OD280/OD315 of diluted wines", "Proline"]

df_wine =  pd.read_csv('/content/drive/Shareddrives/IA Bloque 1/wine.data', names = columns)

df_wine.head()

# Dividimos en variables predictoras y variable a predecir 
from sklearn.model_selection import train_test_split

X = df_wine[[ "Alcohol","Malic acid","Ash","Alcalinity of ash", "Magnesium", "Total phenols", "Flavanoids", "Nonflavanoid phenols"
 	,"Proanthocyanins", "Color intensity", "Hue", "OD280/OD315 of diluted wines", "Proline"]]

y = df_wine["Classification"]

# Obtenemos solamente los valores en arreglos

X = X[:].values
y = y[:].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# Funcion para medir la distancia
def euclidean_distance(x1, x2):
  return np.sqrt(np.sum((x1-x2)**2))

#Creamos la clase de K Vecinos mas cercanos o KNN por sus siglas en ingles
class KNN:

#Inicamos la clase con un valor predeterminado de 3 vecinos
  def __init__(self,k = 3):
    self.k = k

#Utilizando el formato de sklear lo dividimos en fit y predict para entrenar el modelo 
#Entrenamos el modelo llamando a las variables de entrenamiento 

  def fit(self,X,y):
    self.X_train = X
    self.y_train = y
    
# Nos arroja las predicciones  
  def predict(self, X):
    predicted_labels = [self._predict(x) for x in X]
    return np.array(predicted_labels)

# Esta funcion la utilizamos para hacer el trabajo computacional de la prediccion y solo nos arroje los valores
  def _predict(self,x):
    #Con la funcion de distancia, en una lista la almacenamos
    distances = [euclidean_distance(x, x_train) for x_train in self.X_train]
    #Obtenemos el indice de las distancias ordenadas con el numero de vecinos
    k_id = np.argsort(distances)[:self.k]
    #Obtenemos una lista ya organizada, ya con los indices 
    k_n_l = [self.y_train[i] for i in k_id]
    #Obtenemos los indices mas recurrentes
    fam = Counter(k_n_l).most_common(1)
    return fam[0][0]

clf = KNN(k = 3)
clf.fit(X_train, y_train)
prediction = clf.predict(X_test)
print('Predecido')
print(prediction)
print('Valores reales')
print(y_test)
print('Precision')
acc = np.sum(prediction == y_test)/ len(y_test)
print(round(acc * 100,2), '%')

# Aprendizaje 
alpha = 0.0001

#Funciones para la regresion 
h   = lambda x,theta: theta[0]+theta[1]*x
j_i = lambda x,y,theta: (y-h(x,theta))**2 
n = len(y_train)

#Orden 1

theta = [108,34] 

#Definir el numero de iteraciones
for idx in range(100):
  acumDelta = []
  acumDeltaX = []
  for x_i, y_i in zip(X_train,y_train):
    acumDelta.append(h(x_i,theta)-y_i)
    acumDeltaX.append((h(x_i,theta)-y_i)*x_i)

  sJt0 = sum(acumDelta)  
  sJt1 = sum(acumDeltaX)
  theta[0] = theta[0]-alpha/n*sJt0
  theta[1] = theta[1]-alpha/n*sJt1

# Valores obtenidos de theta para la vzlidacion 
print(theta)

#Tamano del entrenamiento 
n_train = len(y_train)

#Tamano de la prueba
n_validate = len(y_test)

# Validación
acumDelta = []
for x_i, y_i in zip(X_test,y_test):
  acumDelta.append(j_i(x_i,y_i,theta))  

sDelta = sum(acumDelta)  
J_validate = 1/(2*n_validate)*sDelta


# Entrenamiento 
acumDelta = []
for x_i, y_i in zip(X_train,y_train):
  acumDelta.append(j_i(x_i,y_i,theta))  

sDelta = sum(acumDelta)  
J_train = 1/(2*n_train)*sDelta


print('Validacion')
print(J_validate)
print()

print('Entrenamiento')
print(J_train)
print()

print('Theta')
print(theta)