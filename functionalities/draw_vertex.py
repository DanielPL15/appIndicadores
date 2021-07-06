# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 12:27:36 2020

@author: Daniel
"""

from sklearn.neighbors import NearestNeighbors
import pandas as pd
import igraph as ig
from igraph import *
# import jgrapht as jgrapht
from plotly.graph_objs import *
import numpy as np

#X = np.array([[-1, -1,3], [-2, -1,4], [-3, -2,5], [1, 1,6], [2, 1,7], [3, 2,8]])

def draw_vertex(df9,df,df11):
   
    #Variable for quantification
    data_top = df.head(1)
    var=data_top.iloc[1:1, 0:50].columns
    titles=list(var)
    long_df=len(titles)
    
    
    # Remove rows with a nan or with a 0 in Considerar_pais
    df = df[df9.Considerar_pais != 0]
    df = df[df['Cluster'].notna()]
    df = df.reset_index(drop=True)
     
    values_df = df[titles[4:long_df]]
    values_array= values_df.rename_axis('ID').values

    values_array = values_array[:, ~np.isnan(values_array).all(axis=0)]
    num=len(values_array)


    # num=0
    # for i in range(0,num_cols):
    #   if 'Unnamed' in values_array[i]:
    #     break
    #   num=num+1
    # values_array = values_array[:, [0,num]]
    
    
    data = df11.rename_axis('ID').values
    nbrs = NearestNeighbors(n_neighbors=int(data[0,1]), algorithm=data[0,0]).fit(values_array)
    distances, indices = nbrs.kneighbors(values_array)
    A=nbrs.kneighbors_graph(values_array).toarray()
    
    #G =  Graph()

    G = Graph()
    
    G.add_vertices(num)
    
    for i in range(num):
        for j in range(num):
            if (A[i,j]):
                G.add_edges([(i,j)])
            
    
    #G=ig.Graph.Read_GML('netscience.gml.txt')
    labels=df['country']
    N=len(labels)
    E=[e.tuple for e in G.es]# list of edges
    layt=G.layout('kk', dim=3) #kamada-kawai layout
    type(layt)
    
    
    #import plotly.plotly as py
    
    Xn=[layt[k][0] for k in range(N)]
    Yn=[layt[k][1] for k in range(N)]
    Xe=[]
    Ye=[]
    for e in E:
        Xe+=[layt[e[0]][0],layt[e[1]][0], None]
        Ye+=[layt[e[0]][1],layt[e[1]][1], None]
    
    trace1=Scatter(x=Xe,
                   y=Ye,
                   mode='lines',
                   line= dict(color='rgb(180,180,180)', width=1),
                   hoverinfo='none'
                   )
    trace2=Scatter(x=Xn,
                   y=Yn,
                   mode='markers',
                   name='ntw',
                   marker=dict(symbol='circle-dot',
                                            size=15,
                                            color=df['Cluster'],
                                            line=dict(color='rgb(50,50,50)', width=0.5)
                                            ),
                   text=labels,
                   hoverinfo='text',
                   hovertext=labels
                   )
    
    axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
              zeroline=False,
              showgrid=False,
              hola='',
              showticklabels=False,
              title=''
              )
    
    layout=Layout(
        showlegend=False,
        autosize=True,
        xaxis= {'visible':False},
        yaxis={'visible':False},
        hovermode='closest',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
        )
    
    data=[trace1, trace2]
    fig=Figure(data=data, layout=layout)

    fig.update_layout(
      autosize=False,
      width=700,
      height=700,
      paper_bgcolor='rgba(0,0,0,0)',
      font_color="#70BFFA"
    )

    return fig
    #fig.write_html('vertex2d.html', auto_open=True)