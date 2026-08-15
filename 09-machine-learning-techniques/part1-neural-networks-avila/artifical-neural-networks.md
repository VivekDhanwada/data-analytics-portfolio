# Artificial Neural Networks


```python
from IPython.display import Image
Image(filename='Image2.png',width = "600",height = "300")
```




    
![png](output_1_0.png)
    



1. Here, each node on the left represents an input feature, the connecting lines represent
the learned coefficients, and the node on the right represents the output, which is a
weighted sum of the inputs.

2. This model has a lot more coefficients (also called weights) to learn: there is one
between every input and every hidden unit (which make up the hidden layer), and
one between every unit in the hidden layer and the output.

3. Computing a series of weighted sums is mathematically the same as computing just
one weighted sum, so to make this model truly more powerful than a linear model,
we need one extra trick. After computing a weighted sum for each hidden unit, a
nonlinear function is applied to the result—usually the rectifying nonlinearity (also
known as rectified linear unit or relu) or the tangens hyperbolicus (tanh). The result of
this function is then used in the weighted sum that computes the output, ŷ. The two
functions are visualized in the following Figure. The relu cuts off values below zero, while tanh
saturates to –1 for low input values and +1 for high input values. Either nonlinear
function allows the neural network to learn much more complicated functions than a
linear model could:


```python
from IPython.display import Image
Image(filename='Image3.png',width = "400",height = "300")
```




    
![png](output_3_0.png)
    



For the small neural network pictured in the first figure, the full formula for computing ŷ in the case of regression would be (when using a tanh nonlinearity):   
h[0] = tanh(w[0, 0] * x[0] + w[1, 0] * x[1] + w[2, 0] * x[2] + w[3, 0] * x[3] + b[0])   
h[1] = tanh(w[0, 1] * x[0] + w[1, 1] * x[1] + w[2, 1] * x[2] + w[3, 1] * x[3] + b[1])   
h[2] = tanh(w[0, 2] * x[0] + w[1, 2] * x[1] + w[2, 2] * x[2] + w[3, 2] * x[3] + b[2])   
ŷ = v[0] * h[0] + v[1] * h[1] + v[2] * h[2] + b

Here, **w** are the weights between the input **x** and the hidden layer **h**, and **v** are the
weights between the hidden layer **h** and the output ŷ. The weights **v** and **w** are learned
from data, **x** are the input features, ŷ is the computed output, and **h** are intermediate
computations. An important parameter that needs to be set by the user is the number
of nodes in the hidden layer. This can be as small as 10 for very small or simple datasets
and as big as 10,000 for very complex data.

Having large neural networks made up of many of these layers of computation is
what inspired the term “deep learning.”

# Data used here

Here, we use the data **Avila** from UCI: https://archive.ics.uci.edu/ml/datasets/Avila#. The Avila data set has been extracted from 800 images of the 'Avila Bible', an XII century giant Latin copy of the Bible. The prediction task consists in associating each pattern to a copyist. In this lab, the‘avila-tr.txt'data is used. For your convenience, I have pre-processed an 'CSV' file in the Github.

### Data Set Information:

CLASS DISTRIBUTION (training set)

A: 4286

B: 5

C: 103

D: 352

E: 1095

F: 1961

G: 446

H: 519

I: 831

W: 44

X: 522

Y: 266

### Attribute Information:

F1: intercolumnar distance

F2: upper margin

F3: lower margin

F4: exploitation

F5: row number

F6: modular ratio

F7: interlinear spacing

F8: weight

F9: peak number

F10: modular ratio/ interlinear spacing

Class: A, B, C, D, E, F, G, H, I, W, X, Y

### Relevant Papers:

C. DeÂ Stefano, M. Maniaci, F. Fontanella, A. ScottoÂ diÂ Freca,
Reliable writer identification in medieval manuscripts through page layout features: The 'Avila' Bible case, Engineering Applications of Artificial Intelligence, Volume 72, 2018, pp. 99-110.

