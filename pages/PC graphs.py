import dash
from dash import html, callback, Output, Input, State, dcc, ctx
import pandas as pd

dash.register_page(__name__, path="/graphs", title="Interactive graphs")


from components.menu import default_df_name
from components.CustomPlot import CustomPlot
from components.selected_images import selected_image_1, selected_image_2

image_selection_tooltip = html.Div("", className="tooltip", id="images-selection-tooltip")

default_df = pd.read_csv('data/' + default_df_name)

loaded_data = {
    default_df_name: default_df
}

highlight_color = 'red'

g1 = CustomPlot(
    x='Principal component 1',
    y='Principal component 3',
    x_title="Principal Component 1",
    y_title="Principal Component 2",
    id="P1-P2",
    df=default_df,
    loaded_data=loaded_data,
)

g2 = CustomPlot(
    x='Principal component 2',
    y='Principal component 3',
    x_title="Principal Component 2",
    y_title="Principal Component 3",
    id="P2-P3",
    df=default_df,
    loaded_data=loaded_data,
)

g3 = CustomPlot(
    x='Principal component 1',
    y='Principal component 3',
    x_title="Principal Component 1",
    y_title="Principal Component 3",
    id="P1-P3",
    df=default_df,
    loaded_data=loaded_data,
)

layout = [
    html.Div([
        html.Div(g1, className="graph-container"),
        html.Div(g2, className="graph-container"),
        html.Div(g3, className="graph-container"),
    ], className="graphs-container"),

    html.Div([
        selected_image_1,
        selected_image_2,
        image_selection_tooltip,
    ], className="images-container"),

    dcc.Store(id="selected_points", data=(None, None)),
    dcc.Store(id="last_selected_points", data=(None, None))
]

@callback(
    Output('selected_points', 'data', allow_duplicate = True),
    Output('last_selected_points', 'data'),

    Input(g1.plot_id, 'clickData'),
    Input(g2.plot_id, 'clickData'),
    Input(g3.plot_id, 'clickData'),

    State('selected_points', 'data'),
    
    prevent_initial_call = True
)

def select_point(clickData1, clickData2, clickData3, selected_points):

    clicked_id = ctx.triggered_id

    clickData = clickData1 if clicked_id == g1.plot_id else clickData2 if clicked_id == g2.plot_id else clickData3

    next_selected_points = [selected_points[0], selected_points[1]]

    selected = clickData["points"][0]["pointNumber"] if clickData else None

    if selected:

        if selected in selected_points:
            index = next_selected_points.index(selected)
            if index == 0:
                next_selected_points = [next_selected_points[1], None]
            else:
                next_selected_points = [next_selected_points[0], None]

        else:
            if selected_points[0] is None:
                next_selected_points[0] = selected
            elif selected_points[1] is None:
                next_selected_points[1] = selected
            elif len(selected_points) == 2:
                next_selected_points[0] = next_selected_points[1]
                next_selected_points[1] = selected

    return tuple(next_selected_points), selected_points


@callback(
    Output('image-left', 'children'),
    Output('image-right', 'children'),
    Output('images-selection-tooltip', 'children'),

    Input('selected_points', 'data'),
    State('csv_name', 'data'),
)
def display_image(selected_points, csv_name):

    image_path_left, image_path_right = None, None
    
    df = loaded_data[csv_name]

    if selected_points[0]:
        point = df.values[selected_points[0]]
        image_path_left = "assets/Galena_binary_images/" + point[-1]
    else:
        image_path_left = None

    if selected_points[1]:
        point = df.values[selected_points[1]]
        image_path_right = "assets/Galena_binary_images/" + point[-1]
    else:
        image_path_right = None

    image_left = html.Div(html.Img(src=image_path_left) if image_path_left else "", className="left")
    image_right = html.Div(html.Img(src=image_path_right) if image_path_right else "", className="right")

    tooltip = "" if image_path_left or image_path_right else "Click on points to display their images !"

    return image_left, image_right, tooltip


@callback(
    Output(g1.plot_id, 'figure', allow_duplicate = True),
    Output(g2.plot_id, 'figure', allow_duplicate = True),
    Output(g3.plot_id, 'figure', allow_duplicate = True),

    Input(g1.plot_id, 'figure'),
    Input(g2.plot_id, 'figure'),
    Input(g3.plot_id, 'figure'),
    Input('selected_points', 'data'),

    State('last_selected_points', 'data'),

    prevent_initial_call = True
)
def sync_point_selection(f1 , f2, f3, selected_points, last_selected_points):


    for figure in [f1, f2, f3]:

        trace = figure['data'][0]

        generic_point_index = 0
        while generic_point_index in last_selected_points:
            generic_point_index += 1

        default_color = trace['marker']['color'][generic_point_index]
        default_size = trace['marker']['size'][generic_point_index]

        for point in last_selected_points:
            if point is not None:
                trace['marker']['color'][point] = default_color
                trace['marker']['size'][point] = default_size

        for point in selected_points:
            if point is not None:
                trace['marker']['color'][point] = highlight_color
                trace['marker']['size'][point] = default_size + 5
        

    return f1, f2, f3


@callback(    
    Output(g1.plot_id, 'figure'),
    Output(g2.plot_id, 'figure'),
    Output(g3.plot_id, 'figure'),
    Output('selected_points', 'data'),
    Input('csv_name', 'data'),
)
def select_csv(csv_name):

    if csv_name not in loaded_data:
        df = pd.read_csv('data/' + csv_name) if csv_name else default_df
        loaded_data[csv_name] = df
    else:
        df = loaded_data[csv_name]

    g1_figure = g1.parse_figure(df=df)

    g2_figure = g2.parse_figure(df=df)

    g3_figure = g3.parse_figure(df=df)

    return g1_figure, g2_figure, g3_figure, [None, None]
