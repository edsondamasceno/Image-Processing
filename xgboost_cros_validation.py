#only xgboost
import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.datasets import mnist
from keras.utils import np_utils
import xgboost
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC,LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix

def load_train_data():
    X_train = np.load('/home/edson/Documentos/Mama-xgboost/Tensor/x_teste4classe.npy')
    Y_train = np.load('/home/edson/Documentos/Mama-xgboost/Tensor/y_teste4classe.npy')
    return X_train, Y_train

(X_train, y_train) = load_train_data()

# data pre-processing
X_train = X_train.reshape(-1, 28*28) / 255.      # normalize
X_train.shape

# k-fold cross validation evaluation of xgboost model
model = xgboost.XGBClassifier(max_depth=7, learning_rate=0.1, n_estimators=1000, nthread=50)
#kfold = KFold(n_splits=10, random_state=7)
results = cross_val_score(model, X_train, y_train, cv=10)

print('\n')
print('Resultado Cros-Validation')
print("Accuracy: %.2f%% (%.3f%%)" % (results.mean()*100, results.std()))
print('\n')
print(results)



