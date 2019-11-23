'''
Created on 7 nov. 2019

@author: ingov
'''
#We import pandas to manage our data through dataframes
import pandas as pd
#We import chi2_contingency from scipy.stats to use Chi-square as an association test
from scipy.stats import chi2_contingency



def rejectHO(pChi2):
    """
    We define a function that given a chi2_contigency object will get the p-value and decide
    if we can reject H0 or we can't depending on if p-value < 0.05 or not
    @param pChi2: An object of type scipy.stats.chi2_contigency
    @return: boolean True if we can reject our H0 and False in case we can't
    """
    print("The probability of H0 being true is {0}".format(pChi2[1]))
    if(pChi2[1]<0.05):
        print("So we can reject our H0. There is a high probability that our variables are not independent")
        print("Which means our variables are likely related")
        return True
    else:
        print("So we can not reject our H0. There is a high probability that our variables are independent")
        return False
    

def performChiSquareTest(*ds):
    """
    This function given an array or list of data series performs a series of transformations to
    turn all these dataseries into a dataframe and performs a chi square association test,
    prints all the important parameters that are used in this kind of test and also returns
    true or false depending on if we can reject our H0 or not using the method "rejectHO" defined
    above. In order for this to work all dataseries must have the same columns
    @param *ds: Several dataseries, they must have the same columns
    @return: boolean True if we can reject our H0 and False in case we can't
    """
    print("Performing some data transformations")
    #We create an empty dataframe
    df = pd.DataFrame()
    #We get the dataframes in dsi one by one
    for dsi in ds:
        print(dsi)
        #We create a new row in our new dataframe that will contain our current dataseries
        #In order to do so we just create a new column whose name is the name of the dso
        #an say it's equal to our dsi
        df[dsi.name] = dsi
    #Now we transpose the dataframe so our dataseries are rows now
    df = df.T
    print("This is our current data:")
    print(df)
    #As in every chi square association test we have to state two hypothesis:
    #H0 our variables are independent, they are not related
    #H1 our variables are not independent, they might be related
    print("We are testing these hypotesis:")
    print("H0: Our variables are independent")
    print("H1: Our variables are not independent")
    #We create our pChi2 object using our newly created dataframe
    pChi2 = chi2_contingency(df)
    #This object offers the following parameters for this test
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
    #We finally return True if we can reject H0 or false if we can't. In other words,
    #we return True is our variable are not likely to be independent and False if they
    #are likely to be independent
    return rejectHO(pChi2)