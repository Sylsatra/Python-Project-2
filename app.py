import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Step 1: Define sections
segment_style = {
    'width': '50%',
    'display': 'inline-block',
    'box-sizing': 'border-box',
    'padding': '10px',
    'vertical-align': 'top',
    'textAlign': 'center'
}

# Step 2: Load data and create scatterplots
data = pd.read_csv('Placement_Data_Full_Class.csv')

# Color for scatterplots
scatter_color_male = '#BED3CB'  # Pastel green
scatter_color_female = '#F9C3B2'  # Pastel pink

fig_male = px.scatter(data[data['gender'] == 'M'], x='degree_p', y='salary')
fig_male.update_traces(marker=dict(color=scatter_color_male))  # Set scatterplot marker color for male
fig_male.update_layout(xaxis_title='Degree Percentage', yaxis_title='Salary')

fig_female = px.scatter(data[data['gender'] == 'F'], x='degree_p', y='salary')
fig_female.update_traces(marker=dict(color=scatter_color_female))  # Set scatterplot marker color for female
fig_female.update_layout(xaxis_title='Degree Percentage', yaxis_title='Salary')

# Color for trendline graphs
trendline_color_male = '#FF9F9C'  # Pastel red
trendline_color_female = '#A7C8F2'  # Pastel blue

fig_male_trend = px.scatter(data[data['gender'] == 'M'], x='degree_p', y='salary', trendline='ols')
fig_male_trend.update_traces(marker=dict(color=scatter_color_male))  # Set scatterplot marker color for male
fig_male_trend.update_traces(line=dict(color=trendline_color_male))  # Set trendline color for male
fig_male_trend.update_layout(xaxis_title='Degree Percentage', yaxis_title='Salary')

fig_female_trend = px.scatter(data[data['gender'] == 'F'], x='degree_p', y='salary', trendline='ols')
fig_female_trend.update_traces(marker=dict(color=scatter_color_female))  # Set scatterplot marker color for female
fig_female_trend.update_traces(line=dict(color=trendline_color_female))  # Set trendline color for female
fig_female_trend.update_layout(xaxis_title='Degree Percentage', yaxis_title='Salary')

# Mixed graph
mixed_fig = px.scatter(
    data,
    x='ssc_p',
    y='degree_p',
    color='degree_t',
    marginal_y='violin',
    marginal_x='box',
    labels={
        'ssc_p': 'Secondary Education Percentage',
        'degree_p': 'Graduation Degree Percentage',
        'degree_t': 'Graduation Degree Type'
    }
)

mixed_fig.update_layout(
    xaxis_title='Secondary Education Percentage',
    yaxis_title='Graduation Degree Percentage',
    showlegend=True,
    legend=dict(
        x=1,
        y=1,
        bgcolor='rgba(255, 255, 255, 0.7)',
        bordercolor='rgba(0, 0, 0, 0.5)',
        borderwidth=1,
        itemwidth=30,
        itemsizing='constant'  # Set itemsizing to 'constant' for square legend items
    )
)
# Create the graph for Segment 4
fig_segment4 = go.Figure()

for i, facet in enumerate(data['hsc_s'].unique()):
    facet_data = data[data['hsc_s'] == facet]

    fig_segment4.add_trace(go.Box(
        x=facet_data['degree_t'],
        y=facet_data['sl_no'],
        name=facet,
        boxmean=True  # Show mean bar without transparency
    ))

fig_segment4.update_layout(
    xaxis_title='Degree Type',
    yaxis_title='Serial Number',
    xaxis_tickangle=-45,
    showlegend=True,
    legend=dict(
        x=1,
        y=1,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(0, 0, 0, 1)',
        borderwidth=1,
        itemwidth=30,
        title='Fields'  # Add the legend title here
    ),
    margin=dict(l=80, r=50, t=100, b=50),
    width=630,
    height=350,
    font=dict(size=10),
)

fig_segment4.update_xaxes(tickangle=-45)

