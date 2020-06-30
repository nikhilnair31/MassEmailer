import os.path
import glob
import importlib
import joblib
import redis
import pandas as pd
import numpy as np
from model_trainer import trainingModel
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

def modelTrain():
    print("Training......\n")
    return trainingModel()

def modelLoad():
    print("Loading......\n")
    latest_file = max(glob.glob('model_versions/*'), key=os.path.getctime)
    print("Latest file at : ", latest_file)
    return joblib.load(latest_file)

#Prints predicted main content
def predict(svm_classifier, scaled_df, text_list, meta_titles, meta_info):
    global predicted_content_type, main_content_text

    main_content_text = []
    predicted_content_type = svm_classifier.predict(scaled_df)
    if 'title' in meta_titles:
        main_content_text.append("\nTitles : "+meta_info[meta_titles.index('title')])
    if 'author' in meta_titles:
        main_content_text.append("\nAuthor : "+meta_info[meta_titles.index('author')])
    if 'domain' in meta_titles:
        main_content_text.append("\nDomain : "+meta_info[meta_titles.index('domain')])
    if 'og:url' in meta_titles:
        main_content_text.append("\nOG:URL : "+meta_info[meta_titles.index('og:url')])
    if 'avgreadtime' in meta_titles:
        main_content_text.append("\nAverage Read Time : "+ str(meta_info[meta_titles.index('avgreadtime')]) + " minutes")
    main_content_text.append("\n<------------------------------------------------------------------------------------->\n")
    for i in range(len(text_list)):
        if(predicted_content_type[i] == 1):
            main_content_text.append(text_list[i])

def main(url, scaled_df, text_list, meta_titles, meta_info):
    print("\nRetrieving text data......\n")

    if len(os.listdir('model_versions/') ) == 0:
        print("Retraining SVM classifier.\n")
        predict(modelTrain(), scaled_df, text_list, meta_titles, meta_info)
    else: 
        print("Using latest SVM classifier.\n")   
        predict(modelLoad(), scaled_df, text_list, meta_titles, meta_info)
        
    return main_content_text