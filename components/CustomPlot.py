import plotly.graph_objects as go

from components.images_hover_plot import ImageHoverPlot

color_axis = "#81a71b"
color_tick = "#BBB"

class CustomPlot(ImageHoverPlot):
    def __init__(
        self, 
        x: str, y: str, x_title: str, y_title: str,
        df, id: str,
        loaded_data
    ):
        self.x = x
        self.y = y
        self.x_title = x_title
        self.y_title = y_title

        figure = go.Figure(
            data=[
                go.Scatter(
                    x=df[x], 
                    y=df[y],
                    mode="markers",
                    marker=dict(
                        color='#5eaeeb'
                    )
                )
            ],
        )

        figure.update_xaxes(title_text=x_title, titlefont=dict(color=color_axis), tickfont=dict(color=color_tick))
        figure.update_yaxes(title_text=y_title, titlefont=dict(color=color_axis), tickfont=dict(color=color_tick))

        super().__init__(loaded_data, figure, id=id)

    def parse_figure(self, df):
        
        n = df.shape[0]

        figure = go.Figure(
            data=[
                go.Scatter(
                    x=df[self.x], 
                    y=df[self.y],
                    mode="markers",
                    marker=dict(
                        color = [self.default_color] * n,
                        size = [self.default_size] * n
                    )
                )
            ],
        )

        figure.update_xaxes(title_text=self.x_title, titlefont=dict(color=color_axis), tickfont=dict(color=color_tick))
        figure.update_yaxes(title_text=self.y_title, titlefont=dict(color=color_axis), tickfont=dict(color=color_tick))
        figure.update_layout(paper_bgcolor='rgba(0,0,0,0)')

        figure.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)', 
            paper_bgcolor='rgba(0, 0, 0, 0)', 
            showlegend=False,
            autosize=True,
            margin=self.margin
        )

        return figure