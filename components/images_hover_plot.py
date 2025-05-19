from dash import html, dcc, callback, Input, Output, no_update, State
import plotly.graph_objects as go

title_color = '#5e9dd7'
axis_color = '#93bde3'
point_color = '#5eaeeb'
clicked_pt_color = '#ffbe0a'
tick_color = '#c8c8c8'

class ImageHoverPlot(html.Div):

    registered = []

    def __init__(self, loaded_data, figure: go.Figure, id: str, margin=dict(b=120, l=20, r=20, t=20, pad=20), width: int=450):
        
        self.registered.append(id)

        self.id = "graph-" + id
        self.plot_id = "scatter-plot-" + id
        tooltip_id = "graph-tooltip-" + id 

        self.selected_indexes = (None, None)
        self.figure = figure
        self.margin = margin

        @callback(
            Output(tooltip_id, "show"),
            Output(tooltip_id, "bbox"),
            Output(tooltip_id, "children"),
            Input(self.plot_id, "hoverData"),
            State('csv_name', 'data'),
        )
        def display_hover(hoverData, csv_name):
            if hoverData is None:
                return False, no_update, no_update

            pt = hoverData["points"][0]
            bbox = pt["bbox"]
            num = pt["pointNumber"]

            current_df = loaded_data[csv_name]
            df_row = current_df.iloc[num]
            img_src = "Galena_binary_images/" + df_row['Target']

            children = [
                html.Div([
                    html.Img(src=img_src, style={"width": "100%"}, className="tooltip-image"),
                ], className="image-tooltip")
            ]

            return True, bbox, children
        
        figure.update_traces(hoverinfo="none", hovertemplate=None)
        
        figure.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)', 
            paper_bgcolor='rgba(0, 0, 0, 0)', 
            showlegend=False,
            autosize=True,
            margin=margin
        )

        trace = next(figure.select_traces())

        n = len(trace.a if isinstance(trace, go.Scatterternary) else trace.x)
        self.default_color = trace.marker.color
        self.default_size = trace.marker.size or 8

        color = [self.default_color] * n
        size = [self.default_size] * n

        # Update trace.
        trace.marker.color = color
        trace.marker.size = size

        super().__init__([
            dcc.Graph(id=self.plot_id, figure=figure, clear_on_unhover=True, responsive=True, style=dict(width=width)),
            dcc.Tooltip(id=tooltip_id),
        ], className="graph", id=self.id)

    def select_point(self, index: int, selection_id: int | None = None):

        if self.selected_indexes[selection_id] is not None:
            self.unselect_point(self.selected_indexes[selection_id])

        trace = next(self.figure.select_traces())

        trace.marker.color[index] = self.selection_color
        trace.marker.size[index] = self.default_size + 5

        selection_id = selection_id or 0 if self.selected_indexes[0] is None else 1

        self.selected_indexes[selection_id] = index

    def unselect_point(self, index: int):

        if index in self.selected_indexes:
            trace = next(self.figure.select_traces())
            trace.marker.color[index] = self.default_color
            trace.marker.size[index] = self.default_size

        self.selected_indexes[self.selected_indexes.index(index)] = None
