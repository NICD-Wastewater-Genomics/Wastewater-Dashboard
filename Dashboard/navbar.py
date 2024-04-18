from dash import html
import dash_bootstrap_components as dbc


def create_navbar():

    navbar = dbc.Navbar(
        id="navbar",
        children=[
            dbc.Row(
                [
                    dbc.Col(html.Img(src='assets/nicd_ww_logo.png', height="150rem")),
                    dbc.Col(
                        dbc.DropdownMenu(
                            nav=True,
                            in_navbar=True,
                            label="Menu",
                            align_end=True,
                            children=[  # Add as many menu items as you need
                                dbc.DropdownMenuItem("SARS-CoV-2- National", href='/'),
                                dbc.DropdownMenuItem(divider=True),
                                dbc.DropdownMenuItem("SARS-CoV-2- Districts", href='/sites'),
                            ],
                        ),
                    ),
                ],
                align="center",
            ),
        ],
        #sticky="top",  # Uncomment if you want the navbar to always appear at the top on scroll.
        color="#CFE18A",
        dark=False,  # Change this to change color of text within the navbar (False for dark text)
    )

    return navbar


def create_footer():
    FOOTER_STYLE = {
        "bottom": 0,
        "left": 0,
        "right": 0,
        "text-align": "center",
        "height": "10rem",
        "padding": "1rem 1rem",
        "background-color": "white",
    }
    fdivs = [html.Hr(),
             html.P(children='Participating Institutions',
             style={"font-weight": "bold",'color':'black'}),
             html.Img(src='assets/nicd_logo.png',height="100rem", style={"margin-right": "20px"}),
             html.Img(src='assets/gcro_logo.png',height="100rem", style={"margin-right": "20px"}),
             html.Img(src='assets/scripps_logo.png',height="100rem", style={"margin-right": "20px"})
             ]
    footer = html.Div(fdivs, style=FOOTER_STYLE)
    return footer