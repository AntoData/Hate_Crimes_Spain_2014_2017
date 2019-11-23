'''
Created on 13 nov. 2019

@author: ingov
'''
#We import the module matplotlib.pyplot so we can use to create and display our charts
import matplotlib.pyplot as plt
"""
This lambda function determines how and when the labels inside the portions of our pie charts
are displayed. Basically we will display the label (expected to be a float) as x.xx% if it is
greater than 5 only
@param pct: the label for the portion in which the pie chart is divided
@return string: x.xx% if it isgreater than 5 or "" if not
"""
mylambdapct = lambda pct: "{0}%".format(round(pct, 2)) if pct > 5 else ''


def piePlotImproved(df,labels,windowTitle,autopct): 
    """
    This function given a dataframe df, the labels to be displayed in labels, a title for the
    window in which we will display the pie chart in windowTitle and function in autopct to 
    control when and how labels inside the portions of the pie chart are displayed, generates
    a figure object and an axis object that contain a pie chart with the parameters described
    previously. Our dataframe df is expected to have just a column and the index or to be a 
    dataseries
    @param df: dataframe for our pie chart
    @param labels: external labels to be displayed
    @param windowTitle: string with a title for the window in which we will display our chart
    @param autopct: function that will determine which and how internal labels are displayed
    inside the portions of our pie chart
    @return figure,axis: We return this tuple of object figure and axis with our chart 
    """
    #We first generate our figure and axis objects fig and axs respectively creating a 1,1 subplot
    #which is basically just a subplot with one chart, just a chart
    fig, axs = plt.subplots(1, 1)
    #If we did not provide labels, we won't use them when calling the method axis.pie
    if labels is None:
        axs.pie(df,autopct=autopct)
    #If we did we call the same method but we include the parameter labels so our labels
    #are displayed
    else:
        axs.pie(df,labels=labels,autopct=autopct)
    #If we gave a window title (in other words our parameter windowTitle is not "" which is 
    #nothing or it is not None) we have to call figure.canvas.set_window_title to provide
    #a title for the window where our chart will be displayed
    if windowTitle != "" or windowTitle is not None:
        fig.canvas.set_window_title(windowTitle)
    #This function makes our layout tight so elements don't interfere or block each other
    fig.tight_layout()
    #We return our object figure fig and axis axs so our chart can be plotted
    return fig,axs

def barPlotWithMean(x,height,mean,windowTitle,xlabel,ylabel,figName):
    """
    This function will generate an object figure and axis for our bar chart with a line displaying
    the mean value of our variables
    @param x: Values to represent in our axis x (rows or different variables to represent)
    @param height: Values to present in our axis y
    @param mean: mean value of our variables to represent   
    @param windowTitle: The title for the window where we will display our chart
    @param xlabel: Label for our axis x
    @param ylabel: label for our axis y
    @param figname: Title for our chart to be displayed
    @return figure,axis: We return this tuple of object figure and axis with our chart 
    """
    #We generate the object figure and axis as fig and axs respectively using plt.subplots(1,1)
    #which basically creates a subplot, a unique plot
    fig, axs = plt.subplots(1, 1)
    #We generate the bar chart
    axs.bar(x,height)
    #We add the line with our mean value to our chart
    axs.hlines(mean,-1,len(x)-1,colors="red",label="mean")
    #We add a note that states that line we created previously is the mean value
    axs.annotate("MEAN", ((len(x))/2,mean+2),color="red")
    #We rotate our label for axis x
    plt.xticks(rotation=90)
    #We use fig.tight_layout() to make all our labels, charts, ... fit in our window
    fig.tight_layout()
    #If the parameter windowTitle is not "" or is not None, we use it as the title of our window
    if windowTitle != "" or windowTitle is not None:
        fig.canvas.set_window_title(windowTitle)
        
    #If the parameter xlabel is not "" or is not None, we use it as the label of our axis x
    if xlabel != "" or xlabel is not None:
        axs.set_xlabel(xlabel)
        
    #If the parameter ylabel is not "" or is not None, we use it as the label of our axis y
    if ylabel != "" or ylabel is not None:
        axs.set_ylabel(ylabel)
    
    #If the parameter figName is not "" or is not None, we use it as the label of our chart
    if figName != "" or figName is not None:
        axs.set_title(figName)
    #We return the objects fig and axs that are our bar chart
    return fig,axs

