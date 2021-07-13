import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

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
    "select distinct(morocco_04_18.dim_region.Region), morocco_04_18.fact_effectifs.EffectifsP_R , morocco_04_18.dim_year.Year from morocco_04_18.dim_region, morocco_04_18.fact_effectifs, morocco_04_18.dim_year where morocco_04_18.fact_effectifs.Id_region = morocco_04_18.dim_region.Id_region and morocco_04_18.fact_effectifs.Id_year = morocco_04_18.dim_year.Id_year",
    con=db)
# fig = px.pie(df8, values='EffectifsP_R', names='Region', color_discrete_sequence=px.colors.sequential.Plasma)
all_years = df8["Year"].unique()
# fig2 = ff.create_table(df8, height_constant=60)

# ---------------------------------------------------------------
layout = html.Div([
                    html.Div([
                        html.Label(['NYC Calls for Animal Rescue']),
                        html.P("Names:"),
                        dcc.Dropdown(
                            id='years', style={'height': '40px', 'width': '100px'},
                            options=[{'value': x, 'label': x}
                                     for x in all_years],
                            value=all_years[3:], ),

                    ]),
                    html.Div([
                        html.Div([
                            dcc.Graph(id='t', figure={}),
                        ], className="four columns"),

                        html.Div([
                            dcc.Graph(id='t2', figure={}),
                        ], className="four columns"),
                        html.Div([
                            dcc.Graph(id='t3', figure={}),
                        ], className="four columns")

                    ], className="row")
])


# ---------------------------------------------------------------
@app.callback(
    Output(component_id='t', component_property='figure'),
    [Input(component_id='years', component_property='value')])
def update_bar_chart(year):
    mask = df8["Year"] == year

    fig = px.pie(df8[mask], values='EffectifsP_R', names='Region', color_discrete_sequence=px.colors.sequential.Plasma)
    return fig

@app.callback(

    Output(component_id='t2', component_property='figure'),
    [Input(component_id='years', component_property='value')])
def update_bar_chart(year):
    mask = df8["Year"] == year
    df1 = df8[mask]
    df2 = df1[['Region', 'EffectifsP_R']]
    fig2 = ff.create_table(df2, height_constant=23)
    fig2.layout.width = 600
    return fig2
@app.callback(

    Output(component_id='t3', component_property='figure'),
    [Input(component_id='years', component_property='value')])
def update_bar_chart(year):
    mask = df8["Year"] == str(int(year)-1)
    df1 = df8[mask]
    df2 = df1[['Region', 'EffectifsP_R']]
    fig3 = ff.create_table(df2, height_constant=23)
    fig3.layout.width = 600

    return fig3

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
