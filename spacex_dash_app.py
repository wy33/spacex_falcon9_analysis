# This dashboard application contains input components such as a dropdown list and a range slider to 
# interact with a pie chart and a scatter point chart. You will be guided to build this dashboard 
# application via the following tasks:

# TASK 1: Add a Launch Site Drop-down Input Component
# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
# TASK 3: Add a Range Slider to Select Payload
# TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot

# After visual analysis using the dashboard, you should be able to obtain some insights to answer the following five questions:

# Which site has the largest successful launches?
# Which site has the highest launch success rate?
# Which payload range(s) has the highest launch success rate?
# Which payload range(s) has the lowest launch success rate?
# Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest launch success rate?



# Install dependencies:
# python3.11 -m pip install pandas dash

# Download skeleton dashboard app and dataset:
# wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
# wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"

# Run app:
# python3.11 spacex_dash_app.py



import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites = spacex_df['Launch Site'].unique()
launch_sites = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=launch_sites,
                                    value='ALL',
                                    placeholder='Select a Launch Site',
                                    searchable=True,    # Can enter keywords to search for launch sites
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, 
            values='class', 
            names='Launch Site', 
            title='Total Launches by Site')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]['class'].value_counts()
        filtered_df = pd.DataFrame({
            'class': filtered_df.index, 
            'count': filtered_df.values
            })
        fig = px.pie(filtered_df, values='count', 
            names='class',
            title=f'Successful vs Unsuccessful Launches for site {entered_site}')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, entered_payload):
    filtered_df = spacex_df
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= entered_payload[0]) & 
                              (filtered_df['Payload Mass (kg)'] <= entered_payload[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, 
            x='Payload Mass (kg)', 
            y='class', 
            color='Booster Version Category', 
            title='Correlation between Payload Mass and Success for all Sites')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, 
            x='Payload Mass (kg)', 
            y='class', 
            color='Booster Version Category', 
            title=f'Correlation between Payload Mass and Success for {entered_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
