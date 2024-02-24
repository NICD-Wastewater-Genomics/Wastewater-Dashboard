import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import json


df = pd.read_csv("data/rsa_cases_vs_levels.csv")
epiweek = df.iloc[-1, 8]
no_cases = df.iloc[-1, 1]
end_week = df.iloc[-1, -1]

def bar_chart(df):

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(
            x=df['epiweek2'], y=df['n'],
            marker_color='gray',
            name="Clinical Cases"),
        secondary_y=False)  # specify for colour for df

    fig.add_trace(
        go.Scatter(
            x=df['epiweek2'], y=df['sum_genomes'],
            line=dict(color="blue", width=4),
            text=df['sum_genomes'],
            name="Wastewater levels"), secondary_y=True)

    fig.update_layout(
        title=' South African SARS-CoV-2 Wastewater Levels',
        barmode='group')

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(l=20, r=20, t=20, b=20))
    fig.update_xaxes(title_text="Epidemiological week")
    fig.update_yaxes(title_text="Laboratory confirmed cases", secondary_y=False)
    fig.update_yaxes(title_text="Genome Copies/ml (N Gene)", secondary_y=True)
    fig.update_layout(width=800) 

    return fig

seq_df = pd.read_csv("data/NICD_monthly.csv",index_col=0)
with open('data/color_map.json') as cdat:
    colorDict = json.load(cdat)
def seq_plot(seq_df,colorDict):
    names = {'variable':'Lineage', 'index':'Month', 'value':'Prevalence'}

    month = seq_df.index
    # print(month)
    # print(seq_df)#"%{label}: <br>Popularity: %{percent} </br> %{text}"
    # print(colorDict)
    fig2 = px.bar(seq_df,x=seq_df.index, y=seq_df.columns,
                  color_discrete_map=colorDict)  # specify for colour for df

    fig2.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.08,
        xanchor="right",
        x=1
    ),margin=dict(l=20, r=20, t=20, b=20))
    fig2.update_layout(width=800) 
    fig2.update_layout(legend_title_text = names['variable'])
    # fig2.update_traces(hovertemplate = 'Lineage: %{y} <br> Month %{x}')
    fig2.update_xaxes(title_text="")
    fig2.update_yaxes(title_text="Lineage Prevalence",range=[0,1])
    return fig2



