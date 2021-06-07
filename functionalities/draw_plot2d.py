from others.exponential_fit import exponential_fit
from others.read_indicator import read_indicator
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_2d(dd1,dd2,dd3,dd4,dd5,dd6):
    file2='static/filtros.xlsx'
    # Dataframe with name and values of indicators
    df = pd.DataFrame()
    df["country"] = read_indicator(dd1,dd2,"Pais")
    df["(x) "+dd3] = read_indicator(dd1,dd2,dd3)
    df["(y) "+dd6] = read_indicator(dd4,dd5,dd6)

    # Dataframe with the column of considerar_pais and Mostrar_etiqueta
    df1 = pd.read_excel(file2, sheet_name='Hoja1', engine='openpyxl')
    df_filter1 = df["(x) " + dd3].notna()
    df_filter2 = df["(y) " + dd6].notna()
    df_filter3 = (df1.Considerar_pais != 0)
    df_all_filters = (df_filter1 & df_filter2 & df_filter3)




    df_etiquetas = df1["Mostrar_etiqueta"]
    df_etiquetas = df_etiquetas[df_all_filters]
    df_etiquetas = df_etiquetas.reset_index(drop=True)

    filter_etiquetas = df_etiquetas!=1

    # Dataframe with the column of the Cluster that each country belongs to
    df2 = pd.read_excel(file2, sheet_name='Cluster', engine='openpyxl')
    df2[df2['Cluster'].isna()] = 0
    df2 = df2[df_all_filters]


    df = df[df_all_filters]
    df = df.reset_index(drop=True)





    df["label"]=df["country"]

    df_country = df["label"]
    df_country[filter_etiquetas]=""
    df["label"] = df_country


    # df.drop("country", inplace=True, axis=1)
    # df_etiquetas = df_etiquetas.reset_index(drop=True)
    # df_country = (df_country.country !=0)
    # df["country"] = df_country
    #df = px.df.tips()

    dict_hover = {"(x) "+dd3: True,"(y) "+dd6: True, "country": True, "label":False}
    fig = px.scatter(df, x="(x) "+dd3, y="(y) "+dd6, color=df2["Cluster"], text= "label", hover_name = "country", hover_data=dict_hover, trendline="ols")
    r_squared = px.get_trendline_results(fig).px_fit_results.iloc[0].rsquared
    slope = px.get_trendline_results(fig).iloc[0]["px_fit_results"].params
    slope = slope.tolist()
    # fig.update_layout(
    #     title_text= "R^2 = "+ str(r_squared)
    # )
    
    #fig.data[0].name = 'observations'

    #fig = exponential_fit(fig, df["(x) "+dd3], df["(y) "+dd6])

    fig.data[0].showlegend = False
    fig.data[1].name = fig.data[1].name  + "Linear  R^2 = "+ str(round(r_squared,3)) + " Slope = "+ str(round(slope[1],3))
    fig.data[1].showlegend = True
    fig.update(layout_coloraxis_showscale=False)


    
    fig.write_html('2DPlot.html', auto_open=True)