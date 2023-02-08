import numpy as np
import argparse
import cv2
import os
import pandas as pd
import shutil
import errno
from matplotlib import pyplot as plt
import csv
import seaborn as sns

from warnings import simplefilter
simplefilter(action='ignore', category=Warning)

import time
from subprocess import check_output

from matplotlib.pyplot import *
from sklearn.metrics import confusion_matrix
from scipy import stats
import scipy.stats as st
from math import *
from sklearn import preprocessing
from warnings import simplefilter
from sklearn import neighbors, metrics, model_selection
from sklearn import tree
from sklearn import ensemble
from sklearn import linear_model
from sklearn import svm
from sklearn import neural_network
from sklearn import feature_selection
from sklearn.decomposition import PCA
from pandas.plotting import parallel_coordinates
from sklearn.tree import export_graphviz
from matplotlib.colors import ListedColormap
from PIL import *
from sklearn.cluster import KMeans
import xgboost
import shap
import eli5
from eli5.sklearn import PermutationImportance
from sklearn.inspection import permutation_importance
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_classification
from sklearn.feature_selection import RFE
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.metrics import precision_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import plot_precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.model_selection import validation_curve
import colorsys  
import timeit




# Funciones para obtencion de Variables

def min_entre_max(imagen):
    histograma = cv2.calcHist([imagen], [0], None, [256], [0,256])[1:] #Calculo el Histograma de la Imagen
    xMax = np.argmax(histograma) #Guardo en xMax la intensidad que más aparece en la imagen
    xMax2 = 0
    xMax3 = 0
    aux = np.zeros(shape = histograma.shape)
    for x in range(len(histograma)):  #Recorremos los 255 valores
        aux[x] = histograma[x]*np.absolute(x - xMax)  #Aplicamos la fórmula
    xMax2 = np.argmax(aux)   #La intensidad que maximiza la fórmula anterior
    xMin = np.argmin(histograma[np.minimum(xMax2, xMax):np.maximum(xMax2, xMax)])  #Guardo en xMin la posición que ocupa el menor comprendido
    umbral = xMin + np.minimum(xMax2, xMax)  #Se la sumo al minimo para que sea la verdadera intensidad
    dif = abs(xMax - xMax2)
    '''
    plt.hist(imagen.ravel(),256,[0,255])   #Pintamos el histograma
    plt.show()
    '''
    return xMax, xMax2, dif, int(histograma[xMax]), int(histograma[xMax2])


def ampliacion_histograma(imagen):
    imagen = np.float32(imagen)
    min = np.min(imagen)
    max = np.max(imagen)
    #print("Rango Dinámico: [",min,",",max,"]")
    
    imagen = 255*(imagen - min) / (max - min)
    imagen = np.uint8(imagen)
    
    min = np.min(imagen)
    max = np.max(imagen)
    #print("Nuevo Rango Dinámico: [",min,",",max,"]")
    return imagen

def ecualizacion_histograma(imagen):
    imagen = np.float32(imagen)
    imagen2 = np.zeros(shape = imagen.shape)
    h, bins = np.histogram(imagen, bins = 256, range = [0,256])
    h = h / np.sum(h)
    hAcumulada = np.cumsum(h)
    imagen2 = hAcumulada[np.int16(imagen)]
    imagen = np.uint8(imagen2*255)
    return imagen  

def imagen_media(imagen, etiquetas, centros):
    imagen2 = np.zeros(imagen.shape)
    imagen2 = centros[etiquetas]
    return np.uint8(imagen2)

def imagen_media_color(imagen,etiquetas,centros):
    imagen2 = np.zeros(imagen.shape)
    imagen2 = centros[etiquetas]
    return np.uint8(imagen2)

