import dash

from dash import html
from dash import dcc
from dash import dash_table
import dash_bootstrap_components as dbc
import create_charts as cc

fig_line_time = cc.line_chart_over_time('EVENTS')
fig_sb_gender_winter = cc.stacked_bar_gender("Winter")
fig_sb_gender_summer = cc.stacked_bar_gender("Summer")
fig_scatter_mapbox_OSM = cc.scatter_mapbox_para_locations("OSM")
fig_scatter_mapbox_USGS = cc.scatter_mapbox_para_locations("USGS")
df_medals_data = cc.top_ten_gold_data()
fig_top_ten_gold = cc.table_top_ten_gold_table(df_medals_data)
df_medals = cc.get_medals_table_data('London', 2012)
fig_cp_map_medals = cc.choropleth_mapbox_medals(df_medals)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

app.layout = dbc.Container(
    [
        html.H1("Paralympic History"),
        html.H2("Has the number of athletes, nations, events and sports changed over time?"),
        dcc.Graph(
            id='line-chart-time',
            figure=fig_line_time
        ),

        html.H2("Has the ratio of male and female athletes changed over time?"),
        html.Div([
            dcc.Graph(
                id='stacked-bar-gender-win',
                figure=fig_sb_gender_winter
            )
        ], style={'display': 'block'}),
        html.Div([
            dcc.Graph(
                id='stacked-bar-gender-sum',
                figure=fig_sb_gender_summer
            )
        ], style={'display': 'block'}),

        html.H2("Where in the world have the Paralympics have been held?"),
        dbc.Row([
            dbc.Col(width=3, children=[
                html.H3('Event highlights'),
                html.P('Hover over the points in the map to see the event highlights', id='highlight-text')
            ]),
            dbc.Col(width=9, children=[
                dcc.Graph(
                    id='scatter-mapbox-osm',
                    figure=fig_scatter_mapbox_OSM
                ),
            ]),
        ]),

        html.P("United States Geological Survey (USGS) version"),
        dcc.Graph(
            id='scatter-mapbox-usgs',
            figure=fig_scatter_mapbox_USGS
        ),

        html.H2("Which countries have won the most gold medals since 1960?"),
        html.P("Plotly Go table"),
        dcc.Graph(
            id='table-top-ten-gold',
            figure=fig_top_ten_gold
        ),

        html.P("Dash table version"),
        dash_table.DataTable(
            id='table-top-ten-gold-dash',
            columns=[{"name": i, "id": i}
                     for i in df_medals_data.columns],
            data=df_medals_data.to_dict('records'),
            style_cell=dict(textAlign='left'),
            style_header=dict(backgroundColor="lightskyblue"),
            style_data=dict(backgroundColor="white")
        ),

        html.H2("What is the medal performance of each country?"),
        html.P('Medal performance in London 2012'),
        dcc.Graph(
            id='cp-map-medals',
            figure=fig_cp_map_medals
        ),

    ],
    fluid=True,
)

if __name__ == '__main__':
    app.run_server(debug=True)
