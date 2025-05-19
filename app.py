import dash
from dash import html, dcc

# Initiate the app
app = dash.Dash(__name__, use_pages=True, prevent_initial_callbacks=True)
server = app.server

from components.menu import menu_layout

app.layout = html.Div([
    menu_layout,
    html.Div([
        dash.page_container
    ], className="main-container"),
    dcc.Store(id="csv_name", data="")
])

if __name__ == '__main__':
    app.run_server(debug=True)
