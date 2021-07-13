import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.figure_factory as ff
import mysql.connector as mysql
from app import app

db = mysql.connect(
    host='localhost',
    user='root',
    passwd='ikram',
    database="morroco1",
    auth_plugin='mysql_native_password',
)
# df8 = pd.read_sql(
#     "select distinct(morocco_04_18.dim_region.Region), morocco_04_18.fact_effectifs.EffectifsP_R ,morocco_04_18.fact_effectifs.EvolutionP_R, morocco_04_18.dim_year.Year from morocco_04_18.dim_region, morocco_04_18.fact_effectifs, morocco_04_18.dim_year where morocco_04_18.fact_effectifs.Id_region = morocco_04_18.dim_region.Id_region and morocco_04_18.fact_effectifs.Id_year = morocco_04_18.dim_year.Id_year",con=db)

df8 = pd.read_sql(
    "select distinct(morocco_04_18.dim_region.Region), morocco_04_18.fact_effectifs.EffectifsP_R ,morocco_04_18.fact_effectifs.EffectifsSC_R ,morocco_04_18.fact_effectifs.EffectifsSQ_R ,morocco_04_18.fact_effectifs.EvolutionP_R,morocco_04_18.fact_effectifs.EvolutionSC_R,morocco_04_18.fact_effectifs.EvolutionSQ_R, morocco_04_18.dim_year.Year from morocco_04_18.dim_region, morocco_04_18.fact_effectifs, morocco_04_18.dim_year where morocco_04_18.fact_effectifs.Id_region = morocco_04_18.dim_region.Id_region and morocco_04_18.fact_effectifs.Id_year = morocco_04_18.dim_year.Id_year",con=db)

all_years = df8["Year"].unique()
a=df8[[ 'EvolutionP_R','EvolutionSC_R','EvolutionSQ_R']].head(0)

# ---------------------------------------------------------------
layout = html.Div([
    html.Div([
        html.Label(['NYC Calls for Animal Rescue']),
        html.P("years:"),
        dcc.Dropdown(
            id='years', style={'height': '40px', 'width': '100px'},
            options=[{'value': x, 'label': x}
                     for x in all_years],
            value=all_years[3:], ),
    ]),
    html.Div([
        html.Label(['test']),
        html.P("education level:"),
        dcc.Dropdown(
            id='el', style={'height': '50px', 'width': '200px'},
            options=[{'value': x, 'label': x}
                     for x in a.columns],
            value=a.columns[-1:], ),
    ]),
    html.Div(id='S'),
    html.Div(id='LY'),
    html.Br(),
    dcc.Graph(id='t1',figure={}),
])
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
    fig2 = ff.create_table(df4, height_constant=27)
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
        return 'Output: {}'.format(total)
    if edlev == 'EvolutionSC_R':
        total = df4['EffectifsSC_R'].sum()
        return 'Output: {}'.format(total)
    if edlev == 'EvolutionSQ_R':
        total = df4['EffectifsSQ_R'].sum()
        return 'Output: {}'.format(total)

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
        return 'LY: {}'.format(total)
    if edlev == 'EvolutionSC_R':
        total = df4['EffectifsSC_R'].sum()
        return 'LY: {}'.format(total)
    if edlev == 'EvolutionSQ_R':
        total = df4['EffectifsSQ_R'].sum()
        return 'LY: {}'.format(total)


