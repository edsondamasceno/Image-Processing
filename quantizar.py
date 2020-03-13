#! /usr/bin/env python

'''
Quantização de imagem em 2D
'''

import numpy as np
import cv2
import glob as g
from sklearn.cluster import KMeans
import libtiff

def quantizar(classe, lista):
    ''''''

    for i in range(len(lista)):
        print('percorrendo a imagem ', lista[i])

        img = cv2.imread(lista[i], cv2.IMREAD_ANYDEPTH)

        ## Amostragem ##
        # Reduzindo a imagem #
        # Seleciona uma em cada 2 colunas, e de cada coluna uma a cada duas linhas
        n = 2
        img_red = img[::n,::n]

        # Os pixels da imagem atual serão duplicados no eixo x e y. Assim, a imagem volta a ter o tamanho 
        # original, mas a partir da imagem reduzida
        # Função: np.repeat(matriz, vezes, eixo). O eixo 0 é a altura e 1 a largura.
        m = 2
        img_aum = np.repeat(img_red, m, axis=0)
        img_aum = np.repeat(img_aum, m, axis=1)

        ## Quantização ##
        # 255 / 31 = 8,22...
        #Imagem com 8 tons de cinza. 
        #Descartar a parte decimal dos números e alterar o vetor para que possua apenas 8 valores.
        r = 31 # 
        img = np.uint16(img / r) * r
        

        if classe == 0:
            separator = '/Benign/'
            # Salvar imagem no disco #
            nome_img = lista[i].split(separator)[1]
            cv2.imwrite('/home/edson/Documentos/Mama-xgboost/CIAR_2018/Benign/' + nome_img, img)
        elif classe == 1:
            separator = '/Invasive/'
            # Salvar imagem no disco #
            nome_img = lista[i].split(separator)[1]
            cv2.imwrite('/home/edson/Documentos/Mama-xgboost/CIAR_2018/Invasive/' + nome_img, img)
        elif classe == 2:
            separator = '/InSitu/'
            # Salvar imagem no disco #
            nome_img = lista[i].split(separator)[1]
            cv2.imwrite('/home/edson/Documentos/Mama-xgboost/CIAR_2018/InSitu/' + nome_img, img)
        else:
            separator = '/Normal/'
            # Salvar imagem no disco #
            nome_img = lista[i].split(separator)[1]
            cv2.imwrite('/home/edson/Documentos/Mama-xgboost/CIAR_2018/Normal/' + nome_img, img)



# tratar a imagem
def getImagens():
    
    path_benign = '/home/edson/Documentos/Image-Mama/CIAR_2018/Benign/'
    path_invasive = '/home/edson/Documentos/Image-Mama/CIAR_2018/Invasive/'
    path_insitu = '/home/edson/Documentos/Image-Mama/CIAR_2018/InSitu/'
    path_normal = '/home/edson/Documentos/Image-Mama/CIAR_2018/Normal/'

    extensao = '*.tif'

    lista_benign = g.glob(path_benign + extensao)
    lista_invasive = g.glob(path_invasive + extensao)
    lista_insitu = g.glob(path_insitu + extensao)
    lista_normal = g.glob(path_normal + extensao)

    quantizar(classe=0, lista=lista_benign)
    quantizar(classe=1, lista=lista_invasive)
    quantizar(classe=2, lista=lista_insitu)
    quantizar(classe=3, lista=lista_normal)


if __name__ == '__main__':
    ''''''
    getImagens()
