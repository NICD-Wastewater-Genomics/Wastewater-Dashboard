import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, timedelta
from dash import html, dcc, Input, Output, callback
import plotly.graph_objects as go
from datetime import timedelta
from savgol import non_uniform_savgol
from load_data import load_monthly_data, load_monthly_data_smoothed, load_rsa_cases_and_levels, load_color_map
from plotly.subplots import make_subplots

dash.register_page(__name__, path='/')

start = '2021-12-15'
end = date.today()+timedelta(days=5)

def get_cards():
    df = load_rsa_cases_and_levels()
    epiweek = df.iloc[-1, -3]
    no_cases = df.iloc[-1, 1]
    no_ww = df.iloc[-1, 2]
    end_week = df.iloc[-1, -1]
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
    return card_content1, card_content2, card_content3, card_content4


def bar_chart():
    df = load_rsa_cases_and_levels()
    df['end'] = pd.to_datetime(df['end'])
    df = df[df['end']>=start]

    df_s = df[['end','sum_genomes']]
    df_s = df_s[~df_s['sum_genomes'].isna()]
    numberDates = [dvi.value/10**11 for dvi in df_s['end']]
    df_s['ww_smoothed'] = non_uniform_savgol(numberDates,df_s['sum_genomes'].to_numpy(),5,1)
    fig = make_subplots(specs=[[{"secondary_y": True}]])#,[{"secondary_y": True}]],rows=2, cols=1,shared_xaxes=True)

    fig.add_trace(
        go.Bar(
            x=df['end'], y=df['n'],
            marker_color='lightgray',
            name="Clinical",
            hovertemplate='%{y} cases',#<br> %{text}',
            textposition = "none"),
        secondary_y=False)#, row=1,col=1)  # specify for colour for df

    fig.add_trace(
        go.Scatter(
            x=df['end'], y=df['sum_genomes'],
            mode='markers',
            line=dict(color="cornflowerblue", width=4),
            hovertemplate='%{y} copies/mL',
            name="Wastewater"),
            secondary_y=True)#,row=1,col=1)

    fig.add_trace(
        go.Scatter(
            x=df_s['end'], y=df_s['ww_smoothed'],
            mode='lines',
            line=dict(color="cornflowerblue", width=4),
            hovertemplate='%{y} copies/mL',
            name="Smoothed wastewater"),
            secondary_y=True)#,row=1,col=1)

    fig.update_layout(
        template='none',
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
    margin=dict(l=45, r=0, t=20, b=50))
    fig.update_xaxes(hoverformat = "%Y, Epiweek %W",)
    fig.update_yaxes(title_text="Laboratory confirmed cases",
                     secondary_y=False,
                     range=[0,df['n'].max()*1.02],
                     showgrid=False,
                     automargin=True,
                     title_standoff=20  # Add space between y-axis label and graph
                     )
    fig.update_yaxes(title_text="Genome Copies/ml (N Gene)",
                     secondary_y=True,
                     range=[0,df['sum_genomes'].max()*1.02],
                     automargin=True,
                     title_standoff=20  # Add space between y-axis label and graph
                     )
    fig.update_layout(width=800,hovermode="x unified", xaxis_range=[start,end])
    fig.update_traces(hoverinfo = 'name+y',cliponaxis=False)
    # fig.update_traces(hovertemplate="%{y}")
    return fig



