import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly_express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import json, urllib
from savgol import non_uniform_savgol
from load_data import load_provincial_cases_levels, load_provincial_merged

dash.register_page(__name__)

# static component loading 
#read in location of each wwtp
sites = pd.read_csv('data/SA_sites_coords.tsv',sep='\t')

# Remove trailing whitespace from column names
sites.columns = sites.columns.str.strip()

sites['Latitude'] = sites['Coords'].apply(lambda x:x.split(',')[0]).astype(float)
sites['Longitude'] = sites['Coords'].apply(lambda x:x.split(',')[1]).astype(float)
sites = sites.dropna(subset=['Metro'])

with open("data/layer1.json") as geofile:
    gjson = json.load(geofile)

dfg = pd.DataFrame()
dfg['province'] = [gj['properties']['PROVINCE'] for gj in gjson['features']]
dfg['val0'] = 0


def sites_container():
    return dbc.Container([
        dbc.Row(
            dbc.Col(
                html.H1(id="H1", children="SARS-CoV-2 Wastewater Surveillance (District Level)",
                        style={'color': 'white', 'textAlign': 'center'}),
                width=12,
                className="mb-4",
            ),
            style={"backgroundColor": "#CFE18A", "paddingTop": 30, "paddingBottom": 30}
        ),
        html.P(children='To provide regional information on SARS-CoV-2 evolution and spread, '
                        'wastewater virus concentration and lineage prevalence trends can be resolved to the level of '
                        'individual wastewater sampling sites. Trends observed at local community collections can help '
                        'identify possible outbreaks prior to broader regional and national spread.',
               style={"fontSize": 20}),
        html.Div(style={"backgroundColor": "#F0FFF0", "padding": "1em", 'borderRadius': '25px'}, children=[
            html.P(id="dropdown_menu", children='Explore a district of interest',
                   style={"fontSize": 25, "textAlign": "center", "fontWeight": "bold", "color": "black"}),
            dbc.Row(
                dbc.Col(dcc.Dropdown(
                    id="my_dropdown",
                    options=[
                        {'label': "Bojanala Platinum - North West", "value": "Bojanala Platinum DM"},
                        {'label': "Buffalo City - Eastern Cape", "value": "Buffalo City MM"},
                        {'label': "Cape Town - Western Cape", "value": "Cape Town MM"},
                        {'label': "Ehlanzeni - Mpumalanga", "value": "Ehlanzeni DM"},
                        {'label': "Ekurhuleni - Gauteng", "value": "Ekurhuleni MM"},
                        {'label': "Ethekwini - KwaZulu Natal", "value": "Ethekwini MM"},
                        {'label': "Frances Baard - Northern Cape", "value": "Frances Baard DM"},
                        {'label': "Johannesburg - Gauteng", "value": "Johannesburg MM"},
                        {'label': "Mangaung - Free State", "value": "Mangaung MM"},
                        {'label': "Nelson Mandela Bay - Eastern Cape", "value": "Nelson Mandela Bay MM"},
                        {'label': "Ngaka Modiri Molema - North West", "value": "Ngaka Modiri Molema DM"},
                        {'label': "Tshwane - Gauteng", "value": "Tshwane MM"},
                        {'label': "Umkhanyakude DM - KwaZulu Natal", "value": "Umkhanyakude DM"},
                        {'label': "Vhembe - Limpopo", "value": "Vhembe DM"}
                    ],
                    value="Johannesburg MM",
                    placeholder="Select a district of interest",
                    multi=False,
                    style={'margin': 'auto', 'width': '100%'}
                ), width=10, className='justify-content-center'),
                style={"alignItems": "center", 'justifyContent': 'center'}
            ),
            html.Div(style={'height': '20px'}),  # Inserting an empty row with 50px height
            dbc.Row([
                dbc.Col(dbc.Card(
                    [
                        dbc.CardHeader(html.H3("Wastewater Sampling Locations",
                                               style={"textAlign": "center", "marginTop": 10, "marginBottom": 0})),
                        dbc.CardBody(dcc.Graph(id='map_plot', config={'displayModeBar': False}, className='responsive-graph'))
                    ],
                    body=True, outline=True, color='primary',
                ), width=12, lg=6),
                dbc.Col(dbc.Card(
                    [
                        dbc.CardHeader(html.H3("SARS-CoV-2 Wastewater Levels",
                                               style={"textAlign": "center", "marginTop": 10, "marginBottom": 0})),
                        dbc.CardBody(dcc.Graph(id="the_graph", config={'displayModeBar': False}, className='responsive-graph'))
                    ],
                    body=True, outline=True, color='primary',
                ), width=12, lg=6),
            ]),
            html.Div(style={'height': '40px'}),
            dbc.Row(
                dbc.Col(dbc.Card(
                    [
                        dbc.CardHeader(html.H3("Lineage Prevalence Observed via Wastewater",
                                               style={"textAlign": "center", "marginTop": 5, "marginBottom": 5})),
                        dbc.CardBody(dcc.Graph(id="seq_graph", config={'displayModeBar': False}, className='graph-item'
                                               ))
                    ],
                    body=True, outline=True, color='primary',
                ), width=12),
            ),
        ]),
    ], fluid=True, style={"padding": "2em 2em 2em 0.5em"})

layout = sites_container


@callback(
    Output("map_plot", "figure"),
    Input("my_dropdown", "value"))
