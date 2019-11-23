'''
Created on 30 oct. 2019

@author: ingov
'''
import pandas as pd

def getDataFrameReady(crime,columnNameToJoin,pathForProvinces,regularExpresionForExcelFiles):
    dfprovinces = pd.read_excel(pathForProvinces)
    df = dfprovinces
    for i in range(2014,2018):
        print(i)
        df1 = pd.read_excel(regularExpresionForExcelFiles+"{0}.xlsx".format(i))
        df1 = df1[[columnNameToJoin,crime]]
        df1.columns = [columnNameToJoin,i]
        #df1.columns = [2014]
        df = df.merge(df1,on=columnNameToJoin).set_index(columnNameToJoin)
    return df