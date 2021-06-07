# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 12:27:36 2020

@author: Daniel
"""

from sklearn.neighbors import NearestNeighbors
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import igraph as ig
from igraph import *
from plotly.graph_objs import *


#X = np.array([[-1, -1,3], [-2, -1,4], [-3, -2,5], [1, 1,6], [2, 1,7], [3, 2,8]])

def draw_vertex3d():

    file2='static/filtros.xlsx'
    
    #Read excel
    df3 = pd.read_excel(file2, sheet_name='Hoja1')
    df2 = pd.read_excel(file2, sheet_name='Cluster')
    df4 = pd.read_excel(file2, sheet_name='Vertex')
    
    #Create dataframes
    df9  = pd.DataFrame(df3)  #Dataframe for country names
    df = pd.DataFrame(df2)  #Dataframe for indicator values
    df11 = pd.DataFrame(df4)  #Dataframe for method and neighbors
    #df10 = df10.loc[:, ~df10.columns.str.contains('^Unnamed')]
    
    #df = pd.concat([df10, df11.reindex(df10.index)], axis=1)
    
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
    num=len(values_array)
    
    
    data = df11.rename_axis('ID').values
    nbrs = NearestNeighbors(n_neighbors=data[0,1], algorithm=data[0,0]).fit(values_array)
    distances, indices = nbrs.kneighbors(values_array)
    A=nbrs.kneighbors_graph(values_array).toarray()
    
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
    Zn=[layt[k][2] for k in range(N)]# z-coordinates
    Xe=[]
    Ye=[]
    Ze=[]
    for e in E:
        Xe+=[layt[e[0]][0],layt[e[1]][0], None]
        Ye+=[layt[e[0]][1],layt[e[1]][1], None]
        Ze+=[layt[e[0]][2],layt[e[1]][2], None]
    
    trace1=Scatter3d(x=Xe,
                   y=Ye,
                   z=Ze,
                   mode='lines',
                   line= dict(color='rgb(210,210,210)', width=1),
                   hoverinfo='none',
                   )
    trace2=Scatter3d(x=Xn,
                   y=Yn,
                   z=Zn,
                   mode='markers',
                   name='ntw',
                   marker=dict(symbol='circle',
                                            size=15,
                                            color=df['Cluster'],
                                            line=dict(color='rgb(50,50,50)', width=0.5)
                                            ),
                   text=labels,
                   hoverinfo='text',
                   )
    
    axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
              zeroline=False,
              showgrid=False,
              showticklabels=False,
              title=''
              )
    
    axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          visible=False,
          showticklabels=False,
          title=''
          )
    
    layout=Layout(
        showlegend=False,
        autosize=True,
        scene=dict(
             xaxis=dict(axis),
             yaxis=dict(axis),
             zaxis=dict(axis),
        ),
        margin=dict(
            t=100
        ),
        hovermode='closest',
        updatemenus=[dict(type='buttons',
         showactive=False,
         y=1,
         x=0.8,
         xanchor='left',
         yanchor='bottom',
         pad=dict(t=45, r=10),
         buttons=[dict(label='Play',
                        method='animate',
                        args=[None, dict(frame=dict(duration=100, redraw=True), 
                                                    transition=dict(duration=0),
                                                    fromcurrent=True,
                                                    mode='immediate'
                                                   )]
                                   )
                             ]
                     )
               ]
        )
    
    data=[trace1, trace2]
    fig=Figure(data=data, layout=layout)
    t = np.linspace(0, 10, 50)
    x, y, z = np.cos(t), np.sin(t), t
        
    def rotate_z(x, y, z, theta):
        w = x+1j*y
        return np.real(np.exp(1j*theta)*w), np.imag(np.exp(1j*theta)*w), z
    
   

    x_eye = -1.25
    y_eye = 2
    z_eye = 0.5
    frames=[]
    for t in np.arange(0, 6.26, 0.1):
        xe, ye, ze = rotate_z(x_eye, y_eye, z_eye, -t)
        frames.append(go.Frame(layout=dict(scene_camera_eye=dict(x=xe, y=ye, z=ze))))
    fig.frames=frames
    
    fig.write_html('vertex3d.html', auto_open=True)


