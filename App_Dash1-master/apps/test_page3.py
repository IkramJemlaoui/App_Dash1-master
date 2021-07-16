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
db = mysql.connect(
    host='localhost',
    user='root',
    passwd='ikram',
    database="morroco1",
    auth_plugin='mysql_native_password',
)
df=pd.read_sql("select distinct(morocco_04_18.dim_region.Region), morocco_04_18.fact_effectifs.EffectifsP_R ,morocco_04_18.fact_effectifs.EvolutionP_R, morocco_04_18.dim_year.Year,morocco_04_18.dim_region.Latitude,morocco_04_18.dim_region.Longitude from morocco_04_18.dim_region, morocco_04_18.fact_effectifs, morocco_04_18.dim_year where  morocco_04_18.fact_effectifs.Id_region = morocco_04_18.dim_region.Id_region  and morocco_04_18.fact_effectifs.Id_year = morocco_04_18.dim_year.Id_year",con=db)
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
df['text'] = df['Region'] + ' ' + 'Rate: ' +' '+ df['EvolutionP_R'].astype(str)



layout = html.Div([

    dcc.Graph(id='the_graph'),

    html.Div([
        dcc.Input(id='input_state', type='number', inputMode='numeric', value=2004,
                  max=2018, min=2004, step=1, required=True),
        html.Button(id='submit_button', n_clicks=0, children='Submit'),
    ],style={'text-align': 'center'}),

])

#---------------------------------------------------------------
@app.callback(

    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='input_state', component_property='value')]
)

def update_output(val_selected):

    if val_selected is None:
        raise PreventUpdate
    else:

        mask = df['Year'] == str(val_selected)
        df1 = df[mask]
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
                    #             cmin = 0,
                    color=df1['EvolutionP_R'],
                    cmin=df1['EvolutionP_R'].min(),
                    cmax=df1['EvolutionP_R'].max(),
                    colorbar_title="Evolution rate<br>2017"
                )
            )
        )

        fig.update_layout(
            title='Most trafficked US airports<br>(Hover for airport names)',
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
