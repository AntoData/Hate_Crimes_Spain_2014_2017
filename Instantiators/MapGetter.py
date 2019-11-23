'''
Created on 27 oct. 2019

@author: ingov
'''
#We import this custom made module that handles how to generate maps and turn them into gifs
from API import MapGenerator as mg
#We import this custom made module that handles how to get the information in the format we need in our dataframes
from data import getDataFrame as gdf

#We define the path for the dataframe of hate crimes per provinces between 2014 and 2017
excelProvinceTotals = r"../data/HateCrimesPerProvincesTotals.xlsx"
#We define the path for the dataframe of lgtbiphobic crimes per provinces between 2014 and 2017
excelgtbiphobiaProvinces = r"../data/lgtbiphobicCrimesPerProvincesTotals.xlsx"
#We define the path for the dataframe of xenophobic crimes per provinces between 2014 and 2017
excelXenophobiaProvinces = r"../data/XenophobicCrimesPerProvincesTotals.xlsx"
#We define the path to the JSON that defines our countries
jsonCountries = r"../data/world-countries.json"
#We define which country we will focus on
country = r"Spain"
#We define the path to the JSON that defines the provinces for our country
jsondata = r"../data/spain-provinces.geojson"
#We define the path for our webdriver
webdriverPath = r"../API/chromedriver.exe"

#We get the information about the total of hate crimes between 2014 and 2017 and turn it into a dataframe
dfTotal = gdf.getDataFrameReady("TOTAL", "Name", "../data/ProvincesCoordinates.xlsx", "../data/HateCrimes")
print(dfTotal)
#We save our dataframe to the file whose path we defined in variable excelProvinceTotals
dfTotal.to_excel(excelProvinceTotals)

#We get the information about the lgtbiphobic crimes between 2014 and 2017 and turn it into a dataframe
dflgtbiphobic = gdf.getDataFrameReady("Lgtbifobia", "Name", "../data/ProvincesCoordinates.xlsx", "../data/HateCrimes")
print(dflgtbiphobic)
#We save our dataframe to the file whose path we defined in variable excellgtbiphobiaTotals
dflgtbiphobic.to_excel(excelgtbiphobiaProvinces)

#We get the information about the xenophobic crimes between 2014 and 2017 and turn it into a dataframe
dfxenophobic = gdf.getDataFrameReady("Xenofobia", "Name", "../data/ProvincesCoordinates.xlsx", "../data/HateCrimes")
print(dfxenophobic)
#We save our dataframe to the file whose path we defined in variable excelXenophobiaTotals
dfxenophobic.to_excel(excelXenophobiaProvinces)

#We define the columns we want to represent in our maps that form our gif files
columns = range(2014,2018)
#We use this custom made module to generate the gif file that contains the different maps with the
#circles representing the data for every year between 2014 and 2017 creating a file centered in each
#polygon that compose our country
mg.mapGeneratorCircles(excelProvinceTotals, jsonCountries, country, jsondata, columns, webdriverPath,"TotalHateCrimes",250,{"Peninsula":[45, -6],"Canary Islands":[27, -13]})
mg.mapGeneratorCircles(excelgtbiphobiaProvinces, jsonCountries, country, jsondata, columns, webdriverPath,"lgtbiphobiaProvinces",500,{"Peninsula":[45, -6],"Canary Islands":[27, -13]})
mg.mapGeneratorCircles(excelXenophobiaProvinces, jsonCountries, country, jsondata, columns,webdriverPath,"XenophobiaProvinces",500,{"Peninsula":[45, -6],"Canary Islands":[27, -13]})