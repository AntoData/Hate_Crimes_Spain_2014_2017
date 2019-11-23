# coding: utf-8
'''
Created on 6 sept. 2019

@author: ingov
'''
#We import folium to handle the creation and edition of maps
import folium
#We import json to handle how we manage our JSON files
import json

def getCoordinatesForRegions(coor,results):
    """
    This is a recursive method that searches for the different coordinates that form a polygon in a JSON
    @param coor: The coordinates we are exploring. At first in this case, the ones that belong to a country
    @param results: List with a list of the coordinates of the different regions
    @param results: We return the results we got in this iteration so we could pass it to the previous
    one recursively
    @return: variable results 
    """
    print(results)
    #If all the elements of one of the elements of the coor are int or float, that means it is
    #a new polygon so we add it to the list of results
    if(all(isinstance(y, (int, float)) for x in coor for y in x)):
        print(results)
        print("New polygon: Adding it to the list")
        results.append(coor)
        return results
    else:
        #Otherwise, we get every element in coor and call this very function recursively for each
        #of those elements
        for i in coor:
            results=getCoordinatesForRegions(i,results)
    #We return the results of this iteration for the next one
    return results

def fourCoordinates(coorList):
    """
    This method compares the different coordinates in our coordinates list for our polygon
    and gets the top, bottom, most right and left points that form our region
    @param coorList: List with the coordinates that belong to a polygon that compose the country/region
    we were checking
    @return: Top, Bottom, Left, Right coordinates that compose our region
    """
    #We create four coordinates for the top, bottom, most left and most right and we equal them
    #to the first coordinate of each type (x or y) in our list
    coorTop, coorBottom, coorLeft, coorRight = coorList[0][0],coorList[0][0],coorList[0][1],coorList[0][1]
    #For each coordinate in our list of coordinates
    for coor in coorList:
        #We check if x coordinate is greater than top coordinate in which case is the new top coordinate
        if(coor[0]>coorTop):
            coorTop = coor[0]
        #We check if x coordinate is lower than top coordinate in which case is the new top coordinate
        if(coor[0]<coorBottom):
            coorBottom = coor[0]
        #We check if y coordinate is greater than most right coordinate in which case is the new most right coordinate
        if(coor[1]>coorRight):
            coorRight = coor[1]
        #We check if y coordinate is lower than most right coordinate in which case is the new most left coordinate
        if(coor[1]<coorLeft):
            coorLeft = coor[1]
    #print(str(coorTop)+" "+str(coorBottom)+" "+str(coorLeft)+" "+str(coorRight))
    #We return our four coordinates
    return coorTop,coorBottom,coorLeft,coorRight


def getMapsFromRegions(jsonPath,region):
    """
    This function gets the path to a JSON and a region and gets a collection of maps centered
    in the polygons that compose that region in that JSON
    @param jsonPath: Path to the JSON with the region we want to get all different polygons that
    compose it in folium maps
    @param region: Region we want to get all the polygons that compose it and save them as folium
    maps in a list
    @return: List with those maps
    """
    #We create an empty list where we will append all folium maps we will create
    rMaps = []
    #We open our JSON file and get all its lines into a variable called sforfile
    f = open(jsonPath,"+r")
    sforfile = ""
    for line in f:
        sforfile += line
    #We load the lines for this JSON into a JSON object
    vis1 = json.loads(sforfile)
    #We turn that JSON object into a dictionaty
    dict1 = dict(vis1)
    #We get the value related to feature (which is where the coordinates and regiosn are usually in a JSON)
    dict2 = dict1["features"]
    #We create an empty list where we will append the coordinates for our region/country
    coor = []
    #We search our region in the JSON, going key by key
    for country in dict2:
        if(country['properties']['name']==region):
            #If we find our region, we save its coordinates
            coor = country["geometry"]['coordinates']
    #We generate an empty list to be used un our recursive function getCoordinatesForRegions
    res = []
    #We call this function to get all the coordinates for that region
    results = getCoordinatesForRegions(coor,res)
    i=0
    #Now we polygon by polygon and get its four significant coordinates calling the function
    #fourCoordinates
    for r in results:
        coorTop,coorBottom,coorLeft,coorRight=fourCoordinates(r)
        vMap = folium.Map()
        print(r)
        #We create in each iteration a folium map centered in those four coordinates
        vMap.fit_bounds([[coorLeft,coorTop],[coorRight,coorBottom]])
        #And we append that map to our list we will return
        rMaps.append(vMap)
        i=i+1
    #We return the list with the folium maps centered in the different polygons that compose
    #the region/country we pass as parameter
    return rMaps

def applyGEOjsonToMaps(path,listMap):
    """
    This fuction applies the same GEOJSON to a list of maps
    @param path: Path to the JSON
    @param listMap: list of maps we will apply this GEOJSON to  
    """
    for vMap in listMap:
        vMap.add_child(folium.GeoJson(open(path,encoding = "utf-8-sig").read()))
    return listMap
        

def getMapsToFile(name,listMaps,path):
    """
    This functions turns a list of maps into HTML files
    @param name: Pattern the name the HTML files will have
    @param listMaps: List of maps we will save as HTML files
    @param path: Path where we will save these files   
    """
    i = 0
    #We get each map in listMaps
    for vMap in listMaps:
        #And save it in path with name "name-i".html where "i" is the iteration
        vMap.save(path+name+"-{0}.html".format(i))
        i=i+1
        
def putCirclesinMap(vMap,dataframe,popupField,latitudeField,longitudeField,valueField,proportion):
    """
    This function draws circles with a proportion related to the value of a field in a dataframe
    @param vMap: Map where we want to draw the circles
    @param dataframe: dataframe where we have the data we will use as value for the radius of these circles
    (we will multiply by proportion to get the radius)
    @param popupfield: Field in our dataframe we will use as information to display in the pop-up
    that is opened when we click in one of these circles we are drawing
    @param latitudeField: Field in our dataframe where we store the latitude of the point where we
    want to display a circle for a particular row
    @param longitudeField: Field in our dataframe where we store the longitude of the point where we
    want to display a circle for a particular row
    @param valueField: Field with the data we will use to get the radius of our circle. We will 
    multiply this by proportion
    @param proportion: Proportion of the size we want our circles to have in relation to our values 
    """
    #For each row in the dataframe we paint a circle using the columns we set up before
    #for that particular eow
    for i in range(0,len(dataframe)):
        vMap.add_child(folium.Circle(
            location=[dataframe.iloc[i][latitudeField], dataframe.iloc[i][longitudeField]],
            popup=dataframe.iloc[i][popupField],
            radius=int(dataframe.iloc[i][valueField]*proportion),
            color='crimson',
            fill=True,
            fill_color='crimson'))
    #We return our map with the circle
    return vMap