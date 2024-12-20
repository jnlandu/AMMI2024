# -*- coding: utf-8 -*-
"""Copy of PCA_Practical_2024.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13d3gdWpzWGycPvyeFR2XZYiqOe2D01Ca

# PCA practical
"""

import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

"""### Background

Principal Component Analysis (PCA) is a simple dimensionality reduction technique that can capture linear correlations between the features. For a given (standardized) data, PCA can be calculated by eigenvalue decomposition of covariance (or correlation) matrix of the data, or Singular Value Decomposition (SVD) of the data matrix. The data standardization includes mean removal and variance normalization.

## **Datasets**

In this Tutorial, we use iris dataset. It consists of 50 samples from each of three species of Iris. The rows being the samples and the columns being: Sepal Length, Sepal Width, Petal Length and Petal Width.
"""

iris = load_iris()
X = iris['data']
y = iris['target']


n_samples, n_features = X.shape

print('Number of samples:', n_samples)
print('Number of features:', n_features)

df = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
    )
df["label"] = iris.target

df

df.info()

"""Let's plot our data and see how it's look like"""

column_names = iris.feature_names

plt.figure(figsize=(16,4))
plt.subplot(1, 3, 1)
plt.title(f"{column_names[0]} vs {column_names[1]}")
plt.scatter(X[:, 0], X[:, 1], c=y)
plt.subplot(1, 3, 2)
plt.title(f"{column_names[1]} vs {column_names[2]}")
plt.scatter(X[:, 1], X[:, 3], c=y)
plt.subplot(1, 3, 3)
plt.title(f"{column_names[2]} vs {column_names[3]}")
plt.scatter(X[:, 2], X[:, 3], c=y)
plt.show()

# Compute the correlation matrix
corr_matrix = df.corr()

# Plot the correlation matrix using a heatmap
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')

# Display the plot
plt.show()

"""##Correlation between variables using correlation matrix:
From the correlation matrix above we observe that there is a reasonable
correlation among the variables and thus principal component analysis will be deployed to extract
features which form the potential classifiers of the flower species.

### 1.   **Data standardization by using this following formula**

 Compute the mean as follows for each variables as
\begin{align*}
\text{Mean} &= \bar{X} = \frac{1}{n}\sum_{i=1}^{n} X_i \
\end{align*}
\begin{align*}
\text{Variance} &= \sigma^2 = \frac{1}{n-1}\sum_{i=1}^{n}(X_i - \bar{X})^2
\end{align*}
Where $X_{i}$ represent the $i^{th}$ variable in the data set.
 To standardize a variable X using its mean ($\bar{X}$) and standard deviation ($\sigma$):

\begin{align*}
\text{Standardized }X &= \frac{X - \bar{X}}{\sigma}
\end{align*}

In this code, $\bar{X}$ represents the sample mean of the variable X, $\sigma$ represents the sample standard deviation of X, and X represents the original unstandardized variable. The resulting standardized variable has a mean of 0 and a standard deviation of 1.
"""



def mean(X): # np.mean(X, axis = 0)

  # Your code here
  mean =  np.sum(X, axis = 0)/X.shape[0]    #np.mean(X, axis = 0)

  return mean
def std(X): # np.std(X, axis = 0)

  # Your code here
  std = np.sqrt(np.sum((X-mean(X))**2, axis = 0)/(X.shape[0]-1))

  return std

def Standardize_data(X):

  # Your code here
  X_std = (X - mean(X))/std(X)

  return X_std

X_std = Standardize_data(X)

assert (np.round(mean(X_std)) == np.array([0., 0., 0., 0.])).all(), "Your mean computation is incorrect"
assert (np.round(std(X_std)) == np.array([1., 1., 1., 1.])).all(), "Your std computation is incorrect"

