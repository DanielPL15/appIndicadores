# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 13:39:38 2020

@author: José Félix
"""


import plotly.express as px
import pandas as pd
import os
    

def draw_map(df1,df10):
    # file2='C:\\Users\\José Félix\\Documents\\Test_gui_Matlab\\cluster_5_6_2020\\filtros.xlsx'
    # print(os.getcwd())
    df10 = df10[df1.Considerar_pais != 0]
    data_top = df10.head(1) #Extrae las cabeceras del dataframe
    var=data_top.iloc[1:1, 4:30].columns #Selecciona una parte del dataframe
    #el colum extrae nombres de columnas
    
    fig = px.choropleth(df10, locations="iso_alpha", 
                        color="Cluster", 
                        hover_data=var,
                        color_discrete_sequence= ['lightgrey','yellow','red',
                                                  'blue','lightgreen',
                                                  'lightsalmon','maroon'],
                        hover_name="country")

    fig.update_layout(
      autosize=False,
      width=1200,
      height=1200,
      coloraxis_showscale=False,
      paper_bgcolor='rgba(0,0,0,0)',
      font_color="#70BFFA"
    )
    return fig
    #fig.write_html('static/map.html', auto_open=True)





# draw_map()


# import plotly.express as px
# import pandas as pd
    

# def draw_map():
#     #file='C:\\Users\José Félix\Python\Datos.xlsx'
#     file2='C:\\Users\\José Félix\\Documents\\Test_gui_Matlab\\Python\\filtros.xlsx'
#     #df1 = pd.read_excel(file, sheet_name='Hoja2')
#     df2 = pd.read_excel(file2, sheet_name='Cluster')
    
#     # df10= pd.concat([df2.country, df2.iso_alpha, 
#     #                  df2.Cluster, df1.IDI, df1.ODS,df2.Cluster_name], axis=1)
#     df10=pd.DataFrame(df2)         
#     data_top = df10.head(1)
#     var=data_top.iloc[1:1, 4:30].columns
    
#     fig = px.choropleth(df10, locations="iso_alpha", 
#                         color="Cluster_name", 
#                         hover_data=var,
#                         color_discrete_sequence= ['lightgrey','yellow','red','blue'],
#                         hover_name="country")
#     #fig = px.choropleth(df, locations="iso_alpha", color="Cluster", hover_name="country", animation_frame="year", range_color=[20,80])
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#     fig.write_html('first_figure.html', auto_open=True)


###version funcionando antes de adaptar###
    
    # import plotly.express as px
    # import pandas as pd
    
    # file='C:\\Users\José Félix\Python\Datos.xlsx'
    # file2='C:\\Users\\José Félix\\Documents\\Test_gui_Matlab\\Python\\filtros.xlsx'
    # df1 = pd.read_excel(file, sheet_name='Hoja2')
    # df2 = pd.read_excel(file2, sheet_name='Cluster')
    
    # df10= pd.concat([df2.country, df2.iso_alpha, 
    #                  df2.Cluster, df1.IDI, df1.ODS,df2.Cluster_name], axis=1)
             
    # fig = px.choropleth(df10, locations="iso_alpha", 
    #                     color="Cluster_name", 
    #                     hover_data=["IDI", "ODS"],
    #                     color_discrete_sequence= ['lightgrey','yellow','red','blue'],
    #                     hover_name="country")
    # #fig = px.choropleth(df, locations="iso_alpha", color="Cluster", hover_name="country", animation_frame="year", range_color=[20,80])
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # fig.write_html('first_figure.html', auto_open=True)
    
    
    


#df = px.data.gapminder()
# fig = px.choropleth(df10, locations="iso_alpha", 
#                     category_orders="Cluster",
#                     color="Cluster", 
#                     hover_name="country",
#                     color_discrete_map

# {[1 0 0],[0 1 0],[0 0 1],[1 1 0]...
#                 [0.6353    0.0784    0.1843], [0 0 0],[0 1 1], [1 0 1]}
# color_discrete_sequence = ['green', 'yellow','red’, ‘black’]