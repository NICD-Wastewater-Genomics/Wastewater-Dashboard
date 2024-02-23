import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from charts import df, bar_chart
from cards import card_content1, card_content2, card_content3
from navbar import create_navbar


NAVBAR = create_navbar()

# app = dash.Dash() if using html layout use this one
app = dash.Dash(external_stylesheets=[dbc.themes.MINTY],
                use_pages=True)

# coordinate page ord
app.layout = dcc.Loading(  # <- Wrap App with Loading Component
    id='loading_page_content',
    children = [
        html.Div([
        NAVBAR,
        dash.page_container
        ])
        ],
    color='primary',
    fullscreen=True
    )


if __name__ == "__main__":
    app.run_server(debug=True)
