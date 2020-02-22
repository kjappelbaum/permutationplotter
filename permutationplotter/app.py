# -*- coding: utf-8 -*-
import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from .permutation import generate_random, plot_permuted, MEAN_X, MEAN_Y, STD_X, STD_Y, N
import pandas as pd

VERSION = 0.1


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX, "assets/dropdown.css"])

app.layout = dbc.Container(
    [
        html.H1("Is there (still) a pattern?", className="display-3"),
        html.Hr(),
        html.P(""),
        html.P(
            [
                "Finding or observing patterns, can be fragile and we always have to keep in mind that we deal with random variables. ",
                "When, after random permutation, you still see a pattern in your data should check your conclusions...",
            ]
        ),
        html.P(
            [
                "This app was inspired by a ",
                html.A(
                    "blog post by Andrew Gelman",
                    href="https://statmodeling.stat.columbia.edu/2020/02/20/an-article-in-a-statistics-or-medical-journal-using-simulations-to-convince-people-of-the-importance-of-random-variation-when-interpreting-statistics/",
                ),
                ".",
            ]
        ),
        html.Div(id="output-data-upload", style={"display": "none"}),
        html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardHeader(
                            dbc.Button(
                                html.H3("Test your data"),
                                color="link",
                                id="group-0-toggle",
                            )
                        ),
                        dbc.Collapse(
                            dbc.CardBody(
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            
                                                    [
                                                        html.H3(
                                                            "Select the columns",
                                                            id="columnselecthead",
                                                        ),
                                                        dbc.Tooltip(
                                                            "Select here the columns from your table that we will use on x and y axis, and the coloring of the points. ",
                                                            target="columnselecthead",
                                                        ),
                                                        dcc.Dropdown(
                                                            options=[], id="xdropdown", 
                                                        ),
                                                        dcc.Dropdown(
                                                            options=[], id="ydropdown", 
                                                        ),
                                                        dcc.Dropdown(
                                                            options=[], id="zdropdown", 
                                                        ),
                                                    ],
                                            md=4,
                                            style={"overflow": "auto",},
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Container(
                                                    [
                                                        html.H2(
                                                            "Upload your tabular data",
                                                            className="display-5",
                                                            id="datauploadheader",
                                                        ),
                                                        dbc.Tooltip(
                                                            "We can read excel files as common tabular data formats such as comma or tab seperated text files. We do not skip any rows or columns. We assume that the first row contains the column names.",
                                                            target="datauploadheader",
                                                        ),
                                                        dcc.Upload(
                                                            id="upload-data",
                                                            children=html.Div(
                                                                [
                                                                    "Drag and Drop or ",
                                                                    html.A(
                                                                        "Select File"
                                                                    ),
                                                                ]
                                                            ),
                                                            style={
                                                                "width": "100%",
                                                                "height": "60px",
                                                                "lineHeight": "60px",
                                                                "borderWidth": "1px",
                                                                "borderStyle": "dashed",
                                                                "borderRadius": "5px",
                                                                "textAlign": "center",
                                                                "margin": "10px",
                                                            },
                                                            # Allow multiple files to be uploaded
                                                            multiple=False,
                                                        ),
                                                    ]
                                                )
                                            ]
                                        ),
                                    ],
                                    style={"display": "flex"},
                                )
                            ),
                            id="collapse-0", 
                        ),
                    ], 
                ),
                dbc.Card(
                    [
                        dbc.CardHeader(
                            dbc.Button(
                                html.H3("Simulate Random Data"),
                                color="link",
                                id="group-1-toggle",
                            )
                        ),
                        dbc.Collapse(
                            dbc.CardBody(
                                html.Div(
                                    [
                                        html.P(
                                            "Use the sliders below to change the properties of the normal distributions from which we draw to generate three plots of random points."
                                        ),
                                        html.P(
                                            "In addition to the points we also show the best linear fit."
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col("mean x", md=2),
                                                dbc.Col(
                                                    [
                                                        dcc.Slider(
                                                            id="meanx",
                                                            min=-100,
                                                            max=100,
                                                            step=0.5,
                                                            value=MEAN_X,
                                                        )
                                                    ]
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col("mean y", md=2),
                                                dbc.Col(
                                                    [
                                                        dcc.Slider(
                                                            id="meany",
                                                            min=-100,
                                                            max=100,
                                                            step=0.5,
                                                            value=MEAN_Y,
                                                        )
                                                    ]
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col("standard deviation x", md=2),
                                                dbc.Col(
                                                    [
                                                        dcc.Slider(
                                                            id="stdx",
                                                            min=0,
                                                            max=100,
                                                            step=0.5,
                                                            value=STD_X,
                                                        )
                                                    ]
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col("standard deviation y", md=2),
                                                dbc.Col(
                                                    [
                                                        dcc.Slider(
                                                            id="stdy",
                                                            min=0,
                                                            max=100,
                                                            step=0.5,
                                                            value=STD_Y,
                                                        )
                                                    ]
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col("number of points", md=2),
                                                dbc.Col(
                                                    [
                                                        dcc.Slider(
                                                            id="npts",
                                                            min=2,
                                                            max=100,
                                                            step=1,
                                                            value=N,
                                                        )
                                                    ]
                                                ),
                                            ]
                                        ),
                                    ]
                                )
                            ),
                            id="collapse-1",
                        ),
                    ],
                ),
            ],
            className="accordion",
        ),
        html.Div(
            [
                html.P(),
                html.H3("Can you distinguish the real data from the permuted data?"),
                html.Div([dcc.Graph(figure=generate_random())], id="plot"),
                dbc.Container([html.P()]),
            ],
            style={"zIndex": -10},
        ),
        html.Hr(),
        html.Footer(
            [
                "© Kevin Maik Jablonka at the Laboratory of Molecular Simulation at EPFL, 2020.  v{}. ".format(
                    VERSION
                ),
                html.A(
                    "Code available on GitHub, please open an issue if you find a bug or a have suggestion.",
                    href="https://github.com/kjappelbaum/permutationplotter",
                ),
            ]
        ),
    ]
)


