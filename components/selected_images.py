from dash import html

encoded_image = None

selected_image_1 = html.Div([
    html.Img(src=f'data:image/png;base64,{encoded_image}'),
], className="images-wrapper left", id="image-left")

selected_image_2 = html.Div([
    html.Img(src=f'data:image/png;base64,{encoded_image}'),
], className="images-wrapper right", id="image-right")