C. De Stefano, F. Fontanella, M. Maniaci and A. Scotto di Freca, 'A Method for Scribe Distinction in Medieval Manuscripts Using Page Layout Features', Lecture Notes in Computer Science, G. Maino and G. Foresti (eds.), Springer-Verlag, vol. 6978, pp. 393-402.

## Import modules


```python
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import ttest_ind

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score

from sklearn.neural_network import MLPClassifier

import warnings
warnings.filterwarnings("ignore")
```

## Load the data


```python
# Load the data and show the basic information
data=pd.read_csv("/content/sample_data/avila-tr.csv")
print('Data size: (%.f, %.f)\n' % data.shape)
data.head()
```

    Data size: (10430, 11)
    






  <div id="df-e5b9db0a-b874-4d18-8c9b-0ae06995dbf1" class="colab-df-container">
    <div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>F1</th>
      <th>F2</th>
      <th>F3</th>
      <th>F4</th>
      <th>F5</th>
      <th>F6</th>
      <th>F7</th>
      <th>F8</th>
      <th>F9</th>
      <th>F10</th>
      <th>Class</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.266074</td>
      <td>-0.165620</td>
      <td>0.320980</td>
      <td>0.483299</td>
      <td>0.172340</td>
      <td>0.273364</td>
      <td>0.371178</td>
      <td>0.929823</td>
      <td>0.251173</td>
      <td>0.159345</td>
      <td>A</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.130292</td>
      <td>0.870736</td>
      <td>-3.210528</td>
      <td>0.062493</td>
      <td>0.261718</td>
      <td>1.436060</td>
      <td>1.465940</td>
      <td>0.636203</td>
      <td>0.282354</td>
      <td>0.515587</td>
      <td>A</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-0.116585</td>
      <td>0.069915</td>
      <td>0.068476</td>
      <td>-0.783147</td>
      <td>0.261718</td>
      <td>0.439463</td>
      <td>-0.081827</td>
      <td>-0.888236</td>
      <td>-0.123005</td>
      <td>0.582939</td>
      <td>A</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.031541</td>
      <td>0.297600</td>
      <td>-3.210528</td>
      <td>-0.583590</td>
      <td>-0.721442</td>
      <td>-0.307984</td>
      <td>0.710932</td>
      <td>1.051693</td>
      <td>0.594169</td>
      <td>-0.533994</td>
      <td>A</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.229043</td>
      <td>0.807926</td>
      <td>-0.052442</td>
      <td>0.082634</td>
      <td>0.261718</td>
      <td>0.148790</td>
      <td>0.635431</td>
      <td>0.051062</td>
      <td>0.032902</td>
      <td>-0.086652</td>
      <td>F</td>
    </tr>
  </tbody>
</table>
</div>
    <div class="colab-df-buttons">

  <div class="colab-df-container">
    <button class="colab-df-convert" onclick="convertToInteractive('df-e5b9db0a-b874-4d18-8c9b-0ae06995dbf1')"
            title="Convert this dataframe to an interactive table."
            style="display:none;">

  <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960">
    <path d="M120-120v-720h720v720H120Zm60-500h600v-160H180v160Zm220 220h160v-160H400v160Zm0 220h160v-160H400v160ZM180-400h160v-160H180v160Zm440 0h160v-160H620v160ZM180-180h160v-160H180v160Zm440 0h160v-160H620v160Z"/>
  </svg>
    </button>

  <style>
    .colab-df-container {
      display:flex;
      gap: 12px;
    }

    .colab-df-convert {
      background-color: #E8F0FE;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      display: none;
      fill: #1967D2;
      height: 32px;
      padding: 0 0 0 0;
      width: 32px;
    }

    .colab-df-convert:hover {
      background-color: #E2EBFA;
      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);
      fill: #174EA6;
    }

    .colab-df-buttons div {
      margin-bottom: 4px;
    }

    [theme=dark] .colab-df-convert {
      background-color: #3B4455;
      fill: #D2E3FC;
    }

    [theme=dark] .colab-df-convert:hover {
      background-color: #434B5C;
      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);
      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));
      fill: #FFFFFF;
    }
  </style>

    <script>
      const buttonEl =
        document.querySelector('#df-e5b9db0a-b874-4d18-8c9b-0ae06995dbf1 button.colab-df-convert');
      buttonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';

      async function convertToInteractive(key) {
        const element = document.querySelector('#df-e5b9db0a-b874-4d18-8c9b-0ae06995dbf1');
        const dataTable =
          await google.colab.kernel.invokeFunction('convertToInteractive',
                                                    [key], {});
        if (!dataTable) return;

        const docLinkHtml = 'Like what you see? Visit the ' +
          '<a target="_blank" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'
          + ' to learn more about interactive tables.';
        element.innerHTML = '';
        dataTable['output_type'] = 'display_data';
        await google.colab.output.renderOutput(dataTable, element);
        const docLink = document.createElement('div');
        docLink.innerHTML = docLinkHtml;
        element.appendChild(docLink);
      }
    </script>
  </div>


