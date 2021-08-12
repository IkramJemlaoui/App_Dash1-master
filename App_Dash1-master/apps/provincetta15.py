# # Environment used: dash1_8_0_env
# import pandas as pd  # (version 1.0.0)
# import plotly.graph_objects as go
# import dash  # (version 1.8.0)
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output, State
# from dash.exceptions import PreventUpdate
# import mysql.connector as mysql
# import plotly.express as px
# import dash_bootstrap_components as dbc
# from app import app
# from dash_extensions import Lottie
# url_coonections = "https://assets3.lottiefiles.com/packages/lf20_mmuvzslg.json"
# B = "https://assets2.lottiefiles.com/packages/lf20_E0dZz7.json"
# B1 = "https://assets1.lottiefiles.com/packages/lf20_ffpacwo2.json"
# options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))
# import json
# f = open('C:/Users/Ikram/Desktop/SIG-BI/provinces_tangerm.geojson')
# data = json.load(f)
#
# db = mysql.connect(
#     host='localhost',
#     user='root',
#     passwd='ikram',
#     database="morroco1",
#     auth_plugin='mysql_native_password',
# )
# df = pd.read_sql(
#     "Select  morocco_04_18.dim_year.Year,  morocco_04_18.dim_region.Region, morocco_04_18.dim_province.province, morocco_04_18.fact_table.EffectifsPrimaryS_Prov,morocco_04_18.fact_table.EvolutionPrimaryS_Prov,morocco_04_18.fact_table.EffectifsPrimaryS_R,morocco_04_18.fact_table.EvolutionPrimaryS_R,morocco_04_18.fact_table.EffectifsSecondaryS_Prov ,morocco_04_18.fact_table.EvolutionSecondaryS_Prov,morocco_04_18.fact_table.EffectifsSecondaryS_R,morocco_04_18.fact_table.EvolutionSecondaryS_R,morocco_04_18.fact_table.EffectifsHighS_Prov,morocco_04_18.fact_table.EvolutionHighS_Prov, morocco_04_18.fact_table.EffectifsHighS_R, morocco_04_18.fact_table.EvolutionHighS_R from morocco_04_18.fact_table, morocco_04_18.dim_year,  morocco_04_18.dim_region,morocco_04_18.dim_province where morocco_04_18.dim_year.year >2014 and morocco_04_18.dim_region.Region like'T%' and morocco_04_18.fact_table.Id_year = morocco_04_18.dim_year.Id_year and morocco_04_18.fact_table.Id_region = morocco_04_18.dim_region.Id_region and morocco_04_18.fact_table.Id_province = morocco_04_18.dim_province.Id_province ",
#     con=db)
# all_years = df["Year"].unique()
# layout = html.Div([
#     html.Hr(),
#     html.Br(),
#     dbc.Row([
#         dbc.Col([dcc.Dropdown(id='R1',
#                               style={'height': '40px', 'width': '300px', 'font-size': '19px'}, )], width=1),
#        dbc.Col([html.P('|')],width=1, style={'color':'red'}),
#         dbc.Col([
#         dcc.Dropdown(
#             id='years1',
#             style={'height': '40px', 'width': '190px','font-size': '19px'},
#             options=[{'value': x, 'label': x}
#                      for x in all_years],
#             value=all_years[3:],
#         ),],width=1),
#
#         dbc.Col([dcc.Dropdown(
#             id='el1',
#             style={'height': '40px', 'width': '190px', 'font-size': '19px'},
#             options=[
#                 {'label': 'Primary school', 'value': 'P'},
#                 {'label': 'Secondary school', 'value': 'S'},
#                 {'label': 'High school', 'value': 'H'}
#             ], )],width=3),
#
#         ]),
#     html.Br(),
#     dbc.Row([dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id="area1")])),width=6),
#     dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id='map_prov1', figure={})])),width=6)
#              ],justify="center"),
#
#     # dbc.Row([dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id='map_prov1', figure={})])),width=9),],justify="center"),
#     dbc.Row([
#             dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id='pie_prov1', figure={})])), width=6),
#             dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id='bar1', figure={})])), width=6)
#         ], align='center'),
#
# ])
# @app.callback(
#     Output(component_id='map_prov1', component_property='figure'),
#    [Input(component_id='years1', component_property='value'),
#     Input(component_id='R1', component_property='value'),
#     Input(component_id='el1', component_property='value')], )
# def update_map(y, r, edlev):
#     if edlev == 'P':
#         x1 = 'EvolutionPrimaryS_Prov'
#     if edlev == 'S':
#         x1 = 'EvolutionSecondaryS_Prov'
#     if edlev == 'H':
#         x1 = 'EvolutionHighS_Prov'
#
#     if y is None:
#         raise PreventUpdate
#     else:
#         mask1 = df["Year"] == str(y)
#         df0 = df[mask1].reset_index()
#         mask1 = df0["Region"] == str(r)
#         df1 = df0[mask1].reset_index()
#
#         fig = px.choropleth_mapbox(df1, geojson=data, color=x1,
#                                    locations="province", featureidkey="properties.province",
#                                    center={"lat": 45.5517, "lon": -73.7073},
#                                    mapbox_style="carto-positron", zoom=9)
#         fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
#
#         return  fig
#
#
#
# @app.callback(
#     Output(component_id='R1', component_property='options'),
#     [Input(component_id='years1', component_property='value')],
# )
# def region_function(y):
#     mask = df["Year"] == str(y)
#     df0 = df[mask]
#     all_Regions = df0["Region"].unique()
#
#     return [{'value': x, 'label': x} for x in all_Regions]
#
#
# @app.callback(
#     Output(component_id='pie_prov1', component_property='figure'),
#     Input(component_id='years1', component_property='value'),
#     Input(component_id='R1', component_property='value'),
#     [Input(component_id='el1', component_property='value')], )
# def update_pie_chart(y, r, edlev):
#     mask = df["Year"] == str(y)
#     if edlev == 'P':
#         x1 = 'EffectifsPrimaryS_Prov'
#     if edlev == 'S':
#         x1 = 'EffectifsSecondaryS_Prov'
#     if edlev == 'H':
#         x1 = 'EffectifsHighS_Prov'
#     df0 = df[mask]
#     mask1 = df0["Region"] == str(r)
#     df1 = df0[mask1]
#     fig = px.pie(df1, values=x1, names='province', color_discrete_sequence=px.colors.sequential.Plasma)
#     fig.update_layout(
#         template='plotly_dark',
#         plot_bgcolor='rgba(0, 0, 0, 0)',
#         paper_bgcolor='rgba(0, 0, 0, 0)',
#         title= 'Effectifs of techers by province')
#     return fig
#
#
# # -------------------------------------------------------------
# @app.callback(
#     Output(component_id='bar1', component_property='figure'),
#     Input(component_id='years1', component_property='value'),
#     Input(component_id='R1', component_property='value'),
#     [Input(component_id='el1', component_property='value')], )
# def update_bar_chart(y, r, edlev):
#     if edlev == 'P':
#         x1 = 'EffectifsPrimaryS_R'
#     if edlev == 'S':
#         x1 = 'EffectifsSecondaryS_R'
#     if edlev == 'H':
#         x1 = 'EffectifsHighS_R'
#     mask1 = df["Region"] == r
#     df1 = df[mask1]
#
#     mask1 = df["Year"] == str(y)
#     mask2 = df["Year"] == str(int(y) - 1)
#
#     df0 = df1[mask1]
#     df1 = df1[mask2]
#     trace1 = go.Bar(  # setup the chart for the selected year
#         x=df0["province"].unique(),  # x for the selected year
#         y=df0[x1],  # y for the selected year
#         marker_color=px.colors.qualitative.Dark24[0],  # color
#         textposition="outside",  # text position
#         name="Selected year",  # legend name
#     )
#
#     trace2 = go.Bar(  # setup the chart for the previous year
#         x=df1["province"].unique(),
#         y=df1[x1],
#         marker_color=px.colors.qualitative.Dark24[1],
#         textposition="outside",
#         name="Previous year ",
#     )
#
#     data = [trace2, trace1]  # combine two charts/columns
#     layout = go.Layout(barmode="group", title="Selected vs previous")  # define how to display the columns
#     fig1 = go.Figure(data=data, layout=layout)
#     fig1.update_layout(
#
#         title=dict(x=0.5), #center the title
#         xaxis_title="Regiongs",#setup the x-axis title
#         yaxis_title="Effectif", #setup the x-axis title
#         margin=dict(l=5, r=5, t=25, b=5),#setup the margin
#         # paper_bgcolor="#fdf2ff", #setup the background color
#         width=850,
#         height=500,
#         template='plotly_dark',
#         plot_bgcolor='rgba(0, 0, 0, 0)',
#         paper_bgcolor='rgba(0, 0, 0, 0)',
#
#     )
#
#     return fig1
# #------------------------------------CALCULE----------------------------------------------------------
# @app.callback(
#     Output(component_id='Sum_LY', component_property='figure'),
#     Input(component_id='years1', component_property='value'),
#     Input(component_id='R1', component_property='value'),
#     Input(component_id='el1', component_property='value'))
# def update_Sum_eff_LY(y, r, edlev):
#
#     mask = df["Year"] == str(int(y)-1)
#     df3 = df[mask]
#     mask1 = df3["Region"] == r
#     df2=df3[mask1]
#     df4 = df2[['Region', 'EffectifsSecondaryS_Prov', 'EffectifsPrimaryS_Prov', 'EffectifsHighS_Prov', 'EvolutionPrimaryS_Prov', 'EvolutionSecondaryS_Prov',
#                'EvolutionHighS_Prov']]
#     if edlev == 'P':
#         total = df4['EffectifsPrimaryS_Prov'].sum()
#         return total
#     if edlev == 'S':
#         total = df4['EffectifsSecondaryS_Prov'].sum()
#         return total
#     if edlev == 'H':
#         total = df4['EffectifsHighS_Prov'].sum()
#         return total
#
# @app.callback(
#     Output(component_id='Sum_Y', component_property='figure'),
#     Input(component_id='R1', component_property='value'),
#     Input(component_id='years1', component_property='value'),
#
#     Input(component_id='el1', component_property='value') )
# def update_sum_eff_Y(r, y, edlev):
#
#     mask = df["Year"] == str(y)
#     df3 = df[mask]
#     mask1 = df3["Region"] == r
#     df2=df3[mask1]
#     df4 = df2[['Region', 'EffectifsSecondaryS_Prov', 'EffectifsPrimaryS_Prov', 'EffectifsHighS_Prov', 'EvolutionPrimaryS_Prov', 'EvolutionSecondaryS_Prov',
#                'EvolutionHighS_Prov']]
#     if edlev == 'P':
#         total = df4['EffectifsPrimaryS_Prov'].sum()
#         return total
#     if edlev == 'S':
#         total = df4['EffectifsSecondaryS_Prov'].sum()
#         return total
#     if edlev == 'H':
#         total = df4['EffectifsHighS_Prov'].sum()
#         return total
#
# @app.callback(
#     Output('rate3', component_property='children'),
#     Input('Sum_LY',component_property='children'),
#     Input('Sum_Y', component_property='children')
#      )
# def update_rate(lyear,year):
#
#         rate = (int(year)-int(lyear))/int(lyear)
#         return round(rate*100,1)
# #----------------------------AREA_chart_FUNCTION------------------------------
# @app.callback(
#     Output("area1", "figure"),
#     Input(component_id='R1', component_property='value'),
#     Input(component_id='el1', component_property='value'),
#     )
# def update_area_chart(r,edlev):
#
#     y = df[df['Region'] == r]
#
#     if edlev == 'P':
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(name='Primary', x=y['Year'], y=y['EvolutionPrimaryS_R'], hoverinfo='x+y',
#                          mode='lines',
#                          line=dict(width=0.5, color='rgb(83, 189, 116)'),
#                          stackgroup='one'))
#     if edlev == 'S':
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(name='Secondary', x=y['Year'], y=y['EvolutionSecondaryS_R'], hoverinfo='x+y',
#                          mode='lines',
#                          line=dict(width=0.5, color='rgb(111, 231, 219)'),
#                          stackgroup='one'))
#     if edlev == 'H':
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(name='High', x=y['Year'], y=y['EvolutionHighS_R'], hoverinfo='x+y',
#                                  mode='lines',
#                                  line=dict(width=0.5, color='rgb(191, 86, 123)'),
#                                  stackgroup='one'))
#     return fig