# Learn about API authentication here: https://plotly.com/python/getting-started
# Find your api_key here: https://plotly.com/settings/api

import chart_studio.plotly as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt

# Scientific libraries
import numpy as np
from scipy.optimize import curve_fit

def exponential_fit(fig,x,y,types_correlations):
    #x=x.to_numpy
    #y=y.to_numpy
    x1=x
    y1=y
    if ('linear' in types_correlations) or ('all' in types_correlations):
        n=2
    else:
        n=1
    def exponential_func(x, a, b):
        #return a*np.exp(b*x)
        return np.multiply(a,np.exp(np.multiply(b,x)))
    def exponential_func2(x, a, b,c,d):
        #return (a*np.exp(b*x) + c*np.exp(d*x)) 
        return np.add(np.multiply(a,np.exp((np.multiply(b,x)))) , np.multiply(c,np.exp(np.multiply(d,x))))

    def poly2_func(x, a, b,c):
        return np.add(np.add(a,np.multiply(b,x)),(np.multiply(c,np.power(x,2))))
    
    def poly3_func(x, a, b, c, d):
        return np.add(np.multiply(b,x) + np.multiply(c,np.power(x,2)) + np.multiply(d,np.power(x,3)),a)

    def logarithmic_func(x, a, b):
        return np.add(a,np.multiply(b,np.log(x)))

    def logistic_func(x, a, b, c):
        return np.divide(a,np.add(1,np.power(np.divide(x,b),c)))


    # def exponential_func(x, a, b, c):
    #     return a*np.exp(-b*x)+c
    
    # def exponential_func2(x, a, b, c):
    #     return a*np.exp(-b*x)+c

    # def poly2_func(x, a, b,c):
    #     return a + b*x + c*x^2
    
    # def poly3_func(x, a, b, c, d):
    #     return a + b*x + c*x^2 + d*x^3

    # def logarithmic_func(x, a, b):
    #     return a + b*np.log(x)

    # def logistic_func(x, a, b, c):
    #     return a/(1+(x/b)^c)  

    # def exponential_func(x, a, b, c):
    #     return np.add(np.multiply(a,np.exp(np.multiply(-b,x))),c)

    # def poly2_func(x, a, b,c):
    #     return np.add(np.add(a,np.multiply(b,x)),(np.multiply(c,np.power(x,2))))
    
    # def poly3_func(x, a, b, c, d):
    #     return a + np.multiply(b,x) + np.multiply(c,np.power(x,2)) + np.multiply(d,np.power(x,3))     
    if ('exponential' in types_correlations) or ('all' in types_correlations):
        try:
            x=x1
            y=y1
            popt, pcov = curve_fit(exponential_func, x, y, maxfev =10000)
            xx= np.linspace(min(x), max(x),1000)
            yy = exponential_func(xx, *popt)
            residuals = y-exponential_func(x,*popt)
            ss_res =np.sum(residuals**2)
            ss_tot = np.sum((y-np.mean(y))**2)
            r_squared = 1 - (ss_res/ss_tot)

            if((r_squared>float(0)) & (r_squared<float(1))):
                # Creating the dataset, and generating the plot
                trace2 = go.Scatter(
                                x=xx,
                                y=yy,
                                mode='lines',
                                marker=go.Marker(color='rgb(255, 0, 0)'),
                                name='Exponential'
                                )

                fig.add_traces(trace2)

                fig.data[n].name = fig.data[n].name  + "  R^2 = "+ str(round(r_squared,3))
                fig.data[n].showlegend = True
                n=n+1
        except Exception as e:
            print(e)
    if ('exponential' in types_correlations) or ('all' in types_correlations):
        try:
            x=x1
            y=y1
            popt, pcov = curve_fit(exponential_func2, x, y,  maxfev =5000)
            xx= np.linspace(min(x), max(x),1000)
            yy = exponential_func2(xx, *popt)
            residuals = y-exponential_func2(x,*popt)
            ss_res =np.sum(residuals**2)
            ss_tot = np.sum((y-np.mean(y))**2)
            r_squared = 1 - (ss_res/ss_tot)
            if((r_squared>float(0)) & (r_squared<float(1))):
                # Creating the dataset, and generating the plot
                trace2 = go.Scatter(
                                x=xx,
                                y=yy,
                                mode='lines',
                                marker=go.Marker(color='rgb(255, 0, 239)'),
                                name='Exponential'
                                )

                fig.add_traces(trace2)

                fig.data[n].name = fig.data[n].name  + "  R^2 = "+ str(round(r_squared,3))
                fig.data[n].showlegend = True
                n=n+1
        except Exception as e:
            print(e)

    if ('poly2' in types_correlations) or ('all' in types_correlations):
        try:
            x=x1
            y=y1
            popt, pcov = curve_fit(poly2_func, x, y,  maxfev =5000)
            xx= np.linspace(min(x), max(x),1000)
            yy = poly2_func(xx, *popt)
            residuals = y-poly2_func(x,*popt)
            ss_res =np.sum(residuals**2)
            ss_tot = np.sum((y-np.mean(y))**2)
            r_squared = 1 - (ss_res/ss_tot)

            if((r_squared>float(0)) & (r_squared<float(1))):
                # Creating the dataset, and generating the plot
                trace2 = go.Scatter(
                                x=xx,
                                y=yy,
                                mode='lines',
                                marker=go.Marker(color='rgb(0, 94, 255)'),
                                name='Poly2'
                                )


                fig.add_traces(trace2)

                fig.data[n].name = fig.data[n].name  + "  R^2 = "+ str(round(r_squared,3))
                fig.data[n].showlegend = True
                n=n+1
        except Exception as e:
            print(e)
    
    if ('poly3' in types_correlations) or ('all' in types_correlations):
        try:
            x=x1
            y=y1
            popt, pcov = curve_fit(poly3_func, x, y,  maxfev =5000)
            xx= np.linspace(min(x), max(x),1000)
            yy = poly3_func(xx, *popt)
            residuals = y-poly3_func(x,*popt)
            ss_res =np.sum(residuals**2)
            ss_tot = np.sum((y-np.mean(y))**2)
            r_squared = 1 - (ss_res/ss_tot)

            if((r_squared>float(0)) & (r_squared<float(1))):
                # Creating the dataset, and generating the plot
                trace2 = go.Scatter(
                                x=xx,
                                y=yy,
                                mode='lines',
                                marker=go.Marker(color='rgb(0, 255, 51)'),
                                name='Poly3'
                                )


                fig.add_traces(trace2)

                fig.data[n].name = fig.data[n].name  + "  R^2 = "+ str(round(r_squared,3))
                fig.data[n].showlegend = True
                n=n+1
        except Exception as e:
            print(e)
    if ('logarithmic' in types_correlations) or ('all' in types_correlations):
        try:
            x=x1
            y=y1
            popt, pcov = curve_fit(logarithmic_func, x, y,  maxfev =5000)
            xx= np.linspace(min(x), max(x),1000)
            yy = logarithmic_func(xx, *popt)
            residuals = y-logarithmic_func(x,*popt)
            ss_res =np.sum(residuals**2)
            ss_tot = np.sum((y-np.mean(y))**2)
            r_squared = 1 - (ss_res/ss_tot)

            if((r_squared>float(0)) & (r_squared<float(1))):
                # Creating the dataset, and generating the plot
                trace2 = go.Scatter(
                                x=xx,
                                y=yy,
                                mode='lines',
                                marker=go.Marker(color='rgb(66, 142, 0)'),
                                name='Logarithmic'
                                )


                fig.add_traces(trace2)

                fig.data[n].name = fig.data[n].name  + "  R^2 = "+ str(round(r_squared,3))
                fig.data[n].showlegend = True
                n=n+1
        except Exception as e:
            print(e)
    if ('logistic' in types_correlations) or ('all' in types_correlations):
        try:
            x=x1
            y=y1
            popt, pcov = curve_fit(logistic_func, x, y,  maxfev =5000)
            xx= np.linspace(min(x), max(x),1000)
            yy = logistic_func(xx, *popt)
            residuals = y-logistic_func(x,*popt)
            ss_res =np.sum(residuals**2)
            ss_tot = np.sum((y-np.mean(y))**2)
            r_squared = 1 - (ss_res/ss_tot)

            if((r_squared>float(0)) & (r_squared<float(1))):
                # Creating the dataset, and generating the plot
                trace2 = go.Scatter(
                                x=xx,
                                y=yy,
                                mode='lines',
                                marker=go.Marker(color='rgb(239, 255, 0)'),
                                name='Logistic'
                                )


                fig.add_traces(trace2)

                fig.data[n].name = fig.data[n].name  + "  R^2 = "+ str(round(r_squared,3))
                fig.data[n].showlegend = True
                n=n+1
        except Exception as e:
            print(e)

    return fig