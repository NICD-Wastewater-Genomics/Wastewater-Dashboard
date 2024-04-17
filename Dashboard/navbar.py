from dash import html
import dash_bootstrap_components as dbc


def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                align_end=True,
                children=[  # Add as many menu items as you need
                    dbc.DropdownMenuItem("SARS-CoV-2- National", href='/'),
                    dbc.DropdownMenuItem(divider=True),
                    # dbc.DropdownMenuItem("Mutations", href='/muts'),
                    # dbc.DropdownMenuItem("Lineages", href='/lins'),
                    # dbc.DropdownMenuItem("Samples", href='/samples'),
                    dbc.DropdownMenuItem("SARS-CoV-2- Districts", href='/sites'),
                ],
            ),
        ],
        brand="NICD Wastewater Genomics",
        brand_href="/",
        sticky="top",  # Uncomment if you want the navbar to always appear at the top on scroll.
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
             html.Img(src='assets/nicd_logo.png',height="100rem"),
             html.Img(src='assets/gcro_logo.png',height="100rem"),
             html.Img(src='assets/scripps_logo.png',height="100rem")
             ]
    footer = html.Div(fdivs, style=FOOTER_STYLE)
    return footer