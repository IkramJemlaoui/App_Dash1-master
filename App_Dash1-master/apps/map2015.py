# Environment used: dash1_8_0_env
import pandas as pd     #(version 1.0.0)
import plotly.graph_objects as go
from app import app
import dash             #(version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import mysql.connector as mysql
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_extensions import Lottie
import json
f = open('C:/Users/Ikram/Desktop/SIG-BI/regions_12_names.geojson')
data = json.load(f)

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
df=pd.read_sql("select distinct(morocco_04_18.dim_region.Region), morocco_04_18.fact_table.EffectifsPrimaryS_R ,morocco_04_18.fact_table.EffectifsSecondaryS_R ,morocco_04_18.fact_table.EffectifsHighS_R ,morocco_04_18.fact_table.EvolutionPrimaryS_R,morocco_04_18.fact_table.EvolutionSecondaryS_R,morocco_04_18.fact_table.EvolutionHighS_R, morocco_04_18.dim_year.Year from morocco_04_18.dim_region, morocco_04_18.fact_table, morocco_04_18.dim_year where morocco_04_18.dim_year.year >2014 and morocco_04_18.fact_table.Id_region = morocco_04_18.dim_region.Id_region and morocco_04_18.fact_table.Id_year = morocco_04_18.dim_year.Id_year",con=db)
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# df['text'] = df['Region'] + ' ' + 'Rate: ' +' '+ df['EvolutionPrimaryS_R'].astype(str)
# a=df[[ 'EvolutionPrimaryS_R','EvolutionSecondaryS_R','EvolutionHighS_R']].head(0)

layout = html.Div([
html.Hr(),
html.Br(),
dbc.Row(dbc.Col([

        dcc.Dropdown(
            id='el2',
            style={'height': '40px', 'width': '190px','font-size': '15px'},
            options=[
                {'label': 'Primary school', 'value': 'P'},
                {'label': 'Secondary school', 'value': 'S'},
                {'label': 'High school', 'value': 'H'}
            ], ),
        html.Br(),
        dcc.Input(id='input_state2', type='number', inputMode='numeric', value=2015,
                  max=2018, min=2015, step=1, required=True,
                  style={'marginRight':'10px','height': '40px', 'width': '100px','font-size': '15px'}),
        html.Button(id='submit_button2', n_clicks=0, children='Submit',
                    style={'height': '40px', 'width': '150px', 'background-color': 'white', 'color': '#9CDBE7',
                           'text-align': 'center', 'vertical-align': 'middle', 'line-height': '50px',
                           'font-size': '20px'}
                    )
    ],width=6),),
html.Br(),
  dbc.Row([
    dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id='the_graph2')])), width=8),
    #---------------
    dbc.Col([
    html.Div([
        dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="67%", height="67%", url=url_coonections)),
                dbc.CardBody([
                    html.H6('Selected year effectif'),
                    html.H2(id='S12' )
                ], style={'textAlign':'center'})
            ]),
        ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(Lottie(options=options, width="67%", height="67%", url=url_coonections)),
                    dbc.CardBody([
                        html.H6('Previvous year effectif'),
                        html.H2(id='LY12')
                    ], style={'textAlign': 'center'})
                ]),
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(Lottie(options=options, width="67%", height="67%", url=url_coonections)),
                    dbc.CardBody([
                        html.H6('Rate'),
                        html.H1(id='rate12')
                    ], style={'textAlign': 'center'})
                ]),
            ], width=4),

        ]),

        html.Br(),
    ], className="row", style={'width': '50%', 'margin': '0 auto'}),

    ],
    width=4
    ),
    #--------------

],align='center'
  ),

    dbc.Row([
    dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id='t72', figure={})])),width=6) ,
    dbc.Col(dbc.Card(dbc.CardBody([dcc.Graph(id='t62', figure={})])), width=6)
    ],align='center'
  ),


],style={ 'margin': '0 auto'})
#---------------------------------------------------------------
@app.callback(

    Output("the_graph2", "figure"),
    [Input(component_id='submit_button2', component_property='n_clicks')],
    [State(component_id='input_state2', component_property='value')],
    [State(component_id='el2', component_property='value')],
)
def update_map(num_clicks, val_selected, edlev):
    if edlev == 'P':
        x1 = 'EvolutionPrimaryS_R'
    if edlev == 'S':
        x1 = 'EvolutionSecondaryS_R'
    if edlev == 'H':
        x1 = 'EvolutionHighS_R'

    if val_selected is None:
        raise PreventUpdate
    else:
        mask1 = df["Year"] == str(val_selected)
        df0 = df[mask1]

        fig = px.choropleth_mapbox(df0, geojson=data, color=x1,
                                   locations="Region", featureidkey="properties.REGIONS",
                                   center={"lat": 45.5517, "lon": -73.7073},
                                   mapbox_style="carto-positron", zoom=9)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


        return  fig

