# -*- coding: utf-8 -*-
"""obesity classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15ex8f9e0VCoBApNrnd4M_E3dWco7BT20
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df= pd.read_csv('/content/Obesity Classification.csv')

df.head()

df.info()

df.describe()

sns.heatmap(df.corr())

sns.countplot(df, x='Gender')

sns.histplot(df, x='Age', bins=20, kde= True, hue= 'Gender')
plt.title('Age Distibution')
plt.show()

sns.histplot(df, x='BMI', bins=20, kde= True, hue='Gender')
plt.title('BMI Distibution')
plt.show()

sns.histplot(df, x='Weight', bins=20, kde= True, hue='Gender')
plt.title('Weight Distibution')
plt.show()

sns.histplot(df, x='Height', bins=20, kde= True, hue='Gender')
plt.title('Height Distibution')
plt.show()

sns.scatterplot(df, x='Weight', y='Height', hue= 'Gender')

import plotly.express as px

fig=px.sunburst(df,path=['Gender','Label'],values=df.value_counts().values)
fig.show()

df2=df.drop('ID',axis=1)
df2=pd.get_dummies(df2)
df2.head()

corr=df2.corr()
mask=np.triu(np.ones_like(corr,dtype=bool))
sns.heatmap(corr,annot=True,mask=mask)
plt.show()

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

df3=df.copy()
df3['Gender'] = le.fit_transform(df3['Gender'])

sns.pairplot(data=df3.drop('ID',axis=1),hue='Label')
plt.show()

df4= df.copy()

bins=[0,20,40,60,80,100,200]
df4['Age_bins']=pd.cut(df['Age'],bins)
df4.head(3)

sns.scatterplot(x='Weight',y='BMI',hue='Age_bins',data=df4,s=100)
plt.title('Weight vs BMI among Age')
plt.show()

sns.lmplot(x='Weight',y='BMI',hue='Label',data=df4)
plt.title('Weight vs BMI among Label')
plt.show()

from sklearn.cluster import KMeans

df5=df.copy()
df5['Gender'] = le.fit_transform(df['Gender'])
df5['Label'] = le.fit_transform(df['Label'])

X=df5.drop('ID',axis=1)
y=df5['Label']

df.dtypes

# df['BMI']= np.int64(df['BMI'])

# df.dtypes

dist_list=[]
for i in range(1,20):
  kmeans=KMeans(n_clusters=i,init='random',random_state=101)
  kmeans.fit(X)
  dist_list.append(kmeans.inertia_)

plt.figure(figsize=(10,5))
plt.plot(range(1,20),dist_list,marker='+')
plt.xlabel('Number of clusters')
plt.ylabel('Distortion')
plt.show()

kmeans3=KMeans(n_clusters=3,random_state=101)

kmeans3.fit(X)

labels=kmeans3.labels_

correct_labels=sum(y==labels)
print('n_clusters=3: %d out of %d samples were correctly labeled.' % (correct_labels,y.size))
print('Accuracy score: {0:0.2f}'.format(correct_labels/float(y.size)))

kmeans4=KMeans(n_clusters=4,random_state=101)

kmeans4.fit(X)

labels=kmeans4.labels_

correct_labels=sum(y==labels)
print('n_clusters=4: %d out of %d samples were correctly labeled.' % (correct_labels,y.size))
print('Accuracy score: {0:0.2f}'.format(correct_labels/float(y.size)))

kmeans5=KMeans(n_clusters=5,random_state=101)

kmeans5.fit(X)

labels=kmeans5.labels_

correct_labels=sum(y==labels)
print('n_clusters=5: %d out of %d samples were correctly labeled.' % (correct_labels,y.size))
print('Accuracy score: {0:0.2f}'.format(correct_labels/float(y.size)))

labels=pd.Series(kmeans4.labels_,name='cluster_number')

df_with_cluster=pd.concat([df,labels],axis=1)
df_with_cluster.head(3)

df_with_cluster['cluster_number'].value_counts().plot(kind='bar')
plt.xlabel('Cluster number')
plt.ylabel('Count')
plt.show()

