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
db = mysql.connect(
    host='localhost',
    user='root',
    passwd='ikram',
    database="morroco1",
    auth_plugin='mysql_native_password',
)
df=pd.read_sql("select distinct(morocco_04_18.dim_region.Region), morocco_04_18.fact_effectifs.EffectifsSC_R ,morocco_04_18.fact_effectifs.EffectifsSQ_R ,morocco_04_18.fact_effectifs.EffectifsP_R ,morocco_04_18.fact_effectifs.EvolutionP_R, morocco_04_18.fact_effectifs.EvolutionSQ_R,morocco_04_18.fact_effectifs.EvolutionSC_R,morocco_04_18.dim_year.Year,morocco_04_18.dim_region.Latitude,morocco_04_18.dim_region.Longitude from morocco_04_18.dim_region, morocco_04_18.fact_effectifs, morocco_04_18.dim_year where  morocco_04_18.fact_effectifs.Id_region = morocco_04_18.dim_region.Id_region  and morocco_04_18.fact_effectifs.Id_year = morocco_04_18.dim_year.Id_year",con=db)
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# df['text'] = df['Region'] + ' ' + 'Rate: ' +' '+ df['EvolutionP_R'].astype(str)
a=df[[ 'EvolutionP_R','EvolutionSC_R','EvolutionSQ_R']].head(0)
mask1 = df["Year"] == '2012'
df0 = df[mask1]
pp=df0.groupby("Region")['EffectifsSQ_R'].agg(sum),
print(pp)
layout = html.Div([
html.Hr(),
html.Br(),

        html.Div([
            dcc.Dropdown(
                id='el',
                options=[{'value': x, 'label': x}
                         for x in a.columns],
                value=a.columns[-1:], ),
        dcc.Input(id='input_state', type='number', inputMode='numeric', value=2004,
                  max=2018, min=2004, step=1, required=True),
        html.Button(id='submit_button', n_clicks=0, children='Submit')],style={'text-align': 'center'}),

html.Hr(),
html.Br(),
    html.Div([
        html.Div(id='S1', className="three columns",
                 style={'height': '50px', 'width': '200px', 'background-color': 'white', 'color': '#9CDBE7',
                        'text-align': 'center', 'vertical-align': 'middle', 'line-height': '50px',
                        'font-size': '20px'}),
        html.Div(id='LY1', className="three columns",
                 style={'height': '50px', 'width': '200px', 'background-color': 'white', 'color': '#9CDBE7',
                        'text-align': 'center', 'vertical-align': 'middle', 'line-height': '50px',
                        'font-size': '20px'}),
        html.Div(id='rate1', className="three columns",
                 style={'height': '50px', 'width': '200px', 'background-color': 'white', 'color': '#9CDBE7',
                        'text-align': 'center', 'vertical-align': 'middle', 'line-height': '50px',
                        'font-size': '20px'}),
        html.Br(),
    ], className="row", style={'width': '50%', 'margin': '0 auto'}),
html.Hr(),
html.Br(),

   html.Div([   html.Div([dcc.Graph(id='the_graph')],className="four columns"),
                html.Div([dcc.Graph(id='t6', figure={})],className="four columns"),
             ],className="row"),



],style={ 'margin': '0 auto'})
#---------------------------------------------------------------
@app.callback(

    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='input_state', component_property='value')],
    [State(component_id='el', component_property='value')],
)

def update_map(num_clicks,val_selected,edlev):



    if val_selected is None:
        raise PreventUpdate
    else:
        mask = df['Year'] == str(val_selected)
        df1 = df[mask]
        df1['text'] = df1['Region'] + ' ' + 'Rate: ' + ' ' + df1[edlev].astype(str) + ' ' + df1['Year']
        fig = go.Figure(data=go.Scattergeo(
                locationmode='ISO-3',
                lon=df1['Longitude'],
                lat=df1['Latitude'],
                text=df1['text'],
                mode='markers',
                marker=dict(
                    size=8,
                    opacity=0.8,
                    reversescale=True,
                    autocolorscale=False,
                    symbol='square',
                    line=dict(
                        width=1,
                        color='rgba(102, 102, 102)'
                    ),
                    colorscale='Blues',
                    color=df1[edlev],
                    cmin=df1[edlev].min(),
                    cmax=df1[edlev].max(),
                    colorbar_title="Evolution rate"
                )
            )
        )

        fig.update_layout(
            title='Most trafficked US airports<br>(Hover for Region names)',
            geo=dict(
                scope='africa',
                showland=True,
                landcolor="rgb(250, 250, 250)",
                subunitcolor="rgb(217, 217, 217)",
                countrycolor="rgb(217, 217, 217)",
                countrywidth=0.5,
                subunitwidth=0.5
            ),
            margin=dict(l=60, r=60, t=50, b=50)
        )

        return  fig

@app.callback(
    Output("t6", "figure"),
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='input_state', component_property='value')],
    [State(component_id='el', component_property='value')],
)

def update_bar_chart(num_clicks,val_selected,edlev):
    mask1 = df["Year"] == str(val_selected)
    mask2 = df["Year"] == str(int(val_selected)-1)
    df0=df[mask1]
    df1=df[mask2]
    if edlev == 'EvolutionP_R':
        x1 = 'EffectifsP_R'
    if edlev == 'EvolutionSC_R':
        x1 = 'EffectifsSC_R'
    if edlev == 'EvolutionSQ_R':
        x1 = 'EffectifsSQ_R'

    trace1 = go.Bar(    #setup the chart for the selected year
        x=df0["Region"].unique(), #x for the selected year
        y=df0['EffectifsSQ_R'],#y for the selected year
        marker_color=px.colors.qualitative.Dark24[0],  #color
        text=df0['EffectifsSQ_R'], #label/text
        textposition="outside", #text position
        name="Selected year", #legend name
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
        paper_bgcolor="#fdf2ff", #setup the background color
        width=850,
        height=500,
    )
    fig1.update_traces(texttemplate="%{text:.2s}") #text formart
    return fig1

#------------------------------------------------------------------------

@app.callback(
    Output('S1', component_property='children'),
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='input_state', component_property='value')],
    [State(component_id='el', component_property='value')],)
def update_bar_chart(num_clicks,val_selected,edlev):

    mask = df["Year"] == str(int(val_selected)-1)
    df3 = df[mask]
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
    Output('LY1', component_property='children'),
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='input_state', component_property='value')],
    [State(component_id='el', component_property='value')],)
def update_bar_chart(num_clicks,val_selected,edlev):

    mask = df["Year"] == str(int(val_selected))
    df3 = df[mask]
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
    Output('rate1', component_property='children'),
    [Input('LY1',component_property='children'),
     Input('S1', component_property='children')
     ])
def update_bar_chart(lyear,year):
    rate = (int(lyear)-int(year))/int(year)
    return round(rate*100,1)