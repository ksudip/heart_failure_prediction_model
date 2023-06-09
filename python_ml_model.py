# -*- coding: utf-8 -*-
"""course_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PacM0d3pjcsQTlTwax7jkunMT211DqOB

**importing data set**
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
from numpy import mean
df=pd.read_csv('/content/drive/MyDrive/files for prml/heart.csv')
print(df)

"""**PREPROCESSING**"""

df=df.dropna(axis=0)
df['Sex']=pd.factorize(df.Sex)[0] #preprocessing and feature extraction pipelines to different subsets of features
df['ChestPainType']=pd.factorize(df.ChestPainType)[0] #numeric data is standard-scaled after mean-imputation, while the categorical data is one-hot encoded
df['RestingECG']=pd.factorize(df.RestingECG)[0]
df['ExerciseAngina']=pd.factorize(df.ExerciseAngina)[0]
df['ST_Slope']=pd.factorize(df.ST_Slope)[0]
print(df)

"""**data visualization**"""

df.describe().T.style.background_gradient(cmap = "Blues")

import seaborn as sns
import matplotlib.pyplot as plt
sns.distplot(df['HeartDisease']);

#kernel density estimation allows probability density estimation
def kde_plot(column, target) :
  if(column!=target): 
    fig, ax = plt.subplots(figsize = (10,7))
    sns.kdeplot(df[df[target]==1][column], alpha=0.5,shade = True, color="red", label="HeartDisease", ax = ax) 
    sns.kdeplot(df[df[target]==0][column], alpha=0.5,shade = True, color="#fccc79", label="NoHeartDisease ", ax = ax)
    plt.title('KDE-Plot of {}'.format(column), fontsize = 18)
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")
    ax.legend();
    plt.show()

columns=df.columns
for column in columns: 
    kde_plot(column, 'HeartDisease')

sns.jointplot(df['Cholesterol'],df['HeartDisease'],kind='kde')
sns.jointplot(df['RestingBP'],df['HeartDisease'],kind='kde')
sns.jointplot(df['FastingBS'],df['HeartDisease'],kind='kde')

data_set=df.copy()
#data_set.insert(0,'heart_disease',)
sns.pairplot(data_set, kind="reg", diag_kind="kde")

from sklearn.preprocessing import MinMaxScaler
X = df.iloc[:,:-1]
scaler= MinMaxScaler()
scaler.fit(X)
data=scaler.transform(X)
data=pd.DataFrame(data)
print(data)

"""**train test split**"""

from sklearn.model_selection  import train_test_split
Y = df['HeartDisease']
X_train, X_test, Y_train, Y_test = train_test_split(data, Y, test_size=0.3, random_state=0)
print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)

X_train=X_train.values
Y_train=Y_train.values
X_test=X_test.values
Y_test=Y_test.values

"""**MODEL SELECTION**"""

from sklearn.linear_model import LogisticRegression
clf = LogisticRegression(random_state=0,max_iter=500).fit(X_train, Y_train)
s=clf.score(X_test,Y_test)
print(s)

"""**bagging classifier**"""

from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
bclf=BaggingClassifier(base_estimator=DecisionTreeClassifier(),n_estimators=10, random_state=0)
bclf.fit(X_train,Y_train)
bclf.score(X_test,Y_test)

"""**svm**"""

from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
clf = svm.SVC(random_state=42)

k=[]  #making list of scores
for i in range(5,20):
  p=cross_val_score(clf, X_train, Y_train, cv=i, scoring='recall_macro')
  k.extend(p)
  print("i =",i,p,'\n')
plt.figure(figsize=(10, 7))
l = np.arange(0, len(k), 1)
plt.plot(l,k)
plt.xlabel("CROSS_VALIDATION")
plt.ylabel("SCORES")
plt.grid(True)
plt.show()

"""**ROC CURVES**"""

from sklearn.metrics import RocCurveDisplay
clf.fit(X_train, Y_train) #clf=svm.SVC(random_state=42)
ax = plt.gca() #patplotlib axes with roc curve(get the current axes)
svc_disp = RocCurveDisplay.from_estimator(clf, X_test, Y_test, ax=ax)

"""**GaussianProcessClassifier**"""

from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
kernel = 1.0 * RBF(1.0)
gpc = GaussianProcessClassifier(kernel=kernel,random_state=0).fit(X_train, Y_train)
gpc.score(X_test, Y_test)

"""**DecisionTreeClassifier**"""

dtc = DecisionTreeClassifier(random_state=0)# random state controls randomness of estimator
n=[]
for i in  range(10,20):
  s=cross_val_score(dtc, data, Y, cv=i) #X
  n.extend(s)
  print("i =", i, s,'\n')
  print('average score for i =',i,'is' ,mean(s),'\n')
#for cv=16 we are getting highest score= 0.9122807
plt.figure(figsize=(10, 7))
l = np.arange(0, len(n), 1)
plt.plot(l,n)
plt.grid(True)
plt.show()