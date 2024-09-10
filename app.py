import dash
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
plot_df = pd.read_csv('PCA2_galena_grains.csv')

# Color
title_color = '#5e9dd7'
axis_color = '#93bde3'
point_color = '#5eaeeb'
clicked_pt_color = '#ffbe0a'
tick_color = '#c8c8c8'

# Create the PCA graph
fig = make_subplots(rows=1, cols=3, vertical_spacing=1)
fig.append_trace(go.Scatter(x=plot_df['Principal component 1'], y=plot_df['Principal component 2'], mode="markers", hoverinfo='text', text=plot_df['Target']), row=1, col=1)
fig.append_trace(go.Scatter(x=plot_df['Principal component 2'], y=plot_df['Principal component 3'], mode="markers", hoverinfo='text', text=plot_df['Target']), row=1, col=2)
fig.append_trace(go.Scatter(x=plot_df['Principal component 1'], y=plot_df['Principal component 3'], mode="markers", hoverinfo='text', text=plot_df['Target']), row=1, col=3)
fig.update_traces(marker=dict(color=[point_color] * len(plot_df)))  # Initialize with blue color
# Dictionnaries for axis label style
axis_font=dict(family='Arial, sans-serif', size=16, color=axis_color)

# Update xaxis properties
fig.update_xaxes(title_text="<b>PC 1: Size</b>", titlefont=axis_font, tickfont=dict(family='Arial, sans-serif', color=tick_color, size=13), gridcolor=tick_color, row=1, col=1)
fig.update_xaxes(title_text="<b>PC 2: Roundness</b>", titlefont=axis_font, tickfont=dict(family='Arial, sans-serif', color=tick_color, size=13), gridcolor=tick_color, row=1, col=2)
fig.update_xaxes(title_text="<b>PC 1: Size</b>", titlefont=axis_font, tickfont=dict(family='Arial, sans-serif', color=tick_color, size=13), gridcolor=tick_color, row=1, col=3)
# Update yaxis properties
fig.update_yaxes(title_text="<b>PC 2: Roundness</b>", titlefont=axis_font, tickfont=dict(family='Arial, sans-serif', color=tick_color, size=13), gridcolor=tick_color, row=1, col=1)
fig.update_yaxes(title_text="<b>PC 3: Roughness</b>", titlefont=axis_font, tickfont=dict(family='Arial, sans-serif', color=tick_color, size=13), gridcolor=tick_color, row=1, col=2)
fig.update_yaxes(title_text="<b>PC 3: Roughness</b>", titlefont=axis_font, tickfont=dict(family='Arial, sans-serif', color=tick_color, size=13), gridcolor=tick_color, row=1, col=3)

# Update labels for the first subplot
fig.update_layout(height=500, width=1340, plot_bgcolor='#36393e', paper_bgcolor='#36393e', showlegend=False)

app.layout = html.Div([
    # Title box
    html.Div([
        html.H1('Intercative PCA plot showing results obtained with galena grain images for the three principal components.')
    ], style={'display': 'flex', 'flexDirection': 'row', 'textAlign': 'center', 'padding': '1.5rem', 'color': title_color, 'font-family': 'Arial', 'font-weight': 'bold'}),
    
    # Text container on the left
    html.Div([
        html.P(
            'The graphs below show the result of the three principal components (PC1 to 3) analysis on the galena shape descriptors. The shape descriptors are extracted from the galena binary images using python.'
            'The librairy is available on GitHub using the following link <>. When you click on a data point, the corresponding image alongside its label will be displayed below the graph, and the data point will turn yellow across all subplots.'
            'The displayed images have a fixed size but the aspect ration is kept. PC1 likely sorts the grains by size (visible thanks to the image resolution), PC2 by roundness, and PC3 by rugosity.')],
            style={'textAlign': 'left', 'margin': '1.25rem', 'color': 'white', 'font-family': 'Arial'}),
    
    # Graph container at the top
    html.Div([
        dcc.Graph(id='scatter-plot', figure=fig),
        dcc.Store(id='last-clicked', data=None),
    ], style={'display': 'flex', 'flexDirection': 'row', 'justify-content': 'center'}),
    
    # Image container on the right
    html.Div(
        id='image-container', style={'flex': '1', 'textAlign': 'center', 'padding': '10px', 'color':clicked_pt_color}
    ),

], style={'backgroundColor': '#36393e', 'color': 'white', 'font-family': 'Arial', 'justify-content': 'center'})

# Function needed for the app
def get_image_path(target_value):
    # Function to get the image path
    return f'Galena_binary_images/{target_value}' #Galena_binary_images/ #Github
    
def display_image_link(clickData, figure, last_clicked):
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
                trace['marker']['color'] = [point_color] * len(plot_df)

        # Update the marker color for all traces
        for trace in figure['data']:
            if last_clicked is not None:
                trace['marker']['color'][last_clicked] = point_color  # Reset previous clicked point color
            trace['marker']['color'][point_index] = clicked_pt_color  # Set new clicked point color

        new_last_clicked = point_index

        # Display the image with maintained aspect ratio
        image_div = html.Div([
            html.Img(src=f'data:image/png;base64,{encoded_image}', style={'width': 'auto', 'height': '25rem', 'margin': '0 auto'}),
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
