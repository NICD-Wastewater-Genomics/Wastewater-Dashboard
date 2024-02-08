import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly_express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
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
               {'label': "Ethekwini - KwaZulu Natal", "value": "Ethekwini MM"},
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

    sites_selected = sites[sites['Metro']==my_dropdown]
    sites_other = sites[sites['Metro']!=my_dropdown]
    dfg0 = dfg.copy()
    dfg0.loc[dfg0['province'].isin(sites_selected['Province']),'val0'] = 14
    fig_map = px.choropleth(dfg0,
                        geojson=gjson,   
                        featureidkey="properties.PROVINCE", 
                        locations = "province",
                        color="val0",color_continuous_scale='YlGn',
                        color_continuous_midpoint=0,
                        range_color=(-2, 20),
                        hover_name="province",
                        hover_data={"province":False,'val0':False}
                        )
    fig_map.update_traces(showlegend=False)

    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0},xaxis={'fixedrange':True},yaxis={'fixedrange':True},dragmode=False)

    fig_selected = px.scatter_geo(sites_selected,
                lat=sites_selected['Latitude'],
                lon=sites_selected['Longitude'],
                hover_name="Site",
                hover_data={'Site':False,'Latitude':False,"Longitude":False},
                )
    fig_selected.update_traces(marker=dict(size=6,line=dict(width=2,
                      color='red')),
                     selector=dict(mode='markers'))
    fig_other = px.scatter_geo(sites_other,
            lat=sites_other['Latitude'],
            lon=sites_other['Longitude'],
            hover_name="Site",
            hover_data={'Site':False,'Latitude':False,"Longitude":False},
            )
    fig_other.update_traces(marker=dict(size=6,line=dict(width=2,
                      color='black')),
                     selector=dict(mode='markers'))
    fig_map.add_trace(
    fig_selected.data[0]
    )
    fig_map.add_trace(
    fig_other.data[0]
    )
    fig_map.update(layout_coloraxis_showscale=False)
    return fig_map


@callback(
    Output("the_graph", "figure"),
    [Input("my_dropdown", "value")]
)
def line_chart(my_dropdown):
    dff = df[(df["District"] == my_dropdown)]
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])

    fig3.add_trace(
        go.Bar(
            x=dff['Date'], y=dff['n'],
            marker_color='gray',
            name="Clinical Cases"),
        secondary_y=False)  # specify for colour for df
    # color mapping
    color_mapping = {'Zandvleit Wastewater Treatment Works': 'blue',
                     'Borcheds Quarry Wastewater Treatment Works': 'red',
                     'East Bank Wastewater Treatment Works': 'blue',
                     'Mdantsane Wastewater Treatment Works': 'red',
                     'ERWAT Vlakplaat Wastewater Treatment Work': 'blue',
                     'Hartebeesfontein Waterworks': 'red',
                     'Northern Wastewater Treatment Works (KZN)': 'blue',
                     'Central Wastewater Treatment Works (KZN)': 'red',
                     'Northern Wastewater Treatment Works (GP)': 'blue',
                     'Goudkoppies Wastewater Treatment Works': 'red',
                     'Sterkwater Wastewater Treatment Works': 'blue',
                     'Bloemspruit Wastewater Treatment Works': 'red',
                     'Brickfield Pre-treatment Works': 'blue',
                     'Kwanobuhle Wastewater Treatment Works': 'red',
                     'Rooiwal Wastewater Treatment Works': 'blue',
                     'Daspoort Wastewater Treatment Works': 'red'}

    # Map 'Site' values to colors using the color_mapping dictionary
    dff['color'] = dff['Site'].map(color_mapping)

    fig3.add_trace(
        go.Scatter(
            x=dff['Date'], y=dff['levels'],
            marker=dict(color=dff['color'], size=8),
            line=dict(width=4),
            text=dff['levels'],
            name="Wastewater levels"), secondary_y=True)


    fig3.update_layout(
        title=' South African SARS-CoV-2 Wastewater Levels',
        barmode='group')

    fig3.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(l=20, r=20, t=20, b=20))
    fig3.update_xaxes(title_text="Epidemiological week")
    fig3.update_yaxes(title_text="Laboratory confirmed cases", secondary_y=False)
    fig3.update_yaxes(title_text="Genome Copies/ml (N Gene)", secondary_y=True)
    fig3.update_layout(width=800)

    return fig3

# print(dff)
# fig = px.line(dff, x="epiweek2", y="levels", color="Site")
# fig.add_bar(dff, x="Date", y="n")
# #fig.update_layout(
#     title=' South African SARS-CoV-2 Wastewater Levels',
#     barmode='group',
#     xaxis=dict(dtick="M1",tickformat="%b\n%Y")
# )
#fig.add_bar(dff, x="Date", y="n")
# fig.update_xaxes(title_text="Epidemiological week")
# fig.update_yaxes(title_text="Log Genome Copies/ml (N Gene)", secondary_y=False)
#
#
# return fig