def calcula_pixeles(imagen):
    filas,columnas,colores = imagen.shape
    rojo = 0
    blanco = 0
    morado = 0
    color = [[0,0,255],[255,255,255],[150,20,75]]
    distancia = [0,0,0]
    for i in range(filas):
        for j in range(columnas):
            for k in range(3):
                distancia[k] = np.sqrt(np.power(imagen[i,j][0] - color[k][0], 2) + np.power(imagen[i,j][1] - color[k][1], 2) + np.power(imagen[i,j][2] - color[k][2], 2))
            
            similitud = np.argmin(distancia)
            
            if similitud == 0:
                rojo += 1
            elif similitud == 1:
                blanco += 1
            elif similitud == 2:
                morado += 1
    print(rojo, blanco, morado)
    return rojo, blanco, morado

def pixeles_porcentajes_RGB(imagen):
    im = Image.open('Imagenes_Resultados/Imagenes_Color_Conversions/Imagenes K-Means/K = 3 V3/' + imagen)
    blanco = 0
    rojo = 0
    morado = 0
    demas = 0
    for pixel in im.getdata():

        if pixel[1]  > 200:  # [255,255,255]
            blanco += 1
        elif pixel[0] < 130: # [75,20,150]
            morado += 1
        else:                # [255,0,0]
            rojo += 1

    porcentaje_blanco = (100*blanco)/(blanco + rojo + morado)
    porcentaje_rojo = (100*rojo)/(blanco + rojo + morado)
    porcentaje_morado = (100*morado)/(blanco + rojo + morado)
    
    return blanco, rojo, morado, np.round(porcentaje_blanco,3), np.round(porcentaje_rojo,3), np.round(porcentaje_morado,3)


# Funciones para creacion de Imagenes

