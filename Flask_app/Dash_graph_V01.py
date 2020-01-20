# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 14:16:45 2020

@author: Milosh
"""

import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('Manual_Log_Filtered_New.csv')
print(df.columns)

servers = df['Server'].unique()
print(servers)

metrics = df['variable'].unique()
print(metrics)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.Div([
        dcc.Dropdown(
        id='servers-radio',
        options=[{'label': k, 'value': k} for k in servers],
        value='A'
        )],style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
        dcc.Dropdown(id='metrics-radio')] ,style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]),

    html.Hr(),

    html.Div(id='display-selected-values'),
    dcc.Graph(id='indicator-graphic')
])


@app.callback(
    Output('metrics-radio', 'options'),
    [Input('servers-radio', 'value')])
def set_metrics_options(selected_country):
    return [{'label': i, 'value': i} for i in metrics]


@app.callback(
    Output('metrics-radio', 'value'),
    [Input('metrics-radio', 'options')])
def set_metrics_value(available_options):
    print(available_options[0]['value'])
    return available_options[0]['value']

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('servers-radio', 'value'),
     Input('metrics-radio', 'value')])

def update_graph(servers,metrics):
    
    print(servers)
    print(metrics)
    
    dff = df[(df["Server"] == servers) & (df["variable"] == metrics)]
    print(dff)

    return {
        'data': [dict(
            x=dff["Time_floor"],
            y=dff["Value"],
            mode='line',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': "Timefloor"
            },
            yaxis={
                'title': metrics
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }



if __name__ == '__main__':
    app.run_server()