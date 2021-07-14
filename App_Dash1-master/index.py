import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import test_page1, test_page2

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Effectif by year |  ', href='/apps/Eff_by'),
        dcc.Link('rate _by year', href='/apps/rate_by'),
    ], className="row"),
    html.Div(id='page-content', children=[]),
],className="body")


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/Eff_by':
        return test_page1.layout
    if pathname == '/apps/rate_by':
        return test_page2.layout
    else:
        return "choose a page"


if __name__ == '__main__':
    app.run_server(debug=True,port=8051)

