# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 18:32:10 2020

@author: José Félix
"""


import plotly.graph_objects as go
import pandas as pd
import numpy as np


def draw_parallel(df1,df10,df11):

    
    # Remove rows with a nan
    df10 = df10[df1.Considerar_pais != 0]
    df10 = df10[np.logical_not(np.isnan(df10.Cluster))]
    df10 = df10.reset_index(drop=True)
    df11 = df11[df1.Considerar_pais != 0]
    df11 = df11[np.logical_not(np.isnan(df11.Cluster))]
    df11 = df11.reset_index(drop=True)
    
    data_top = df10.head(1)
    var=data_top.iloc[1:1, 4:30].columns
    var2=list(var)
    nn=0
    for i in range(0,len(var2)):
      if 'Unnamed' in var2[i]:
        break
      nn=nn+1
    
    # Create dimensions
    dim_var =[]                           
    for i in range(nn):
        orden1=df10.sort_values(by=[var2[i]], ascending=False).index.values
        orden2=df11.iloc[orden1,4+i]
        dim_var.insert(0,go.parcats.Dimension(values=df11.iloc[:,4+i], label=var2[i],
                                   categoryarray=orden2,
                                   categoryorder='array'))
                                 
    # # Create parcats trace
    color = df10.Cluster
    # colorscale = [[0, 'lightsteelblue'], [1, 'mediumseagreen']];
    # colorscale= ['lightgrey','yellow','red',
    #             'blue','lightgreen',
    #             'lightsalmon','maroon']
    
    fig = go.Figure(data = [go.Parcats(dimensions=dim_var,
              line={'color': color, 'colorscale': 'viridis', 'shape': 'hspline'},
              hoveron='color', hoverinfo='count',
              labelfont={'size': 14, 'family': 'Arial'},
              tickfont={'size': 10, 'family': 'Arial'},
              sortpaths='forward',
              arrangement='freeform')])
    fig.update_layout(
      autosize=False,
      width=1200,
      height=600,
      paper_bgcolor='rgba(0,0,0,0)',
      font_color="#70BFFA"
    )
    return fig
    
    #fig.write_html('static/parallel.html', auto_open=True)