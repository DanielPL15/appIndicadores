# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 17:37:44 2021

@author: Daniel Peña
"""


from functionalities.draw_plot2d import plot_2d
from others.read_indicator_sunburst import read_indicator_sunburst
from dash_html_components.Div import Div
from dash_html_components.Spacer import Spacer
import pandas as pd
import dash_bootstrap_components as dbc
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import ALL, State, MATCH, ALLSMALLER, Input, Output, State
import plotly.express as px
from functionalities.draw_radar import draw_radar
from functionalities.draw_parallel import draw_parallel
from functionalities.draw_sunburst import draw_sunburst
from functionalities.draw_map import draw_map
from functionalities.draw_vertex import draw_vertex
# from functionalities.draw_vertex import draw_vertex
import dash_auth
import xlrd
import openpyxl
from others.write_excel import *
import glob
import ntpath
import random
import dash_table

df = pd.read_excel("indicators/ODS2020.xlsx", engine='openpyxl')

file2='filtros.xlsx'
df1 = pd.read_excel(file2, sheet_name='Hoja1', engine='openpyxl')
df2 = pd.read_excel(file2, sheet_name='Cluster', engine='openpyxl')
df3 = pd.read_excel(file2, sheet_name='Parallel', engine='openpyxl')

# Creation of a list of dictionaries. Each of them with the name and ID of one country
df6 = df1[['NUESTRO_ID','country']]
df6.rename(columns = {'NUESTRO_ID' : 'value', 'country' : 'label'}, inplace = True)
df6_dict = df6.to_dict('records')

# Names of the excel files
file_list_path = glob.glob("indicators/*.xlsx")
n=0
file_list=[]
for i in file_list_path:
    file_list.append(ntpath.basename(i))
    n=n+1

# Default values for dropdows
df_file_list = pd.DataFrame({'label':file_list,'value':file_list_path})
df_file_list_dict = df_file_list.to_dict('records')


book = openpyxl.load_workbook('indicators/ODS2020.xlsx')
default_sheets = book.sheetnames
df_default_sheets = pd.DataFrame({'label':default_sheets,'value':default_sheets})
df_default_sheets_dict = df_default_sheets.to_dict('records')

df_aux = pd.read_excel("indicators/ODS2020.xlsx", sheet_name='Hoja1', engine='openpyxl')
default_indicators = list(df_aux.columns)[2:]
df_default_indicators = pd.DataFrame({'label':default_indicators,'value':default_indicators})
df_default_indicators_dict = df_default_indicators.to_dict('records')


# DataFrame with file, sheet and indicator

# Dictionary with the variables for the cluster: contains file, sheet and indicator name
cluster_variables_dict={}
cluster_variables_list=[]


options_method_vertex = pd.DataFrame({'label':['Auto','Ball Tree','KD tree','Brute'],'value':['auto','ball_tree','kd_tree','brute']})
options_method_vertex = options_method_vertex.to_dict('records')

options_neigh_vertex = pd.DataFrame({'label':['1','2','3','4','5','6','7'],'value':['1','2','3','4','5','6','7']})
options_neigh_vertex = options_neigh_vertex.to_dict('records')


# you need to include __name__ in your Dash constructor if
# you plan to use a custom CSS or JavaScript in your Dash apps
app = dash.Dash(__name__,  external_stylesheets=[dbc.themes.SUPERHERO], suppress_callback_exceptions=True)

server = app.server

auth = dash_auth.BasicAuth(
    app,
    {'dani': '1234',
    'josefelix':'1234'}
    )   


# Content of Filter Tab
def filter_tab():

    return html.Div([
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H5('Considered countries'),
                        html.Button('Save', id='save_considered', className='btn btn-secondary', n_clicks=0),
                        dbc.Toast(
                            "Saved correctly",
                            id="toast_saved",
                            is_open=False,
                            dismissable=True,
                            duration=2500,
                            icon="success"),
                    ],
                    width={'size': True, 'offset': 1}
                ),
                dbc.Col(
                    [
                        html.H5('Desired country labels'),
                        html.Button('Save', id='save_desired', className='btn btn-secondary', n_clicks=0),
                        dbc.Toast(
                            "Saved correctly",
                            id="toast_desired",
                            is_open=False,
                            dismissable=True,
                            duration=2500,
                            icon="success"),
                    ],
                    width={'size': True, 'offset': 1}
                )
            ],align='start'),
        dbc.Row(
            [
                dbc.Col(dbc.Checklist(id='ckl_considered',
                                    options= df6_dict,
                                    className='container p-3 my-3 border'
                                    ),
                        width={'size': 3, 'offset': 1},
                ),
                dbc.Col(dbc.Checklist(id='ckl_desired',
                                    options= df6_dict,
                                    className='container p-3 my-3 border'
                                    ),
                        width={'size': 3, 'offset': 3},
                )                
            ],
        align='center')

    ])
# Content of Cluster Tab
def cluster_tab():
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H5('Select Cluster variables', style={'padding':'10px','background-color':'#06619e'}),
                dcc.Dropdown(
                    id='dropdown_file_cluster',
                    options=df_file_list_dict,
                    className="dropbtn",
                    value='indicators\ODS2020.xlsx',
                    placeholder='Select a group of indicators',
                    clearable=False,
                ),
                dcc.Dropdown(
                    id='dropdown_sheet_cluster',
                    options=df_default_sheets_dict,
                    className="dropbtn",
                    value='Hoja1',
                    placeholder='Select a subgroup of indicators',
                    clearable=False,
                ),
                dcc.Dropdown(
                    id='dropdown_indicator_cluster',
                    options=df_default_indicators_dict,
                    className="dropbtn",
                    value='2020 Global Index Score (0-100)',
                    placeholder='Select an indicator',
                    clearable=False,
                ),
                html.Div([
                    html.Div([
                        dbc.Button(
                            'Add Variable',
                            id="confirm_variable_cluster",
                            className='primary',
                            n_clicks=0,
                        )],
                         style={'padding':5,'width': '33%', 'display': 'inline-block'},
                        ),
                    html.Div([
                        dbc.Button(
                            'Clear List',
                            id="clear_variable_list",
                            className='primary',
                            n_clicks=0,
                        )],
                        style={'padding':5,'width': '33%', 'display': 'inline-block'},
                        ),
                    html.Div([
                        dbc.Button(
                            'Make Cluster',
                            id="make_cluster_button",
                            className='primary',
                            n_clicks=0,
                        )],
                        style={'padding':5,'width': '33%', 'display': 'inline-block'}
                    )],
                style={'padding':20}),
                ],
                width={'size': 4, 'offset': 0}),
            dbc.Col([
                html.H5('List of Cluster variables', style={'padding':'10px','background-color':'#06619e'}),
                dbc.ListGroup(
                    id='list_variables_cluster'
                    )
                ],   
                width={'size': 2, 'offset': 0}),
            dbc.Col([
                html.Div(
                        id = 'future_table_of_clusters',
                        children = []
                    )
                ],
                width={'size': 5, 'offset': 0}),
        ]),
    ], style={'padding':20})
# Content of Plot Tab
def plot_tab():
    return html.Div([
            dbc.Row([
                    dbc.Col([
                    html.Div(
                        id = 'menu_plot2D',
                            children = [html.H3('Plot a 2D graphic', style={'padding':'10px','background-color':'#06619e'}),
                            html.Div([
                                    html.H5('Variable in x', style={'padding':'10px','background-color':'#06619e'}),
                                    dcc.Dropdown(
                                        id='dropdown_file_x',
                                        options=df_file_list_dict,
                                        className="dropbtn",
                                        value='indicators\ODS2020.xlsx',
                                        placeholder='Select a group of indicators',
                                        clearable=False,
                                    ),
                                    dcc.Dropdown(
                                        id='dropdown_sheet_x',
                                        options=df_default_sheets_dict,
                                        className="dropbtn",
                                        value='Hoja1',
                                        placeholder='Select a subgroup of indicators',
                                        clearable=False,
                                    ),
                                    dcc.Dropdown(
                                        id='dropdown_indicator_x',
                                        options=df_default_indicators_dict,
                                        className="dropbtn",
                                        value='2020 Global Index Score (0-100)',
                                        placeholder='Select an indicator',
                                        clearable=False,
                                    ),
                            ],
                            style={'padding':5}),
                                html.Div([
                                    html.H5('Variable in y', style={'padding':'10px','background-color':'#06619e'}),
                                    dcc.Dropdown(
                                        id='dropdown_file_y',
                                        options=df_file_list_dict,
                                        className="dropbtn",
                                        value='indicators\ODS2020.xlsx',
                                        placeholder='Select a group of indicators',
                                        clearable=False,
                                    ),
                                    dcc.Dropdown(
                                        id='dropdown_sheet_y',
                                        options=df_default_sheets_dict,
                                        className="dropbtn",
                                        value='Hoja1',
                                        placeholder='Select a subgroup of indicators',
                                        clearable=False,
                                    ),
                                    dcc.Dropdown(
                                        id='dropdown_indicator_y',
                                        options=df_default_indicators_dict,
                                        className="dropbtn",
                                        value='2020 Global Index Score (0-100)',
                                        placeholder='Select an indicator',
                                        clearable=False,
                                    ),
                                ],
                            style={'padding':5}),
                            html.Div(
                                html.Button('Plot', id='submit_plot2D', className='btn btn-secondary btn-lg btn-block', n_clicks=0),
                            style={'padding':5, 'textAlign': 'center'}),
                        ],
                        style={'padding':5}),
                    ],
                    width={'size': 3,  "offset": 0}),
                dbc.Col([
                    html.Div([
                        html.H3('Variables for Vertex', style={'padding':'10px','background-color':'#06619e'}),
                        dcc.Dropdown(
                            id='method_vertex',
                            options=options_method_vertex,
                            className="dropbtn",
                            value='Hoja1',
                            placeholder='Select a method',
                            clearable=False,
                        ),
                        dcc.Dropdown(
                            id='dropdown_indicator_cluster',
                            options=options_neigh_vertex,
                            className="dropbtn",
                            value='2020 Global Index Score (0-100)',
                            placeholder='Select Number of Neighbors',
                            clearable=False,
                        ),
                        html.Div(
                        html.Button('Plot 2D', id='submit_vertex', className='btn btn-secondary btn-lg btn-block', n_clicks=0),
                        style={'padding':5, 'textAlign': 'center'}),
                        html.Div(
                        html.Button('Plot 3D', id='submit_vertex3d', className='btn btn-secondary btn-lg btn-block', n_clicks=0),
                        style={'padding':5, 'textAlign': 'center'}),
                    ],
                    style={'padding':5})
                ],
                width={'size': 3,  "offset": 0}),
                dbc.Col(
                        html.Div([
                            html.H3('Sunburst', style={'padding':'10px','background-color':'#06619e'}),
                            dcc.Dropdown(
                                id='dropdown_file_sunburst',
                                options=df_file_list_dict,
                                className="dropbtn",
                                value='indicators\ODS2020.xlsx',
                                placeholder='Select a group of indicators',
                                clearable=False,
                            ),
                            dcc.Dropdown(
                                id='dropdown_sheet_sunburst',
                                options=df_default_sheets_dict,
                                className="dropbtn",
                                value='Hoja1',
                                placeholder='Select a subgroup of indicators',
                                clearable=False,
                            ),
                            dcc.Dropdown(
                                id='dropdown_indicator_sunburst',
                                options=df_default_indicators_dict,
                                className="dropbtn",
                                value='2020 Global Index Score (0-100)',
                                placeholder='Select an indicator',
                                clearable=False,
                            ),
                            html.Div(
                            html.Button('Plot', id='submit_sunburst', className='btn btn-secondary btn-lg btn-block', n_clicks=0),
                            style={'padding':5, 'textAlign': 'center'}),
                        ],
                        style={'padding':5}),
                        width={'size': 3,  "offset": 0}),
                html.Div([
                    html.H3('Other graphics', style={'padding':'10px','background-color':'#06619e'}),
                    html.Div(
                    dbc.Col(html.Button('Map', id='submit_map', className='btn btn-secondary', n_clicks=0),
                        width={'size': 1,  "offset": 0}),
                    style={'padding':5}),
                    html.Div(
                    dbc.Col(html.Button('Parallel', id='submit_parallel', className='btn btn-secondary', n_clicks=0),
                        width={'size': 1,  "offset": 0}),
                    style={'padding':5}),
                    html.Div(
                    dbc.Col(html.Button('Radar', id='submit_radar', className='btn btn-secondary', n_clicks=0),
                        width={'size': 1,  "offset": 0}),
                    style={'padding':5}),
                ],style={'padding':5}),
        ]),
        dbc.Row(
            dbc.Col(
                html.Div(id='container', children=[]),
                width={'size': 4,  "offset": 6})),
    ])

#---------------------------------------------------------------
app.layout = html.Div([
    dbc.Row(dbc.Col(html.H1("Analysis of composite indicators"),width={'size':12,"offset":3})),
    html.Div([
        dbc.Tabs(id='tabs-example', active_tab='About', className="nav nav-tabs", children=[
        dbc.Tab(label='About', tab_id='About', className='nav-link active'),
        dbc.Tab(label='Filter', tab_id='Filter', className='nav-link active'),
        dbc.Tab(label='Cluster', tab_id='Cluster', className='nav-link active'),
        dbc.Tab(label='Plot', tab_id='Plot', className='nav-link active'),
        ]),
        html.Div(id='tabs-example-content'),
    ])
])

#---------------------------------------------------------------
# Callback for the tab menu
@app.callback(Output('tabs-example-content', 'children'),
              Input('tabs-example', 'active_tab'))
def render_content(tab):
    if tab == 'About':
        return dbc.Row(dbc.Col(html.Div(children=[
                    html.P('This application allows you to compare composite indicators.'),
                    html.P('Steps to use the app:'),
                    html.P("1.    In the filter tab: Choose the countries you want to analize"),
                    html.P("2.    In the cluster tab: You can create clusters of countries according to indicators you select. You can visualize them graphically in some of the representations of the Plot Tab"),
                    html.P("3.    In the plot tab: Vizualize graphics of the parameters chosen before"),
                    ],
                style={'padding': 20}),
            width={'size': 12,  "offset":0})
        )
    elif tab == 'Filter':
        return filter_tab()
    elif tab== 'Cluster':
        return cluster_tab()
    elif tab== 'Plot':
        return plot_tab()

#Callback for the Buttons inside filter tab
@app.callback(
    Output(component_id='toast_saved', component_property='is_open'),
    [Input(component_id='save_considered', component_property='n_clicks'),
     Input(component_id='ckl_considered', component_property='value')]
)

def update_graph(bt1,value):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'save_considered' in changed_id:
        l_aux = [int(0)]*int(max(df1.NUESTRO_ID)) 
        if value: # Check if Checklist is empty
            for i in value:
                l_aux[i-1]=1 # Assign one to selected countries
        df_aux=pd.DataFrame(l_aux)
        write_excel(df_aux,file2,'Hoja1',1,2)
        return True
    return False
@app.callback(
    Output(component_id='toast_desired', component_property='is_open'),
    [Input(component_id='save_desired', component_property='n_clicks'),
     Input(component_id='ckl_desired', component_property='value')]
)

def update_graph(bt1,value):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'save_desired' in changed_id:
        l_aux = [int(0)]*int(max(df1.NUESTRO_ID))
        if value: # Check if Checklist is empty
            for i in value:
                l_aux[i-1]=1 # Assign one to selected countries
        df_aux=pd.DataFrame(l_aux)
        write_excel(df_aux,file2,'Hoja1',1,3)
        return True
    return False


# Callbacks for the Dropdowns in the Cluster tab

# When you choose a different file or sheet you want to see the corresponding new sheets and indicators
@app.callback(
    [Output(component_id='dropdown_sheet_cluster', component_property='options'),
    Output(component_id='dropdown_sheet_cluster', component_property='value'), 
    Output(component_id='dropdown_indicator_cluster', component_property='options'),
    Output(component_id='dropdown_indicator_cluster', component_property='value')],
    [Input(component_id='dropdown_file_cluster', component_property='value'),
    Input(component_id='dropdown_sheet_cluster', component_property='value')]
)
def update_dd1(dd1,dd2):
    # Obtain dic with sheets from current selected file and a random value to
    wb=openpyxl.load_workbook(dd1)
    a=wb.sheetnames
    df_sheets_dict = pd.DataFrame({'label':a,'value':a}).to_dict('records')
    value_sheets = random.choice(a)

    # Obtain dic with the indicators of the current selected sheet
    df_aux = pd.read_excel(dd1, sheet_name=dd2, engine='openpyxl')
    a=list(df_aux.columns)[2:]
    df_indicators_dict =pd.DataFrame({'label':a,'value':a}).to_dict('records')
    value_indicators = random.choice(a)
    return df_sheets_dict, value_sheets, df_indicators_dict, value_indicators


# Callbacks for the Dropdowns in the Plot tab

# Plot 2D: x axis
# When you choose a different file or sheet you want to see the corresponding new sheets and indicators
@app.callback(
    [Output(component_id='dropdown_sheet_x', component_property='options'),
    Output(component_id='dropdown_sheet_x', component_property='value'), 
    Output(component_id='dropdown_indicator_x', component_property='options'),
    Output(component_id='dropdown_indicator_x', component_property='value')],
    [Input(component_id='dropdown_file_x', component_property='value'),
    Input(component_id='dropdown_sheet_x', component_property='value')]
)
def update_dd1(dd1,dd2):
    # Obtain dic with sheets from current selected file and a random value to
    wb=openpyxl.load_workbook(dd1)
    a=wb.sheetnames
    df_sheets_dict = pd.DataFrame({'label':a,'value':a}).to_dict('records')
    value_sheets = random.choice(a)

    # Obtain dic with the indicators of the current selected sheet
    df_aux = pd.read_excel(dd1, sheet_name=dd2, engine='openpyxl')
    a=list(df_aux.columns)[2:]
    df_indicators_dict =pd.DataFrame({'label':a,'value':a}).to_dict('records')
    value_indicators = random.choice(a)
    return df_sheets_dict, value_sheets, df_indicators_dict, value_indicators

# Plot 2D: y axis
# When you choose a different file or sheet you want to see the corresponding new sheets and indicators
@app.callback(
    [Output(component_id='dropdown_sheet_y', component_property='options'),
    Output(component_id='dropdown_sheet_y', component_property='value'), 
    Output(component_id='dropdown_indicator_y', component_property='options'),
    Output(component_id='dropdown_indicator_y', component_property='value')],
    [Input(component_id='dropdown_file_y', component_property='value'),
    Input(component_id='dropdown_sheet_y', component_property='value')]
)
def update_dd1(dd1,dd2):
    # Obtain dic with sheets from current selected file and a random value to
    wb=openpyxl.load_workbook(dd1)
    a=wb.sheetnames
    df_sheets_dict = pd.DataFrame({'label':a,'value':a}).to_dict('records')
    value_sheets = random.choice(a)

    # Obtain dic with the indicators of the current selected sheet
    df_aux = pd.read_excel(dd1, sheet_name=dd2, engine='openpyxl')
    a=list(df_aux.columns)[2:]
    df_indicators_dict =pd.DataFrame({'label':a,'value':a}).to_dict('records')
    value_indicators = random.choice(a)
    return df_sheets_dict, value_sheets, df_indicators_dict, value_indicators

# Sunburst
# When you choose a different file or sheet you want to see the corresponding new sheets and indicators
@app.callback(
    [Output(component_id='dropdown_sheet_sunburst', component_property='options'),
    Output(component_id='dropdown_sheet_sunburst', component_property='value'), 
    Output(component_id='dropdown_indicator_sunburst', component_property='options'),
    Output(component_id='dropdown_indicator_sunburst', component_property='value')],
    [Input(component_id='dropdown_file_sunburst', component_property='value'),
    Input(component_id='dropdown_sheet_sunburst', component_property='value')]
)
def update_dd1(dd1,dd2):
    # Obtain dic with sheets from current selected file and a random value to
    wb=openpyxl.load_workbook(dd1)
    a=wb.sheetnames
    df_sheets_dict = pd.DataFrame({'label':a,'value':a}).to_dict('records')
    value_sheets = random.choice(a)

    # Obtain dic with the indicators of the current selected sheet
    df_aux = pd.read_excel(dd1, sheet_name=dd2, engine='openpyxl')
    a=list(df_aux.columns)[2:]
    df_indicators_dict =pd.DataFrame({'label':a,'value':a}).to_dict('records')
    value_indicators = random.choice(a)
    return df_sheets_dict, value_sheets, df_indicators_dict, value_indicators

# # Add a variable to the cluster list

@app.callback(
    [Output(component_id='list_variables_cluster', component_property='children')],
    [Input(component_id='confirm_variable_cluster', component_property='n_clicks'),
    Input(component_id='clear_variable_list', component_property='n_clicks'),
    State(component_id='dropdown_file_cluster', component_property='value'),
    State(component_id='dropdown_sheet_cluster', component_property='value'),
    State(component_id='dropdown_indicator_cluster', component_property='value'),
    State('list_variables_cluster','children')]
)

def update_list_cluster(bt1,bt2,file_chosen,sheet_chosen,indicator_chosen, listChildren):
    
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id not in ['confirm_variable_cluster', 'clear_variable_list']:
        raise dash.exceptions.PreventUpdate
    else:
        if not listChildren:
            df_for_list_cluster_variable = pd.DataFrame()
            listChildren = []
        if button_id == 'clear_variable_list':
            return [[]]
        listChildren.append(dbc.ListGroupItem(indicator_chosen))
        #write_excel(pd.DataFrame([file_chosen,sheet_chosen,indicator_chosen]),file2,"Cluster_var",)
        df_for_list_cluster_variable = df_for_list_cluster_variable.append([file_chosen,sheet_chosen,indicator_chosen])

    
    return [listChildren]

    # Show the list of countries that belong to a cluster
    
@app.callback(
    [Output(component_id='future_table_of_clusters', component_property='children')],
    [Input(component_id='make_cluster_button', component_property='n_clicks'),
    State(component_id='list_variables_cluster', component_property='value')
    ]
)

def show_list_of_clusters(cluster_button,list_variables_cluster):
        # return dbc.Table(
        # [html.Thead(html.Tr([html.Th("Cluster 1"), html.Th("Cluster 2"), html.Th("Cluster 3"), html.Th("Cluster 4"),  html.Th("Cluster 5")]))],
        # id ='table_of_clusters'
        dfClustersSheet = pd.read_excel('filtros.xlsx', sheet_name='Cluster', engine='openpyxl')
        dfClustersSheet2 = dfClustersSheet[["country","Cluster"]]
        n=1
        df_total = pd.DataFrame()
        a = dfClustersSheet2["country"].loc[dfClustersSheet2['Cluster']==1]
        while(dfClustersSheet2["country"].loc[dfClustersSheet2['Cluster']==n].empty==False):
            new_column = dfClustersSheet2["country"].loc[dfClustersSheet2['Cluster']==n]
            new_column.reset_index(drop=True, inplace=True)
            df_total['Cluster '+str(n)]=new_column
            #df_total = df_total.rename(index={0: 'Cluster'+str(n)})
            n=n+1

        return [dbc.Table.from_dataframe(df_total, striped=True,bordered = True, hover=True)]

# Callback for the Buttons inside Plot tab
@app.callback(
    [Output(component_id='container', component_property='children')],
    [Input(component_id='submit_parallel', component_property='n_clicks'),
    Input(component_id='submit_radar', component_property='n_clicks'),
    Input(component_id='submit_map', component_property='n_clicks'),
    Input(component_id='submit_sunburst', component_property='n_clicks'),
    Input(component_id='submit_vertex', component_property='n_clicks'),
    Input(component_id='submit_vertex3d', component_property='n_clicks'),
    Input(component_id='submit_plot2D', component_property='n_clicks'),
    State(component_id='dropdown_file_sunburst', component_property='value'),
    State(component_id='dropdown_sheet_sunburst', component_property='value'),
    State(component_id='dropdown_indicator_sunburst', component_property='value'),
    State(component_id='dropdown_file_x', component_property='value'),
    State(component_id='dropdown_sheet_x', component_property='value'),
    State(component_id='dropdown_indicator_x', component_property='value'),
    State(component_id='dropdown_file_y', component_property='value'),
    State(component_id='dropdown_sheet_y', component_property='value'),
    State(component_id='dropdown_indicator_y', component_property='value')
    ]
    )

def update_graph(bt1,bt2,bt3,bt4,bt5,bt6,bt7,dd1_sun,dd2_sun,dd3_sun,dd1_2d,dd2_2d,dd3_2d,dd4_2d,dd5_2d,dd6_2d):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'submit_parallel' in changed_id:
        draw_parallel(df2,df3)
        return [html.Div(id='sth')]
    elif 'submit_radar' in changed_id:
        figure=draw_radar(df1,df2)
        return [html.Div(id='sth')]

    elif 'submit_sunburst' in changed_id:
        df4 = read_indicator_sunburst(dd1_sun,dd2_sun,dd3_sun)
        draw_sunburst(df1,df2,df4)
        return [html.Div(id='sth')]

    elif 'submit_map' in changed_id:
        figure=draw_map(df2)
        return [html.Div(id='sth')]
        
    elif 'submit_vertex' in changed_id:
        df5 = pd.read_excel(file2, sheet_name='Vertex', engine='openpyxl')
        write_excel(df_aux,file2,'Vertex',2,1)
        draw_vertex(df1,df2,df5)
        return [html.Div(id='sth')]

    elif 'submit_vertex3d' in changed_id:
        msg = 'Button 3 was most recently clicked'
    elif 'submit_plot2D' in changed_id:
         plot_2d(dd1_2d,dd2_2d,dd3_2d,dd4_2d,dd5_2d,dd6_2d)
         return [html.Div(id='sth')]
    return [html.Div(id='sth')]
    
if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_ui=True, dev_tools_props_check=True)