<div id="df-b382cec5-b553-48a7-9fc1-1d2dd85cd30d">
  <button class="colab-df-quickchart" onclick="quickchart('df-b382cec5-b553-48a7-9fc1-1d2dd85cd30d')"
            title="Suggest charts."
            style="display:none;">

<svg xmlns="http://www.w3.org/2000/svg" height="24px"viewBox="0 0 24 24"
     width="24px">
    <g>
        <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>
    </g>
</svg>
  </button>

<style>
  .colab-df-quickchart {
      --bg-color: #E8F0FE;
      --fill-color: #1967D2;
      --hover-bg-color: #E2EBFA;
      --hover-fill-color: #174EA6;
      --disabled-fill-color: #AAA;
      --disabled-bg-color: #DDD;
  }

  [theme=dark] .colab-df-quickchart {
      --bg-color: #3B4455;
      --fill-color: #D2E3FC;
      --hover-bg-color: #434B5C;
      --hover-fill-color: #FFFFFF;
      --disabled-bg-color: #3B4455;
      --disabled-fill-color: #666;
  }

  .colab-df-quickchart {
    background-color: var(--bg-color);
    border: none;
    border-radius: 50%;
    cursor: pointer;
    display: none;
    fill: var(--fill-color);
    height: 32px;
    padding: 0;
    width: 32px;
  }

  .colab-df-quickchart:hover {
    background-color: var(--hover-bg-color);
    box-shadow: 0 1px 2px rgba(60, 64, 67, 0.3), 0 1px 3px 1px rgba(60, 64, 67, 0.15);
    fill: var(--button-hover-fill-color);
  }

  .colab-df-quickchart-complete:disabled,
  .colab-df-quickchart-complete:disabled:hover {
    background-color: var(--disabled-bg-color);
    fill: var(--disabled-fill-color);
    box-shadow: none;
  }

  .colab-df-spinner {
    border: 2px solid var(--fill-color);
    border-color: transparent;
    border-bottom-color: var(--fill-color);
    animation:
      spin 1s steps(1) infinite;
  }

  @keyframes spin {
    0% {
      border-color: transparent;
      border-bottom-color: var(--fill-color);
      border-left-color: var(--fill-color);
    }
    20% {
      border-color: transparent;
      border-left-color: var(--fill-color);
      border-top-color: var(--fill-color);
    }
    30% {
      border-color: transparent;
      border-left-color: var(--fill-color);
      border-top-color: var(--fill-color);
      border-right-color: var(--fill-color);
    }
    40% {
      border-color: transparent;
      border-right-color: var(--fill-color);
      border-top-color: var(--fill-color);
    }
    60% {
      border-color: transparent;
      border-right-color: var(--fill-color);
    }
    80% {
      border-color: transparent;
      border-right-color: var(--fill-color);
      border-bottom-color: var(--fill-color);
    }
    90% {
      border-color: transparent;
      border-bottom-color: var(--fill-color);
    }
  }
