import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

FILE_PATH = r'/Users/ahmednader/Desktop/retail project/datasets/retail_analytics_20k.csv'

df = pd.read_csv(FILE_PATH)

data = df.groupby('quarter')['profit_egp'].sum().reset_index()

fig = px.bar(data, x='quarter', y='profit_egp')

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Profit per Qurater'),
    dcc.Dropdown(
        id='dropdown_region',
        options=[
        {'label': r, 'value': r} for r in df['region'].unique()
    ]),
    dcc.Graph(id='profit_per_region_fig'),
])

@app.callback(
        Output('profit_per_region_fig', 'figure'),
        Input('dropdown_region', 'value'),
        Input('interval_component', 'n_intervals')
)
def update_dashboard(selected_region, n_intervals):
    df = pd.read_csv(FILE_PATH)
    if selected_region==None:
        data = df.groupby('quarter')['profit_egp'].sum().reset_index()
        fig = px.bar(data, x='quarter', y='profit_egp')
    else:
        filterd_df = df[df['region'] == selected_region]
        profit_per_region = filterd_df.groupby('quarter')['profit_egp'].sum().reset_index()
        fig = px.bar(profit_per_region, x='quarter', y='profit_egp')
    return fig

app.run()