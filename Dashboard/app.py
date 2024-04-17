import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from charts import df, bar_chart
from cards import card_content1, card_content2, card_content3
from navbar import create_navbar, create_footer


NAVBAR = create_navbar()
footer = create_footer()

app = dash.Dash(external_stylesheets=[dbc.themes.MINTY],
                use_pages=True)


# coordinate page order
app.layout = dcc.Loading(  
    id='loading_page_content',
    children = [
        html.Div([
        NAVBAR,
        dash.page_container,
        footer])
        ],
    color='primary',
    fullscreen=True
    )


if __name__ == "__main__":
    app.run_server(debug=True)
