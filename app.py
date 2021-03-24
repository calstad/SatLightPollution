# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import base64
import datetime
import io
import os
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
tle_path = 'tle.txt'
sle_path = 'sle.txt'

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
os.system(f"slp --tle-file {tle_path} --out {sle_path}")

df = pd.read_csv(sle_path, sep="\t")
df = df.sort_values('time_s')  # ensure chronological order
df = df.reset_index(drop=True)
# print(df.head)
df['NORAD'] = df['NORAD'].astype(str)  # ensure NORAD id's are discrete

fig = px.scatter(df, x='Position_wrt_FOV_Azimuth_deg', y='Position_wrt_FOV_Radius_deg',
                 animation_frame="time_s", animation_group="NORAD", size="apparent_magnitude", hover_name="NORAD",
                 range_x=[-1.1, 1.1], range_y=[-1.1, 1.1], color="NORAD")

app.layout = html.Div(children=[

    html.H1(children='Satellite FOV',
            style={
                'text-align': 'center'
            }),

    html.Div(children='Satellites in view for given viewing window',
             style={
                 'text-align': 'center'
             }),

    dcc.Graph(
        id='satellite-graph',
        figure=fig
    ),

    html.Div(id='output-data'),
])


if __name__ == '__main__':
    app.run_server(debug=True, port=8051, host='0.0.0.0')
