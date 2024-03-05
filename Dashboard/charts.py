import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
from datetime import date
from scipy.signal import savgol_filter
from savgol import non_uniform_savgol
start = '2021-12-15'
end = date.today()

df = pd.read_csv("data/rsa_cases_vs_levels.csv")

epiweek = df.iloc[-1, 8]
no_cases = df.iloc[-1, 1]
end_week = df.iloc[-1, -1]
df['end'] = pd.to_datetime(df['end'])
df = df[df['end']>=start]


df_s = df[['end','sum_genomes']]
df_s = df_s[~df_s['sum_genomes'].isna()]
numberDates = [dvi.value/10**11 for dvi in df_s['end']]
df_s['ww_smoothed'] = non_uniform_savgol(numberDates,df_s['sum_genomes'].to_numpy(),5,1)

def bar_chart(df):

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
            name="WW Smoothed"), 
            secondary_y=True)#,row=1,col=1)

    fig.update_layout(
        template='none',
        barmode='group')

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(l=45, r=0, t=20, b=50))
    fig.update_xaxes(hoverformat = "%Y, Epiweek %W",)
    fig.update_yaxes(title_text="Laboratory confirmed cases", secondary_y=False, range=[0,df['n'].max()*1.02],showgrid=False)
    fig.update_yaxes(title_text="Genome Copies/ml (N Gene)", secondary_y=True,range=[0,df['sum_genomes'].max()*1.02])
    fig.update_layout(width=800,hovermode="x unified", xaxis_range=[start,end]) 
    fig.update_traces(hoverinfo = 'name+y')
    # fig.update_traces(hovertemplate="%{y}")



    return fig



