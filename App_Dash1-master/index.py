import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import test_page1, test_page2, home_page, test_page3, province

from dash_extensions import Lottie
import dash_bootstrap_components as dbc

B = "https://assets2.lottiefiles.com/packages/lf20_Pth0RM.json"
B1 = "https://assets1.lottiefiles.com/packages/lf20_ffpacwo2.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

# styling the sidebar
SIDEBAR_STYLE = {
    "background-color": "#f8f9fa",
}
sidebar = html.Div(
    [
        dbc.Navbar(
            [
                dbc.NavLink("Home", href="/apps/", active="exact"),
                # dbc.NavLink("Page 1", href="/apps/Eff_by", active="exact"),
                dbc.NavLink("Page 2", href="/apps/rate_by", active="exact"),
                dbc.NavLink("Province", href="/apps/prov", active="exact"),
                dbc.DropdownMenu(
                    [dbc.DropdownMenuItem(dbc.NavLink("Page 1", href="/apps/Eff_by", active="exact"), style={'font-size': '20px'}),
                     dbc.DropdownMenuItem(dbc.NavLink("Page 3", href="/apps/map", active="exact"),style={'font-size': '20px'})],
                    label="Region",
                    nav=True,
                    style={'font-size': '20px'}
                ),
            ],
            expand='md',
            color="dark",
            dark=True,
            style={'font-size': '20px'}
        ),
    ],

)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # dbc.Row(dbc.Col(html.Div([
    #     html.H2("Rate by year"),
    #     html.Img(src="/assets/A.png")
    # ], className="banner"),),),
   dbc.Row(dbc.Col(html.Div(sidebar),),),
   dbc.Row(dbc.Row(html.Div(id='page-content', children=[]),),),

],className="body")
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/Eff_by':
        return test_page1.layout
    if pathname == '/apps/rate_by':
        return test_page2.layout
    if pathname == '/apps/map':
        return test_page3.layout
    if pathname == '/apps/prov':
        return province.layout
    else:
        return home_page.layout



if __name__ == '__main__':
    app.run_server(debug=True,port=8053)

