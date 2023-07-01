import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import pandas as pd
from pandas_profiling import ProfileReport
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
                    style={'display': 'flex', 'justify-content': 'flex-end', 'margin-bottom': '20px'},
                    children=[
                        html.Div(
                          html.Img(src=app.get_asset_url('1.svg'), width='180px', height='55px'), style={'width': '210px','object-fit': 'cover', 'padding':'10px', 'margin': 'auto', 'margin-left': '10px', 'margin-right': '10px', 'border': '1px solid white', 'border-radius': '10px', 'box-shadow': '2px 2px 5px 0px rgba(0,0,0,0.3)', 'background-color': 'white'}
                        ),
                        html.Div(
                            style={'width': '300px', 'margin-left': '15px', 'margin-right': '10px', 'border': '1px solid white', 'border-radius': '10px', 'box-shadow': '2px 2px 5px 0px rgba(0,0,0,0.3)', 'background-color': 'white'},
                            children=[
                                html.H4('Genders selection', style={'color': '#2980b9', 'margin': '10px', 'font-family': 'Arial'}),
                                dcc.Dropdown(
                                    id='gender-dropdown',
                                    options=[
                                        {'label': 'Male', 'value': 'M'},
                                        {'label': 'Female', 'value': 'F'}
                                    ],
                                    value=[],
                                    multi=True,
                                    placeholder='Select Genders',
                                    style={'width': '97%', 'margin': 'auto','font-family': 'Arial'}
                                )
                            ]
                        ),
                        html.Div(
                            style={'width': '320px', 'margin-left': '15px', 'margin-right': '0px', 'border': '1px solid white', 'border-radius': '10px', 'box-shadow': '2px 2px 5px 0px rgba(0,0,0,0.3)', 'background-color': 'white'},
                            children=[
                                html.H3('Salary Slider', style={ 'fontSize':'16px','color': '#2980b9', 'margin': '10px', 'font-family': 'Arial'}),
                                dcc.Slider(
                                    id='salary-slider',
                                    min=data['salary'].min(),
                                    max=data['salary'].max(),
                                    step=100000,
                                    value=data['salary'].min(),
                                    marks={i*1000000: f'${i}M' for i in range(0, int(data['salary'].max() / 1000000), 100)},
                                ),
                                html.Div(id='salary-range-output')
                            ]
                        )
                    ]
                ),
                html.Div(
                    style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '20px'},
                    children=[
                        html.Div(
                            style={'width': '426.6px', 'border': '1px solid white', 'padding': '10px', 'margin-right': '10px', 'border-radius': '10px', 'box-shadow': '2px 2px 5px 0px rgba(0,0,0,0.3)', 'background-color': 'white'},
                            children=[
                                html.H4('Degree Types: Secondary & Graduation Percentage', style={'color': '#2980b9', 'margin': '10px', 'font-family': 'Arial','text-align': 'center'}),
                                dcc.Graph(
                                    id='mixed-graph',
                                    figure=mixed_fig,
                                    config={'displayModeBar': False},
                                    style={'width': '100%', 'height': '350px', 'object-fit': 'contain','font-family': 'Arial'}
                                )
                            ]
                        ),
                        html.Div(
                            style={'width': '426.6px', 'border': '1px solid white', 'padding': '10px', 'border-radius': '10px', 'box-shadow': '2px 2px 5px 0px rgba(0,0,0,0.3)', 'background-color': 'white'},
                            children=[
                                html.H4('Scatterplot: Salary, Education & Experience', style={'color': '#2980b9', 'margin': '10px', 'font-family': 'Arial','text-align': 'center'}),
                                dcc.Graph(
                                    id='scatterplot',
                                    figure=scatter_fig,
                                    config={'displayModeBar': False},
                                    style={'width': '100%', 'height': '350px', 'object-fit': 'contain','font-family': 'Arial'}
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '0px'},
                    children=[
                        html.Div(
                            style={'width': '270px', 'border': '1px solid white', 'padding': '10px', 'margin-right': '5px', 'border-radius': '10px', 'box-shadow': '2px 2px 5px 0px rgba(0,0,0,0.3)', 'background-color': 'white'},
                            children=[
                                html.H4('Degree types removal', style={'color': '#2980b9', 'margin': '10px', 'font-family': 'Arial'}),
                                dcc.Dropdown(
                                    id='remove-degree-dropdown',
                                    options=[
                                        {'label': 'Sci&Tech', 'value': 'Sci&Tech'},
                                        {'label': 'Comm&Mgmt', 'value': 'Comm&Mgmt'},
                                        {'label': 'Others', 'value': 'Others'}
                                    ],
                                    value=[],
                                    multi=True,
                                    placeholder='Remove Degree Categories',
                                    style={'width': '100%','font-family': 'Arial'}
                                )
                            ]
                        ),
                        html.Div(
                            style={'width': '270px', 'margin-left': '10px', 'margin-right': '10px', 'padding': '10px', 'border': '1px solid white', 'border-radius': '10px', 'box-shadow': '2px 2px 5px 0px rgba(0,0,0,0.3)', 'background-color': 'white'},
                            children=[
                                html.H4('Work Experience Removal', style={'color': '#2980b9', 'margin': '10px', 'font-family': 'Arial'}),
                                dcc.Dropdown(
                                    id='remove-workex-dropdown',
                                    options=[
                                        {'label': 'Yes', 'value': 'Yes'},
                                        {'label': 'No', 'value': 'No'}
                                    ],
                                    value=[],
                                    multi=True,
                                    placeholder='Remove Workex',
                                    style={'width': '100%','font-family': 'Arial'}
                                )
                            ]
                        ),
                        html.Div(
                            style={'width': '270px', 'border': '1px solid white', 'margin-left': '5px', 'padding': '10px', 'border-radius': '10px', 'box-shadow': '2px 2px 5px 0px rgba(0,0,0,0.3)', 'background-color': 'white'},
                            children=[
                                html.H4('Toggle Trendline', style={'color': '#2980b9', 'margin': '10px', 'font-family': 'Arial'}),
                                dcc.RadioItems(
                                    id='toggle-trendline',
                                    options=[
                                        {'label': 'Scatter', 'value': 'scatter'},
                                        {'label': 'Trendline', 'value': 'trendline'}
                                    ],
                                    value='scatter',
                                    labelStyle={'display': 'inline-block', 'margin-right': '10px','font-family': 'Arial'}
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

@app.server.route('/pdf')
def serve_pdf():
    pdf_path = 'assets/1.pdf'
    return flask.send_file(pdf_path, attachment_filename='1.pdf')
    
@app.callback(
    Output('salary-range-output', 'children'),
    Input('salary-slider', 'value')
)
def update_salary_range_output(salary):
    min_salary = '$0'  # Replace 0 with the actual minimum value
    max_salary = '$1000000'  # Replace 100000 with the actual maximum value

    return html.Div(
        [
            html.Div(f'{min_salary}', style={'font-family': 'Arial','color': '#2980b9', 'textAlign': 'left', 'marginTop': '-25px','marginLeft': '15px'}),
            html.Div(f'{max_salary}', style={'font-family': 'Arial','color': '#2980b9', 'textAlign': 'right', 'marginTop': '-25px','marginRight': '10px'})
        ],
        style={'display': 'flex', 'justifyContent': 'space-between'}
    )

@app.callback(
    Output('mixed-graph', 'figure'),
    Output('scatterplot', 'figure'),
    Input('gender-dropdown', 'value'),
    Input('salary-slider', 'value'),
    Input('remove-degree-dropdown', 'value'),
    Input('remove-workex-dropdown', 'value'),
    Input('toggle-trendline', 'value')
)
def update_graphs(gender_value, salary_value, remove_degree_value, remove_workex_value, trendline_value):
    filtered_data = data.copy()

    # Filter by gender
    if gender_value:
        filtered_data = filtered_data[filtered_data['gender'].isin(gender_value)]

    # Filter by salary
    filtered_data = filtered_data[filtered_data['salary'] >= salary_value]

    # Remove selected degree types
    if remove_degree_value:
        filtered_data = filtered_data[~filtered_data['degree_t'].isin(remove_degree_value)]

    # Remove selected workex values
    if remove_workex_value:
        filtered_data = filtered_data[~filtered_data['workex'].isin(remove_workex_value)]

    mixed_fig = px.scatter(
        filtered_data,
        x='ssc_p',
        y='degree_p',
        color='degree_t',
        marginal_y='violin',
        marginal_x='box',
        trendline='ols' if trendline_value == 'trendline' else None
    )
    # Update mixed_fig layout
    mixed_fig.update_layout(
        showlegend=False,
        xaxis_title='Secondary Education Percentage',
        yaxis_title='Graduation Degree Percentage',
        xaxis=dict(
            title=dict(
                font=dict(
                    family='Arial'
                )
            )
        ),
        yaxis=dict(
            title=dict(
                font=dict(
                    family='Arial'
                )
            )
        )
    )

    scatter_fig = px.scatter(
        filtered_data,
        x='degree_p',
        y='salary',
        color='gender',
        trendline='ols' if trendline_value == 'trendline' else None
    )
    # Update scatter_fig layout
    scatter_fig.update_layout(
        showlegend=False,
        xaxis_title='Secondary Education Percentage',
        yaxis_title='Salary',
        xaxis=dict(
            title=dict(
                font=dict(
                    family='Arial'
                )
            )
        ),
        yaxis=dict(
            title=dict(
                font=dict(
                    family='Arial'
                )
            )
        )
    )

    return mixed_fig, scatter_fig

if __name__ == '__main__':
    app.run_server(debug=True)
