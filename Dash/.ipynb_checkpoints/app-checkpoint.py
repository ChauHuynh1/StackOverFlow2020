import pandas as pd

# load data
abalone_p ="abalone.data.csv"
df = pd.read_csv(abalone_p, sep=',', decimal='.', header=None,
names=['Sex', 'Length', 'Diameter', 'Height', 'Whole weight', 'Shucked weight', 'Viscera weight', 'Shell weight', 'Rings'])

# column list to choose from
column_list = ['Length', 'Diameter', 'Height', 'Whole weight', 'Shucked weight', 'Viscera weight', 'Shell weight', 'Rings']


# import dash
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Initialise the app
app = dash.Dash(__name__)


# Callback for interactive scatterplot
@app.callback(Output('scatterplot', 'figure'),
              [Input('selector1', 'value'), Input('selector2', 'value')])
def update_scatterplot(selector1, selector2):
    ''' Draw traces of the feature 'value' based one the currently selected column '''
    # STEP 1
    trace = []  
    df_sub = df
    # STEP 2
    # Draw and append traces for each column
    for gender in list(df_sub['Sex'].unique()):   
        trace.append(go.Scatter(x=df_sub[df_sub['Sex'] == gender][selector1],
                                 y=df_sub[df_sub['Sex'] == gender][selector2],
                                 mode='markers',
                                 name=gender,
                                 textposition='bottom center'))  
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  autosize=True,
                  title={'text': 'Abalone Scatter Plot based on Sex', 'font': {'color': 'white'}, 'x': 0.5},
              ),
              }
    return figure



# Define the app
app.layout = html.Div(
    children=[
        html.Div(className='row',  # Define the row element
                 children=[
                     
                     # Define the left element
                     html.Div(className='four columns div-user-controls',
                              children = [
                                  html.H2('Abalone Visualisation Dashboard'),
                                  html.P('''Visualising the abalone dataset with Plotly - Dash'''),
                                  html.P('''Pick the x and y columns from the dropdown below.'''),
                                # Adding option to select columns
                                  html.Div(className='div-for-dropdown',
                                           children=[
                                               dcc.Dropdown(id='selector1',
                                                            options=[
                                                                {"label": i, "value": i}
                                                                for i in column_list
                                                            ],
                                                            multi=False,
                                                            placeholder="Select x column",
                                                            value='Diameter',
                                                           )
                                           ]
                                          ),
                                  html.Div(className='div-for-dropdown',
                                           children=[
                                               dcc.Dropdown(id='selector2',
                                                            options=[
                                                                {"label": i, "value": i}
                                                                for i in column_list
                                                            ],
                                                            multi=False,
                                                            placeholder="Select y column",
                                                            value='Rings',
                                                           )
                                           ]
                                          ),

                              ]
                             ),


                     
                     # Define the right element
                     html.Div(className='eight columns div-for-charts bg-grey',
                              children = [
                                  dcc.Graph(id='scatterplot',
                                            config={'displayModeBar': False},
                                            animate=True,
#                                             figure=px.scatter(df,
#                                                               x='Diameter',
#                                                               y='Rings',
#                                                               color='Sex',
#                                                               template='plotly_dark').update_layout(
#                                                 {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
#                                                  'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                                           )
                              ]
                             )

                 ]
                )
    ]

)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=True)