@app.callback(
    Output("t62", "figure"),
    [Input(component_id='submit_button2', component_property='n_clicks')],
    [State(component_id='input_state2', component_property='value')],
    [State(component_id='el2', component_property='value')],
)

def update_bar_chart(num_clicks,val_selected,edlev):
    if edlev == 'P':
        x1 = 'EffectifsPrimaryS_R'
    if edlev == 'S':
        x1 = 'EffectifsSecondaryS_R'
    if edlev == 'H':
        x1 = 'EffectifsHighS_R'


    mask1 = df["Year"] == str(val_selected)
    mask2 = df["Year"] == str(int(val_selected)-1)
    df0=df[mask1]
    df1=df[mask2]
    trace1 = go.Bar(  # setup the chart for the selected year
        x=df0["Region"].unique(),  # x for the selected year
        y=df0[x1],  # y for the selected year
        marker_color=px.colors.qualitative.Dark24[0],  # color
        text=df0[x1],  # label/text
        textposition="outside",  # text position
        name="Selected year",  # legend name
    )

    trace2 = go.Bar(   #setup the chart for the previous year
        x=df1["Region"].unique(),
        y=df1[x1],
        text=df1[x1],
        marker_color=px.colors.qualitative.Dark24[1],
        textposition="outside",
        name="Previous year ",
    )

    data = [trace2, trace1] #combine two charts/columns
    layout = go.Layout(barmode="group", title="Selected vs previous") #define how to display the columns
    fig1 = go.Figure(data=data, layout=layout)
    fig1.update_layout(

        title=dict(x=0.5), #center the title
        xaxis_title="Regiongs",#setup the x-axis title
        yaxis_title="Effectif", #setup the x-axis title
        margin=dict(l=5, r=5, t=25, b=5),#setup the margin
        # paper_bgcolor="#fdf2ff", #setup the background color
        width=850,
        height=500,
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',

    )
    fig1.update_traces(texttemplate="%{text:.2s}") #text formart
    return fig1

#------------------------------------------------------------------------

@app.callback(
    Output('LY12', component_property='children'),
    [Input(component_id='submit_button2', component_property='n_clicks')],
    [State(component_id='input_state2', component_property='value')],
    [State(component_id='el2', component_property='value')],)
def update_sum_eff_ly(num_clicks,val_selected,edlev):

    mask = df["Year"] == str(int(val_selected)-1)
    df3 = df[mask]
    df4 = df3[['Region', 'EffectifsSecondaryS_R', 'EffectifsPrimaryS_R', 'EffectifsHighS_R', 'EvolutionPrimaryS_R', 'EvolutionSecondaryS_R',
               'EvolutionHighS_R']]
    if edlev == 'P':
        total = df4['EffectifsPrimaryS_R'].sum()
        return total
    if edlev == 'S':
        total = df4['EffectifsSecondaryS_R'].sum()
        return total
    if edlev == 'H':
        total = df4['EffectifsHighS_R'].sum()
        return total

@app.callback(
    Output('S12', component_property='children'),
    [Input(component_id='submit_button2', component_property='n_clicks')],
    [State(component_id='input_state2', component_property='value')],
    [State(component_id='el2', component_property='value')],)
def update_sum_eff_Sy(num_clicks,val_selected,edlev):

    mask = df["Year"] == str(int(val_selected))
    df3 = df[mask]
    df4 = df3[['Region', 'EffectifsSecondaryS_R', 'EffectifsPrimaryS_R', 'EffectifsHighS_R', 'EvolutionPrimaryS_R', 'EvolutionSecondaryS_R',
               'EvolutionHighS_R']]
    if edlev == 'P':
        total = df4['EffectifsPrimaryS_R'].sum()
        return total
    if edlev == 'S':
        total = df4['EffectifsSecondaryS_R'].sum()
        return total
    if edlev == 'H':
        total = df4['EffectifsHighS_R'].sum()
        return total

@app.callback(
    Output('rate12', component_property='children'),
    [Input('LY12',component_property='children'),
     Input('S12', component_property='children')
     ])
def update_rate(lyear,year):

        rate = (int(year)-int(lyear))/int(lyear)
        return round(rate*100,1)


@app.callback(
    Output(component_id='t72', component_property='figure'),
    [Input(component_id='submit_button2', component_property='n_clicks')],
    [State(component_id='input_state2', component_property='value')],
    [State(component_id='el2', component_property='value')],)
def update_pie_chart(num_clicks,val_selected,edlev):
    mask = df["Year"] == str(val_selected)
    if edlev == 'P':
        x1 = 'EffectifsPrimaryS_R'
    if edlev == 'S':
        x1 = 'EffectifsSecondaryS_R'
    if edlev == 'H':
        x1 = 'EffectifsSQ_R'

    fig = px.pie(df[mask], values=x1, names='Region', color_discrete_sequence=px.colors.sequential.Plasma)
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )
    return fig
