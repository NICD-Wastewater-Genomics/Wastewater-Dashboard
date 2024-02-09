import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from cards import card_content1, card_content2, card_content3
from charts import df, bar_chart, seq_df, seq_plot, colorDict

dash.register_page(__name__, path='/')

 
layout = dbc.Container([
    dbc.Row(
        [dbc.Col(
            [html.H1(id="H1", children="SARS-CoV-2 Wastewater Dashboard")],
            xl=12, lg=12, md=12, sm=12, xs=12)], style={"textAlign": "center", "marginTop": 30, "marginBottom": 30}),
    dbc.Row([
        dbc.Col(dbc.Card(card_content1, color="primary", inverse=True)),  # inverse ensures text & card colour inverted
        dbc.Col(dbc.Card(card_content2, color="primary", inverse=True)),
        dbc.Col(dbc.Card(card_content3, color="primary", inverse=True))
        ]),
    dbc.Row([
        dcc.Graph(id="bar_plot", figure=bar_chart(df), config={'displayModeBar': False})
        ]),
    dbc.Row([
    dcc.Graph(id="seq_plot", figure=seq_plot(seq_df, colorDict), config={'displayModeBar': False})
     ]),
    ])#, fluid=True)  # fills up empty space with the graphs
