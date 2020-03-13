'''
Descritores de textura GLCM 
'''

import glob as g
import cv2
import libtiff

import numpy as np
from skimage.feature import greycomatrix, greycoprops
from skimage import io, color, img_as_ubyte


def normalize(valor):
    return int(valor) / 255 # 8 Bits
    #return int(valor) / 4095 # 12 Bits
    #return int(valor) / 65535 # 16 Bits


def getMinimum(image):
    ''''''
    menor = 255 # 8 Bits
    #menor = 4095 # 12 Bits
    #menor = 65535 # 16 Bits
    
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i][j] < menor:
                menor = image[i][j]
    return menor


def getMaximum(image):
    ''''''
    maior = 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i][j] > maior:
                maior = image[i][j]
    return maior


def geraSVMfile(rotulo, lista_feat, name_file, path_out, modo):
    ''''''
    arquivo = open(path_out + name_file, modo)
    featureFile = str(rotulo) + " "
    arquivo.write(featureFile)
    for i in range(len(lista_feat)):
        linha = str(str(i + 1) + ":" + str(lista_feat[i]) + " ")
        print('linha ', str(i + 1), " = ", linha)
        arquivo.write(linha)
    arquivo.write('\n')
    arquivo.close()

def run_imagens(classe, lista, modo):

    contrast = 0.0
    dissimilarity = 0.0
    homogeneity = 0.0
    energy = 0.0
    correlation = 0.0
    asm = 0.0

    for i in range(len(lista)):
        print('percorrendo a imagem ', lista[i])

        img = cv2.imread(lista[i], 0)

        gray = color.rgb2gray(img)
        image = img_as_ubyte(gray)

        bins = np.array([0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 255]) #16-bit
        inds = np.digitize(image, bins)

        max_value = inds.max()+1
        #matrix_coocurrence = greycomatrix(inds, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4], levels=max_value, 
        #    normed=False, symmetric=False)
        matrix_coocurrence = greycomatrix(inds, [1], [0], levels=max_value, 
            normed=False, symmetric=False)


        # GLCM properties
        contrast = greycoprops(matrix_coocurrence, 'contrast')
        dissimilarity = greycoprops(matrix_coocurrence, 'dissimilarity')
        homogeneity = greycoprops(matrix_coocurrence, 'homogeneity')
        energy = greycoprops(matrix_coocurrence, 'energy')
        correlation = greycoprops(matrix_coocurrence, 'correlation')
        asm = greycoprops(matrix_coocurrence, 'ASM')

        feat = []
        feat.append(contrast)
        feat.append(dissimilarity)
        feat.append(homogeneity)
        feat.append(energy)
        feat.append(correlation)
        feat.append(asm)

        print('imagem ' + str(i) + ' da classe ' + str(classe) + ' foi processada ')
        name = 'glcm_teste03.libsvm'
        path_file = '/home/edson/Documentos/Mama-GLCM/'

        for _indice in feat:
            print('processando  = ', _indice)
        geraSVMfile(rotulo=classe, lista_feat=feat, name_file=name, path_out=path_file, modo=modo)

# tratar a imagem
def getImagens():
    #path_benign = '/home/edson/Documentos/Image-Mama/CIAR_2018/Benign/'
    path_invasive = '/home/edson/Documentos/Image-Mama/CIAR_2018/Invasive/'
    path_insitu = '/home/edson/Documentos/Image-Mama/CIAR_2018/InSitu/'
    #path_normal = '/home/edson/Documentos/Image-Mama/CIAR_2018/Normal/'

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
