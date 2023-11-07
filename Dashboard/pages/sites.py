import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly_express as px
import pandas as pd
import json
dash.register_page(__name__)

df = pd.read_csv("data/provincial_cases_vs_levels.csv")


#read in location of each wwtp
sites = pd.read_csv('data/SA_sites_coords.tsv',sep='\t')
sites['Latitude'] = sites['Coords'].apply(lambda x:x.split(',')[0]).astype(float)
sites['Longitude'] = sites['Coords'].apply(lambda x:x.split(',')[1]).astype(float)

sites = sites.dropna(subset=['Metro'])
# sites['color'] = 'black'
with open("data/layer1.json") as geofile:
    gjson = json.load(geofile)

dfg = pd.DataFrame()
dfg['province'] = [gj['properties']['PROVINCE'] for gj in gjson['features']]
dfg['val0'] = 0
# dfg = pd.DataFrame([{'province':'NC','val0':2.4},
#                    {'province':'WC','val0':5.4},
#                    {'province':'EC','val0':5.4},
#                    {'province':'LIM','val0':5.4}])

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
           value= "Johannesburg MM",
           placeholder="Please select a province",
           multi=False,
           style={"width": "50%"}
         )

layout = html.Div([
    html.Div([
        html.Label(["SARS-CoV-2 Wastewater Levels"]),
        dropdown,
        dcc.Graph(id='map_plot')
    ]),
    

    html.Div([
        dcc.Graph(id="the_graph")
    ]),

])

@callback(
    Output("map_plot", "figure"),
    Input("my_dropdown", "value"))
def make_map(my_dropdown):
    fig20 = px.choropleth(dfg,
                        geojson=gjson,   
                        featureidkey="properties.PROVINCE", 
                        locations = "province",
                        color="val0",color_continuous_scale='YlOrBr',
                        color_continuous_midpoint=0,
                        range_color=(-5, 20),
                        hover_name="province",
                        hover_data={"province":False,'val0':False}
                        )
    fig20.update_traces(showlegend=False)

    fig20.update_geos(fitbounds="locations", visible=False)
    fig20.update_layout(margin={"r":0,"t":0,"l":0,"b":0},xaxis={'fixedrange':True},yaxis={'fixedrange':True},dragmode=False)

    sites2 = sites[sites['Metro']==my_dropdown]
    sites0 = sites[sites['Metro']!=my_dropdown]

    fig2 = px.scatter_geo(sites2,
                lat=sites2['Latitude'],
                lon=sites2['Longitude'],
                hover_name="Site",
                hover_data={'Site':False,'Latitude':False,"Longitude":False},
                )
    fig2.update_traces(marker=dict(size=6,line=dict(width=2,
                      color='red')),
                     selector=dict(mode='markers'))
    fig0 = px.scatter_geo(sites0,
            lat=sites0['Latitude'],
            lon=sites0['Longitude'],
            hover_name="Site",
            hover_data={'Site':False,'Latitude':False,"Longitude":False},
            )
    fig0.update_traces(marker=dict(size=6,line=dict(width=2,
                      color='black')),
                     selector=dict(mode='markers'))
    fig20.add_trace(
    fig2.data[0]
    )
    fig20.add_trace(
    fig0.data[0]
    )
    fig20.update(layout_coloraxis_showscale=False)
    return fig20


@callback(
    Output("the_graph", "figure"),
    [Input("my_dropdown", "value")]
)
def line_chart(my_dropdown):
    dff = df[(df["District_Name"] == my_dropdown)]
    # print(dff)
    fig = px.line(dff, x="Date", y="loglevels", color="Site_Name")

    fig.update_layout(
        title=' South African SARS-CoV-2 Wastewater Levels',
        barmode='group',
        xaxis=dict(dtick="M1",tickformat="%b\n%Y")
    )

    fig.update_xaxes(title_text="Epidemiological week")
    fig.update_yaxes(title_text="Log Genome Copies/ml (N Gene)", secondary_y=False)


    return fig
