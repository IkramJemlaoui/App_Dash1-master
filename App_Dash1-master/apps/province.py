# Environment used: dash1_8_0_env
import pandas as pd  # (version 1.0.0)
import plotly.graph_objects as go
import dash  # (version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import mysql.connector as mysql
import plotly.express as px
import dash_bootstrap_components as dbc
from app import app
from dash_extensions import Lottie

db = mysql.connect(
    host='localhost',
    user='root',
    passwd='ikram',
    database="morroco1",
    auth_plugin='mysql_native_password',
)
df = pd.read_sql(
    "Select  morocco_04_18.dim_year.year,  morocco_04_18.dim_region.Region, morocco_04_18.dim_province.province,  morocco_04_18.fact_effectifs.EffectifsP_P,morocco_04_18.fact_effectifs.EvolutionP_P, morocco_04_18.fact_effectifs.EffectifsP_R,morocco_04_18.fact_effectifs.EvolutionP_R,morocco_04_18.fact_effectifs.EffectifsSC_P,morocco_04_18.fact_effectifs.EvolutionSC_P, morocco_04_18.fact_effectifs.EffectifsSC_R,morocco_04_18.fact_effectifs.EvolutionSC_R,morocco_04_18.fact_effectifs.EffectifsSQ_P,morocco_04_18.fact_effectifs.EvolutionSQ_P, morocco_04_18.fact_effectifs.EffectifsSQ_R,morocco_04_18.fact_effectifs.EvolutionSQ_R from morocco_04_18.fact_effectifs, morocco_04_18.dim_year,  morocco_04_18.dim_region, morocco_04_18.dim_province where morocco_04_18.fact_effectifs.Id_year = morocco_04_18.dim_year.Id_year and morocco_04_18.fact_effectifs.Id_region = morocco_04_18.dim_region.Id_region and morocco_04_18.fact_effectifs.Id_province = morocco_04_18.dim_province.Id_province",
    con=db)
all_years = df["year"].unique()


layout = html.Div([
    html.Hr(),
    html.Br(),
    dbc.Row(dbc.Col([

        dcc.Dropdown(
            id='years',
            options=[{'value': x, 'label': x}
                     for x in all_years],
            value=all_years[3:],
        ),
        dcc.Dropdown(id='R'),
        dcc.Dropdown(
            id='el',
            style={'height': '40px', 'width': '190px', 'font-size': '15px'},
            options=[
                {'label': 'Primary school', 'value': 'P'},
                {'label': 'Secondary school', 'value': 'S'},
                {'label': 'High school', 'value': 'H'}
            ], ),
        dcc.Graph(id='pie_prov', figure={}),
        dcc.Graph(id='bar', figure={})

    ], style={'margin': '0 auto'}))

])

@app.callback(
    Output(component_id='R', component_property='options'),
    [Input(component_id='years', component_property='value')],
)
def year_function(y):
    mask = df["year"] == str(y)
    df0 = df[mask]
    all_Regions = df0["Region"].unique()

    return [{'value': x, 'label': x} for x in all_Regions]


@app.callback(
    Output(component_id='pie_prov', component_property='figure'),
    [Input(component_id='years', component_property='value')],
    [Input(component_id='R', component_property='value')],
    [Input(component_id='el', component_property='value')], )
def update_pie_chart(y, r, edlev):
    mask = df["year"] == str(y)
    if edlev == 'P':
        x1 = 'EffectifsP_P'
    if edlev == 'S':
        x1 = 'EffectifsSC_P'
    if edlev == 'H':
        x1 = 'EffectifsSQ_P'

    df0 = df[mask]
    mask1 = df0["Region"] == str(r)
    df1 = df0[mask1]

    fig = px.pie(df1, values=x1, names='province', color_discrete_sequence=px.colors.sequential.Plasma)

    return fig


# -------------------------------------------------------------
@app.callback(
    Output(component_id='bar', component_property='figure'),
    [Input(component_id='years', component_property='value')],
    [Input(component_id='R', component_property='value')],
    [Input(component_id='el', component_property='value')], )
def update_bar_chart(y, r, edlev):
    if edlev == 'P':
        x1 = 'EffectifsP_R'
    if edlev == 'S':
        x1 = 'EffectifsSC_R'
    if edlev == 'H':
        x1 = 'EffectifsSQ_R'
    mask1 = df["Region"] == r
    df1 = df[mask1]

    mask1 = df["year"] == str(y)
    mask2 = df["year"] == str(int(y) - 1)

    df0 = df1[mask1]
    df1 = df1[mask2]
    trace1 = go.Bar(  # setup the chart for the selected year
        x=df0["province"].unique(),  # x for the selected year
        y=df0[x1],  # y for the selected year
        marker_color=px.colors.qualitative.Dark24[0],  # color
        textposition="outside",  # text position
        name="Selected year",  # legend name
    )

    trace2 = go.Bar(  # setup the chart for the previous year
        x=df1["province"].unique(),
        y=df1[x1],
        marker_color=px.colors.qualitative.Dark24[1],
        textposition="outside",
        name="Previous year ",
    )

    data = [trace2, trace1]  # combine two charts/columns
    layout = go.Layout(barmode="group", title="Selected vs previous")  # define how to display the columns
    fig1 = go.Figure(data=data, layout=layout)

    return fig1
