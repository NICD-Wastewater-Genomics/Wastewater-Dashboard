from dash import html
import dash_bootstrap_components as dbc
from charts import epiweek, no_cases, end_week, no_ww

# data cards: epidemiological week, Week ending, Confirmed covid cases this week,
# layout

# card contents

card_content1 = [
    dbc.CardHeader("Epidemiological Week"),
    dbc.CardBody(
        [
            html.H5(epiweek, className="card-title")
        ]
    )
]

card_content2 = [
    dbc.CardHeader("Week Ending"),
    dbc.CardBody(
        [
            html.H5(end_week, className="card-title"),
        ]
    )
]

card_content3 = [
    dbc.CardHeader("Laboratory-confirmed Cases"),
    dbc.CardBody(
        [
            html.H5(no_cases, className="card-title"),
        ]
    )
]

card_content4 = [
    dbc.CardHeader("Wastewater samples collected"),
    dbc.CardBody(
        [
            html.H5(no_ww, className="card-title"),
        ]
    )
]
