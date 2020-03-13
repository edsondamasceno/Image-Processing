#! /usr/bin/env python

'''
Quantização de imagem em 2D
'''

import numpy as np
import cv2
import glob as g
from sklearn.cluster import KMeans
import libtiff

def quantizar(classe, lista, bitsOriginal, BitsQuantizacao):
	''''''

	for i in range(len(lista)):
		print('percorrendo a imagem ', lista[i])

		img = cv2.imread(lista[i], cv2.IMREAD_ANYDEPTH)
		
		potencia = pow(2, (bitsOriginal - BitsQuantizacao))
		linha, coluna = img.shape

		for lin in range(linha):
			for col in range(coluna):
				img[lin, col] = int((img[lin, col]) / potencia)

		if classe == 0:
			separator = '/Benign/'
			# Salvar imagem no disco #
			nome_img = lista[i].split(separator)[1]
			cv2.imwrite('/home/edson/Documentos/MAMA/Quantizada_08/Benigno/' + nome_img, img)
		elif classe == 1:
			separator = '/Invasive/'
			# Salvar imagem no disco #
			nome_img = lista[i].split(separator)[1]
			cv2.imwrite('/home/edson/Documentos/MAMA/Quantizada_08/Invasivo/' + nome_img, img)
		elif classe == 2:
			separator = '/InSitu/'
			# Salvar imagem no disco #
			nome_img = lista[i].split(separator)[1]
			cv2.imwrite('/home/edson/Documentos/MAMA/Quantizada_08/InSitu/' + nome_img, img)
		else:
			separator = '/Normal/'
			# Salvar imagem no disco #
			nome_img = lista[i].split(separator)[1]
			cv2.imwrite('/home/edson/Documentos/MAMA/Quantizada_08/Normal/' + nome_img, img)



# tratar a imagem
def getImagens():
    
    path_benign = '/home/edson/Documentos/MAMA/CIAR_2018/Benign/'
    path_invasive = '/home/edson/Documentos/MAMA/CIAR_2018/Invasive/'
    path_insitu = '/home/edson/Documentos/MAMA/CIAR_2018/InSitu/'
    path_normal = '/home/edson/Documentos/MAMA/CIAR_2018/Normal/'

    extensao = '*.tif'

    lista_benign = g.glob(path_benign + extensao)
    lista_invasive = g.glob(path_invasive + extensao)
    lista_insitu = g.glob(path_insitu + extensao)
    lista_normal = g.glob(path_normal + extensao)

    quantizar(classe=0, lista=lista_benign, bitsOriginal=16, BitsQuantizacao=8)
    quantizar(classe=1, lista=lista_invasive, bitsOriginal=16, BitsQuantizacao=8)
    quantizar(classe=2, lista=lista_insitu, bitsOriginal=16, BitsQuantizacao=8)
    quantizar(classe=3, lista=lista_normal, bitsOriginal=16, BitsQuantizacao=8)


if __name__ == '__main__':
    ''''''
    getImagens()
