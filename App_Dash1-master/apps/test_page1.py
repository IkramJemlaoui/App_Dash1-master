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
    " select distinct(morocco_04_18.dim_region.Region), morocco_04_18.fact_table.EffectifsPrimaryS_R , morocco_04_18.fact_table.EffectifsSecondaryS_R ,morocco_04_18.fact_table.EffectifsHighS_R ,morocco_04_18.dim_year.Year from morocco_04_18.dim_region, morocco_04_18.fact_table, morocco_04_18.dim_year where morocco_04_18.fact_table.Id_region = morocco_04_18.dim_region.Id_region and morocco_04_18.fact_table.Id_year = morocco_04_18.dim_year.Id_year",
    con=db)

all_years = df8["Year"].unique()
a=df8[[ 'EffectifsSecondaryS_R','EffectifsPrimaryS_R','EffectifsHighS_R']].head(0)

# ---------------------------------------------------------------
layout = html.Div([
        html.Div([
                    html.Div([
                        html.Label(['NYC Calls for Animal Rescue']),
                        html.P("Names:"),
                        dcc.Dropdown(
                            id='years', style={'height': '40px', 'width': '100px'},
                            options=[{'value': x, 'label': x}
                                     for x in all_years],
                            value=all_years[3:], ),

                    ], className="four columns"),
                    html.Div([
                        html.Label(['test']),
                        html.P("education level:"),
                        dcc.Dropdown(
                            id='el', style={'height': '50px', 'width': '200px'},
                            options=[{'value': x, 'label': x}
                                     for x in a.columns],
                            value=a.columns[-1:], ),
                    ], className="four columns"),
                    ],className="row"),
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
    [Input(component_id='years', component_property='value'),
     Input(component_id='el', component_property='value')])
def update_bar_chart(year,edlev):
    mask = df8["Year"] == year

    fig = px.pie(df8[mask], values=edlev, names='Region', color_discrete_sequence=px.colors.sequential.Plasma)
    return fig

@app.callback(

    Output(component_id='t2', component_property='figure'),
    [Input(component_id='years', component_property='value'),
     Input(component_id='el', component_property='value')])
def update_bar_chart(year,edlev):
    mask = df8["Year"] == year
    df1 = df8[mask]
    df2 = df1[['Region', edlev]]
    fig2 = ff.create_table(df2, height_constant=23)
    fig2.layout.width = 600
    return fig2
@app.callback(

    Output(component_id='t3', component_property='figure'),
    [Input(component_id='years', component_property='value'),
     Input(component_id='el', component_property='value')])
def update_bar_chart(year,edlev):
    mask = df8["Year"] == str(int(year)-1)
    df1 = df8[mask]
    df2 = df1[['Region', edlev]]
    fig3 = ff.create_table(df2, height_constant=23)
    fig3.layout.width = 600

    return fig3