def make_map(my_dropdown):

    sites_selected = sites[sites['Metro']==my_dropdown].copy()
    sites_other = sites[sites['Metro']!=my_dropdown].copy()
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

    df = load_provincial_cases_levels()
    dff = df[(df["District"] == my_dropdown)]
    unique_sites = dff['Site'].unique() #identifying all the unique site names so we can use it in for loop and create a graph for each
    max_case = dff['n'].max()
    max_level = dff['levels'].max()
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    dff0 = dff[['Date','n']].drop_duplicates(keep='first')
    fig3.add_trace(
    go.Bar(
        x=dff0['Date'], y=dff0['n'],
        marker_color='blue',
        name="Clinical Cases"),
    secondary_y=False)

    for j0, site in enumerate(unique_sites):

        color0 = px.colors.qualitative.Set2[j0]
        site_df = dff[dff['Site'] == site]

        df_s1 = site_df[['Date','levels']]
        df_s1['Date'] = pd.to_datetime(df_s1['Date'])
        df_s1 = df_s1[~df_s1['levels'].isna()]

        #the newer sites only have a few data points - not enough to normalise using savgol- so for now I'm adding a condition that if
        #the length of the data is not equal to the window size in the savgol filter, then ignore

        if len(df_s1) >= 7:  # make sure this is the same as window size stated in non_uniform_savgol function
            numberDates = [dvi.value/10**11 for dvi in df_s1['Date']]
            df_s1['ww_smoothed'] = non_uniform_savgol(numberDates,df_s1['levels'].to_numpy(),7,1)
        else:
            df_s1['ww_smoothed'] = df_s1['levels'] #use original data without smoothing

        fig3.add_trace(
            go.Scatter(
                x=site_df['Date'], y=site_df['levels'],
                mode='markers',
                marker=dict(size=8,color=color0),
                # line=dict(width=2,color=color0),
                text=site_df['Site'],
                showlegend=True,
                name=f"Site {site}"),
            secondary_y=True
        )
        fig3.add_trace(
            go.Scatter(
                x=df_s1['Date'], y=df_s1['ww_smoothed'],
                mode='lines',
                # marker=dict(size=8),
                line=dict(width=2,color=color0),
                text=site_df['Site'],
                showlegend=False,
                name=f"Site {site}"),
            secondary_y=True
        )

    fig3.update_layout(
        title=' SARS-CoV-2 Wastewater Levels',
        barmode='group',
        margin=dict(l=20, r=20, t=40, b=80),  # Increase bottom margin
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,  # Move legend below the plot
            xanchor="center",
            x=0.5
        )
    )
    fig3.update_xaxes(title_text="Epidemiological week")
    fig3.update_yaxes(title_text="Laboratory confirmed cases", secondary_y=False, range=[0, max_case * 1.02])
    fig3.update_yaxes(title_text="Genome Copies/ml (N Gene)", secondary_y=True, range=[0, max_level * 1.02])

    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig3

@callback(
    Output("seq_graph", "figure"),
    [Input("my_dropdown", "value")]
)

def lineage_summary(my_dropdown):

    from datetime import date, timedelta
    start0 = date.today()-timedelta(days=365)
    df2_exploded = load_provincial_merged()

    df2_exploded_filtered = df2_exploded[df2_exploded["District"] == my_dropdown]
    # for now, just do the dumb thing. Take the most abundant lineages.
    recent = df2_exploded_filtered[df2_exploded_filtered['Date']>=start0.strftime("%Y-%m-%d")]
    top = list(recent.groupby('Lineages')['Abundances'].sum().sort_values(ascending=False).index[0:11])
    top.append('Other')
    df2_exploded_filtered['Lineages']  = df2_exploded_filtered['Lineages'].apply(lambda x: x if x in top else "Other")
    df2_exploded_filtered = df2_exploded_filtered.groupby(['Site','Sample','Lineages','Date','District'])['Abundances'].sum().reset_index()

    # Define a color sequence for lineages
    with urllib.request.urlopen("https://raw.githubusercontent.com/NICD-Wastewater-Genomics/NICD-Dash-Data/main/color_map.json") as cdat:
        lineage_color_map = json.load(cdat)
    # lineage_colors = px.colors.qualitative.Set3[0:len(top)]
    # lineage_color_map = dict(zip(top, lineage_colors))
    # Create a subplot for each site within the selected district
    unique_sites = df2_exploded_filtered['Site'].unique()

    # Determine the number of rows needed based on the number of unique sites
    num_rows = (len(unique_sites) + 1) // 2

    #eventually we should probably use shared x axes, with
    fig = make_subplots(rows=num_rows, cols=2, shared_xaxes=False, shared_yaxes=False,
                        subplot_titles=unique_sites)
    cSet = []
    for i, site in enumerate(unique_sites, start=1):
        site_df = df2_exploded_filtered[df2_exploded_filtered['Site'] == site].copy()
        # print(df2_exploded_filtered)

        site_df["Abundances"] = site_df['Abundances']*100.
        # print(site_df.groupby("Date")["Abundances"].sum())
        # Calculate the row and column indices for the subplot
        row_index = (i - 1) // 2 + 1
        col_index = (i - 1) % 2 + 1
        if 'Hartebees' in site:
            print(lineage_color_map)
            print(site_df[site_df['Lineages']=='NB.1.8.1.X'])
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
                        # stackgroup='one',
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
                    # stackgroup='one',
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

    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5,
            font={'size': 20}
        ),
        height=500 * num_rows,
        barmode="stack",
        xaxis=dict(tickformat='%b %Y'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=80)
    )
    return fig
