'''
Descritores de textura ->
'''

import glob as g
import cv2
import libtiff
import numpy as np
from sklearn.cluster import KMeans


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
    featureFile = str(rotulo)
    for i in range(len(lista_feat)):
        #linha = str(str(i + 1) + ":" + str(lista_feat[i]) + " ")
        linha = str(str(lista_feat[i]) + ",")
        print('linha ', str(i + 1), " = ", linha)
        arquivo.write(linha)
    arquivo.write(featureFile)
    arquivo.write('\n')
    arquivo.close()

def saveImageName(name_file, path_out, image_name, modo):
    arquivo = open(path_out + name_file, modo)
    arquivo.write(image_name)
    arquivo.write('\n')
    arquivo.close()
    
def run_imagens(classe, lista, modo):
    ''''''

    prodind = 0.0
    dis = 0
    valorMPD = 0.0
    SPD = 0.0
    S1 = 0.0
    S2 = 0.0
    PD = 0.0
    soma1 = 0
    somatorio = 0
    MNND = 0.0
    q = 0.0

    for i in range(len(lista)):
        print('percorrendo a imagem ', lista[i])

        img = cv2.imread(lista[i], 0)
        #img = cv2.imread(lista[i], cv2.IMREAD_ANYDEPTH)

        min = getMinimum(image=img)
        max = getMaximum(image=img)

        sizeHistograma = 256 # 8 Bits
        #sizeHistograma = 4095 # 12 Bits
        #sizeHistograma = 65535 # 16 Bits

        hist = list(range(sizeHistograma))
        distance = list(range(sizeHistograma))

        background = min

        for b in range(img.shape[0]):
            for c in range(img.shape[1]):
                value = img[b][c]
                if int(value) > 0:
                    hist[value] += 1

        especie = 0

        for d in range(0, sizeHistograma):
            if int(hist[d]) > 0:
                especie += 1

        diagonal = 0.0
        foraDiagonal = 0.0

        for e in range(img.shape[0]):
            for f in range(img.shape[1]):
                if int(img[e][f]) != background:
                    if int(e) == int(f):
                        _valor = img[e][f] + min
                        diagonal += normalize(_valor)
                    else:
                        _valor = float(img[e][f] + min)
                        foraDiagonal += normalize(_valor)

        indices = []
        PSV = 0.0
        PSR = 0.0

        indices.append(float(((especie * diagonal) - foraDiagonal) / (especie * (especie - 1))))
        indices.append(float(especie * indices[0]))

        PSV = indices[0]
        PSR = indices[1]

        for x in range(0, sizeHistograma):
            for y in range(x + 1, sizeHistograma):
                if x == 0:
                    distance[x] = (y - x + 1)
                else:
                    distance[x] = (y - x + 2)

                prodind = (distance[x] * hist[x] * hist[y])
                somatorio += (hist[x] * hist[y])

                for q in range(x, y):
                    MNND = MNND + (distance[x] * hist[q])

        t = ((sizeHistograma - 1) / 2.0)
        total = sizeHistograma * t

        for x in range(0, sizeHistograma):
            for y in range(x + 1, sizeHistograma):
                if x == 0:
                    dis = (y - x) + 1
                else:
                    dis = (y - x) + 2

                prodind += (dis * hist[x] * hist[y])
                somatorio += (hist[x] * hist[y])

                for indice in range(x, (y + 1)):
                    soma1 += hist[indice]

                Ai = 0.0
                Ai = soma1 / ((y - x) + 1)
                S1 += (dis * Ai)
                S2 += Ai

            valorMPD += prodind

        PD = S1 / S2
        q = valorMPD / somatorio
        SPD = total * q

        feat = []
        feat.append(PSV)
        feat.append(PSR)
        feat.append(MNND)
        feat.append(PD)
        feat.append(SPD)

        print('imagem ' + str(i) + ' da classe ' + str(classe) + ' foi processada ')
        name = 'edson.csv'
        name_img = 'edson_imagens.csv'
        path_file = '/home/edson/Documentos/MAMA-CBIR/'

        for _indice in feat:
            print('processando  = ', _indice)
        geraSVMfile(rotulo=classe, lista_feat=feat, name_file=name, path_out=path_file, modo=modo)

        if classe == 0:
            separator = '/InSitu/'
            # Salvar imagem no disco #
            nome_img = lista[i].split(separator)[1]
            saveImageName(name_file=name_img, path_out=path_file, image_name=nome_img, modo=modo)
        elif classe == 1:
            separator = '/Invasive/'
            # Salvar imagem no disco #
            nome_img = lista[i].split(separator)[1]
            saveImageName(name_file=name_img, path_out=path_file, image_name=nome_img, modo=modo)
        elif classe == 2:
            separator = '/Benign/'
            # Salvar imagem no disco #
            nome_img = lista[i].split(separator)[1]
            saveImageName(name_file=name_img, path_out=path_file, image_name=nome_img, modo=modo)
        else:
            separator = '/Normal/'
            # Salvar imagem no disco #
            nome_img = lista[i].split(separator)[1]
            saveImageName(name_file=name_img, path_out=path_file, image_name=nome_img, modo=modo)



# tratar a imagem
def getImagens():

    #path = '/home/edson/Documentos/MAMA-CBIR/ICIAR2018_BACH/ICIAR2018_BACH_Challenge_TestDataset/Photos/'
    #extensao = '*.tif'
    #lista = g.glob(path + extensao)
    #run_imagens(classe=4, lista=lista, modo='a')

    #path_benign = '/home/edson/Documentos/Image-Mama/CIAR_2018/Benign/'
    path_invasive = '/home/edson/Documentos/Image-Mama/CIAR_2018/Invasive/'
    path_insitu = '/home/edson/Documentos/Image-Mama/CIAR_2018/InSitu/'
    #path_normal = '/home/edson/Documentos/Image-Mama/CIAR_2018/Normal/'

    extensao = '*.tif'

    #lista_benign = g.glob(path_benign + extensao)
    lista_invasive = g.glob(path_invasive + extensao)
    lista_insitu = g.glob(path_insitu + extensao)
    #lista_normal = g.glob(path_normal + extensao)

    #run_imagens(classe=0, lista=lista_benign, modo='a')
    run_imagens(classe=1, lista=lista_invasive, modo='a')
    run_imagens(classe=0, lista=lista_insitu, modo='a')
    #run_imagens(classe=3, lista=lista_normal, modo='a')


if __name__ == '__main__':
    ''''''
    getImagens()
