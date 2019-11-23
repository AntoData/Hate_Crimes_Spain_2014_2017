
'''
Created on 30 oct. 2019

@author: ingov
'''
#We import pandas to handle dataframes
import pandas as pd
#We import matplotlib.pyplot to handle how to display charts
import matplotlib.pyplot as plt
#We import this custom made module that 
from API import GraphUtils as gu


#We create this list to save all our dataframes
dfList = []
for i in range(2014,2018):
    df = pd.read_excel("../data/HateCrimes{0}.xlsx".format(i))
    dfList.append(df)

#We create this list to save all provinces whose number of hate crimes is greater than average
listOfProvincesWithGreaterThanMean = None
#We go through every dataframe in our list of dataframes
for i in range(0,len(dfList)):
    #We get the mean of hate crimes for each dataframe/each years
    print("Mean of hate crimes per province in Spain during {0}".format(i+2014)) 
    print(dfList[i].mean())
    print(dfList[i]["TOTAL"].mean())
    #We set the column for the name of the provinces as index
    dfri = dfList[i][["Name","TOTAL"]].set_index("Name")
    mean = dfri["TOTAL"].mean()
    #We use this custom made function to plot a bar graph with the number of hate crimes
    #in each province plus a line with the mean of hate crimes in Spanish provinces during that
    #year
    fig,axs = gu.barPlotWithMean(dfri.index,dfri["TOTAL"],mean,"Hate crimes in Spain in {0}".format(i+2014),"Provinces","Reported Crimes",None)
    #We display this graph
    plt.show()
    #We build this list to keep the names of provinces where the number of hate crimes are greater
    #than the mean of hate crimes
    labels = []
    for j in range(0,len(dfri.index)):
        #If in that province the number of hate crimes is greater than the mean,
        #We add the name of the province
        if(dfri.iloc[j]["TOTAL"]>mean):
            labels.append(dfri.index[j])
        else:
            #Otherwise we just add a blank string
            labels.append("")
    #We use this custom made function to plot a pie chart
    fig,axs = gu.piePlotImproved(dfri["TOTAL"],labels,"Pie for hate crimes in {0}".format(i+2014),gu.mylambdapct)
    #We display it
    plt.show()
    #Now we will gather information about provinces where the number of hate crimes is greater than
    #the average for that year
    print("Provinces where the total of hate crimes was greater than the mean of hate crimes in Spain in {0}".format(i+2014))
    #We filter our dataframe to get only the provinces where the number of hate crimes is greater than
    #the average for that year
    print(dfri[dfri["TOTAL"]>mean].sort_index())
    print("Hate crimes per day in Spain in {0}".format(i+2014))
    #We also display the number of hate crimes per day in total
    print(dfri["TOTAL"].sum()/365)
    dfri = dfri[dfri["TOTAL"]>mean].sort_index()
    dfri.reset_index(inplace=True)
    #We save the name of provinces where the number of hate crimes is greater than the average
    #every year between 2014 and 2017
    if listOfProvincesWithGreaterThanMean == None:
        #If the object is None is because we are using it for the first time
        print(dfri["Name"])
        #We just say that this set is equals to the names of provinces from our dataframe
        #we filtered to keep only the name of provinces where the number of hate crimes is greater
        #than average
        listOfProvincesWithGreaterThanMean = set(dfri["Name"])
    else:
        #Now, we use the operator & to only keep in every iteration the provinces that had
        #a number of hate crimes greater than average for every other year
        listOfProvincesWithGreaterThanMean = listOfProvincesWithGreaterThanMean & set(dfri["Name"])
    print("Standard deviation during of hate crimes between provinces in {0} in Spain was {1}".format((i+2014),dfri["TOTAL"].std()))
#We print the list of provinces where the number of hate crimes has been greater than average
#every year between 2014 and 2017
print("Provinces where hate crimes have been greater than average every year from 2014 to 2017")
print(listOfProvincesWithGreaterThanMean)
dfpopulation = pd.read_excel("../data/PopulationProvinces.xlsx").set_index("Name")
for province in listOfProvincesWithGreaterThanMean:
    for i in range(0,len(dfList)):
        dfri = dfList[i][["Name","TOTAL"]].set_index("Name")
        t = dfpopulation[i+2014].loc[province]/dfri["TOTAL"].loc[province]
        print("In {0} in {1} we had a hate crime per {2} people".format(province,(i+2014),t))
       
#Now we go through every dataframe (every year)
for i in range(0,len(dfList)):
    #We use mean() to get the average number of hate crimes in every province between 2014 and 2017
    print("Mean of lgtbiphoobic crimes per province in Spain during {0}".format(i+2014)) 
    print(dfList[i]["Lgtbifobia"].mean())
    #We make some transformations to get only the provinces where the number of hate crimes
    #is greater than the average
    dfri = dfList[i][["Name","Lgtbifobia"]].set_index("Name")
    print("Provinces where the total of Lgtbiphobic crimes was greater than the mean of Lgtbiphobic crimes in Spain in {0}".format(i+2014))
    print(dfri[dfri["Lgtbifobia"]>dfri["Lgtbifobia"].mean()].sort_index())
    #We print the number of hate crimes per day in Spain between 2014 and 2017
    print("Lgtbiphobic crimes per day in Spain in {0}".format(i+2014))
    print(dfri["Lgtbifobia"].sum()/365)