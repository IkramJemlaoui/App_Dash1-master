import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
import mysql.connector as mysql
from app import app
import plotly.graph_objects as go
import plotly.express as px
from dash_extensions import Lottie

url_coonections = "https://assets3.lottiefiles.com/packages/lf20_mmuvzslg.json"
B = "https://assets2.lottiefiles.com/packages/lf20_E0dZz7.json"
B1 = "https://assets1.lottiefiles.com/packages/lf20_ffpacwo2.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

db = mysql.connect(
    host='localhost',
    user='root',
    passwd='ikram',
    database="morroco1",
    auth_plugin='mysql_native_password',
)

df8 = pd.read_sql(
    "select distinct(morocco_04_18.dim_region.Region), morocco_04_18.fact_effectifs.EffectifsP_R ,morocco_04_18.fact_effectifs.EffectifsSC_R ,morocco_04_18.fact_effectifs.EffectifsSQ_R ,morocco_04_18.fact_effectifs.EvolutionP_R,morocco_04_18.fact_effectifs.EvolutionSC_R,morocco_04_18.fact_effectifs.EvolutionSQ_R, morocco_04_18.dim_year.Year from morocco_04_18.dim_region, morocco_04_18.fact_effectifs, morocco_04_18.dim_year where morocco_04_18.fact_effectifs.Id_region = morocco_04_18.dim_region.Id_region and morocco_04_18.fact_effectifs.Id_year = morocco_04_18.dim_year.Id_year",con=db)

all_years = df8["Year"].unique()
a=df8[[ 'EvolutionP_R','EvolutionSC_R','EvolutionSQ_R']].head(0)

# ---------------------------------------------------------------
layout = dbc.Container([

    html.Div([
    html.Div([
        html.H2("Rate by year"),
        html.Img(src="/assets/A.png")
    ], className="banner"),
    html.Div([
    html.Div([
        html.P("Choose a year:"),
        dcc.Dropdown(
            id='years', style={'height': '40px', 'width': '100px'},
            options=[{'value': x, 'label': x}
                     for x in all_years],
            value=all_years[3:], ),
    ], className="four columns"),
    html.Div([
        html.P("Education level:"),
        dcc.Dropdown(
            id='el', style={'height': '50px', 'width': '200px'},
            options=[{'value': x, 'label': x}
                     for x in a.columns],
            value=a.columns[-1:], ),
    ], className="four columns"),
    ],className="row"),
    html.Div([
        html.Div([dbc.CardHeader(Lottie(options=options, width="35%", height="25%", url=B))], className="three columns",style={'height': '50px', 'width': '200px','background-color': 'white'}),
        html.Div([dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=B))], className="three columns",style={'height': '50px', 'width': '200px','background-color': 'white'}),
        html.Div([dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_coonections))], className="three columns",style={'height': '50px', 'width': '200px','background-color': 'white'}),
        html.Br(),
    ], className="row"),

    html.Div([
    html.Div(id='S',className="three columns",style={'height': '50px', 'width': '200px','background-color': 'white','color':'#9CDBE7','text-align':'center','vertical-align': 'middle','line-height': '50px'}),
    html.Div(id='LY', className="three columns",style={'height': '50px', 'width': '200px','background-color': 'white','color':'#9CDBE7','text-align':'center','vertical-align': 'middle','line-height': '50px'}),
    html.Div(id='rate',className="three columns",style={'height': '50px', 'width': '200px','background-color': 'white','color':'#9CDBE7','text-align':'center','vertical-align': 'middle','line-height': '50px'}),
    html.Br(),
    ],className="row"),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([
    html.Div(
        [dcc.Graph(id='t1',figure={}),],
        className="five columns"
    ),
    html.Div(
        [dcc.Graph(id='t4', figure={}),],
        className="five columns"
    ),
    ],className="row"),

],className="body"
)],fluid=True)
# ---------------------------------------------------------------
@app.callback(
    Output(component_id='t1', component_property='figure'),
    [Input(component_id='years', component_property='value'),
     Input(component_id='el', component_property='value')])
