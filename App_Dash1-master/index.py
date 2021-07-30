import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server
# Connect to your app pages
from apps import test_page1, test_page2, home_page, test_page3, province,map2015 , map2014, provincetta15
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
                dbc.DropdownMenu(
                    [dbc.DropdownMenuItem(dbc.NavLink("Page 1", href="/apps/Eff_by", active="exact"), style={'font-size': '20px'}),
                     dbc.DropdownMenuItem(dbc.NavLink("map2015", href="/apps/map15", active="exact"),style={'font-size': '20px'}),
                    dbc.DropdownMenuItem(dbc.NavLink("map2014", href="/apps/map14", active="exact"),style={'font-size': '20px'}),
                     ],
                    label="Region",
                    nav=True,
                    style={'font-size': '20px'}
                ),
                dbc.DropdownMenu(
                    [dbc.DropdownMenuItem(dbc.NavLink("Province", href="/apps/prov", active="exact"),
                                          style={'font-size': '20px'}),
                     dbc.DropdownMenuItem(dbc.NavLink("provincetta15", href="/apps/prov15", active="exact"),
                                          style={'font-size': '20px'}),
                     ],
                    label="Province",
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
   dbc.Row(dbc.Col(html.Div(sidebar),),),
   dbc.Row(dbc.Row(html.Div(id='page-content', children=[]),),),

],className="body")
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/Eff_by':
        return test_page1.layout
    if pathname == '/apps/prov':
        return province.layout
    if pathname == '/apps/map15':
        return map2015.layout
    if pathname == '/apps/map14':
        return map2014.layout
    if pathname == '/apps/prov15':
        return provincetta15.layout
    else:
        return home_page.layout

if __name__ == '__main__':
    app.run_server(debug=True,port=8053)

