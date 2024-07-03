import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from navbar import create_navbar, create_footer


NAVBAR = create_navbar()
footer = create_footer()

external_stylesheets = [dbc.themes.MINTY, "/assets/style.css"]

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                use_pages=True)

server = app.server

# coordinate page order
def serve_layout():
    return dcc.Loading(  
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

app.layout = serve_layout


if __name__ == "__main__":
    app.run_server()