def parse_contents(contents, filename):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.StringIO(decoded.decode("utf-8")))
        elif "txt" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "tsv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    except Exception as e:
        app.logger.error(e)
        return html.Div(["There was an error processing this file."])

    return df.to_json()


@app.callback(
    Output("output-data-upload", "children"),
    [Input("upload-data", "contents"), Input("upload-data", "filename")],
)
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [parse_contents(list_of_contents, list_of_names)]
        return children


@app.callback(
    Output("xdropdown", "options"), [Input("output-data-upload", "children")],
)
def update_dropdowns(jsonified_cleaned_data):
    if jsonified_cleaned_data is not None:
        app.logger.info(jsonified_cleaned_data)
        df = pd.read_json(jsonified_cleaned_data[0])
        columns = list(df.columns)
        items = [{"label": column, "value": column} for column in columns]

        return items
    else:
        return []


@app.callback(
    Output("ydropdown", "options"), [Input("output-data-upload", "children")],
)
def update_dropdowns(jsonified_cleaned_data):
    if jsonified_cleaned_data is not None:
        app.logger.info(jsonified_cleaned_data)
        df = pd.read_json(jsonified_cleaned_data[0])
        columns = list(df.columns)
        items = [{"label": column, "value": column} for column in columns]

        return items
    else:
        return []


@app.callback(
    Output("zdropdown", "options"), [Input("output-data-upload", "children")],
)
def update_dropdowns(jsonified_cleaned_data):
    if jsonified_cleaned_data is not None:
        app.logger.info(jsonified_cleaned_data)
        df = pd.read_json(jsonified_cleaned_data[0])
        columns = list(df.columns)
        items = [{"label": column, "value": column} for column in columns]

        return items
    else:
        return []


@app.callback(
    Output("plot", "children"),
    [
        Input("npts", "value"),
        Input("meanx", "value"),
        Input("meany", "value"),
        Input("stdx", "value"),
        Input("stdy", "value"),
        Input("output-data-upload", "children"),
        Input("xdropdown", "value"),
        Input("ydropdown", "value"),
        Input("zdropdown", "value"),
    ],
)
def update_plot(n, meanx, meany, stdx, stdy, jsonified_cleaned_data, xcol, ycol, zcol):
    ctx = dash.callback_context
    triggered_by = ctx.triggered[0]["prop_id"].split(".")[0]
    app.logger.info("Plot updated triggered by {}".format(triggered_by))

    if triggered_by in ["meanx", "meany", "stdx", "stdy", "npts"]:
        print("plotting")
        return dcc.Graph(figure=generate_random(n, meanx, stdx, meany, stdy))
    elif triggered_by in ["xdropdown", "ydropdown", "zdropdown"]:
        if jsonified_cleaned_data is not None:
            app.logger.info("found df")
            df = pd.read_json(jsonified_cleaned_data[0])
            if not None in [xcol, ycol, zcol]:
                app.logger.info("plotting data")
                return dcc.Graph(figure=plot_permuted(df, xcol, ycol, zcol))


@app.callback(
    [Output(f"collapse-{i}", "is_open") for i in [0, 1]],
    [Input(f"group-{i}-toggle", "n_clicks") for i in [0, 1]],
    [State(f"collapse-{i}", "is_open") for i in [0, 1]],
)
def toggle_accordion(n1, n2, is_open1, is_open2):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ""
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "group-0-toggle" and n1:
        return not is_open1, False
    elif button_id == "group-1-toggle" and n2:
        return False, not is_open2
    else:
        return not is_open1, False
    return False, False


if __name__ == "__main__":
    app.run_server(debug=True)

