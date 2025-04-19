# !pip install pandas numpy plotly dash dash-bootstrap-components pyngrok

import dash
from dash import dcc, html, Input, Output, State, ctx, dash_table
import plotly.express as px
import pandas as pd
import requests
import datetime

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# URLs for USGS data
USGS_URLS = {
    'day': 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.csv',
    'week': 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.csv',
    'month': 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv'
}

# Region bounding boxes
REGIONS = {
    'world': (-180, 180, -90, 90),
    'na': (-170, -50, 10, 84),
    'sa': (-90, -30, -60, 15),
    'eu': (-25, 60, 35, 70),
    'as': (60, 180, 5, 80),
    'af': (-20, 55, -35, 38),
    'oc': (110, 180, -50, 10)
}


def fetch_data(period):
    try:
        url = USGS_URLS[period]
        df = pd.read_csv(url)
        df['time'] = pd.to_datetime(df['time'])
        return df
    except Exception as e:
        return pd.DataFrame()


app.layout = html.Div([
    html.H2("Live Earthquake Monitor", style={"textAlign": "center"}),

    html.Div([
        html.Div([
            html.Label("Time Period"),
            dcc.RadioItems(
                id='time_period',
                options=[
                    {'label': 'Past 24 Hours', 'value': 'day'},
                    {'label': 'Past 7 Days', 'value': 'week'},
                    {'label': 'Past 30 Days', 'value': 'month'}
                ],
                value='week',
                inline=True
            ),
        ], style={"width": "30%"}),

        html.Div([
            html.Label("Minimum Magnitude"),
            dcc.Slider(id='min_magnitude', min=0, max=10, step=0.5, value=2.5,
                       marks={i: str(i) for i in range(0, 11)}),
        ], style={"width": "30%"}),

        html.Div([
            html.Label("Region"),
            dcc.Dropdown(id='region',
                         options=[
                             {'label': 'Worldwide', 'value': 'world'},
                             {'label': 'North America', 'value': 'na'},
                             {'label': 'South America', 'value': 'sa'},
                             {'label': 'Europe', 'value': 'eu'},
                             {'label': 'Asia', 'value': 'as'},
                             {'label': 'Africa', 'value': 'af'},
                             {'label': 'Oceania', 'value': 'oc'}
                         ],
                         value='world'),
        ], style={"width": "30%"})

    ], style={"display": "flex", "justifyContent": "space-around", "gap": "10px", "marginBottom": "10px"}),

    html.Div(style={"textAlign": "center"}, children=[
        html.Button("Refresh Data", id="refresh", n_clicks=0, style={"marginBottom": "20px"})
    ]),

    html.Div(id='stats', style={"display": "flex", "justifyContent": "space-around", "marginBottom": "20px"}),

    html.Div([
        html.Div(dcc.Graph(id='map', config={"displayModeBar": False}), style={"flex": 1}),
        html.Div([
            dcc.Graph(id='histogram', config={"displayModeBar": False}, style={"height": "250px"}),
            dcc.Graph(id='timeseries', config={"displayModeBar": False}, style={"height": "250px"}),
        ], style={"flex": 1, "display": "flex", "flexDirection": "column", "gap": "10px"}),
    ], style={"display": "flex", "gap": "10px", "marginBottom": "20px"}),

    html.Div([
        html.Div(dcc.Graph(id='depth_mag', config={"displayModeBar": False}, style={"height": "300px"}), style={"flex": 1}),
        html.Div(dcc.Graph(id='top_regions', config={"displayModeBar": False}, style={"height": "300px"}), style={"flex": 1})
    ], style={"display": "flex", "gap": "10px"}),

    html.H4("Earthquake Data Table", style={"textAlign": "center", "marginTop": "30px"}),
    dash_table.DataTable(id='data_table', page_size=5, style_table={'overflowX': 'auto'})
], style={"padding": "20px", "maxWidth": "1600px", "margin": "auto"})


@app.callback(
    Output('stats', 'children'),
    Output('map', 'figure'),
    Output('histogram', 'figure'),
    Output('timeseries', 'figure'),
    Output('depth_mag', 'figure'),
    Output('top_regions', 'figure'),
    Output('data_table', 'data'),
    Output('data_table', 'columns'),
    Input('refresh', 'n_clicks'),
    State('time_period', 'value'),
    State('min_magnitude', 'value'),
    State('region', 'value')
)
def update_dashboard(n, time_period, min_mag, region):
    df = fetch_data(time_period)
    if df.empty:
        return [html.Div("No data")]*8

    df = df[df['mag'] >= min_mag]
    lon_min, lon_max, lat_min, lat_max = REGIONS[region]
    df = df[(df['longitude'].between(lon_min, lon_max)) & (df['latitude'].between(lat_min, lat_max))]

    total_quakes = len(df)
    max_mag = df['mag'].max()
    recent_time = df['time'].max()
    significant = len(df[df['mag'] >= 6])

    stats = [
        html.Div([html.H4("Total Quakes"), html.P(f"{total_quakes}")]),
        html.Div([html.H4("Max Magnitude"), html.P(f"{max_mag:.1f}")]),
        html.Div([html.H4("Most Recent"), html.P(str(recent_time))]),
        html.Div([html.H4("Significant (6.0+)"), html.P(f"{significant}")])
    ]

    map_fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", color="mag",
                                 size="mag", hover_name="place",
                                 hover_data={"time": True, "depth": True},
                                 zoom=1, height=400, color_continuous_scale="Turbo")
    map_fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})

    hist = px.histogram(df, x='mag', nbins=20, title="Magnitude Distribution")
    time_series = px.line(df.groupby(df['time'].dt.date).size().reset_index(name='count'),
                          x='time', y='count', title="Earthquakes Over Time")
    scatter = px.scatter(df, x='mag', y='depth', color='mag', title="Depth vs Magnitude")

    df['region'] = df['place'].apply(lambda x: x.split(',')[-1] if ',' in x else 'Other')
    region_counts = df['region'].value_counts().nlargest(10).reset_index()
    region_counts.columns = ['region', 'count']
    bar = px.bar(region_counts, x='region', y='count', title="Top Regions by Count")

    table_data = df[['time', 'mag', 'place', 'depth']].copy()
    columns = [{'name': i, 'id': i} for i in table_data.columns]

    return stats, map_fig, hist, time_series, scatter, bar, table_data.to_dict('records'), columns


if __name__ == '__main__':
#   app.run(debug=True, mode='external')
  app.run(debug=True)
