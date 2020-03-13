'''
Descritores de textura LBP
'''

import glob as g
import cv2
import libtiff

from skimage import feature
import numpy as np
from skimage import io, color, img_as_ubyte
from scipy.stats import itemfreq


def geraSVMfile(rotulo, lista_feat, name_file, path_out, modo):
    ''''''
    arquivo = open(path_out + name_file, modo)
    featureFile = str(rotulo)
    for i in range(len(lista_feat)):
        #linha = str(str(i + 1) + ":" + str(lista_feat[i]) + " ")
        linha = str(str(lista_feat[i]) + ",")
        print('linha ', str(i + 1), " = ", linha)
        arquivo.write(linha)
    arquivo.write(featureFile)
    arquivo.write('\n')
    arquivo.close()

def run_imagens(classe, lista, modo):

    lbp = 0.0
    hist = 0.0
    

    for i in range(len(lista)):
        print('percorrendo a imagem ', lista[i])

        img = cv2.imread(lista[i], 0)

        gray = color.rgb2gray(img)
        image = img_as_ubyte(gray)

        # Raio a ser considerado 
        radius = 1 #3
        # Número de pontos a serem considerados vizinhos
        numPoints = 8 #8 * radius

        lbp = feature.local_binary_pattern(img, numPoints, radius, method="uniform")

        # Calculate the histogram
        x = itemfreq(lbp.ravel())
        # Normalize the histogram
        hist = x[:, 1]/sum(x[:, 1])

        feat = []
        feat.append(hist)

        print('imagem ' + str(i) + ' da classe ' + str(classe) + ' foi processada ')
        name = 'lbp_teste03.csv'
        path_file = '/home/edson/Documentos/Mama-LBP/'

        for _indice in feat:
            print('processando  = ', _indice)
        geraSVMfile(rotulo=classe, lista_feat=feat, name_file=name, path_out=path_file, modo=modo)

# tratar a imagem
def getImagens():
    #path_benign = '/home/edson/Documentos/Mama-LBP/Quantizada/Benign/'
    path_invasive = '/home/edson/Documentos/Mama-LBP/Quantizada/Invasive/'
    path_insitu = '/home/edson/Documentos/Mama-LBP/Quantizada/InSitu/'
    #path_normal = '/home/edson/Documentos/Mama-LBP/Quantizada/Normal/'

    extensao = '*.tif'

    #lista_benign = g.glob(path_benign + extensao)
    lista_invasive = g.glob(path_invasive + extensao)
    lista_insitu = g.glob(path_insitu + extensao)
    #lista_normal = g.glob(path_normal + extensao)

    #run_imagens(classe=1, lista=lista_benign, modo='a')
    run_imagens(classe=0, lista=lista_invasive, modo='a')
    run_imagens(classe=1, lista=lista_insitu, modo='a')
    #run_imagens(classe=1, lista=lista_normal, modo='a')


if __name__ == '__main__':
    ''''''
    getImagens()
