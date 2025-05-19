import dash
from dash import html

dash.register_page(__name__, path="/", title="Graphs description")

layout = [
    html.Div([
        html.P([
            'The interactive graphs show the result of the three principal components (Principal component 1 to 3)'
            ' analysis on the galena shape descriptors.'
            " Shape descriptors are categorized into form, roundness, and roughness according to the Barrett's (1980) definition."
            ' The classification of a descriptor is determined by the original intent of its author or its prevalent usage.'
            ' These results come from a series of two articles, the ',
            html.A('first published', href="https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2025.1508690/full"),
            ' and the second under review.'
        ]),
        html.P([
            'The shape descriptors are extracted from the galena binary images using Python.'
            'The library is available on GitHub using the following ',
            html.A("link", href="https://github.com/Cyrilkt/Image-Processing-Descriptors"),
            '. When you click on a data point, the corresponding image will be displayed below the graph,'
            ' and the data point will turn red across all related graphs.'
        ]),

        html.Div([
            html.H2('Form descriptors PCA:'),
            html.P(['PC1: sorts the grains by size,', 
                    html.Br(), 'PC2: sorts the grains by roundness,', 
                    html.Br(), 'PC3: sorts the grains by roughness.']),
            html.P(['Data: PCA2_form_galena_grains.csv']),
        ]),

        html.Div([
            html.H2('Roundness descriptors PCA:'),
            html.P(['PC1: sorts the grains from stubby very angular rectangular grains to smooth rounded grains,', 
                    html.Br(), 'PC2: sorts the grains from elongated angular rectangular grains to smooth rounded grains,', 
                    html.Br(), 'PC3: sorts the grains by roughness.']),
            html.P(['Data: PCA1_roundness_galena_grains.csv']),
        ]),

        html.Div([
            html.H2('Roughness descriptors PCA:'),
            html.P(['PC1: sorts the grains by roughness,', 
                    html.Br(), 'PC2: sorts the grain by area,', 
                    html.Br(), 'PC3: sorts the grains by form and roundness.']),
            html.P(['Data: PCA1_roughness_galena_grains.csv']),
        ]),

    ]),

]