</style>

  <script>
    async function quickchart(key) {
      const quickchartButtonEl =
        document.querySelector('#' + key + ' button');
      quickchartButtonEl.disabled = true;  // To prevent multiple clicks.
      quickchartButtonEl.classList.add('colab-df-spinner');
      try {
        const charts = await google.colab.kernel.invokeFunction(
            'suggestCharts', [key], {});
      } catch (error) {
        console.error('Error during call to suggestCharts:', error);
      }
      quickchartButtonEl.classList.remove('colab-df-spinner');
      quickchartButtonEl.classList.add('colab-df-quickchart-complete');
    }
    (() => {
      let quickchartButtonEl =
        document.querySelector('#df-b382cec5-b553-48a7-9fc1-1d2dd85cd30d button');
      quickchartButtonEl.style.display =
        google.colab.kernel.accessAllowed ? 'block' : 'none';
    })();
  </script>
</div>
    </div>
  </div>




## Study the Multi-layer Perceptron model and its parameters
We will use the multi-layer percepton to understand the basic usage of artificial neural network models. Class [MLPClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html#sklearn.neural_network.MLPClassifier) implements a multi-layer perceptron (MLP) algorithm that trains using Backpropagation. MLPClassifier has many parameters to configure. The effects of some important parameters have been discussed in our lecture, e.g., activation functions, number of hidden layers, number of units in a hidden layer, gradient descent, regularization, etc. So, in this workshop we would like to empirically study these parameters.

### 1. Basic usage of the model


```python
# Specify features and the target
X = data.drop(['Class'], axis = 'columns')
y = data['Class']

# Split the dataset into training data and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=42)

# Training the MLPClassifier with the default parameters (random_state=42)
clf = MLPClassifier(random_state=42)
clf.fit(X_train, y_train)

# Output the accuracy on training data and test data respectively
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy: %.4f \n' % accuracy)
```

    Accuracy: 0.7584 
    



```python
# Explore the learned MLP model
print(clf)
print('\n# of layers (including the input layer): %.f\n' % clf.n_layers_)
print('MLP structure: %.f X %.f X %.f\n' % (X.shape[1], clf.get_params()['hidden_layer_sizes'][0], clf.n_outputs_))
```

    MLPClassifier(random_state=42)
    
    # of layers (including the input layer): 3
    
    MLP structure: 10 X 100 X 12
    


### 2. Use 10-fold cross validation to report a more robust testing performance


```python
# Use 10-fold cross validation to validate the model
clf = MLPClassifier(random_state=42)
scores_mlp_default = cross_val_score(clf, X, y, cv=10, verbose=1)
print('Accuracy range for Multi-layer Perceptron: [%.4f, %.4f]; mean: %.4f; std: %.4f\n'
      % (scores_mlp_default.min(), scores_mlp_default.max(), scores_mlp_default.mean(), scores_mlp_default.std()))
```

    Accuracy range for Multi-layer Perceptron: [0.7574, 0.7862]; mean: 0.7743; std: 0.0082
    


### 3. Increase the number of hidden units
Here, we draw a figure to report the testing accuray with differnt number of hidden units [10,20,30,40,50,60,70,80,90,100]. The parameter 'hidden_layer_sizes' accepts a list of numbers specifying the number of units in each hidden layer. We plot the relationship between the parameter and the accuracy score.


```python
# For each number of hidden units, we use 10-fold cross validation to report the testing accuracy.
# N.B.: The execution time is relatively long. This is to let you experience the intenstive computaiton required by artificial neural network models.
cv_scores = []
cv_scores_std = []
hidden_unit_numbers = [[10],[20],[30],[40],[50],[60],[70],[80],[90],[100]]
for i in hidden_unit_numbers:
    clf_mlp = MLPClassifier(hidden_layer_sizes=i, random_state=42)
    scores = cross_val_score(clf_mlp, X, y, scoring='accuracy', cv=10, verbose=1)
    cv_scores.append(scores.mean())
    cv_scores_std.append(scores.std())
```


```python
# Plot the relationship
plt.errorbar(hidden_unit_numbers, cv_scores, yerr=cv_scores_std, marker='x', label='Accuracy')
plt.xlabel('Size of hidden units')
plt.ylim(0.5, 0.9)
plt.ylabel('Accuracy')
plt.legend(loc='best')
plt.show()
```


    
![png](output_27_0.png)
    


**It can be seen that the accuracy increases when the number of units in the hidden layer increases. The reason is the a model with a bigger number of hiden layer units has a higher complexity to capture the information in data.**

### Task1. Number of hidder layers
Set the number of hidden layers as two, and each has 100 units. Please report the accuracy score and compare it with the single hidden layer case mentioend above. Note that the execution time for this task is relative long. To track the progress of the execution, you could set the verbose parameter in the cross_val_score method as 'verbose=1'.


```python
# Try a MLP model with two hidden layers

```


```python
from sklearn.neural_network import MLPClassifier
clf_mlp= MLPClassifier(hidden_layer_sizes=[100,100],random_state=45)
scores_mlp_2layers=cross_val_score(clf_mlp, X, y, scoring='accuracy', cv=10, verbose=1)
print('Accuracy range for MLP with two hidden layers :[%.4f,%.4f]; mean: %.4f; std: %.4f\n'
       %(scores_mlp_2layers.min(), scores_mlp_2layers.max(),scores_mlp_2layers.mean(), scores_mlp_2layers.std()))
t,p= ttest_ind(scores_mlp_default, scores_mlp_2layers)
print('t,p: %.4f, %.6f\n' %(t,p))
```

    Accuracy range for MLP with two hidden layers :[0.8754,0.9060]; mean: 0.8867; std: 0.0083
    
    t,p: -28.8818, 0.000000
    


### 4. Choose solver for the learning process
As discussed in our lecture, we can use gradient descent methods (standard gradient and stochastic gradient descent) to learn weights for the error minimization problem. Moreover, we can have other solvers for the optimization problem. Here, we draw a figure to report the accuray with differnt solvers. The parameter 'solver' can take values from ['lbfgs','sgd', 'adam']. 'sgd' represents stochastic gradient descent.


```python
# Try different solvers
cv_scores = []
cv_scores_std = []
solvers = ['lbfgs', 'sgd', 'adam']
for i in solvers:
    clf_mlp = MLPClassifier(solver=i, random_state=42)
    scores = cross_val_score(clf_mlp, X, y, scoring='accuracy', cv=10)
    cv_scores.append(scores.mean())
    cv_scores_std.append(scores.std())
```


```python
# Plot the relationship
plt.bar(solvers, cv_scores, yerr=cv_scores_std, label='Accuracy')
plt.xlabel('Solvers')
plt.ylim([0.5, 1])
plt.ylabel('Accuracy')
plt.legend(loc='best')
plt.show()
```


    
![png](output_34_0.png)
    


**It can be seen that sgd doesn't perform as well as the other two solvers**

### Task2. Activation functions
It can be seen above that the default activation function is 'ReLU'. As we discussed in our lecture, we could have different types of activation functions. Please try the possible functions 'identity’, ‘logistic’, ‘tanh’, and ‘relu’ provided by the API. Draw a figure to report the accuray with differnt activation functions.


```python
# Try different activation functions

```


```python
cv_scores= []
cv_scores_std=[]
functions= ['identity', 'logistic', 'tanh','relu']
for i in functions:
  clf_mlp= MLPClassifier(activation=i, random_state=42)
  scores= cross_val_score(clf_mlp,X,y, scoring='accuracy',cv=10)
  cv_scores.append(scores.mean())
  cv_scores_std.append(scores.std())
```


```python
#Plot the Relationship
plt.bar(functions,cv_scores,yerr=cv_scores_std,label='Accuracy')
plt.xlabel('Activation function')
plt.ylim([0.5,1])
plt.ylabel('Accuracy')
plt.legend(loc='best')
plt.show()
```


    
![png](output_39_0.png)
    


### 5. Use different values of alpha
The parameter alpha is the L2 penalty (regularization term) to overcome the overfitting issue. It balance the error caused the data and that by the model structure (number of weights).
Here, please draw a figure to report the accuray with differnt values of alpha [0.0001,0.001,0.01, 0.1,1].


```python
# Try different regulaization parameters
cv_scores = []
cv_scores_std = []
alphas = [0.0001,0.001,0.01, 0.1,1]
for i in alphas:
    clf_mlp = MLPClassifier(alpha=i, random_state=42)
    scores = cross_val_score(clf_mlp, X, y, scoring='accuracy', cv=10)
    cv_scores.append(scores.mean())
    cv_scores_std.append(scores.std())
```


```python
# Plot the relationship
plt.errorbar(alphas, cv_scores, yerr=cv_scores_std, marker='x', label='Accuracy')
plt.xscale('log')
plt.xlabel('alpha')
plt.ylim([0.6, 0.85])
plt.ylabel('Accuracy')
plt.legend(loc='best')
plt.show()
```


    
![png](output_42_0.png)
    


**It can be seen that when alpha increases, the prediction accuracy drops, showing that the overfitting issue of the model on this dataset is not a big problem.**

### Task3. Increase the number of iterations
This is related to the early stopping technique we mentioned in the lecture. Please explore when is good enough to stop the iteration of weight updating. Please draw a figure to report the accuray with differnt number of iterations [200,400,600,800,1000]. The parameter 'max_iter' can specify this setting. Note that the execution time for this task is relative long. To track the progress of the execution, you could set the verbose parameter in the cross_val_score method as 'verbose=1'.


```python
# Try different number of iterations. Plot the relationship between the performance and the number of iterations.

```


```python
cv_scores= []
cv_scores_std=[]
iteration_numbers=  [200,400,600,800,1000]
for i in iteration_numbers:
    clf_mlp = MLPClassifier(random_state=42,max_iter=i)
    scores = cross_val_score(clf_mlp, X, y, scoring='accuracy', cv=10)
    cv_scores.append(scores.mean())
    cv_scores_std.append(scores.std())

```


```python
plt.errorbar(iteration_numbers, cv_scores, yerr=cv_scores_std, marker='x', label='Accuracy')

plt.xlabel('Iteration Number')
plt.ylim([0.4, 1.1])
plt.ylabel('Accuracy')
plt.legend(loc='best')
plt.show()
```


    
![png](output_47_0.png)
    


## Comparing with other classification models
### Task4. Compare the results with Naive Bayes (GaussianNB) and K-Nearest Neighbors (K=1)
Compare their accuracy scores and use t test to show if their perofrmance has siginficantly different with significance level 0.05.


```python
# Compare with the two models we used before

```


```python
# Compare with the two models we used before from sklearn.naive bayes import GaussianNB
from sklearn.naive_bayes import GaussianNB
clf_gnb = GaussianNB ()

scores_gnb = cross_val_score(clf_gnb, X, y, cv=10)
print('Accuracy range for Gaussian Naive Bayes classifier: [%.4f, %.4f]; mean: %.4f; std: %.4f\n'
% (scores_gnb.min(), scores_gnb.max (), scores_gnb .mean (), scores_gnb.std()))

# This is to show t-test on their performances.
from scipy.stats import test_ind
t, p = test_ind(scores_mlp_default, scores_gnb)
print ('t, p: %.4f, %.6f\n' % (t, p))

from sklearn. neighbors import KNeighborsClassifier
clf_knn = KNeighborsClassifier (n_neighbors=1)

scores_knn = cross_val_score(clf_knn, X, y, cv=10)
print ('Accuracy range for KNN classifier: [%.4f, %.4f]; mean: %.4f; std: %.4f \n'
       % (scores_knn.min(), scores_knn. max (), scores_knn. mean (), scores_knn.std()))

# This is to show t-test on their performances.
t, p = test_ind(scores_mlp_default, scores_knn)
print ('t, p: %.4f, %.6fIn' % (t, p))
```
