
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.preprocessing import normalize

from util.util import plot_confusion_matrix, confusion_matrix
import numpy as np
from matplotlib import pyplot as plt

def get_data(path_data):
    """
    formata os dados do arquivo dos descritores
    para converter em uma lista de FEATURES e LABELS
    """

    FEATURES = [] # lista de caracteristicas
    LABELS = [] # lista de rotulos

    file_data = open(path_data, 'r')

    for i in file_data:
        lista = str(i).split(' ')
        F = []
        for j in range(len(lista)):
            if j == 0:
                LABELS.append(lista[j])
            else:
                if lista[j] != '\n':
                    value = lista[j].split(':')[1]
                    F.append(value)
        FEATURES.append(F)
    return LABELS, FEATURES


def classificar_com_SVM(X_train, X_test, y_train, y_test):

    print("SVM")

    c_svm = SVC(kernel='rbf', random_state=0, gamma=1, C=1) # SVM com kernel RBF
    #c_svm = SVC(kernel='poly', random_state=0, gamma=0.1, C=1) # SVM com kernel polinomial

    c_svm.fit(X_train, y_train) # treina o modelo

    y_pred =  c_svm.predict(X_test) # faz a predicao sobre os dados de teste

    # model accuracy for X_test
    accuracy = c_svm.score(X_test, y_test) 
    print('Accuracy = ', accuracy)

    # creating a confusion matrix 
    cm = confusion_matrix(y_test, y_pred) 
    print('Confusion matrix')
    print(cm)


def model(LABELS, FEATURES):

    #TRAIN = 0.2
    #TEST = 1 - TRAIN
    TEST = 0.2
    TRAIN = 1 - TEST

    # formata os dados de terino e teste
    X_train, X_test, y_train, y_test = train_test_split(FEATURES, LABELS, test_size=TEST)

    classificar_com_SVM(X_train, X_test, y_train, y_test) # classificador SVM


def classificar(path_arquivo_descritor):

    # obtem a lista de labels e caracteristicas
    L, F = get_data(path_arquivo_descritor)

    # normalizando os dados
    F = normalize(F, axis=0, norm='max')

    # cria o modelo, classifica e gera as matrizes de confusao
    model(L, F)


if __name__ == '__main__':
    """"""
    classificar('/home/edson/Documentos/Mama-SVM/Descritor/teste4classe.libsvm') # Teste 4 classe