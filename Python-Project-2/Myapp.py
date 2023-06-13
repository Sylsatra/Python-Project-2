
from flask import Flask, render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import io
import base64
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def index():
    # Load the data from the CSV file
    data = pd.read_csv("/Users/duongtrunghai/Desktop/Placement_Data_Full_Class.csv")  # Replace with the correct file path

    # Your data processing code
    grouped = data.groupby(['hsc_s', 'workex', 'status']).size().reset_index(name='count')

    placed_data = grouped[grouped['status'] == 'Placed']
    not_placed_data = grouped[grouped['status'] == 'Not Placed']

    # Create the placed bar chart
    placed_fig = px.bar(
        placed_data, 
        x='hsc_s', 
        y='count', 
        color='workex', 
        barmode='stack',
        labels={'count': 'Number of Candidates'},
        title='Placed Candidates by Higher Secondary Education and Work Experience',
        color_discrete_sequence=['#22A699', '#E1812C'],
        width=900,  
        height=700
    )

    # Create the not placed bar chart
    not_placed_fig = px.bar(
        not_placed_data, 
        x='hsc_s', 
        y='count', 
        color='workex', 
        barmode='stack',
        labels={'count': 'Number of Candidates'},
        title='Not Placed Candidates by Higher Secondary Education and Work Experience',
        color_discrete_sequence=['#22A699', '#E1812C'],
        width=900,  
        height=700
    )
     # Adjust the bar width for the placed bar chart
    placed_fig.update_traces(marker=dict(line=dict(width=1.2)))  # Adjust the width as needed

    # Adjust the bar width for the not placed bar chart
    not_placed_fig.update_traces(marker=dict(line=dict(width=1.2)))  # Adjust the width as needed

    # Adjust the gap between bars
    placed_fig.update_layout(bargap=0.3)  # Adjust the gap as needed
    not_placed_fig.update_layout(bargap=0.3)  # Adjust the gap as needed

    # Convert the figures to JSON strings
    placed_graph_json = placed_fig.to_json()
    not_placed_graph_json = not_placed_fig.to_json()

    return render_template('index.html', placed_graph=placed_graph_json, not_placed_graph=not_placed_graph_json)

if __name__ == '__main__':
    app.run(debug=True)
