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
fig = make_subplots(rows=3, cols=1, vertical_spacing=0.06)
fig.append_trace(go.Scatter(x=plot_df['Principal component 1'], y=plot_df['Principal component 2'], mode="markers", hoverinfo='text', text=plot_df['Target']), row=1, col=1)
fig.append_trace(go.Scatter(x=plot_df['Principal component 2'], y=plot_df['Principal component 3'], mode="markers", hoverinfo='text', text=plot_df['Target']), row=2, col=1)
fig.append_trace(go.Scatter(x=plot_df['Principal component 1'], y=plot_df['Principal component 3'], mode="markers", hoverinfo='text', text=plot_df['Target']), row=3, col=1)
fig.update_traces(marker=dict(color=['blue'] * len(plot_df)))
# Update xaxis labels
fig.update_xaxes(title_text="Principal component 1", row=1, col=1)
fig.update_xaxes(title_text="Principal component 2", row=2, col=1)
fig.update_xaxes(title_text="Principal component 1", row=3, col=1)
# Update yaxis labels
fig.update_yaxes(title_text="Principal component 2", row=1, col=1)
fig.update_yaxes(title_text="Principal component 3", row=2, col=1)
fig.update_yaxes(title_text="Principal component 3", row=3, col=1)
# Update the layout of the figure then the app
fig.update_layout(height=900, width=600, title="PCA plot with images", template='simple_white', showlegend=False)

app.layout = html.Div([
    dcc.Graph(id='scatter-plot', figure=fig, style={'width': '70%', 'display': 'inline-block'}),
    dcc.Store(id='last-clicked', data=None),
    html.Div(id='image-container', style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'})
], style={'backgroundColor': 'white', 'color': 'black', 'font-family': 'Arial'})
# Callback needed
@app.callback(Output('scatter-plot', 'figure'), Output('image-container', 'children'), Output('last-clicked', 'data'),
			  Input('scatter-plot', 'clickData'), State('scatter-plot', 'figure'), State('last-clicked', 'data'))

# Function needed for the app
def get_image_path(target_value):
    # Function to get the image path
    base_path = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    image_folder = 'Galena_binary_images'
    return os.path.join(base_path, image_folder, target_value)

def display_image_link(clickData, figure, last_clicked):
	# Function that displays the image of the clicked linked point in one of the three PCA plots, making the point red for visualization purposes.
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
            html.Img(src=f'data:image/png;base64,{encoded_image}',
					 style={'width': '400px', 'height': 'auto', 'margin': '0 auto'}),
            html.Br(),
            html.A('Open Graph in New Window', href='http://localhost:8050', target='_blank', 
                   style={'fontSize': '20px', 'textDecoration': 'none', 'color': 'blue'})
        ])
        return figure, image_div, new_last_clicked
    return figure, "Click on a point to see the image", last_clicked

if __name__ == '__main__':
	app.run_server(debug=True)