"""### 2.   compute the covariance matrix

Determine the covariance matrix of the data set

$\text{Cov}(X_i,X_j) = \frac{1}{n-1}\sum_{k=1}^{n}(X_{i}^{k}-\bar{X}i)(X_{j}^{k}-\bar{X}_j)$
\begin{equation*}
\mathbf{S} = \frac{1}{n-1}\mathbf{X}^\top\mathbf{X},
\end{equation*}

where $\mathbf{X}$ is the $n \times p$ matrix of standardized data, and $\mathbf{S}$ is the $p \times p$ sample covariance matrix. The $(i,j)$th entry of $\mathbf{S}$ is given by

\begin{equation*}
s_{i,j} = \frac{1}{n-1}\sum_{k=1}^{n} x_{k,i}x_{k,j},
\end{equation*}

where $x_{k,i}$ and $x_{k,j}$ are the $i$th and $j$th standardized variables, respectively, for the $k$th observation.


It is important to note that the covariance matrix is a square, postive definate ,symmetric matric of dimension p by p where p is the number of variables
"""

def covariance(X):

  ## Your code here
  cov = (X.T@X)/(X.shape[0]-1)

  return cov

Cov_mat = covariance(X_std)
Cov_mat

"""### 3.   Compute the eigenvalue and eigenvector of our covariance matrix
Compute eigen values and standardised eigen vectors of the covariance matrix
Let $A$ be the covariance matrix of a dataset $X$, then the eigenvalue equation is given by:

\begin{equation*}
A\mathbf{v} = \lambda \mathbf{v}
\end{equation*}

where $\mathbf{v}$ is the eigenvector of $A$ and $\lambda$ is the corresponding eigenvalue.

To find the eigenvalues and eigenvectors, we can solve this equation using the characteristic polynomial of $A$:

\begin{equation*}
\det(A - \lambda I) = 0
\end{equation*}

where $I$ is the identity matrix of the same size as $A$. Solving for $\lambda$ gives the eigenvalues, and substituting each eigenvalue back into the equation $A\mathbf{v} = \lambda \mathbf{v}$ gives the corresponding eigenvectors.

"""

from numpy.linalg import eig

# Your code here
eigen_values, eigen_vectors = np.linalg.eig(Cov_mat)   # return eigen values and eigen vectors

print(eigen_values)
print(" ---------   ")
print(eigen_vectors)

"""*   rank the eigenvalues and their associated eigenvectors in decreasing order"""

print(eigen_values)
idx = np.array([np.abs(i) for i in eigen_values]).argsort()[::-1]
print(idx)

print(" --------------------------------------------------- ")

eigen_values_sorted = eigen_values[idx]
eigen_vectors_sorted = eigen_vectors.T[:,idx]

print(eigen_vectors_sorted)

"""
######   Choose the number component that will the number of dimensions of the new feature subspace  

*   To be able to visualize our data on the new subspace we will choose 2  
*   Retain at least 95% percent from the cumulayive explained variance

"""

explained_variance = [(i / sum(eigen_values))*100 for i in eigen_values_sorted]
explained_variance = np.round(explained_variance, 2)
cum_explained_variance = np.cumsum(explained_variance)

print('Explained variance: {}'.format(explained_variance))
print('Cumulative explained variance: {}'.format(cum_explained_variance))

plt.plot(np.arange(1,X.shape[1]+1), cum_explained_variance, '-o')
plt.xticks(np.arange(1,X.shape[1]+1))
plt.xlabel('Number of components')
plt.ylabel('Cumulative explained variance');
plt.grid()
plt.show()

"""#### Project our data onto the subspace"""

# Get our projection matrix
c = 2
P = eigen_vectors_sorted[:c, :] # Projection matrix


X_proj = X_std.dot(P.T)
X_proj.shape

plt.title(f"PC1 vs PC2")
plt.scatter(X_proj[:, 0], X_proj[:, 1], c=y)
plt.xlabel('PC1'); plt.xticks([])
plt.ylabel('PC2'); plt.yticks([])
plt.show()



"""## Using sklearn"""

from sklearn.decomposition import PCA

#define PCA model to use
pca = PCA(n_components=4)

#fit PCA model to data
pca.fit(X_std)

explained_variance = pca.explained_variance_
print(f"Explained_variance: {explained_variance}")
explained_variance_ratio_percent = pca.explained_variance_ratio_ * 100
print(f"Explained_variance_ratio: {explained_variance_ratio_percent}")
cum_explained_variance = np.cumsum(explained_variance_ratio_percent)

