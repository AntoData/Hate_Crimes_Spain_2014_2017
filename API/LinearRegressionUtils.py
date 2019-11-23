'''
Created on 30 oct. 2019

@author: ingov
'''
from sklearn import linear_model
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import numpy as np


class LinearRegressionUtils:
    """
    We create this class that encapsulates the functionality to perform a linear regression 
    """
    def __init__(self,X,Y,X_name,Y_name):
        """
        This is the constructor of this class
        @param X: Data series that contains variable X for our linear regression
        @param Y: Data series that contains variable Y for our linear regression
        @param X_name: Variable X's name
        @param Y_name: Variable Y's name    
        """
        if(not isinstance(X,np.ndarray)):
            #We need to perform this transformation in order for our methods to work
            #We need to transform X in a numpy.array
            print("Variable X was not an instance of np.ndarray, performing transformation")
            self.__X = np.array(X)
        else:
            self.__X = X
        self.__Y = Y
        #We generate an object linear_model.LinearModel() to handle this linear regression
        self.__regr = linear_model.LinearRegression()
        try:
            self.__regr.fit(self.__X,self.__Y)
        except:
            #It may happen that our parameter X is not a 2D array, in which case
            #we can fix it using reshape(-1,1)
            print("Our variable X was not a 2D array, performing this transformation")
            self.__X = self.__X.reshape(-1,1)
            #Now that we have our variable X and Y added to our object, we use the method
            #"fit" from linear_model.LinearModel().fit() to generate this regression
            self.__regr.fit(self.__X,self.__Y)
        #We get the coeficient of correlation and add it to our object
        self.__coef = self.__regr.coef_
        print(self.__regr.coef_)
        #We get the predict values of Y for our initial X and add it to our object
        self.__Y_pred_default = self.__regr.predict(self.__X)
        #We use the method r2_score to get the value r2 of our variable Y and our predicted values Y
        self.__rsquare = r2_score(self.__Y, self.__Y_pred_default)
        self.__X_name = X_name
        self.__Y_name = Y_name
        
        
    @property
    def X(self):
        return self.__X
    
    @X.setter
    def X(self,x):
        self.__X = x
    
    @property
    def Y(self):
        return self.__Y
    
    @Y.setter
    def Y(self,y):
        self.__Y = y
    
    @property
    def X_name(self):
        return self.__X_name
    
    @X_name.setter
    def X_name(self,x_name):
        self.__X_name = x_name
    
    @property
    def Y_name(self):
        return self.__Y_name
    
    @Y_name.setter
    def Y_name(self,y_name):
        self.__Y_name = y_name
        
    @property
    def regr(self):
        return self.__regr
    
    @property
    def coef(self):
        return self.__coef
    
    @property
    def Y_pred_default(self):
        return self.__Y_pred_default
    
    @property
    def rsquare(self):
        return self.__rsquare
        
    def generate_Linear_Correlation_Graph(self,colour_scatter,colour_line,title):
        """
        This function generates a chart with a scatter plot of points for our X and Y values
        and a line that represents the our linear function and displays it
        @param colour_scatter: Color for the points in our scatter plot with the points representing
        the different values for our variables
        @param colour_line: colour for the line that represents our linear regression function
        @param title: title for our window    
        """
        #We generate our scatter plot with our variables X and Y
        plt.scatter(self.X, self.Y, color = colour_scatter )
        #We display our function for our linear regression
        plt.plot(self.X,self.Y_pred_default,color=colour_line)
        #We set the name of our variable X as the label for axis X
        plt.xlabel(self.X_name)
        #We set the name of our variable Y as the label for axis Y
        plt.ylabel(self.Y_name)
        #We set the parameter title as the title for the window where we display our chart
        plt.title(title)
        for i in range(0,len(self.__Y)):
            #We add a note that provides information about our points in the scatter plots
            #We use the name of the columns in our dataseries Y as the string to display in the
            #notes. We then display the note over the point (self.__X[i][0] gets the value
            #of variable X and self.__Y.iloc[i] gets the value of our variable Y
            plt.annotate(self.__Y.index[i], np.array((self.__X[i][0],self.__Y.iloc[i]))) 
        #We display the chart
        plt.show()
            
    def print_evaluation_for_rsquare(self):
        """
        This function get the value of variable R square for our regression and displays a message
        giving information about how strong the correlation is
        """
        print("R square is {0}".format(self.rsquare))
        if(self.rsquare == 1):
            print("There is a perfect correlation between our variables {0} and {1}".format(self.X_name,self.Y_name))
        elif(1 > self.rsquare >= 0.7):
            print("There is a very strong correlation between our variables {0} and {1}".format(self.X_name,self.Y_name))
        elif(0.7 > self.rsquare >= 0.5):
            print("There is strong correlation between our variables {0} and {1}".format(self.X_name,self.Y_name))
        elif(0.5 > self.rsquare > 0.3):
            print("There is correlation between our variables {0} and {1}".format(self.X_name,self.Y_name))
        elif(0.3 >= self.rsquare > 0):
            print("There is very weak correlation between our variables {0} and {1}".format(self.X_name,self.Y_name))
        elif(self.rsquare == 0):
            print("There is absolutely no correlation between our variables {0} and {1}".format(self.X_name,self.Y_name))
            
    def print_stats(self):
        """
        This function just prints several variables for our linear regression
        """
        print("Variable X represents {0}".format(self.X_name))
        print("Values:")
        print(self.X)
        print("Variable Y represents {0}".format(self.Y_name))
        print("Values:")
        print(self.Y)
        print("R square value is: {0}".format(self.rsquare))