def kMeans_3_V3_RangoAmpliado():
    for image in range(len(DATASET1_ID_NAME)):
        NAME = DATASET1_ID_NAME[image]
        print(NAME)
        # Imagen con Histograma Ampliado [0,255]
        img_normal = cv2.imread('Dataset de Prueba/ALL_Images/' + DATASET1_ID_NAME[image] + '_1.jpg')
        nueva_imagen = ampliacion_histograma(img_normal)
        '''
        # La pasamos de BGR a HSV en el rango de colores
        hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

        # Aplicamos una mascara para mostrar solamente los colores dentro del rango que queramos
        mask = cv2.inRange(hsv, (60, 60, 0), (150, 255, 255))
        mask = cv2.blur(mask, (3, 3)) 

        # Guardamos una segunda mascara con booleanos
        imask = mask <= 0

        # Creamos una matriz para almacenar los pixeles seleccionados
        nueva_imagen = np.zeros_like(imagen, np.uint8)
        
        # Creamos una matriz para almacenar los pixeles seleccionados
        mascara = np.zeros_like(imagen, np.uint8)

        # Difuminamos la imagen para reducir el ruido
        imagen = cv2.blur(imagen, (3, 3))
        
        # Asignamos a nuestra nueva imagen los pixeles seleccionados
        nueva_imagen[imask] = imagen[imask]
        '''
        filas,columnas,colores = nueva_imagen.shape
        
        for i in range(filas):
            for j in range(columnas):
                if nueva_imagen[i,j][0] == 0 & nueva_imagen[i,j][1] == 0 & nueva_imagen[i,j][2] == 0:
                    nueva_imagen[i,j][0] = 150
                    nueva_imagen[i,j][1] = 20
                    nueva_imagen[i,j][2] = 75
                    #mascara[i,j][0] = 150
                    #mascara[i,j][1] = 20
                    #mascara[i,j][2] = 75
                    
        # Difuminamos la imagen para reducir el ruido
        nueva_imagen = cv2.blur(nueva_imagen, (10, 10))
                    
        alg = KMeans(n_clusters=3, n_init = 10)
        alg.fit(nueva_imagen.reshape(nueva_imagen.shape[0]* nueva_imagen.shape[1], 3))
        centros = alg.cluster_centers_
        etiquetas = alg.labels_.reshape([filas,columnas])

        imagenfinal = imagen_media_color(nueva_imagen,etiquetas,centros)

        aux = np.zeros(shape = (4,3))
        count = 0
        array_colores = np.zeros(3)
        
        #for i in range(filas):
            #for j in range(columnas):
                #if mascara[i,j][0] == 150:
                    #imagenfinal[i,j][0] = 150
                    #imagenfinal[i,j][1] = 20
                    #imagenfinal[i,j][2] = 75
        
        
        for i in range(filas):
            for j in range(columnas):
                if (np.any(aux == imagenfinal[i,j])) == False:
                    aux[count] = imagenfinal[i,j] 
                    count += 1
        print(aux)
        
        # Es posible que haya cuatro colores, en ese caso, trataremos como globulos rojos a los dos intermedios
        colores_ordenados = np.argsort([int(np.sum(aux[0]))*-1, int(np.sum(aux[1]))*-1, int(np.sum(aux[2]))*-1, int(np.sum(aux[3]))*-1])
        
        # Si hay tres colores 
        if int(aux[3][0]) == 0 and int(aux[3][1]) == 0 and int(aux[3][2]) == 0:
            fondo = aux[colores_ordenados[0]]
            globulos_rojos = aux[colores_ordenados[1]]
        
        # Si hay cuatro colores
        else:
            fondo = aux[colores_ordenados[0]]
            globulos_rojos = aux[colores_ordenados[1]]
            globulos_rojos_2 = aux[colores_ordenados[2]]
        
        print(fondo,globulos_rojos)
        
        # Ponemos el mismo color de fondo
        for i in range(filas):
            for j in range(columnas):
                if int(imagenfinal[i,j][0]) == int(fondo[0]) and int(imagenfinal[i,j][1]) == int(fondo[1]) and int(imagenfinal[i,j][2]) == int(fondo[2]):
                    for c in range(3):
                        imagenfinal[i,j][c] = 255
                elif int(imagenfinal[i,j][0]) == int(globulos_rojos_2[0]) and int(imagenfinal[i,j][1]) == int(globulos_rojos_2[1]) and int(imagenfinal[i,j][2]) == int(globulos_rojos_2[2]):
                    imagenfinal[i,j][0] = 0
                    imagenfinal[i,j][1] = 0
                    imagenfinal[i,j][2] = 255
                elif int(imagenfinal[i,j][0]) == int(globulos_rojos[0]) and int(imagenfinal[i,j][1]) == int(globulos_rojos[1]) and int(imagenfinal[i,j][2]) == int(globulos_rojos[2]):
                    imagenfinal[i,j][0] = 0
                    imagenfinal[i,j][1] = 0
                    imagenfinal[i,j][2] = 255

        vis = np.concatenate((nueva_imagen, imagenfinal), axis=1)
        
        cv2.imwrite('Imagenes_Resultados/Comparacion de Imagenes/Dataset2 - Kmeans V3/'  + NAME + '_1_RangoAmpliado.jpg', vis)

