'''
Created on 8 sept. 2019

@author: ingov
'''
#selenium to display the html files in a browser and get screenshots
from selenium import webdriver
#time to set a delay between the opening of the browser and the screenshot
import time
#os to manage folders and path for the html, png and gif files
import os
#imageio to turn a collection of pngs to gif
import imageio

def fromFoliumMaptoGIF(listMaps,pathName,webdriverPath):
    """
    Basically, this is a function that given a list of objects of type map from Folium,
    will save it as an HTML. Then, we will open these HTML files in a headless browser using Selenium
    and save them as images. Finally, we will use these images in a certain order to create
    a gif that shows an animation of the evolution of these maps.
    @param listMaps: a list of objects of type map from Folium to save as PNG files and turn into
    the gif
    @param pathName: the path for our files (which includes a basic name for our files but with no extension)
    @param webdriverPath: in order to be able to open our browser using selenium we neeed to provide the path for
    the webdriver in the parameter webdriverpath 
    """
    #We create a variable "i" to be used as a counter, this will be part of the name of our files
    i = 0
    #We create this empty list that will contain the paths where the images taken to the HTML file
    #when it was opened using Selenium are
    pngFiles = []
    print("Applying headless configuration to Chrome webdriver")
    #We first generate this object to handle the configuration of our Chrome webdriver
    chromeOptions = webdriver.ChromeOptions()
    #We set it up to be headless like this
    chromeOptions.add_argument("--headless")
    #We create a Chrome browser
    print("Opening headless Chrome browser")
    print(os.getcwd()+"\\"+webdriverPath)
    #Now we create our Chrome browser object, we need to provide the full path for our
    #webdriver using the parameter of this function called webdriverPath
    browser = webdriver.Chrome(executable_path=os.getcwd()+"\\"+webdriverPath,chrome_options=chromeOptions)
    #We maximize the window
    browser.maximize_window()
    #Now for each map in our list of maps in function parameter listMaps
    for vMap in listMaps:
        print("Processing file number {0} of {1}".format(i+1,len(listMaps)))
        #We generate the full path for our HTML file needed to be opened in a browser and take a
        #screenshot. We add the value of "i" to the path so we are always creating a new file 
        #and never overwriting
        htmlResult = os.getcwd()+"\\..\\HTML\\"+pathName+"{0}.html".format(i)
        #We generate the full path for our PNG file which will contain the screenshot taken to
        #the HTML file we open in this iteration using our webdriver. We add the value of "i"
        #to the path so we are always creating a new file and never overwriting  
        pngResult = os.getcwd()+"\\..\\png\\"+pathName+"{0}.png".format(i)
        print("Saving HTML file number {0}".format(i))
        #We save our map as the HTML file in the path given in htmlResult
        vMap.save(htmlResult)
        #We open the freshly created html
        browser.get("file:///"+htmlResult)
        #Give the map tiles some time to load
        time.sleep(5)
        #We take a screenshot of the browser and save it to a png file
        browser.save_screenshot(pngResult)
        #We save the file paths to the list pngFiles
        pngFiles.append(pngResult)
        #We use "i" as a way to order our files
        i+=1
    #We close the browser
    browser.quit()
    #images is a list where we will keep the png files opened
    images = []
    #We go through the screenshot and turn open them with imageio
    for filename in pngFiles:
        images.append(imageio.imread(filename))
        #We turn the images to our gif
    imageio.mimsave(os.getcwd()+"\\..\\Results\\"+pathName+".gif", images,fps=0.5)