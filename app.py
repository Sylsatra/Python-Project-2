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

app.layout = dbc.Container(
    style={'background-color': '#E3F4F4'},
    fluid=True,
    children=[
        dbc.Row(
            style={'marginTop': '20px'},
            children=[
                dbc.Col(
                    width=3,
                    children=[
                        html.Div(
                            style={'padding': '10px', 'border-bottom': '2px solid white', 'background-color': 'white'},
                            children=[
                                html.H3('Our Products', style={'color': '#2c3e50', 'margin': '0', 'font-family': 'Arial'}),
                            ]
                        ),
                        html.A('Home Page', href='/', style={'display': 'block', 'margin-bottom': '20px', 'padding': '15px', 'color': '#2980b9', 'text-decoration': 'none', 'font-family': 'Arial', 'font-size': '18px', 'line-height': '24px', 'border': '1px solid #ddd', 'outline': 'none', 'box-shadow': '2px 2px 5px 0px rgba(0,0,0,0.3)'}),
                        html.A('PDF Report', id='pdf-link', href='/pdf', style={'display': 'block', 'margin-bottom': '20px', 'padding': '15px', 'color': '#2980b9', 'text-decoration': 'none', 'font-family': 'Arial', 'font-size': '18px', 'line-height': '24px', 'border': '1px solid #ddd', 'outline': 'none', 'box-shadow': '2px 2px 5px 0px rgba(0,0,0,0.3)'})
                    ]
                ),
                dbc.Col(
                    width=9,
                    children=[
                        dbc.Row(
                            style={'marginTop': '20px'},
                            children=[
                                dbc.Col(
                                    width=4,
                                    children=[
                                        html.Div(
                                            style={'border': '1px solid white', 'border-radius': '10px', 'background-color': 'white', 'margin-bottom': '20px', 'padding': '10px'},
                                            children=[
                                                                                               html.H4('Genders selection', style={'color': '#2980b9', 'margin': '10px'}),
                                                dcc.Dropdown(
                                                    id='gender-dropdown',
                                                    options=[
                                                        {'label': 'Male', 'value': 'M'},
                                                        {'label': 'Female', 'value': 'F'}
                                                    ],
                                                    value='M',
                                                    clearable=False
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    width=4,
                                    children=[
                                        html.Div(
                                            style={'border': '1px solid white', 'border-radius': '10px', 'background-color': 'white', 'margin-bottom': '20px', 'padding': '10px'},
                                            children=[
                                                html.H4('Degree types', style={'color': '#2980b9', 'margin': '10px'}),
                                                dcc.Dropdown(
                                                    id='degree-dropdown',
                                                    options=[
                                                        {'label': 'Science', 'value': 'Sci&Tech'},
                                                        {'label': 'Commerce', 'value': 'Comm&Mgmt'},
                                                        {'label': 'Arts', 'value': 'Arts'}
                                                    ],
                                                    value='Sci&Tech',
                                                    clearable=False
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    width=4,
                                    children=[
                                        html.Div(
                                            style={'border': '1px solid white', 'border-radius': '10px', 'background-color': 'white', 'margin-bottom': '20px', 'padding': '10px'},
                                            children=[
                                                html.H4('Select Scatter Plot', style={'color': '#2980b9', 'margin': '10px'}),
                                                dcc.Dropdown(
                                                    id='plot-dropdown',
                                                    options=[
                                                        {'label': 'Mixed Plot', 'value': 'mixed'},
                                                        {'label': 'Scatter Plot', 'value': 'scatter'}
                                                    ],
                                                    value='mixed',
                                                    clearable=False
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    width=12,
                                    children=[
                                        dcc.Graph(id='graph')
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    Output('graph', 'figure'),
    Input('gender-dropdown', 'value'),
    Input('degree-dropdown', 'value'),
    Input('plot-dropdown', 'value')
)
def update_graph(gender, degree, plot_type):
    if plot_type == 'mixed':
        filtered_data = data[(data['gender'] == gender) & (data['degree_t'] == degree)]
        fig = px.scatter(
            filtered_data,
            x='ssc_p',
            y='degree_p',
            color='degree_t',
            marginal_y='violin',
            marginal_x='box',
        )
        fig.update_layout(showlegend=False)
    elif plot_type == 'scatter':
        filtered_data = data[(data['gender'] == gender)]
        fig = px.scatter(
            filtered_data,
            x='degree_p',
            y='salary',
            color='gender',
        )
        fig.update_layout(showlegend=False)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

