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
from lib.OutlierDetection import moving_average, detect_outliers

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


def get_log_filtered(f):
    """
    Function to compute per-server/time aggregations of a given logfile.

    Parameters
    ----------
        f: logfile 

    Returns
    -------
        filtered_logfile_name: string
    """

    df = pd.read_csv(os.path.join(LOG_PATH, f), sep = ";", error_bad_lines=False)

    # Split dataframe into three dataframes based on Server
    df = df.drop(['Message_type', 'Transaction_ID','To_Server', 'Message'], axis=1)

    df = df.reset_index()
    df = df.drop(['index'], axis=1)
    df["Time"]=df["Time"].div(60)
    df["Time_floor"] = np.floor(df["Time"]).astype("int")
    df = df.groupby(['Server','Time_floor'], as_index=False).mean()
    df = df.drop(['Time'], axis=1)

    df_melt = pd.melt(
                    df, 
                    id_vars = ["Server", "Time_floor"], 
                    value_vars = ["CPU Usage","Memory Usage"], 
                    value_name = "Value"
    )

    df_melt = df_melt.sort_values(by=["Server", "Time_floor"])

    file_out_filtered = f.split('.')[0] + "_filtered.csv"
    df_melt.to_csv(os.path.join(LOG_PATH, 'filtered', file_out_filtered))

    return file_out_filtered




def show_dash_graphs(dashapp, f, eventId):
    """
    Function to generate Dash visualizations for a given simulation logfile.

    Parameters
    ----------
        dashapp: Dash app object
        f: logfile 
        eventId: current time, in order to avoid callback duplicates

    Returns
    -------
        Dash Graph
    """
    f_filtered = get_log_filtered(f)

    if f_filtered:

        df = pd.read_csv(os.path.join(LOG_PATH, 'filtered', f_filtered))

        servers = df['Server'].unique()
        metrics = df['variable'].unique()
        std_dict = {'Std = 1':1, 'Std = 2':2, 'Std = 3':3, 'Std = 4':4}

        dashapp.layout = html.Div([
            html.Div([

                html.Div('Server', style={'color': 'black', 'fontSize': 14}),
                html.Div([
                    dcc.Dropdown(
                        id='servers-radio-{}'.format(eventId),
                        options=[{'label': k, 'value': k} for k in servers],
                        value='A'
                    )],
                    style={'width': '48%', 'display': 'inline-block'}
                ),
                
                
                html.Div([
                    html.Div('Outlier Std Threshold', style={'color': 'black', 'fontSize': 14}),
                    dcc.Dropdown(
                        id='std-radio-{}'.format(eventId),
                        options=[{'label': i[0], 'value': i[1]} for i in std_dict.items()],
                        value=2
                    ),
                    dcc.Checklist(
                        id='show-mv-avg-{}'.format(eventId),
                        options=[
                            {'label': 'Show Rolling Average', 'value': 'Yes'}
                        ],
                        value=['Yes'],
                        labelStyle={'display': 'inline-block'}
                    )],
                    style={'width': '48%',  'float': 'right', 'display': 'inline-block'}
                ),



            ]),

            html.Div('Metric', style={'color': 'black', 'fontSize': 14}),
            html.Div([
                dcc.Dropdown(id='metrics-radio-{}'.format(eventId))],
                style={'width': '48%', 'display': 'inline-block'}
            ),

            html.Div(id='display-selected-values-{}'.format(eventId)),
            dcc.Graph(id='indicator-graphic-{}'.format(eventId))


        ])


        @dashapp.callback(
            Output('metrics-radio-{}'.format(eventId), 'options'),
            [Input('servers-radio-{}'.format(eventId), 'value')])
        def set_metrics_options(selected_country):
            return [{'label': i, 'value': i} for i in metrics]

        @dashapp.callback(
            Output('metrics-radio-{}'.format(eventId), 'value'),
            [Input('metrics-radio-{}'.format(eventId), 'options')])
        def set_metrics_value(available_options):
            return available_options[0]['value']

        @dashapp.callback(
            Output('indicator-graphic-{}'.format(eventId), 'figure'),
            [Input('servers-radio-{}'.format(eventId), 'value'),
             Input('metrics-radio-{}'.format(eventId), 'value'),
             Input('std-radio-{}'.format(eventId), 'value'),
             Input('show-mv-avg-{}'.format(eventId), 'value')])

        def update_graph(servers, metrics, std, show_mv_avg):

            dff = df[(df["Server"] == servers) & (df["variable"] == metrics)]

            # Outliers
            outliers = detect_outliers(
                                        list(dff["Value"]), 
                                        s=std, 
                                        filename='outliers_' + metrics + '_' + f_filtered
                        )

            outliers_X = list(outliers.keys())
            outliers_Y = list(outliers.values())

            data = [
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
                    ]
      
            # Moving average
            if show_mv_avg:
                n = 10
                mv_avg_Y = moving_average(list(dff["Value"]))
                mv_avg_X = list(range(0+n-1, len(mv_avg_Y)+n-1))

                data.append(
                            dict(
                                x=mv_avg_X,
                                y=mv_avg_Y,
                                mode='line',
                                marker={
                                    'size': 8,
                                    'opacity': 0.8,
                                    'line': {'width': 0.5, 'color': 'white'},
                                    'color': '#ffe063'
                                },
                                name="Rolling Average"
                            )
                    )

            return {
                'data': data,
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

    else:
        print("Filtered logfile could not be generated. Check get_log_filtered() for details.")