def kMeans_3_V3():
    for image in range(0,len(DATASET1_ID_NAME)):
        NAME = DATASET1_ID_NAME[image]
        print(NAME)
        
        imagen = cv2.imread('Dataset de Prueba/ALL_Images/' + DATASET1_ID_NAME[image] + '_1.jpg')
        
        # La pasamos de BGR a HSV en el rango de colores
        #hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

        # Aplicamos una mascara para mostrar solamente los colores dentro del rango que queramos
        #mask = cv2.inRange(hsv, (60, 60, 0), (150, 255, 255))
        #mask = cv2.blur(mask, (3, 3)) 

        # Guardamos una segunda mascara con booleanos
        #imask = mask <= 0

        # Creamos una matriz para almacenar los pixeles seleccionados
        #nueva_imagen = np.zeros_like(imagen, np.uint8)
        
        # Creamos una matriz para almacenar los pixeles seleccionados
        #mascara = np.zeros_like(imagen, np.uint8)

        # Difuminamos la imagen para reducir el ruido
        #imagen = cv2.blur(imagen, (3, 3))

        # Asignamos a nuestra nueva imagen los pixeles seleccionados
        #nueva_imagen[imask] = imagen[imask]
        
        filas,columnas,colores = imagen.shape
        
        for i in range(filas):
            for j in range(columnas):
                if imagen[i,j][0] == 0 & imagen[i,j][1] == 0 & imagen[i,j][2] == 0:
                    imagen[i,j][0] = 150
                    imagen[i,j][1] = 20
                    imagen[i,j][2] = 75
                    mascara[i,j][0] = 150
                    mascara[i,j][1] = 20
                    mascara[i,j][2] = 75
                    
        # Difuminamos la imagen para reducir el ruido
        imagen = cv2.blur(imagen, (10, 10))
                    
        alg = KMeans(n_clusters=3, n_init = 10)
        alg.fit(imagen.reshape(imagen.shape[0]* imagen.shape[1], 3))
        centros = alg.cluster_centers_
        etiquetas = alg.labels_.reshape([filas,columnas])

        imagenfinal = imagen_media_color(imagen,etiquetas,centros)

        aux = np.zeros(shape = (4,3))
        count = 0
        array_colores = np.zeros(3)
        
        #for i in range(filas):
            #for j in range(columnas):
                #if mascara[i,j][0] == 150:
                    #imagenfinal[i,j][0] = 150
                    #imagenfinal[i,j][1] = 20
                    #imagenfinal[i,j][2] = 75
        
        
        for i in range(filas):
            for j in range(columnas):
                if (np.any(aux == imagenfinal[i,j])) == False:
                    aux[count] = imagenfinal[i,j] 
                    count += 1
        print(aux)
        
        # Es posible que haya cuatro colores, en ese caso, trataremos como globulos rojos a los dos intermedios
        colores_ordenados = np.argsort([int(np.sum(aux[0]))*-1, int(np.sum(aux[1]))*-1, int(np.sum(aux[2]))*-1, int(np.sum(aux[3]))*-1])
        
        # Si hay tres colores 
        if int(aux[3][0]) == 0 and int(aux[3][1]) == 0 and int(aux[3][2]) == 0:
            fondo = aux[colores_ordenados[0]]
            globulos_rojos = aux[colores_ordenados[1]]
        
        # Si hay cuatro colores
        else:
            fondo = aux[colores_ordenados[0]]
            globulos_rojos = aux[colores_ordenados[1]]
            globulos_rojos_2 = aux[colores_ordenados[2]]
        
        print(fondo,globulos_rojos)
        
        # Ponemos el mismo color de fondo
        for i in range(filas):
            for j in range(columnas):
                if int(imagenfinal[i,j][0]) == int(fondo[0]) and int(imagenfinal[i,j][1]) == int(fondo[1]) and int(imagenfinal[i,j][2]) == int(fondo[2]):
                    for c in range(3):
                        imagenfinal[i,j][c] = 255
                elif int(imagenfinal[i,j][0]) == int(globulos_rojos_2[0]) and int(imagenfinal[i,j][1]) == int(globulos_rojos_2[1]) and int(imagenfinal[i,j][2]) == int(globulos_rojos_2[2]):
                    imagenfinal[i,j][0] = 0
                    imagenfinal[i,j][1] = 0
                    imagenfinal[i,j][2] = 255
                elif int(imagenfinal[i,j][0]) == int(globulos_rojos[0]) and int(imagenfinal[i,j][1]) == int(globulos_rojos[1]) and int(imagenfinal[i,j][2]) == int(globulos_rojos[2]):
                    imagenfinal[i,j][0] = 0
                    imagenfinal[i,j][1] = 0
                    imagenfinal[i,j][2] = 255
        
        cv2.imwrite('Imagenes_Resultados/Imagenes_Color_Conversions/Imagenes K-Means/K = 3 V3 Dataset2/'  + NAME + '_1.jpg', imagenfinal)


