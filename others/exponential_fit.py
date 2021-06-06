# Learn about API authentication here: https://plotly.com/python/getting-started
# Find your api_key here: https://plotly.com/settings/api

import chart_studio.plotly as py
import plotly.graph_objs as go

# Scientific libraries
import numpy as np
from scipy.optimize import curve_fit

def exponential_fit(fig,x,y):
    x=x.to_numpy
    y=y.to_numpy
    def exponential_func(x, a, b, c):
        return a*np.exp(-b*x)+c

    def poly2_func(x, a, b,c):
        return a + b*x + c*x^2
    
    def poly3_func(x, a, b, c, d):
        return a + b*x + c*x^2 + d*x^3

    def logarithmic_func(x, a, b):
        return a + b*np.log(x)

    def logistic_func(x, a, b, c):
        return a/(1+np.exp(-b*(x-c)))        

    try:
        popt, pcov = curve_fit(exponential_func, x, y,[0,0,0], maxfev=10000000000)

        xx = np.linspace(min(x), max(x), 1000)
        yy = exponential_func(xx, *popt)
        residuals = yy-exponential_func(xx,*popt)
        ss_res =np.sum(residuals**2)
        ss_tot = np.sum((yy-np.mean(yy))**2)
        r_squared = 1 - (ss_res/ss_tot)

        # Creating the dataset, and generating the plot
        trace2 = go.Scatter(
                        x=xx,
                        y=yy,
                        marker=go.Marker(color='rgb(31, 119, 180)'),
                        name='Exponential'
                        )

        fig.add_traces(trace2)

        fig.data[2].name = fig.data[2].name  + "  R^2 = "+ str(round(r_squared,3))
        fig.data[2].showlegend = True
    except:
        print("")
    try:
        popt, pcov = curve_fit(poly2_func, x, y,[0,0,0], maxfev=1000000000)

        xx = np.linspace(min(x), max(x), 1000)
        yy = poly2_func(xx, *popt)

        # Creating the dataset, and generating the plot
        trace2 = go.Scatter(
                        x=xx,
                        y=yy,
                        marker=go.Marker(color='rgb(31, 119, 180)'),
                        name='Poly2'
                        )


        fig.add_traces(trace2)
    except:
        print("")
    try:
        popt, pcov = curve_fit(poly3_func, x, y,[0,0,0,0], maxfev=100000000)

        xx = np.linspace(min(x), max(x), 1000)
        yy = poly3_func(xx, *popt)

        # Creating the dataset, and generating the plot
        trace2 = go.Scatter(
                        x=xx,
                        y=yy,
                        marker=go.Marker(color='rgb(31, 119, 180)'),
                        name='Poly3'
                        )


        fig.add_traces(trace2)
    except:
        print("")

    try:
        popt, pcov = curve_fit(logarithmic_func, x, y,[0,0,0], maxfev=10000000)

        xx = np.linspace(min(x), max(x), 1000)
        yy = logarithmic_func(xx, *popt)

        # Creating the dataset, and generating the plot
        trace2 = go.Scatter(
                        x=xx,
                        y=yy,
                        marker=go.Marker(color='rgb(31, 119, 180)'),
                        name='Logarithmic'
                        )


        fig.add_traces(trace2)
    except:
        print("")

    try:
        popt, pcov = curve_fit(logistic_func, x, y,[0,0,0,0], maxfev=10000000)

        xx = np.linspace(min(x), max(x), 1000)
        yy = logistic_func(xx, *popt)

        # Creating the dataset, and generating the plot
        trace2 = go.Scatter(
                        x=xx,
                        y=yy,
                        marker=go.Marker(color='rgb(31, 119, 180)'),
                        name='Logistic'
                        )


        fig.add_traces(trace2)
    except:
        print("")

    return fig