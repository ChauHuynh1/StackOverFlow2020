import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Load data
df = pd.read_csv('survey.csv', delimiter=',')

# Initialise the app
app = dash.Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


# Define the app
app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                  # Define the left element
                                  html.Div(className='four columns div-user-controls',
                                           children = [
                                                html.H2('Assignment 1: Data Preparation and Exploration'),
                                                html.P('''Student Name: Nguyen Dang Huynh Chau'''),
                                                html.P('''Student ID: s3777214'''),
                                                html.P('''Lecturer: Vo Ngoc Yen Nhi'''),
                                                html.Br(),
                                                #Drop down button for graph 1
                                                dcc.Dropdown(
                                                    id='dropDown',
                                                    options=[
                                                        {'label': 'Converted Comp Yearly', 'value': 'ConvertedCompYearly'},
                                                        {'label': u'Years Code', 'value': 'YearsCode'}
                                                    ],
                                                    value='MainBranch'
                                                ),
                                                html.Br(),
                                                #Radio down button for graph 2
                                                html.Label('Select component for second graph'),
                                                dcc.RadioItems(
                                                    id='radioButton',
                                                    options=[{'label': i, 'value': i} for i in ['Age', 'EdLevel']],
                                                    value='Age',
                                                    labelStyle={'display': 'inline-block', 'marginTop': '5px'}
                                                ),
                                                
                                                html.Br(),
                                                #Check box for graph 3
                                                html.Label('Checkboxes'),
                                                dcc.Checklist(
                                                    id='checkBox',
                                                    options=[
                                                        {'label': 'New York City', 'value': 'NYC'},
                                                        {'label': u'Montréal', 'value': 'MTL'},
                                                        {'label': 'San Francisco', 'value': 'SF'}
                                                    ],
                                                    value=['MTL', 'SF']
                                                ),
                                           ]
                                  ),  
                                  
                                  # Define the right element
                                  html.Div(className='eight columns div-for-charts',
                                            children = [
                                                dcc.Graph(id='graph-with-slider'),
                                                
                                                dcc.Slider(
                                                    id='year-slider',
                                                    min=df['YearsCode'].min(),
                                                    max=df['YearsCode'].max(),
                                                    value=df['YearsCode'].min(),
                                                    marks={ 0: '00.00', 5: '5.00', 10: '10.00', 15: '15.00', 20: '20.00', 25: '25.00', 30: '30.00', 35: '35.00',
                                                            40: '40.00', 45: '45.00', 50: '50.00', 55: '55.00', 60: '60.00' }, 
                                                    step=None
                                                ),
                                                html.Br(),
                                                html.Br(),
                                                html.Br(),

                                                dcc.Graph(id='graph-with-RadioButton')

                                            ]
                                        )
                                  ])
                                ])

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value'),
     Input('dropDown', 'value'),
    ])
def update_figure(selected_year, selected_column):
    filtered_df = df[df.YearsCode >= selected_year]

    if(selected_column == "YearsCode"):
        fig = px.scatter(filtered_df, x='YearsCode', y='EdLevel', color="MainBranch")
    else:
        fig = px.scatter(filtered_df, x='ConvertedCompYearly', y='MainBranch', color="EdLevel")

    return fig


@app.callback(
    Output('graph-with-RadioButton', 'figure'),
    [Input('year-slider', 'value'),
     Input('radioButton', 'value'),
    ])
def update_figure(selected_year, selected):
    filtered_df = df[df.YearsCode >= selected_year]
    
    filtered_df = df[df.ConvertedCompYearly <= 60000]
    
    filtered_df.query('MainBranch == "i am a developer by profession" ', inplace = True)

    if(selected == "EdLevel"):
        fig = px.scatter(filtered_df, x='ConvertedCompYearly', y='Country', color="EdLevel")
    else:
        fig = px.scatter(filtered_df, x='ConvertedCompYearly', y='Country', color="Age")
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)