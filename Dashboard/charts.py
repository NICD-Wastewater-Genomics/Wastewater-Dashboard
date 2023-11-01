import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd



df = pd.read_csv("rsa_cases_vs_levels.csv")
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

    fig.update_xaxes(title_text="Epidemiological week")
    fig.update_yaxes(title_text="Laboratory confirmed cases", secondary_y=False)
    fig.update_yaxes(title_text="Genome Copies/ml (N Gene)", secondary_y=True)

    return fig