def update_bar_chart(year,edlev):
    df = df8[['Region',edlev,'Year']]
    mask = df["Year"] == year
    df3 = df[mask]
    df4 = df3[['Region', edlev]]
    fig2 = ff.create_table(df4, height_constant=25)
    fig2.layout.width = 600
    return fig2


@app.callback(
    Output('S', component_property='children'),
    [Input(component_id='years', component_property='value'),
     Input(component_id='el', component_property='value')
     ])
def update_bar_chart(year, edlev):

    mask = df8["Year"] == year
    df3 = df8[mask]
    df4 = df3[['Region', 'EffectifsSC_R', 'EffectifsP_R', 'EffectifsSQ_R','EvolutionP_R','EvolutionSC_R','EvolutionSQ_R']]
    if edlev == 'EvolutionP_R':
        total = df4['EffectifsP_R'].sum()
        return total
    if edlev == 'EvolutionSC_R':
        total = df4['EffectifsSC_R'].sum()
        return total
    if edlev == 'EvolutionSQ_R':
        total = df4['EffectifsSQ_R'].sum()
        return total

@app.callback(
    Output('LY', component_property='children'),
    [Input(component_id='years', component_property='value'),
     Input(component_id='el', component_property='value')
     ])
def update_bar_chart(year, edlev):

    mask = df8["Year"] == str(int(year)-1)
    df3 = df8[mask]
    df4 = df3[['Region', 'EffectifsSC_R', 'EffectifsP_R', 'EffectifsSQ_R', 'EvolutionP_R', 'EvolutionSC_R',
               'EvolutionSQ_R']]
    if edlev == 'EvolutionP_R':
        total = df4['EffectifsP_R'].sum()
        return total
    if edlev == 'EvolutionSC_R':
        total = df4['EffectifsSC_R'].sum()
        return total
    if edlev == 'EvolutionSQ_R':
        total = df4['EffectifsSQ_R'].sum()
        return total

@app.callback(
    Output("t4", "figure"),
    [Input("years", "value"),
     Input(component_id='el', component_property='value')
     ])
def update_bar_chart(year,edlev):
    mask1 = df8["Year"] == year
    mask2 = df8["Year"] == str(int(year)-1)
    df0=df8[mask1]
    df1=df8[mask2]
    if edlev == 'EvolutionP_R':
        x = 'EffectifsP_R'
    if edlev == 'EvolutionSC_R':
        x = 'EffectifsSC_R'
    if edlev == 'EvolutionSQ_R':
        x = 'EffectifsSQ_R'

    trace1 = go.Bar(    #setup the chart for Resolved records
        x=df0["Region"].unique(), #x for Resolved records
        y=df0.groupby("Region")[x].agg(sum),#y for Resolved records
        marker_color=px.colors.qualitative.Dark24[0],  #color
        text=df0.groupby("Region")[x].agg(sum), #label/text
        textposition="outside", #text position
        name="Selected year", #legend name
    )

    trace2 = go.Bar(   #setup the chart for Unresolved records
        x=df1["Region"].unique(),
        y=df1.groupby("Region")[x].agg(sum),
        text=df1.groupby("Region")[x].agg(sum),
        marker_color=px.colors.qualitative.Dark24[1],
        textposition="outside",
        name="Previous year ",
    )

    data = [trace1, trace2] #combine two charts/columns
    layout = go.Layout(barmode="group", title="Resolved vs Unresolved") #define how to display the columns
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(
        title=dict(x=0.5), #center the title
        xaxis_title="Regiongs",#setup the x-axis title
        yaxis_title="Effectif", #setup the x-axis title
        margin=dict(l=5, r=5, t=25, b=5),#setup the margin
        paper_bgcolor="#fdf2ff", #setup the background color
        width=850,
        height=500,
    )
    fig.update_traces(texttemplate="%{text:.2s}") #text formart
    return fig

@app.callback(
    Output('rate', component_property='children'),
    [Input('LY',component_property='children'),
     Input('S', component_property='children')
     ])
def update_bar_chart(lyear,year):
    rate = (int(year)-int(lyear))/int(lyear)
    return round(rate*100,1)