plt.plot(np.arange(1,X_std.shape[1]+1), cum_explained_variance, '-o')
plt.xticks(np.arange(1,X_std.shape[1]+1))
plt.xlabel('Number of components')
plt.ylabel('Cumulative explained variance');
plt.grid()
plt.show()

"""*  Kaiser'rule witch keep all the components with eigenvalues greater than 1."""

## Transform data
X_proj = pca.transform(X_std)
X_proj[:10]

plt.title(f"PC1 vs PC2")
plt.scatter(X_proj[:, 0], X_proj[:, 1], c=y)
plt.xlabel('PC1'); plt.xticks([])
plt.ylabel('PC2'); plt.yticks([])
plt.show()





"""Build your own pca class using function we did in this tutorial. Your class should have at least the following methods:


*   def fit(X)
*   def transform(X)

"""



class myPCA:
  def __init__(self,n_components=None):

    self.n_components = n_components
    self.std_data = True
    self.explained_variance = None
    self.cum_explained_variance = None
    self.mean = None
    self.std = None
    self.eigvalues = None
    self.eigvectors = None
    self.cov_matrix = None
    self.projected_X = None
    self.projected_matrix = None
    self.standardized_data = None



  def fit(self, X, y=None):

    """
    Return the object itsself

    y : ignored; X: the array-like

    """
    self.__fit(X)
    return self

  def transform(self):
    #eigen_values, eigen_vectors = np.linalg.eig(self.cov_matrix(self.std(X)))
    """

    """
    #self.projected_X = self.standardized_data.dot(self.projected_matrix.T)

    return self.projected_X

  #@_fit_context(prefer_skip_nested_validation=True)
  def __fit(self, X, y=None):

    ## Center the data:
    self.mean = np.sum(X, axis = 0)/X.shape[0]

    ## Compute the std
    self.std =  (np.sum((X-self.mean)**2, axis = 0)/(X.shape[0]-1))**.5

    ## Standardize the data:
    self.standardized_data = (X-self.mean)/self.std

    ## Covariance matrix:
    self.cov_matrix = (1/(self.standardized_data.shape[0]-1))*(self.standardized_data.T @ self.standardized_data)
    ## Compute eigenvalues

    self.eigvalues, self.eigvectors = np.linalg.eig(self.cov_matrix)
    #return self.eigvalues, self.eigvectors


    ## Projection matrix:

    self.projected_matrix = self.eigvectors[:self.n_components, :]

    ## Projected data
    self.projected_X =  X.dot(self.projected_matrix.T)  #Do not use X

    ## Explained variance and cummulated explained variance ratio:
    self.explained_variance = [ (i / sum(self.eigvalues))*100 for i in self.eigvalues]
    self.cum_explained_variance = np.cumsum(self.explained_variance)
    self.explained_variance = np.round(explained_variance, 2)


  def plot(self,y):

    ## Plot the projected data:
    return self.__plot(y)

  def kaiser(self):
    ## Print the Kaiser's rule:
    plt.plot(np.arange(1,self.standardized_data.shape[1]+1), self.cum_explained_variance, '-o')
    plt.xticks(np.arange(1,self.standardized_data.shape[1]+1))
    plt.xlabel('Number of components')
    plt.ylabel('Cumulative explained variance');
    plt.grid()
    plt.show()


  def __plot(self,y):
    plt.title(f"PC1 vs PC2")
    plt.scatter(self.projected_X[:,0], self.projected_X[:, 1], c=y)
    plt.xlabel('PC1'); plt.xticks([])
    plt.ylabel('PC2'); plt.yticks([])
    plt.show()

my_pca = myPCA(n_components=2)
my_pca.fit(X)
my_pca.plot(y)

my_pca.kaiser()

### get tyhe explained variance:
print('Explained variance: {}'.format(my_pca.explained_variance))

## get the cum. explained variance
print('Cumulative explained variance: {}'.format(my_pca.cum_explained_variance))

print('Covariance matrix: \n',my_pca.cov_matrix)

my_pca.transform().shape