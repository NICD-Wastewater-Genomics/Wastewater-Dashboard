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
        # sticky="top",  # Uncomment if you want the navbar to always appear at the top on scroll.
        color="dark",  # Change this to change color of the navbar e.g. "primary", "secondary" etc.
        dark=True,  # Change this to change color of text within the navbar (False for dark text)
    )

    return navbar

# navbar = dbc.Navbar(
#     dbc.Container(
#         [
#             html.A(
#                 dbc.Row(
#                     [
#                         dbc.Col(dbc.NavbarBrand("NICD Wastewater Genomics", className="ms-2")),
#                     ],
#                     align="center",
#                     className="g-0",
#                 ),
#                 href="/",
#                 style={"textDecoration": "none"},
#             ),
#             dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
#             dbc.Collapse(
#                 search_bar,
#                 id="navbar-collapse",
#                 is_open=False,
#                 navbar=True,
#             ),
#         ]
#     ),
#     color="dark",
#     dark=True,
# )
