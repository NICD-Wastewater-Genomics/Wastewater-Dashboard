import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly_express as px
import pandas as pd

dash.register_page(__name__)

df = pd.read_csv("provincial_cases_vs_levels.csv")


dropdown = dcc.Dropdown(
           id="my_dropdown",
           options=[
               {'label': "Buffalo City - Eastern Cape", "value": "Buffalo City MM"},
               {'label': "Nelson Mandela Bay - Eastern Cape", "value": "Nelson Mandela Bay MM"},
               {'label': "Mangaung - Free State", "value": "Mangaung MM"},
               {'label': "Ekurhuleni - Gauteng", "value": "Ekurhuleni MM"},
               {'label': "Johannesburg - Gauteng", "value": "Johannesburg MM"},
               {'label': "Tshwane - Gauteng", "value": "Tshwane MM"},
               {'label': "Ethekwini MM - KwaZulu Natal", "value": "Ethekwini MM"},
               {'label': "Cape Town - Western Cape", "value": "Cape Town MM"}
                    ],
           value= "Gauteng",
           placeholder="Please select a province",
           multi=False,
           style={"width": "50%"}
         )

layout = html.Div([
    html.Div([
        html.Label(["SARS-CoV-2 Wastewater Levels"]),
        dropdown
    ]),

    html.Div([
        dcc.Graph(id="the_graph")
    ]),

])

@callback(
    Output("the_graph", "figure"),
    [Input("my_dropdown", "value")]
)

def line_chart(my_dropdown):

    dff = df[(df["District_Name"] == my_dropdown)]

    fig = px.line(dff, x="Date", y="loglevels", color="Site_Name")

    fig.update_layout(
        title=' South African SARS-CoV-2 Wastewater Levels',
        barmode='group',
        xaxis=dict(dtick="M1",tickformat="%b\n%Y")
    )

    fig.update_xaxes(title_text="Epidemiological week")
    fig.update_yaxes(title_text="Log Genome Copies/ml (N Gene)", secondary_y=False)


    return fig
