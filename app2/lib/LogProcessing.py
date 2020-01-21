"""
This file contains a set of methods to process a simulation logfile.
Such calculations are later used to generate visualizations.

@author Antonio Samaniego / Milos Dragojevic
@file   LogProcessing.py
@scope  public
"""

# third party dependencies
import math
import os
import csv
import json
import pandas as pd
import numpy as np
from flask.json import jsonify, load
import dash
import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# local dependencies
from lib.OutlierDetection import detect_outliers

# Global vars
# Set location of log folder relative to this script
LOG_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logs'))


def get_endpoint_json(f):
    # Read in the log data
    log_df = pd.read_csv(os.path.join(LOG_PATH, f), sep=';')

    # Create 'final_matrix' (initially a zeros matrix)
    rows = log_df['Server'].dropna().unique()
    cols = log_df['To_Server'].dropna().unique()
    final_matrix = pd.DataFrame(0, index=cols, columns=rows)

    # Filter by Server and To_Server
    filtered_log_df = log_df[['Server', 'To_Server']]

    # Group by unique combinations and count occurrences
    endpoint_df = filtered_log_df.groupby(
        ['Server', 'To_Server']).size().reset_index().rename(columns={0: 'count'})

    endpoint_json = {
        "nodes": [],
        "links": []
    }

    groups = cols
    for idx, g in enumerate(groups):
        endpoint_json["nodes"].append({
            "id": g,
            "group": idx + 1
        })

    for idx, r in endpoint_df.iterrows():
        endpoint_json["links"].append({
            "source": r['Server'],
            "target": r['To_Server'],
            "value": r['count']
        })

    return jsonify(endpoint_json)


def get_endpoint_matrix(f):
    # Read in the log data
    log_df = pd.read_csv(os.path.join(LOG_PATH, f), sep=';')

    # Create 'final_matrix' (initially a zeros matrix)
    rows = log_df['Server'].dropna().unique()
    cols = log_df['To_Server'].dropna().unique()
    final_matrix = pd.DataFrame(0, index=cols, columns=rows)

    # Filter by Server and To_Server
    filtered_log_df = log_df[['Server', 'To_Server']]

    # Group by unique combinations and count occurrences
    endpoint_df = filtered_log_df.groupby(
        ['Server', 'To_Server']).size().reset_index().rename(columns={0: 'count'})

    # Iterate over combinations in grouped_by df and fill in occurrences in final_matrix df
    for index, row in endpoint_df.iterrows():
        final_matrix.loc[row['To_Server']][row['Server']] = row['count']

    # Convert 'final_matrix' df to array and prepare data for jsonify
    final_matrix_arr = final_matrix.values.tolist()
    json_convert = {"data":
                    {"matrix": final_matrix_arr,
                        "names": rows.tolist()},
                    "message": "Success"}

    return jsonify(json_convert)


def show_dash_graphs(dashapp):
    """
    Function to generate Dash visualizations from a simulation logfile.

    Parameters
    ----------
        dashapp: Dash app object

    Returns
    -------
        Dash Graph
    """

    f = 'Manual_Log_Filtered_New.csv'

    df = pd.read_csv(os.path.join(LOG_PATH, f))
    servers = df['Server'].unique()
    metrics = df['variable'].unique()
    std_dict = {'Std = 1':1, 'Std = 2':2, 'Std = 3':3, 'Std = 4':4}

    dashapp.layout = html.Div([
        html.Div([

            html.Div('Server', style={'color': 'black', 'fontSize': 14}),
            html.Div([
                dcc.Dropdown(
                    id='servers-radio',
                    options=[{'label': k, 'value': k} for k in servers],
                    value='A'
                )],
                style={'width': '48%', 'display': 'inline-block'}
            ),
            
            
            html.Div([
                html.Div('Outlier Std Threshold', style={'color': 'black', 'fontSize': 14}),
                dcc.Dropdown(
                    id='std-radio',
                    options=[{'label': i[0], 'value': i[1]} for i in std_dict.items()],
                    value=2
                )],
                style={'width': '48%',  'float': 'right', 'display': 'inline-block'}
            )

        ]),

        html.Div('Metric', style={'color': 'black', 'fontSize': 14}),
        html.Div([
            dcc.Dropdown(id='metrics-radio')],
            style={'width': '48%', 'display': 'inline-block'}
        ),

        html.Div(id='display-selected-values'),
        dcc.Graph(id='indicator-graphic')


    ])


    @dashapp.callback(
        Output('metrics-radio', 'options'),
        [Input('servers-radio', 'value')])
    def set_metrics_options(selected_country):
        return [{'label': i, 'value': i} for i in metrics]

    @dashapp.callback(
        Output('metrics-radio', 'value'),
        [Input('metrics-radio', 'options')])
    def set_metrics_value(available_options):
        return available_options[0]['value']

    @dashapp.callback(
        Output('indicator-graphic', 'figure'),
        [Input('servers-radio', 'value'),
         Input('metrics-radio', 'value'),
         Input('std-radio', 'value')])

    def update_graph(servers, metrics, std):
        
        if not std:
            std = 3

        dff = df[(df["Server"] == servers) & (df["variable"] == metrics)]

        # Outliers
        outliers = detect_outliers(
                                    list(dff["Value"]), 
                                    s=std, 
                                    filename='outliers_' + metrics + '_' + 'Manual_Log_Filtered_New.csv'
                    )

        outliers_X = list(outliers.keys())
        outliers_Y = list(outliers.values())

        return {
            'data': [
                    dict(
                            x=dff["Time_floor"],
                            y=dff["Value"],
                            mode='line',
                            marker={
                                'size': 15,
                                'opacity': 0.5,
                                'line': {'width': 0.5, 'color': 'white'}
                            },
                            name="Usage"
                        ),
                    dict(
                            x=outliers_X,
                            y=outliers_Y,
                            mode='markers',
                            marker= {"color": 'red'},
                            name="Outliers"
                        )
                    ],

            'layout': dict(
                xaxis={
                    'title': "Time"
                },
                yaxis={
                    'title': metrics
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest'
            )
        }




