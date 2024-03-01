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

df2 = pd.read_csv("data/seq_data.csv")



### this shouldn't be there, dropping for now. 

# Convert the 'lineages' column to a list of lists
df2['Lineages'] = df2['Lineages'].apply(lambda x: x.split() if isinstance(x, str) else [])

# Convert the 'abundances' column to a list of lists
df2['Abundances'] = df2['Abundances'].apply(lambda x: [float(val) for val in x.split()] if isinstance(x, str) else [])

# Explode the 'lineages' and 'abundances' columns to separate rows
df2_exploded = df2.explode(['Lineages','Abundances'])


# Reset the index after exploding
df2_exploded = df2_exploded.reset_index(drop=True)


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

layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1("SARS-CoV-2 Wastewater- Provincial"), xl=12, lg=12, md=12, sm=12, xs=12),
        style={"textAlign": "center", "marginTop": 30, "marginBottom": 30}
    ),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
                id="my_dropdown",
                options=[
                    {'label': "Buffalo City - Eastern Cape", "value": "Buffalo City MM"},
                    {'label': "Nelson Mandela Bay - Eastern Cape", "value": "Nelson Mandela Bay MM"},
                    {'label': "Mangaung - Free State", "value": "Mangaung MM"},
                    {'label': "Ekurhuleni - Gauteng", "value": "Ekurhuleni MM"},
                    {'label': "Johannesburg - Gauteng", "value": "Johannesburg MM"},
                    {'label': "Tshwane - Gauteng", "value": "Tshwane MM"},
                    {'label': "Ethekwini - KwaZulu Natal", "value": "Ethekwini MM"},
                    {'label': "Cape Town - Western Cape", "value": "Cape Town MM"},
                    {'label': "Ehlanzeni - Mpumalanga", "value": "Ehlanzeni DM"},
                    {'label': "Rustenburg - North West", "value": "Rustenburg Local Municipality"},
                    {'label': "Cape Town - Limpopo", "value": "Vhembe DM"},
                ],
                value="Johannesburg MM",
                placeholder="Please select a province",
                multi=False,
                style={"width": "60%"}
            ), width=12),
    ]),
    html.Div(style={'height': '60px'}),  # Inserting an empty row with 50px height
    dbc.Row([
        dbc.Col(dcc.Graph(id='map_plot', config={'displayModeBar': False}), width=6),
        dbc.Col(dcc.Graph(id="the_graph", config={'displayModeBar': False}), width=6),
    ]),
    html.Div(style={'height': '85px'}),  # Inserting an empty row with 20px height
    dbc.Row([
        dbc.Col(dcc.Graph(id="seq_graph", config={'displayModeBar': False}), width=12),
    ]),
], fluid=True)


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
    unique_sites = dff['Site'].unique() #identifying all the unique site names so we can use it in for loop and create a graph for each

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])


    fig3.add_trace(
        go.Bar(
            x=dff['Date'], y=dff['n'],
            marker_color='blue',
            name="Clinical Cases"),
        secondary_y=False)  # specify for colour for df

    for site in unique_sites:
        site_df = dff[dff['Site'] == site]

        fig3.add_trace(
            go.Scatter(
                x=site_df['Date'], y=site_df['levels'],
                mode='lines+markers',
                marker=dict(size=8),
                line=dict(width=2),
                text=site_df['Site'],
                showlegend=True,
                name=f"Site {site}"),
            secondary_y=True
        )


    fig3.update_layout(
        title=' SARS-CoV-2 Wastewater Levels',
        barmode='group',
    )

    # Add black line along axes
    fig3.update_xaxes(showline=True, linewidth=1, linecolor='black')
    fig3.update_yaxes(showline=True, linewidth=1, linecolor='black')

    fig3.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.35,
        xanchor="center",
        x=0.4,
    ),
    margin=dict(l=20, r=20, t=40, b=20))
    fig3.update_xaxes(title_text="Epidemiological week")
    fig3.update_yaxes(title_text="Laboratory confirmed cases", secondary_y=False)
    fig3.update_yaxes(title_text="Genome Copies/ml (N Gene)", secondary_y=True)
    # fig3.update_layout(width=800),

    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

    return fig3

@callback(
    Output("seq_graph", "figure"),
    [Input("my_dropdown", "value")]
)

def lineage_summary(my_dropdown):
    # global df2_exploded  # Add this line to declare df2_exploded as a global variable
    df2_exploded_filtered = df2_exploded[df2_exploded["District"] == my_dropdown]

    # for now, just do the dumb thing. Take the most abundant lineages. 
    top = list(df2_exploded_filtered.groupby('Lineages')['Abundances'].sum().sort_values(ascending=False).index[0:11])
    top.append('Other')
    df2_exploded_filtered['Lineages']  = df2_exploded_filtered['Lineages'].apply(lambda x: x if x in top else "Other")
    df2_exploded_filtered = df2_exploded_filtered.groupby(['Site','Sample','Lineages','Date','District','Coverage'])['Abundances'].sum().reset_index()
    
    # Define a color sequence for lineages
    lineage_colors = px.colors.qualitative.Set3[0:len(top)]
    lineage_color_map = dict(zip(top, lineage_colors))
    # Create a subplot for each site within the selected district
    unique_sites = df2_exploded_filtered['Site'].unique()

    # Determine the number of rows needed based on the number of unique sites
    num_rows = (len(unique_sites) + 1) // 2

    #eventually we should probably use shared x axes, with 
    fig = make_subplots(rows=num_rows, cols=2, shared_xaxes=True, shared_yaxes=False,
                        subplot_titles=unique_sites)
    cSet = []
    for i, site in enumerate(unique_sites, start=1):
        site_df = df2_exploded_filtered[df2_exploded_filtered['Site'] == site].copy()

        site_df["Abundances"] = site_df['Abundances']*100.
        # print(site_df.groupby("Date")["Abundances"].sum())
        # Calculate the row and column indices for the subplot
        row_index = (i - 1) // 2 + 1
        col_index = (i - 1) % 2 + 1
        
        for lineage, color in lineage_color_map.items():
            lineage_df = site_df[site_df['Lineages'] == lineage]
            if lineage_df.shape[0]==0:
                continue
            if lineage in cSet:
                fig.add_trace(
                    go.Bar(
                        x=lineage_df['Date'],
                        y=lineage_df['Abundances'],
                        name=lineage,  # Use lineage name as legend entry
                        marker_color=lineage_color_map[lineage],
                        showlegend=False,
                        width = 300000000
                    ),
                    row=row_index, col=col_index
                )
            else:
                cSet.append(lineage)
                fig.add_trace(
                go.Bar(
                    x=lineage_df['Date'],
                    y=lineage_df['Abundances'],
                    name=lineage,  # Use lineage name as legend entry
                    marker_color=lineage_color_map[lineage],
                    showlegend=True,
                    width= 300000000
                ),
                row=row_index, col=col_index
            )
        #
        fig.update_xaxes(showticklabels=True, row=row_index, col=col_index)

        # Set y-axis range for each subplot
        fig.update_yaxes(showticklabels=True, title='Lineage Prevalence',range=[0, 100.], row=row_index, col=col_index)

        # Add black line along axes
        fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
        fig.update_yaxes(showline=True, showgrid=True,linewidth=1, linecolor='black')

    fig.update_layout(showlegend=True,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=0.93),
                      height=500 * num_rows,
                      barmode="stack",
                      xaxis=dict(tickformat='%b %Y'),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=20, r=20, t=40, b=20)
                      )
    return fig



