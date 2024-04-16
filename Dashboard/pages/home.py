import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from cards import card_content1, card_content2, card_content3, card_content4
from charts import df, bar_chart
import pandas as pd
from datetime import date, timedelta
import json
from dash import html, dcc, Input, Output, callback
import plotly.graph_objects as go
from datetime import timedelta

start = '2021-12-15'
end = date.today()


dash.register_page(__name__, path='/')

 
seq_df = pd.read_csv("data/NICD_monthly.csv",index_col=0)
seq_df = seq_df[seq_df.index >=start] # switch to last 12 or 24 months? 

seq_df_daily = pd.read_csv("data/NICD_daily_smoothed.csv",index_col=0)
seq_df_daily = seq_df_daily[seq_df_daily.index >=start] # switch to last 12 or 24 months? 

with open('data/color_map.json') as cdat:
    colorDict = json.load(cdat)

layout = dbc.Container([
    dbc.Row(
        [dbc.Col(
            [html.H1(id="H1", children="SARS-CoV-2 Wastewater Dashboard")],
            xl=12, lg=12, md=12, sm=12, xs=12)], style={"textAlign": "center", "marginTop": 30, "marginBottom": 10}),
    html.Div(style={'height': '30px'}),
    html.P(id="intro", children='To monitor the levels of SARS-CoV-2 infections across South Africa,\
        NICD measures virus concentrations in community wastewater (sewage). SARS-CoV-2 virus is\
        excreted in stool by persons with COVID-19 and can be detected at wastewater aggregation sites.\
        The levels of SARS-CoV-2 in wastewater reflect caseload and geographic distribution of cases,\
        and often provide an early warning of increases in infections in the community.',style={"font-size":20}),
html.Div(style={'height': '50px'}),
    dbc.Row([
        dbc.Col(dbc.Card(card_content1, color="primary", inverse=True)),  # inverse ensures text & card colour inverted
        dbc.Col(dbc.Card(card_content2, color="primary", inverse=True)),
        dbc.Col(dbc.Card(card_content3, color="primary", inverse=True)),
        dbc.Col(dbc.Card(card_content4, color="primary", inverse=True))
        ]),
    html.Div(style={'height': '50px'}),  # Inserting an empty row with 50px height
    html.H3(id="H3_",children=' National SARS-CoV-2 Wastewater Levels', style={"textAlign": "center",  "marginTop": 10,"marginBottom": 0}),
    dbc.Row([
        dcc.Graph(id="bar_plot", figure=bar_chart(df), config={'displayModeBar': False})
        ]),
    html.Div(style={'height': '25px'}),  # Inserting an empty row with 50px height
    html.P(id="seq_intro", children=['To monitor the evolution and spread SARS-CoV-2\
        lineages across South Africa, wastewater virus sequencing followed by bioinformatic analyses with the ',
        html.A("Freyja",href='https://github.com/andersen-lab/Freyja'),
        ' bioinformatic tool allows for the determination of variants in each wastewater sample.\
        Samples are aggregated across all sites, providing a national characterization of lineage prevalence.'],style={"font-size":20}),
html.Div(style={'height': '50px'}),
    html.H3(id="H3", children="Lineage Prevalence Observed via Wastewater",style={"textAlign": "center", "marginTop": 5,"marginBottom": 5}),
    html.Div(
                [dbc.RadioItems(
                    id="plottype",
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active",
                    options=[
                        { "label": "Monthly Trends", "value": "monthly" },
                        { "label": "Smoothed Daily Trends", "value": "daily" },
                    ],
                    value="monthly",
                    style={ "width": "100%", "justifyContent": "flex-end" }
                )],style={ "marginTop": 0,"marginBottom": 0}),
    dbc.Row([
        dcc.Graph(id="seq_graph0", config={'displayModeBar': False},style={ "width": "100%"})
     ]),
    # add logos here!! 
    ])

@callback(
    Output("seq_graph0", "figure"),
    Input("plottype", "value"),suppress_callback_exceptions=True)
def seq_plot(plottype):
    names = {'variable':'Lineage', 'index':'Month', 'value':'Prevalence'}

    month = seq_df.index
    if plottype=='monthly':
        fig2 = go.Figure(data=[go.Bar(name=sfc, x=seq_df.index, y=seq_df[sfc], marker_color=colorDict[sfc]) for sfc in seq_df.columns])
        # # Change the bar mode
        fig2.update_layout(barmode='stack',yaxis_tickformat = '.0%')
        fig2.update_layout(legend_title_text=names['variable'])
    else:
        fig2 = go.Figure([go.Scatter(name=sfc,x=seq_df_daily.index, y=seq_df_daily[sfc], marker_color=colorDict[sfc],
                                      mode='lines', stackgroup='one', fillcolor=colorDict[sfc],
                                      line=dict(width=0.0)) for sfc in seq_df_daily.columns])
        fig2.update_layout(legend_title_text=names['variable'],hovermode='x unified',hoverlabel=dict(font_size=12), yaxis_tickformat = '.0%')
    fig2.update_layout(
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-.35,
        xanchor="right",
        x=1,
        font={'size':15}
    ),margin=dict(l=40, r=75, t=15, b=0))

    fig2.update_layout(xaxis_range=[start, end], template='none')
    # fig2.update_traces(hovertemplate = 'Lineage: %{y} <br> Month %{x}')
    fig2.update_xaxes(title_text="",hoverformat = "%b %Y")
    fig2.update_yaxes(title_text="Lineage Prevalence",range=[0,1.01] #,tickformat='%' adding the tickformat as % does something weird to the y-axis
                      )
    return fig2


