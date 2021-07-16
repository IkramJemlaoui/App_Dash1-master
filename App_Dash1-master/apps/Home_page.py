import dash_html_components as html
from dash_extensions import Lottie
import dash_bootstrap_components as dbc

B = "https://assets10.lottiefiles.com/packages/lf20_yRrgc4.json"

options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))
layout = html.Div([
    html.Div([
html.Div([dbc.CardHeader(Lottie(options=options, width="100%", height="100%", url=B))],
         className="three columns",style={'height': '350px', 'width': '1000px','background-color': 'rgb(253, 242, 524)'}),

    ]),
], className="body")