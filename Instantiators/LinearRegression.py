'''
Created on 27 oct. 2019

@author: ingov
'''
#We import pandas to manage our data through dataframes
import pandas as pd
#We import this modules to handle linear regression tasks
from sklearn import datasets, linear_model
#We import this modules to handle r square calculations
from sklearn.metrics import mean_squared_error,r2_score
#We import matplotlib to handle how to plot charts
import matplotlib.pyplot as plt
#We import numpy to handle math tasks
import numpy as np
#We import this custom made module to handle how to get the information in the format
#we need for our dataframes
from data import getDataFrame as gdf

#We create two different dataframes reading those excel files
print("Loading data")
dflgtbiphobia = gdf.getDataFrameReady("Lgtbifobia", "Name", "../data/ProvincesCoordinates.xlsx", "../data/HateCrimes")
print(dflgtbiphobia)

dfxenophobia = gdf.getDataFrameReady("Xenofobia", "Name", "../data/ProvincesCoordinates.xlsx", "../data/HateCrimes")
print(dfxenophobia)
#We create a dataframe using the dataframe that contains the data for lgtbiphobic crimes
#but we filter the dataframe getting only the columns that contain the number of crimes per year
#and use the function sum() to get the total of lgtbiphobic crimes every year. We also use the
#function rename to give this dataseries a name so when it necomes a row for our dataframe, it
#has an index with an appropiate name
print("Performing some transformations")
df = pd.DataFrame(dflgtbiphobia[range(2014,2018)].sum().rename("lgtbiphobia"))
#We transpose the dataframe so now it has one row and 4 columns. The row represents lgtbiphobic
#crimes and every column represent the number of those crimes per year
df = df.T
#Now we add the xenophonic crimes per year, using the same transformation we used earlier
#we get the number of those crimes per year using sum and we give the row a name so it has an
#index with an appropiate name
df = df.append(dfxenophobia[range(2014,2018)].sum().rename("Xenophobia"))
#Now we have a valid matrix for chi square. As we have our variables as row and the frequency
#for each different year as columns
print("Our data for our regression:")
print(df)
#We have to get our two variables in different array series. We use loc to get the row whose
#index is the variable we are looking for and we rename it. We have to build it as a numpy array
#so we can use the function reshape with parameters (-1,1) so our array is a 2D array
#This is needed for variable X in a next step
X = np.array(df.loc["lgtbiphobia"].rename("lgtbiphobia"))
X = X.reshape(-1,1)
print("Our variable X: lgtbiphobic crimes:\n{0}".format(X))
#We get our variable Y to check if there is linear correlation. In this case, there is no need
#to transform this series into a numpy array
Y = df.loc["Xenophobia"].rename("Xenophobia")
print("Our variable Y: xenophobic crimes:\n{0}".format(Y))
#We create an object for linear regression using linear_model
regr = linear_model.LinearRegression()
#We use the function fit and the objects that represents our variables X and Y to make our
#object for linear regression to update all variables for linear regression with our data
regr.fit(X,Y)
#We get the correlation coefficient using the first position of the variable coef_ of our object
#for linear regression
coefcorr = regr.coef_[0]
print("Coeficientes: ",coefcorr)
#We evalutate the correlation between our variables
if(coefcorr == 1):
    print("There is a perfect positive correlation between our variables")
elif(1 > coefcorr >= 0.7):
    print("There is a strong positive correlation between our variables")
elif(0.7 > coefcorr >= 0.5):
    print("There is positive correlation between our variables")
elif(0.5 > coefcorr > 0):
    print("There is very weak positive correlation between our variables")
elif(coefcorr == 0):
    print("There is absolutely no correlation between our variables")
elif(coefcorr == -1):
    print("There is a perfect negative correlation between our variables")
elif(-1 < coefcorr <= -0.7):
    print("There is a strong negative correlation between our variables")
elif(-0.7 < coefcorr <= -0.5):
    print("There is negative correlation between our variables")
elif(-0.5 < coefcorr < 0):
    print("There is a very weak negative correlation between our variables")

#Now we use our variable X and the method predict to generate the value for our variable Y
#that this linear model returns as a prediction
Y_pred = regr.predict(X)
print("Y_pred")
print(Y_pred)
#Now we get the parameter R square, which measures the differences between our variable Y
# and the values we predict for this variable Y in our model
rsquare = r2_score(Y, Y_pred)
print("R cuadrado: ",rsquare)
if(rsquare == 1):
    print("There is a perfect correlation between our variables")
elif(1 > rsquare >= 0.7):
    print("There is a very strong correlation between our variables")
elif(0.7 > rsquare >= 0.5):
    print("There is strong correlation between our variables")
elif(0.5 > rsquare > 0.3):
    print("There is correlation between our variables")
elif(0.3 >= rsquare > 0):
    print("There is very weak correlation between our variables")
elif(rsquare == 0):
    print("There is absolutely no correlation between our variables")
#So our variables are likely not independent, but there is a very week negative correlation between
#them
plt.scatter(X, Y, color = "black" )
plt.plot(X,Y_pred,color="Blue")
plt.xlabel("Lgtbiphobic crimes")
plt.ylabel("Xenophobic crimes")
plt.title("Linear Regression Graph")
for i in range(0,len(df.columns)):
    plt.annotate(df.columns[i], np.array(df[df.columns[i]])) 
plt.show()