# Step 4: Create app layout
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
app.layout = html.Div(
    style={'backgroundColor': '#C7EFCF', 'color': '#333333'},  # Set background color and text color
    children=[
        dcc.Tabs(
            id='tabs',
            value='visualize-tab',
            children=[
                dcc.Tab(
                    label='Visualize',
                    value='visualize-tab',
                    style={'backgroundColor': '#A2DED0', 'color': '#333333'},  # Set tab background color and text color
                    selected_style={'backgroundColor': '#66BDA3', 'color': '#FFFFFF'},  # Set selected tab background color and text color
                    children=[
                        html.Div([
                            html.Div(children=[
                                html.Div(
                                    id='graph-container',
                                    children=[
                                        html.Div([
                                            html.H2(
                                                'Percentage of Secondary Education and Graduation Degree',
                                                style={'color': '#66BDA3'}  # Set title color
                                            ),
                                            dcc.Graph(
                                                id='mixed-graph',
                                                figure=mixed_fig,
                                                style={'backgroundColor': '#F5FAF8'}  # Set graph background color
                                            ),
                                        ], style=segment_style),
                                        html.Div([
                                            html.H2(
                                                'The number of higher secondary education degree specializations across different fields and genders',
                                                style={'color': '#66BDA3'}  # Set title color
                                            ),
                                            dcc.Graph(
                                                id='segment4-graph',
                                                figure=fig_segment4,
                                                style={'backgroundColor': '#F5FAF8'}  # Set graph background color
                                            ),
                                            dcc.Checklist(
                                                id='degree-toggle',
                                                options=[{'label': t, 'value': t} for t in data['degree_t'].unique()],
                                                value=list(data['degree_t'].unique()),
                                                labelStyle={'display': 'inline-block', 'color': '#333333'},  # Set checkbox label text color
                                                style={'marginTop': '10px'}  # Add some margin to the checkbox
                                            ),
                                        ], style=segment_style),
                                    ],
                                ),
                                html.Div(children=[
                                    dcc.Dropdown(
                                        id='dropdown',
                                        options=[
                                            {'label': 'Both Scatters', 'value': 'both-scatter'},
                                            {'label': 'Trend line male', 'value': 'trend-male'},
                                            {'label': 'Trend line female', 'value': 'trend-female'},
                                        ],
                                        value='both-scatter',
                                        placeholder='Select an option',
                                        style={'width': '200px'}
                                    ),
                                ], style=segment_style),
                            ]),
                            html.Div(
                                id='visualize-tab-contents',
                                style={'color': '#333333'}  # Set text color
                            )  # Updated ID and text color for the div
                        ])
                    ]
                ),
                dcc.Tab(
                    label='Data',
                    value='data-tab',
                    style={'backgroundColor': '#A2DED0', 'color': '#333333'},
                    selected_style={'backgroundColor': '#66BDA3', 'color': '#FFFFFF'},
                    children=[
                        html.Div([
                            html.H2(
                                'Data Tab Content',
                                style={'color': '#66BDA3'}
                            ),
                            dash_table.DataTable(
                                id='data-table',
                                columns=[{'name': col, 'id': col} for col in data.columns],
                                data=data.to_dict('records'),
                                style_table={'overflowX': 'scroll'},
                                style_cell={'minWidth': '100px', 'textAlign': 'left'},
                                style_header={'fontWeight': 'bold'},
                                page_size=20
                            ),
                        ]),
                    ]
                ),
            ]
        )
    ]
)

# Step 5: Define the callbacks
@app.callback(
    Output('visualize-tab-contents', 'children'),  # Updated ID for the Output
    [Input('dropdown', 'value')]
)
def update_visualize_tab(selected_option):
    if selected_option == 'both-scatter':
        return [
            html.Div([
                html.H2('Earnings of Males by Degree Proportion'),
                dcc.Graph(id='scatter-male-graph', figure=fig_male),
            ], style=segment_style),
            html.Div([
                html.H2('Earnings of Females by Degree Proportion'),
                dcc.Graph(id='scatter-female-graph', figure=fig_female),
            ], style=segment_style),
        ]
    elif selected_option == 'trend-male':
        return [
            html.Div([
                html.H2('Trend line male'),
                dcc.Graph(id='trend-male-graph', figure=fig_male_trend),
            ], style=segment_style),
            html.Div([
                html.H2('Earnings of Females by Degree Proportion'),
                dcc.Graph(id='scatter-female-graph', figure=fig_female),
            ], style=segment_style),
        ]
    elif selected_option == 'trend-female':
        return [
            html.Div([
                html.H2('Earnings of Males by Degree Proportion'),
                dcc.Graph(id='scatter-male-graph', figure=fig_male),
            ], style=segment_style),
            html.Div([
                html.H2('Trend line female'),
                dcc.Graph(id='trend-female-graph', figure=fig_female_trend),
            ], style=segment_style),
        ]
    else:
        return []


@app.callback(
    Output('segment4-graph', 'figure'),
    [Input('degree-toggle', 'value')]
)
def update_segment4_graph(selected_degrees):
    filtered_data = data[data['degree_t'].isin(selected_degrees)]

    fig_segment4 = go.Figure()

    for i, facet in enumerate(filtered_data['hsc_s'].unique()):
        facet_data = filtered_data[filtered_data['hsc_s'] == facet]

        fig_segment4.add_trace(go.Box(
            x=facet_data['degree_t'],
            y=facet_data['sl_no'],
            name=facet,
             marker_color=px.colors.qualitative.Plotly[i % 100],
    marker=dict(
        opacity=1,
        color=px.colors.qualitative.Plotly[i % 100],
        line=dict(
            color=px.colors.qualitative.Plotly[i % 100],
            width=1
        )
    )
        ))

    fig_segment4.update_layout(
        xaxis_title='Degree Type',
        yaxis_title='Serial Number',
        xaxis_tickangle=-45,
        showlegend=True,
        legend=dict(
            x=1,
            y=1,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(0, 0, 0, 1)',
            borderwidth=1,
            itemwidth=30,
            title='Fields'  # Add the legend title here
        ),
        margin=dict(l=80, r=50, t=100, b=50),
        width=630,
        height=350,
        font=dict(size=10),
    )

    fig_segment4.update_xaxes(tickangle=-45)

    return fig_segment4


@app.callback(
    Output('data-display', 'children'),
    [Input('tabs', 'value')]
)
def update_data_tab(tab):
    if tab == 'data-tab':
        return [
            html.Code(data.to_csv(index=False))
        ]
    else:
        return []


# Step 6: Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
