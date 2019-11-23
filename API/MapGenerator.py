
'''
Created on 27 oct. 2019

@author: ingov
'''
#We import the module folium which will handle the creating and customization of maps
import folium
#We import pandas to manage our csv files
import pandas as pd
#We import GifGenerator from API that encapsulates the process to turn a collection of images
#into a gif
from API import GifGenerator as gg
#We import RegionsInJson from API to 
from API import RegionsInJson as rij
#DivIcon to create an html div to display the year of the statistics
from folium.features import DivIcon

def mapGeneratorCircles(csvPath,jsonContriesPath,country,jsonProvincesPath,columns,webdriverPath,projectName,scale,polygons):
    """
    This function generates a gif file consisting of the different maps. We generate the html
    file for each map and open them in a headless browser and we take a screenshot.
    @param csvPath: This is a string that contains the path to our csv that will generate a
    dataframe (our dataframe should have fields "Name", "Latitude" and "Longitude" and at least
    the columns that we provide in the parameter columns
    @param jsonCountriesPath: Path that will contain the JSON with the information about countries.
    We will search the parameter country in this json to zoom our HTML to the different polygons
    that form our country. We will create a different HTML file for each polygon
    @param country: Country we will zoom our HTML files to (we will create different
    HTML files if the country is divided in different polygons e.g. the UK: one for
    Great Britain and another for Northen Ireland)
    @param jsonProvincesPath: Path for the JSON we will use to divide our map in provinces/regions
    @param columns: Columns in the dataframe we want to represent for each iteration in the map
    @param webdriverPath: Path for the webdriver we will use to display our map in a browser
    @param projectName: string we will use to name our files
    @param scale: radius of the circles per unit
    @param polygons: Dictionary where we put the name of the polygons in which we will divide our map
    and generate a new file to display them with value the point where we want to display the
    name of the column we are representing in that file we will generate
    """
    #We have a json with the different provinces in which we want to divide our map
    jsondata = jsonProvincesPath
    #We read the dataframe with the information we want to represent
    df = pd.read_excel(csvPath)
    print(df)
    #We generate a dictionary where key is the name of the region and value is a list where
    #we will be adding the HTML files that display that region/polygon
    regionsInMap = {}
    for region in polygons.keys():
        regionsInMap[region] = []
    
    #To make things easier we generate a list with the keys of our dictionary of regions
    #that we will access using an integer iterator k
    lRegions = list(polygons.keys())
    #For each column
    for i in columns:
        #We get the different polygons that form our country
        lMap = rij.getMapsFromRegions(jsonContriesPath,country)
        #We apply our json with the division by provinces to each one of them
        lMap = rij.applyGEOjsonToMaps(jsondata, lMap)
        #We generate a dataframe with just the columns "Name", "Latitude", "Longitude"
        #and the column i
        dfi=df[['Name','Latitude','Longitude',i]].copy()
        #Now for each polygon we for this column, we will put the corresponding circles
        #and add to its map and we will add it to the corresponding list in the dictionary
        for k in range(0,len(lMap)):
            #We get the map in the position "k" and put the corresponding circles there
            lMap[k]=rij.putCirclesinMap(lMap[k],dfi,'Name','Latitude','Longitude',i,scale)
            #Now we use the function parameter polygon and get the corresponding point in which
            #we said we wanted to display this marker using the list of the keys of regions and 
            #getting the one in the position k
            folium.map.Marker(
                polygons[lRegions[k]],
                icon=DivIcon(
                    icon_size=(150,36),
                    icon_anchor=(0,0),
                    html='<div style="font-size: 36pt">{0}</div>'.format(i))).add_to(lMap[k])
            #We finally add the resulting map to the corresponding list in the dictionary of polygons/regions
            regionsInMap[lRegions[k]].append(lMap[k])
    #We create a list to store all our maps            
    totalMaps = []
    #We get the list of maps for every polygon and add it to our totalMaps list
    for region in regionsInMap.keys():
        totalMaps = totalMaps + regionsInMap[region]
    #Now we call to our method to generate the GIF file
    gg.fromFoliumMaptoGIF(totalMaps, projectName,webdriverPath) 