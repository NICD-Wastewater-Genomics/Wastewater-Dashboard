import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from charts import df, bar_chart
from cards import card_content1, card_content2, card_content3
from navbar import navbar

# app = dash.Dash() if using html layout use this one
app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])

app.layout = dbc.Container([
    html.Div(id="parent", children=[navbar]),
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
        dbc.Col([dcc.Graph(id="bar_plot", figure=bar_chart(df))])
        ]),
    ], fluid=True)  # fills up empty space with the graphs

if __name__ == "__main__":
    app.run_server()
