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
df8 = pd.read_sql(
    "select distinct(morocco_04_18.dim_region.Region), morocco_04_18.fact_effectifs.EffectifsP_R ,morocco_04_18.fact_effectifs.EvolutionP_R, morocco_04_18.dim_year.Year from morocco_04_18.dim_region, morocco_04_18.fact_effectifs, morocco_04_18.dim_year where morocco_04_18.fact_effectifs.Id_region = morocco_04_18.dim_region.Id_region and morocco_04_18.fact_effectifs.Id_year = morocco_04_18.dim_year.Id_year",con=db)

# fig2 = ff.create_table(df8[['Region','EvolutionP_R','Year']], height_constant=60)
all_years = df8["Year"].unique()

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

    dcc.Graph(id='t1',figure={}),
])
# ---------------------------------------------------------------
@app.callback(
    Output(component_id='t1', component_property='figure'),
    [Input(component_id='years', component_property='value')])
def update_bar_chart(year):
    df = df8[['Region','EvolutionP_R','Year']]
    mask = df["Year"] == year
    df3 = df[mask]
    df4 = df3[['Region', 'EvolutionP_R']]
    fig2 = ff.create_table(df4, height_constant=27)
    fig2.layout.width = 600
    return fig2

