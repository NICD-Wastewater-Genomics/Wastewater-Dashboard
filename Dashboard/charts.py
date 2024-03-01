import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import json
from datetime import date

start = '2021-12-15'
end = date.today()

df = pd.read_csv("data/rsa_cases_vs_levels.csv")
epiweek = df.iloc[-1, 8]
no_cases = df.iloc[-1, 1]
end_week = df.iloc[-1, -1]
df = df[df['end']>=start]
print(df) 
def bar_chart(df):

    fig = make_subplots(specs=[[{"secondary_y": True}]])#,[{"secondary_y": True}]],rows=2, cols=1,shared_xaxes=True)

    fig.add_trace(
        go.Bar(
            x=df['end'], y=df['n'],
            marker_color='gray',
            name="Clinical",
            hovertemplate='%{y} cases',#<br> %{text}',
            textposition = "none"),
        secondary_y=False)#, row=1,col=1)  # specify for colour for df

    fig.add_trace(
        go.Scatter(
            x=df['end'], y=df['sum_genomes'],
            mode='lines+markers',
            line=dict(color="blue", width=4),
            hovertemplate='%{y} copies/mL',
            name="Wastewater"), secondary_y=True)#,row=1,col=1)

    fig.update_layout(
        barmode='group')

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(l=0, r=0, t=20, b=20))
    fig.update_xaxes(hoverformat = "%Y, Epiweek %W")
    fig.update_yaxes(title_text="Laboratory confirmed cases", secondary_y=False)
    fig.update_yaxes(title_text="Genome Copies/ml (N Gene)", secondary_y=True)
    fig.update_layout(width=800,hovermode="x unified", xaxis_range=[start,end]) 
    fig.update_traces(hoverinfo = 'name+y')
    # fig.update_traces(hovertemplate="%{y}")



    return fig

seq_df = pd.read_csv("data/NICD_monthly.csv",index_col=0)
seq_df = seq_df[seq_df.index >=start] # switch to last 12 or 24 months? 
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


    fig2.update_layout(
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.08,
        xanchor="right",
        x=1
    ),margin=dict(l=0, r=75, t=30, b=20))
    fig2.update_layout(width=800, xaxis_range=[start,end]) 
    fig2.update_layout(legend_title_text = names['variable'])
    # fig2.update_traces(hovertemplate = 'Lineage: %{y} <br> Month %{x}')
    fig2.update_xaxes(title_text="")
    fig2.update_yaxes(title_text="Lineage Prevalence",range=[0,1])
    return fig2



