# coding: utf-8
'''
Created on 7 nov. 2019

@author: ingov
'''
#We import this custom made module that handles how to perform a chi square association test
from API import ChiSquareAssociationTestUtils as cs
#We import this custom made module that handles how to get the information to generate our dataframes
from data import getDataFrame as gdf
#We import this custom made module that handles linear regression
from API import LinearRegressionUtils as lru
#We import the module pandas that handles how to manage dataframe
import pandas as pd

#We define the list of crimes we want to research
crimes = ["Antisemita","Aporofobia","Religión","Discapacidad","Lgtbifobia","Xenofobia"]

#We define an empty dictionary for our results performing chi square association tests
#We will save those variable that are likely to be related
results = {}
#For each type of crime
for i in range(0,len(crimes)):
    #We get the information about that type of crime for every year in a data frame using our custom module
    ds1 = gdf.getDataFrameReady(crimes[i], "Name", "../data/ProvincesCoordinates.xlsx", "../data/HateCrimes")
    #We filter and just keep the index and the columns that contain the frequency of that crime between 2014 and 2017
    #and we rename the dataframe as the crime
    ds1 = ds1[range(2014,2018)].sum().rename(crimes[i])
    #For each of the other types of crimes
    for j in range(i+1,len(crimes)):
        print("DATA")
        print(ds1)
        #We get the information about that type of crime for every year in a data frame using our custom module
        ds2 = gdf.getDataFrameReady(crimes[j], "Name", "../data/ProvincesCoordinates.xlsx", "../data/HateCrimes")
        #We filter and just keep the index and the columns that contain the frequency of that crime between 2014 and 2017
        #and we rename the dataframe as the crime
        ds2 = ds2[range(2014,2018)].sum().rename(crimes[j])
        print(ds2)
        #Now we use this custom made method that return true if our variable are likely to be dependent or false otherwise
        related = cs.performChiSquareTest(ds1,ds2)
        #We group these variables
        variables = (crimes[i],crimes[j])
        #We save if they are related or not
        results[variables] = related
        
print(results)

#For each pair of variables analyzed
for vKey in results:
    #If they are likely to be dependent we perform a linear regression analysis
    if(results[vKey]==True):
        print("Loading data")
        #We get the data for our first type of crime in the pair
        ds1 = gdf.getDataFrameReady(vKey[0], "Name", "../data/ProvincesCoordinates.xlsx", "../data/HateCrimes")
        print(ds1)
        #We get the data for our second type of crime in the pair
        ds2 = gdf.getDataFrameReady(vKey[1], "Name", "../data/ProvincesCoordinates.xlsx", "../data/HateCrimes")
        print(ds2)
        #We perform some needed transformations in our dataframes to perform our linear regression analysis
        print("Performing some transformations")
        df = pd.DataFrame(ds1[range(2014,2018)].sum().rename(vKey[0]))
        df = df.T
        df = df.append(ds2[range(2014,2018)].sum().rename(vKey[1]))
        print("Our data for our regression:")
        print(df)
        #We define our variable X
        X = df.loc[vKey[0]].rename(vKey[0])
        #We define our variable Y
        Y = df.loc[vKey[1]].rename(vKey[1])
        #We use this custom made class that performs the linear regression analysis
        LinearRegUtils = lru.LinearRegressionUtils(X,Y,X.name,Y.name)
        #This method prints some basic stats of our analysis
        LinearRegUtils.print_stats()
        #We check what the correlation between our variables is
        LinearRegUtils.print_evaluation_for_rsquare()
        #We plot a graph with scatter points with our data and a linear function with our regression function
        LinearRegUtils.generate_Linear_Correlation_Graph("black", "blue", "Linear Regression Graph")