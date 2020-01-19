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
    df = pd.read_csv(os.path.join(LOG_PATH, 'Manual_Log_Filtered.csv'),
                     sep=",", error_bad_lines=False)

    dashapp.layout = html.Div([
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
            ],
            data=df.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=10,
        ),
        html.Div(id='datatable-interactivity-container')
    ])

    @dashapp.callback(
        Output('datatable-interactivity', 'style_data_conditional'),
        [Input('datatable-interactivity', 'selected_columns')]
    )
    def update_styles(selected_columns):
        return [{
            'if': {'column_id': i},
            'background_color': '#D2F3FF'
        } for i in selected_columns]

    @dashapp.callback(
        Output('datatable-interactivity-container', "children"),
        [Input('datatable-interactivity', "derived_virtual_data"),
         Input('datatable-interactivity', "derived_virtual_selected_rows")])
    def update_graphs(rows, derived_virtual_selected_rows):
        # When the table is first rendered, `derived_virtual_data` and
        # `derived_virtual_selected_rows` will be `None`. This is due to an
        # idiosyncracy in Dash (unsupplied properties are always None and Dash
        # calls the dependent callbacks when the component is first rendered).
        # So, if `rows` is `None`, then the component was just rendered
        # and its value will be the same as the component's dataframe.
        # Instead of setting `None` in here, you could also set
        # `derived_virtual_data=df.to_rows('dict')` when you initialize
        # the component.
        if derived_virtual_selected_rows is None:
            derived_virtual_selected_rows = []

        dff = df if rows is None else pd.DataFrame(rows)

        colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
                  for i in range(len(dff))]

        # Outliers
        outlier_list = []
        sim_file = 'Manual_Log_Filtered.csv'
        metrics = ["CPU Usage", "Memory Usage"]
        num_std_dev = 3

        for column in metrics:
            if column in dff:
                outlier_list.append(detect_outliers(
                    list(dff[column]), s=num_std_dev, filename='outliers_' + column + '_' + sim_file))

        metric_outliers = {}
        for idx, metric in enumerate(metrics):
            metric_outliers[metric] = [list(outlier_list[idx].keys()),
                                       list(outlier_list[idx].values())]

        aux_X = list(range(0, dff[column].shape[0]))

        fig = [
            dcc.Graph(
                id=column,
                figure={
                    "data": [
                        {
                            # "x": dff["Time_floor"],
                            "x": aux_X,
                            "y": dff[column],
                            "type": "line",
                            "marker": {"color": colors},
                            "name": "usage"
                        },
                        {
                            "x": metric_outliers[column][0],
                            "y": metric_outliers[column][1],
                            'mode': 'markers',
                            "marker": {"color": 'red'},
                            "name": "outliers"
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {
                            "automargin": True,
                            "title": {"text": column}
                        },
                        "height": 250,
                        "margin": {"t": 10, "l": 10, "r": 10},
                    },
                },
            )


            # check if column exists - user may have deleted it
            # If `column.deletable=False`, then you don't
            # need to do this check.
            for column in metrics if column in dff
        ]

        return fig
