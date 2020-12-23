## main page ##
### ONTARIO SCHOOLS COVID-19 ANALYSIS ###
#### PLOTLY DASH APP - VERSION 2.01 ####

##### BY: PETER STANGOLIS #####

## Import the required libraries ##
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import metrics, sch_select


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('(1) Daily Metrics |  ', href='/apps/metrics'),
        dcc.Link('(2) Search by School - Municipality', href='/apps/sch_select'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/metrics':
        return metrics.layout
    if pathname == '/apps/sch_select':
        return sch_select.layout
    else:
        return "Please choose a link above to view dashboard"


if __name__ == '__main__':
    app.run_server(debug=True)
