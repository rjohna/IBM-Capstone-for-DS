
# In this lab, you will build a Plotly Dash application 
# for users to perform interactive visual analytics 
# on SpaceX launch data in real-time.

# The application contains input components 
# such as a dropdown list and a range slider to interact 
# with a pie chart and a scatter point chart. 

# You will be guided to build this dashboard application
# with the following tasks:

# TASK 1: Add a Launch Site Drop-down Input Component
# TASK 2: Add a callback function to render success-pie-chart 
#         based on selected site dropdown
# TASK 3: Add a Range Slider to Select Payload
# TASK 4: Add a callback function to render the 
#         success-payload-scatter-chart scatter plot



# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
    

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
    

# Create a dash application
app = dash.Dash(__name__)
    

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                            style={'textAlign': 'center', 'color': '#503D36',
                                                   'font-size': 40}),

                                    # TASK 1: Add a Launch Site Drop down Input Compnent
                                    dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                            ],
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                            ),
                                    html.Br(),
                                    
    

                                    # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                    # If launch site was selected, show Success vs. Failed counts for the site
                                    html.Div(dcc.Graph(id='success-pie-chart')),
                                    html.Br(),           
                                    
                                    html.P("Payload range (Kg):"),

                                    # TASK 3: Add a slider to select payload range
                                    dcc.RangeSlider(id='payload-slider',
                                        min=0, max=10000, step=1000,
                                        marks={0: '0',
                                            1000: '1000',
                                            2000: '2000',
                                            3000: '3000',
                                            4000: '4000',
                                            5000: '5000',
                                            6000: '6000',
                                            7000: '7000',
                                            8000: '8000',
                                            9000: '9000',
                                            10000: '10000'
                                            },
                                        allowCross=False,
                                        value=[min_payload, max_payload]),

                                    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                    ])
    

# TASK 2:
#Add callback function for `site-dropdown` as input, `success-pie-chart` based on selected site dropdown
#Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
        Input(component_id='site-dropdown', component_property='value'))
    

def get_pie_chart(entered_site):
        filtered_df = spacex_df
        if entered_site == 'ALL':
            fig = px.pie(filtered_df, values='class', 
            names='Launch Site', 
            title='Launch Site Success Rate')
            return fig
        else:
            # return the outcomes piechart for a selected site
            filtered_df=spacex_df[spacex_df['Launch Site']==entered_site]
            df1=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
            title_pie = f'Success count for {entered_site}'
            fig=px.pie(df1,values='class count',names='class',title=title_pie)
            return fig
    

# TASK 4:
# Add a callback function to render the success-payload-scatter-chart scatter plot
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                    [Input(component_id='site-dropdown', component_property='value'), 
                    Input(component_id="payload-slider", component_property="value")])
    

def get_scatter(entered_site, slider_range):
    

        low, high = slider_range
        slide=(spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        dropdown_scatter=spacex_df[slide]
    

        if entered_site == 'ALL':
            fig = px.scatter(
                dropdown_scatter, x='Payload Mass (kg)', y='class',
                hover_data=['Booster Version'],
                color='Booster Version Category',
                title='Correlation between Payload and Success for all Sites')
            return fig
        else:
            dropdown_scatter = dropdown_scatter[spacex_df['Launch Site'] == entered_site]
            title_scatter = f'Success by Payload Size for {entered_site}'
            fig=px.scatter(
                dropdown_scatter,x='Payload Mass (kg)', y='class', 
                title = title_scatter, 
                color='Booster Version Category')
            return fig

            
# Run the app
if __name__ == '__main__':
    app.run_server()