def home_container():
    card_contents = get_cards()
    return dbc.Container([
        dbc.Row(
            dbc.Col(
                html.H1(id="H1", children="SARS-CoV-2 Wastewater Surveillance", style={'color': 'white'}),
                width=12
            ),
            style={"textAlign": "center", "paddingTop": 30, "paddingBottom": 30, "backgroundColor": "#A6CE39"}
        ),
        html.Div(style={'height': '15px'}),
        dbc.Row(
            [dbc.Col(dbc.Card(card_contents[i], color="primary", inverse=True, className="content-card"),
                     width=12 // 4) for i in range(4)],
            className="card-col"
        ),
        html.Div(style={'height': '25px'}),
        html.P(
            id="intro",
            children=(
                'To monitor the levels of SARS-CoV-2 infections across South Africa, NICD measures virus concentrations in '
                'community wastewater (sewage). SARS-CoV-2 virus fragments are excreted in stool by persons with COVID-19 and '
                'can be detected at wastewater aggregation sites. The levels of SARS-CoV-2 in wastewater reflect caseload and '
                'geographic distribution of cases, and often provide an early warning of increases in infections in the community.'
            ),
            style={"font-size": 20}
        ),
        html.Div(style={'height': '25px'}),
        html.H3(
            id="H3_", children='National SARS-CoV-2 Wastewater Levels',
            style={"textAlign": "center", "marginTop": 10, "marginBottom": 0}
        ),
        html.Div(style={'height': '15px'}),
        dbc.Row(
            dcc.Graph(id="bar_plot", figure=bar_chart(), config={'displayModeBar': False,'doubleClick': 'reset'}),
            style={"width": "100%", "align-items": "center", 'justify-content': 'center', 'margin': 'auto'}
        ),
        html.Div(style={'height': '25px'}),
        html.P(
            id="seq_intro",
            children=[
                'To track the evolution and spread of SARS-CoV-2 lineages across South Africa, wastewater virus sequencing followed by bioinformatic analyses with the ',
                html.A("Freyja", href='https://github.com/andersen-lab/Freyja'),
                ' bioinformatic tool allows for the determination of variants in each wastewater sample. Samples are aggregated across all sites, providing a national characterization of lineage prevalence.'
            ],
            style={"font-size": 20}
        ),
        html.Div(style={'height': '30px'}),
        html.H3(
            id="H3", children="SARS-CoV-2 Lineage Prevalence Observed via Wastewater",
            style={"textAlign": "center", "marginTop": 5, "marginBottom": 5}
        ),
        html.Div(style={'height': '15px'}),
        html.Div(
            dbc.RadioItems(
                id="plottype",
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[
                    {"label": "Monthly Trends", "value": "monthly"},
                    {"label": "Smoothed Daily Trends", "value": "daily"}
                ],
                value="daily",
                style={"width": "100%", "justify-content": "flex-end"}
            ),
            style={"marginTop": 0, "marginBottom": 0}
        ),
        html.Div(style={'height': '15px'}),
        dbc.Row(
            dcc.Graph(id="seq_graph0", config={'displayModeBar': False}),
            style={"width": "100%", "align-items": "center", 'justify-content': 'center', 'margin': 'auto'}
        )
    ], fluid=True)

layout = home_container


@callback(
    Output("seq_graph0", "figure"),
    Input("plottype", "value"))#,suppress_callback_exceptions=True)
def seq_plot(plottype):
    colorDict = load_color_map()
    names = {'variable':'Lineage', 'index':'Month', 'value':'Prevalence'}
    if plottype=='monthly':
        seq_df = load_monthly_data()
        seq_df = seq_df[seq_df.index >=start] # switch to last 12 or 24 months?
        fig2 = go.Figure(data=[go.Bar(name=sfc, x=seq_df.index, y=seq_df[sfc], marker_color=colorDict[sfc]) for sfc in seq_df.columns])
        # # Change the bar mode
        fig2.update_layout(barmode='stack',yaxis_tickformat = '.0%')
        fig2.update_layout(legend_title_text=names['variable'])
        fig2.update_xaxes(title_text="",hoverformat = "%b %Y")
    else:
        seq_df_daily  = load_monthly_data_smoothed()
        seq_df_daily = seq_df_daily[seq_df_daily.index >=start] # switch to last 12 or 24 months?

        fig2 = go.Figure([go.Scatter(name=sfc,x=seq_df_daily.index, y=seq_df_daily[sfc], marker_color=colorDict[sfc],
                                      mode='lines', stackgroup='one', fillcolor=colorDict[sfc],
                                      line=dict(width=0.0)) for sfc in seq_df_daily.columns])
        fig2.update_layout(legend_title_text=names['variable'],hovermode='x unified',hoverlabel=dict(font_size=12), yaxis_tickformat = '.0%')
        fig2.update_xaxes(title_text="",hoverformat = "%b %d %Y")
    fig2.update_layout(
        legend=dict(
        orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5,
        font={'size':15}
    ),margin=dict(l=40, r=75, t=15, b=0))

    fig2.update_layout(xaxis_range=[start, end], template='none')
    # fig2.update_traces(hovertemplate = 'Lineage: %{y} <br> Month %{x}')
    fig2.update_yaxes(title_text="Lineage Prevalence",
                      range=[0,1.01], #,tickformat='%' adding the tickformat as % does something weird to the y-axis
                      automargin=True,
                      title_standoff=20 # Add space between y-axis label and graph
    )
    return fig2




