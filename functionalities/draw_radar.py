import plotly.graph_objects as go
import pandas as pd
import numpy as np
def draw_radar(df9,df10, white_back2):



    # Remove rows with a nan
    df10 = df10[df9.Considerar_pais != 0]
    df10 = df10[np.logical_not(np.isnan(df10.Cluster))]
    df10 = df10.reset_index(drop=True)
    
    
    #Keep names
    names=list(df10.country)


      
    #Keep titles
    data_top = df10.head(1)
    var=data_top.iloc[1:1, 4:30].columns
    categories=list(var)

    nn=0
    for i in range(0,len(categories)):
      if 'Unnamed' in categories[i]:
        break
      nn=nn+1
    
    categories = categories[0:nn]
    
    #Keep values
    values = df10[categories]
    
    
    #Create figure
    fig = go.Figure()
    
    
    # Create dimensions                      
    for i in range(len(names)):
        fig.add_trace(go.Scatterpolar(
            r= values.loc[i],
            theta=categories,
            fill='none',
            name=names[i],
        ))
    
    



    if white_back2:
      fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, values.max()]
          )),
        #polar_bgcolor='rgba(255,255,255,0.5)',
        autosize=False,
        width=1200,
        height=800,
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="#000000"
      )
    else:
      fig.update_layout(
        polar=dict(
            radialaxis=dict(
            visible=True,
            range=[0, values.max()]
          )),
        polar_bgcolor='rgba(99,143,156,0.5)',
        autosize=False,
        width=1200,
        height=800,
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="#70BFFA"
      )
    return fig
    #fig.write_html('static/radar.html', auto_open=True)