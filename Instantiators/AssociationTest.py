'''
Created on 27 oct. 2019

@author: ingov
'''
#We import pandas to manage our data through dataframes
import pandas as pd
#We import chi2_contingency from scipy.stats to use Chi-square as an association test
from scipy.stats import chi2_contingency
#We import this custom made module to handle how to get the information in our dataframes
from data import getDataFrame as gdf
"""
We are testing if the frequencies of different kinds of hate crimes have some sort of sort of relation
between them. In this case, we are testing if the frequencies of crimes caused by lgtbiphobia and crimes 
cause by xenophobia in Spain between 2014 and 2017 (unfortunately, official data is only provided 
for those years at this point) are independent or not
In order to do so, we are using The Chi Square Test of Association.
For starters, we need two different hypothesis:
H0: The frequencies of crimes caused by lgtbiphobia and xenophobia in Spain between 2014 and 2017 
are independent.
H1: The frequencies of crimes caused by lgtbiphobia and xenophobia in Spain between 2014 and 2017 
are NOT independent. There is a correlation between them.
"""
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
print("Our data for our test:")
print(df)
#To perform The Chi Square Test of Association, we only have to use the method chi2_contingency
# we imported from scipy.stats and pass the dataframe we generated as a parameter
pChi2 = chi2_contingency(df)
#This method will return an object which is an array that has different elements used in chi square
print("Chi square statistic:")
print(pChi2[0])
"""
A chi square statistic is a test that measures how expectations compare to actual observed data
If we were doing this by hand, we would have now to check our reference table and with this data
we would check what is the approximate value of our p-value to assert if H0 is true or not, using
also the degrees of freedom
"""
print("P-value")
print(pChi2[1])
"""
This is the value that determines if H0 is true or we can reject it. Scientific consensus is
that if is lower than 0.05 we can reject H0. It is the probability that H0 is true. In other words,
the probability that our variables are indeed independent
"""
print("Degrees of freedom")
print(pChi2[2])
"""
(r-1)(c-1) where r is the number of rows and c is the number of columns
"""
print("Contingency matrix")
print(pChi2[3])
"""
Matrix with the total frequencies of every row and column. If we were doing this whole process by
#hand we would use those total frequencies for our calculations
"""
"""
To make this a little bit more interesting we are defining this function that will take the object
that chi2_contingency from scipy.stats returns and determines if H0 can or can't be reject
"""
def rejectHO(pChi2):
    print("The probability of H0 being true is {0}".format(pChi2[1]))
    if(pChi2[1]<0.05):
        print("So we can reject our H0. There is a high probability that our variables are not independent")
        print("Which means our variables are likely related")
        return True
    else:
        print("So we can not reject our H0. There is a high probability that our variables are independent")
        return False
    
if(rejectHO(pChi2)):
    print("We can't say lgtbiphobic and xenophobic crimes are independent in Spain between 2014 and 2017")
    print("They are very likely to be related")
else:
    print("We can say lgtbiphobic and xenophobic crimes are independent in Spain between 2014 and 2017")