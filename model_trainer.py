import joblib
import time
import multiscript_config as msc
import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

#To avoid getting dataconverstion warnings
import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)

def getdata():
    global df
    df = pd.read_csv('training\svm_training_data.csv').fillna(0)
    df = df.drop(['tag', 'text', 'atext'],axis=1)
    cleandata(df)

def cleandata(df):
    global X, Xx, X_train,X_test, y_train, y_test, Y
    Y = []
    for val in df['content']:
        if(val == 'NC'):
            Y.append(0)
        else:
            Y.append(1)
    X = StandardScaler().fit_transform(df.drop(['content'],axis=1))
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.10)

def trainingModel():
    ker = msc.SVM_KERNEL
    class_weight = msc.SVM_CLASS_WEIGHTS
    gamma = msc.SVM_GAMMA
    #print("\n", class_weight, "\t", ker.upper(), "\t", ker.upper(), "\n")
    getdata()
    svclassifier = SVC(kernel=ker, gamma=gamma, class_weight = class_weight)
    svclassifier.fit(X_train, y_train)
    joblib.dump(svclassifier, "model_versions\svm_%s.pkl" % time.time()) 
    return svclassifier

# Run while testing for performance metrics
def stats(svclassifier):
    y_pred = svclassifier.predict(X_test)
    print(__name__)
    print("\n", confusion_matrix(y_test,y_pred), "\n")
    print(classification_report(y_test,y_pred))

if __name__ == '__main__':
    getdata()
    stats(trainingModel())