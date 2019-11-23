'''
Created on 30 oct. 2019

@author: ingov
'''
#We import pandas to manage our data through dataframes
import pandas as pd
#We import this custom made module that handles linear regression tasks
from API import LinearRegressionUtils as lru
#We import this custom mode module that handles how to get information in the format we need
from data import getDataFrame as gdf

#We define these variables with the path to our excel files with the data for hate crimes
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
X = df.loc["lgtbiphobia"].rename("lgtbiphobia")
Y = df.loc["Xenophobia"].rename("Xenophobia")
LinearRegUtils = lru.LinearRegressionUtils(X,Y,X.name,Y.name)
LinearRegUtils.print_stats()
#We evalutate the correlation between our variables
LinearRegUtils.print_evaluation_for_rsquare()
LinearRegUtils.generate_Linear_Correlation_Graph("black", "blue", "Linear Regression Graph")