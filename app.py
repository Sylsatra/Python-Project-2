import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import os
import flask

app = dash.Dash(__name__)
server = app.server

# Create the scatter graph
data = pd.read_csv('data.csv')
mixed_fig = px.scatter(
    data,
    x='ssc_p',
    y='degree_p',
    color='degree_t',
    marginal_y='violin',
    marginal_x='box',
)
mixed_fig.update_layout(showlegend=False)

scatter_fig = px.scatter(
    data,
    x='degree_p',
    y='salary',
    color='gender',
)
scatter_fig.update_layout(showlegend=False)  # Remove the legend from the scatter plot

app.layout = html.Div(
    style={'background-color': '#E3F4F4', 'display': 'flex', 'height': '100vh', 'margin': '0 0 0 -15px'},
    children=[
        html.Div(
            style={'width': '320px', 'height': '590px', 'border': '1px solid #ddd', 'border-radius': '10px', 'margin': '10px', 'background-color': 'white', 'margin-right': '5px', 'padding': '20px', 'text-align': 'center', 'box-shadow': '2px 2px 5px 0px rgba(0,0,0,0.3)'},
            children=[
                # Side tab title
                html.Div(
                    style={'padding': '10px', 'border-bottom': '2px solid white', 'background-color': 'white'},
                    children=[
                        html.H3('Our Products', style={'color': '#2c3e50', 'margin': '0', 'font-family': 'Arial'}),
                    ]
                ),
                # Button 1
                html.A('Home Page', href='/', style={'background-color': 'white', 'display': 'block', 'margin-bottom': '20px', 'padding': '15px', 'color': '#2980b9', 'text-decoration': 'none', 'font-family': 'Arial', 'font-size': '18px', 'line-height': '24px', 'border': '1px solid #ddd', 'outline': 'none', 'box-shadow': '2px 2px 5px 0px rgba(0,0,0,0.3)'}),
                # Button 2
                html.A('PDF Report', id='pdf-link', href='/pdf', style={'background-color': 'white', 'display': 'block', 'margin-bottom': '20px', 'padding': '15px', 'color': '#2980b9', 'text-decoration': 'none', 'font-family': 'Arial', 'font-size': '18px', 'line-height': '24px', 'border': '1px solid #ddd', 'outline': 'none', 'box-shadow': '2px 2px 5px 0px rgba(0,0,0,0.3)'})
            ]
        ),
        html.Div(
            style={'flex': '1', 'padding': '0px 0px', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'flex-end', 'justify-content': 'top', 'margin': '10px'},
            children=[
                html.Div(
                    style={'display': 'flex', 'justify-content': 'flex-end', 'margin':'10px','bottom': '10px'},
                    children=[
                        # Dropdown menu
                        dcc.Dropdown(
                            id='graph-dropdown',
                            options=[
                                {'label': 'Mixed Graph', 'value': 'mixed'},
                                {'label': 'Scatter Graph', 'value': 'scatter'},
                            ],
                            value='mixed',
                            style={'width': '200px', 'margin-right': '10px'}
                        ),
                        # Button
                        html.Button('Update Graph', id='graph-button', n_clicks=0, style={'background-color': '#2980b9', 'color': 'white', 'border': 'none', 'border-radius': '5px', 'padding': '10px 20px', 'font-size': '14px', 'cursor': 'pointer'}),
                    ]
                ),
                # Graph
                dcc.Graph(id='graph'),
            ]
        )
    ]
)


@app.callback(
    Output('graph', 'figure'),
    Input('graph-button', 'n_clicks'),
    State('graph-dropdown', 'value')
)
def update_graph(n_clicks, graph_type):
    if graph_type == 'mixed':
        return mixed_fig
    elif graph_type == 'scatter':
        return scatter_fig
    else:
        return {}


if __name__ == '__main__':
    app.run_server(debug=True)

