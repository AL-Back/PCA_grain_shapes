import dash, os
from dash import html, dcc, callback, Input, Output

data_files = [file_name for file_name in os.listdir('data') if file_name.endswith(".csv")]
default_df_name = data_files[0] if data_files else None

menu_layout = html.Header([

    html.Div([

        html.Div("Galena grain shape analysis", className="title"),

        html.Div([

            html.Div(
                dcc.Link(page["title"], href=page["relative_path"]), 
                className="button"
            ) for page in dash.page_registry.values()

        ], className="nav"),

        dcc.Dropdown(
            id="csv_selector",
            options=data_files,
            className="csv-selector",
            value=data_files[0]
            
        )

    ], className="menu-container")

], className="menu")


@callback(
    Output('csv_name', 'data'),
    Input("csv_selector", 'value'),
)
def csv_source_updated(csv_selector_data):
    return csv_selector_data

