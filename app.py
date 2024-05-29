import dash
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import base64

# Initiate the app
app = dash.Dash(__name__)
server = app.server

# Get the PCA data
plot_df = pd.read_csv('PCA_galena_grains.csv')

# Create the PCA graph
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.06)
fig.append_trace(go.Scatter(x=plot_df['Principal component 1'], y=plot_df['Principal component 2'], mode="markers", hoverinfo='text', text=plot_df['Target']), row=1, col=1)
fig.append_trace(go.Scatter(x=plot_df['Principal component 2'], y=plot_df['Principal component 3'], mode="markers", hoverinfo='text', text=plot_df['Target']), row=1, col=2)
fig.append_trace(go.Scatter(x=plot_df['Principal component 1'], y=plot_df['Principal component 3'], mode="markers", hoverinfo='text', text=plot_df['Target']), row=1, col=3)
fig.update_traces(marker=dict(color=['blue'] * len(plot_df)))  # Initialize with blue color
# Dictionnaries for axis label style
axis_font=dict(family='Arial, sans-serif', size=14, color='black')

# Update xaxis properties
fig.update_xaxes(title_text="<i>PC 1</i>", titlefont=axis_font, row=1, col=1)
fig.update_xaxes(title_text="<i>PC 2</i>", titlefont=axis_font, row=1, col=2)
fig.update_xaxes(title_text="<i>PC 1</i>", titlefont=axis_font, row=1, col=3)
# Update yaxis properties
fig.update_yaxes(title_text="<i>PC 2</i>", titlefont=axis_font, row=1, col=1)
fig.update_yaxes(title_text="<i>PC 3</i>", titlefont=axis_font, row=1, col=2)
fig.update_yaxes(title_text="<i>PC 3</i>", titlefont=axis_font, row=1, col=3)
# Update labels for the first subplot
fig.update_layout(height=500, width=1340, title={'text': '<b>Intercative PCA plot showing result obtained with<br>galena grain images for the three principal components.</b>',
                                                'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'}, template='simple_white', showlegend=False)
# Application layout
app.layout = html.Div([
    # Graph container at the top
    dcc.Graph(id='scatter-plot', figure=fig),
    dcc.Store(id='last-clicked', data=None),
    # Container for the image and text side by side
    html.Div([
        # Text container on the left
        html.Div([
            html.P(
                'This is the explanatory text for the graph. It provides details and context to help interpret the visualized data. '
                'You can add as much text as needed here to explain the graph clearly.',
                style={'textAlign': 'left', 'margin': '20px'}
            )
        ], style={'flex': '1', 'padding': '10px'}),
        # Image container on the right
        html.Div(
            id='image-container', style={'flex': '1', 'textAlign': 'center', 'padding': '10px'}
        ),
    ], style={'display': 'flex', 'flexDirection': 'row'}),
], style={'backgroundColor': 'white', 'color': 'black', 'font-family': 'Arial'})

# Function needed for the app
def get_image_path(target_value):
    # Function to get the image path
    return f'Galena_binary_images/{target_value}'

def display_image_link(clickData, figure, last_clicked):
    # Function that the the image related to the point clecked and change its color 
    # for visualization purposes
    if clickData:
        point_clicked = clickData['points'][0]
        target_value = point_clicked['text']
        point_index = point_clicked['pointIndex']
        # Get the image path, read it and encode
        image_path = get_image_path(target_value)
        encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode()
        # Ensure 'color' is a list of colors for all traces
        for trace in figure['data']:
            if isinstance(trace['marker']['color'], str):
                trace['marker']['color'] = ['blue'] * len(plot_df)
        # Update the marker color for all traces
        for trace in figure['data']:
            if last_clicked is not None:
                trace['marker']['color'][last_clicked] = 'blue'  # Reset previous clicked point color
            trace['marker']['color'][point_index] = 'red'  # Set new clicked point color

        new_last_clicked = point_index
        # Display the image with maintained aspect ratio
        image_div = html.Div([
            html.Img(src=f'data:image/png;base64,{encoded_image}', style={'width': 'auto', 'height': '400px', 'margin': '0 auto'}),
            html.Br(),
            html.H4(target_value.rsplit('.', 1)[0], style={'textAlign': 'center'})
        ])
        return figure, image_div, new_last_clicked
    return figure, "Click on a point to see the image", last_clicked

# Callback needed
@app.callback(
    Output('scatter-plot', 'figure'),
    Output('image-container', 'children'),
    Output('last-clicked', 'data'),
    Input('scatter-plot', 'clickData'),
    State('scatter-plot', 'figure'),
    State('last-clicked', 'data')
)

def update_figure(clickData, figure, last_clicked):
    # Function taht update the figure
    return display_image_link(clickData, figure, last_clicked)

if __name__ == '__main__':
    app.run_server(debug=True)
