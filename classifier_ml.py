import pandas as pd
import pyprind
import os
import io
import numpy as np
import imp

###Step 1 : read everything into Pandas Dataframe
basepath = "./"
labels = {'gates':1 , 'other' :0}
pbar = pyprind.ProgBar(50000)
df = pd.DataFrame()

for s in ("test","train"):
    for l in ("gates","other"):
        path= os.path.join(basepath, s, l)
        for file in os.listdir(path):
            with io.open(os.path.join(path,file),'r',encoding='utf-8') as infile:
                txt = infile.read()
            df = df.append([[txt, labels[l]]], ignore_index=True)
            pbar.update()
df.columns = ['article' , 'author']
feature_set = df.loc[:,:].values


###Step 2: Data split 
from sklearn.model_selection import train_test_split
features_train, features_test, labels_train, labels_test = train_test_split (df['article'],df['author'] ,test_size=0.2, random_state=42)

### Step 3: tf-idf ( Term frequency - inversse document frequency) processing

from sklearn.feature_extraction.text import TfidfVectorizer as TFIV

get_stop_words= TFIV(  max_features=None, 
        strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
        use_idf=1,smooth_idf=1,sublinear_tf=1,
        stop_words = 'english')

my_stop_words = set(get_stop_words.get_stop_words())
my_stop_words.add("link")

tfv = TFIV(  max_features=None, 
        strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
        use_idf=1,smooth_idf=1,sublinear_tf=1,
        stop_words = my_stop_words)

my_stop_words = tfv.get_stop_words()
tfid_train=tfv.fit_transform(features_train)
tfid_test =tfv.transform(features_test)


from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn import svm

parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
svc = svm.SVC(gamma="scale")
clf = GridSearchCV (svc, parameters, cv=5)
clf.fit(tfid_train,labels_train)

#Step 4 : cross validation or other type of validation to check your accurarcy 
from sklearn.model_selection import cross_val_score
from sklearn import metrics
scores = cross_val_score(clf, tfid_test, labels_test, cv=5)
scoresF1 = cross_val_score ( clf, tfid_test, labels_test, cv = 5, scoring = 'f1_macro' )
print ("F1 scores: ",scoresF1)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
 

###Step 5 : test with predictions !!!!
df = pd.DataFrame()
path= os.path.join("test/final_predictions")
for file in os.listdir(path):
    with io.open(os.path.join(path,file),'r',encoding='utf-8') as infile:
        txt = infile.read()
    df = df.append([[txt, "to_predict",file ]], ignore_index=True)

df.columns = ['article' , 'author', 'filename']
test_article = tfv.transform(df['article'])

predictions= (clf.predict(test_article))
file_counter = 0


for pred in predictions:
    if pred == 1:
        print ("The File %15s" %df['filename'][file_counter],"was written by Bill Gates")
    elif pred ==0:
        print("The File %15s"  %df ['filename'][file_counter], "was written by someone else than Bill Gates")
    file_counter+=1
