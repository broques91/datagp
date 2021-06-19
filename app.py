import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import numpy as np
import folium
import os


# Import data
df = pd.read_csv("data/liens_villes.csv")
df_auto = pd.read_csv("data/automobile.csv")
df_csp = pd.read_csv("data/csp.csv")
df_delinquance = pd.read_csv("data/delinquance.csv")
df_immo = pd.read_csv("data/immobilier.csv")
df_demographie = pd.read_csv("data/demographie.csv")
df_emploi = pd.read_csv("data/emploi.csv")
df_entreprise = pd.read_csv("data/entreprises.csv")
df_infos = pd.read_csv("data/infos.csv")
df_salaire = pd.read_csv("data/salaires.csv")
df_sante_social = pd.read_csv("data/sante_social.csv")

# Dropdown selection ville
villes = [{"label": ville, "value": ville} for ville in df["ville"].unique()]

app = dash.Dash(__name__)
app.title = "DataGP"
app.layout = html.Div(
    [
        html.H1("DataGP"),
        html.Div(
            [
                html.H4("Ville: "),
                dcc.Dropdown(
                    id="dropdown-ville", options=villes, value="Basse-Terre (97100)"
                ),
            ],
            id="ville-picker",
        ),
        html.Div(
            [
                dcc.Tabs(
                    id="tabs",
                    value="tab-1",
                    children=[
                        # Infos
                        dcc.Tab(
                            label="Infos générales",
                            children=[
                                html.Div(
                                    [html.H3("Infos Générales", className="tab-title")]
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="table-infos",
                                                    style_cell={
                                                        "font-family": "Montserrat"
                                                    },
                                                    style_data_conditional=[
                                                        {
                                                            "if": {
                                                                "column_id": "label"
                                                            },
                                                            "textAlign": "left",
                                                        }
                                                    ]
                                                    + [
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248,248,248)",
                                                        }
                                                    ],
                                                    style_header={
                                                        "backgroundColor": "rgb(230,230,230)",
                                                        "fontWeight": "bold",
                                                    },
                                                )
                                            ],
                                            id="infos",
                                            className="six columns",
                                        ),
                                        html.Div(id="map", className="six columns"),
                                    ],
                                    className="row",
                                ),
                            ],
                        ),
                        # Démographie
                        dcc.Tab(
                            label="Démographie",
                            children=[
                                html.H3("Population Française", className="tab-title"),
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Graph(id="population")],
                                            className="six columns graph-demo",
                                        ),
                                        html.Div(
                                            [dcc.Graph(id="naissances-deces")],
                                            className="six columns graph-demo",
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Graph(id="hommes-femmes")],
                                            className="four columns repartition-graph",
                                        ),
                                        html.Div(
                                            [dcc.Graph(id="age")],
                                            className="four columns repartition-graph",
                                        ),
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="repartition",
                                                    style_data_conditional=[
                                                        {
                                                            "if": {
                                                                "column_id": "label"
                                                            },
                                                            "textAlign": "left",
                                                        }
                                                    ]
                                                    + [
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248,248,248)",
                                                        }
                                                    ],
                                                    style_cell={
                                                        "font-family": "Montserrat"
                                                    },
                                                    style_header={
                                                        "backgroundColor": "rgb(230,230,230)",
                                                        "fontWeight": "bold",
                                                    },
                                                )
                                            ],
                                            className="four columns repartition-table",
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Graph(id="composition-famille")],
                                            className="four columns repartition-graph",
                                        ),
                                        html.Div(
                                            [dcc.Graph(id="statut-marital")],
                                            className="four columns repartition-graph",
                                        ),
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="repartition-famille",
                                                    style_data_conditional=[
                                                        {
                                                            "if": {
                                                                "column_id": "label"
                                                            },
                                                            "textAlign": "left",
                                                        }
                                                    ]
                                                    + [
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248,248,248)",
                                                        }
                                                    ],
                                                    style_cell={
                                                        "font-family": "Montserrat"
                                                    },
                                                    style_header={
                                                        "backgroundColor": "rgb(230,230,230)",
                                                        "fontWeight": "bold",
                                                    },
                                                )
                                            ],
                                            className="four columns repartition-table",
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Br(),
                                # Population etrangere
                                html.H3("Population étrangère", className="tab-title"),
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Graph(id="population-etrangers")],
                                            className="twelve columns graph-demo",
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Graph(id="hommes-femmes-etrangers")],
                                            className="four columns repartition-graph",
                                        ),
                                        html.Div(
                                            [dcc.Graph(id="age-etrangers")],
                                            className="four columns repartition-graph",
                                        ),
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="repartition-etrangers",
                                                    style_data_conditional=[
                                                        {
                                                            "if": {
                                                                "column_id": "label"
                                                            },
                                                            "textAlign": "left",
                                                        }
                                                    ]
                                                    + [
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248,248,248)",
                                                        }
                                                    ],
                                                    style_cell={
                                                        "font-family": "Montserrat"
                                                    },
                                                    style_header={
                                                        "backgroundColor": "rgb(230,230,230)",
                                                        "fontWeight": "bold",
                                                    },
                                                )
                                            ],
                                            className="four columns repartition-table",
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Br(),
                                # Population immigree
                                html.H3("Population immigrée", className="tab-title"),
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Graph(id="population-immigres")],
                                            className="twelve columns graph-demo",
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Graph(id="hommes-femmes-immigres")],
                                            className="four columns repartition-graph",
                                        ),
                                        html.Div(
                                            [dcc.Graph(id="age-immigres")],
                                            className="four columns repartition-graph",
                                        ),
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="repartition-immigres",
                                                    style_data_conditional=[
                                                        {
                                                            "if": {
                                                                "column_id": "label"
                                                            },
                                                            "textAlign": "left",
                                                        }
                                                    ]
                                                    + [
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248,248,248)",
                                                        }
                                                    ],
                                                    style_cell={
                                                        "font-family": "Montserrat"
                                                    },
                                                    style_header={
                                                        "backgroundColor": "rgb(230,230,230)",
                                                        "fontWeight": "bold",
                                                    },
                                                )
                                            ],
                                            className="four columns repartition-table",
                                        ),
                                    ],
                                    className="row",
                                ),
                            ],
                        ),
                        # Santé / Social
                        dcc.Tab(
                            label="Santé et Social",
                            children=[
                                html.Div(
                                    [
                                        html.H3("Santé", className="tab-title"),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [dcc.Graph(id="practiciens")],
                                                    className="six columns",
                                                ),
                                                html.Div(
                                                    [
                                                        dash_table.DataTable(
                                                            id="table-practiciens",
                                                            style_data_conditional=[
                                                                {
                                                                    "if": {
                                                                        "column_id": "label"
                                                                    },
                                                                    "textAlign": "left",
                                                                }
                                                            ]
                                                            + [
                                                                {
                                                                    "if": {
                                                                        "row_index": "odd"
                                                                    },
                                                                    "backgroundColor": "rgb(248,248,248)",
                                                                }
                                                            ],
                                                            style_cell={
                                                                "font-family": "Montserrat"
                                                            },
                                                            style_header={
                                                                "backgroundColor": "rgb(230,230,230)",
                                                                "fontWeight": "bold",
                                                            },
                                                        )
                                                    ],
                                                    className="six columns repartition-table",
                                                ),
                                            ],
                                            className="row",
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [dcc.Graph(id="etablissements")],
                                                    className="six columns",
                                                ),
                                                html.Div(
                                                    [
                                                        dash_table.DataTable(
                                                            id="table-etablissements",
                                                            style_data_conditional=[
                                                                {
                                                                    "if": {
                                                                        "column_id": "label"
                                                                    },
                                                                    "textAlign": "left",
                                                                }
                                                            ]
                                                            + [
                                                                {
                                                                    "if": {
                                                                        "row_index": "odd"
                                                                    },
                                                                    "backgroundColor": "rgb(248,248,248)",
                                                                }
                                                            ],
                                                            style_cell={
                                                                "font-family": "Montserrat"
                                                            },
                                                            style_header={
                                                                "backgroundColor": "rgb(230,230,230)",
                                                                "fontWeight": "bold",
                                                            },
                                                        )
                                                    ],
                                                    className="six columns repartition-table",
                                                ),
                                            ],
                                            className="row",
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H3("Social", className="tab-title"),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [dcc.Graph(id="caf")],
                                                    className="six columns",
                                                ),
                                                html.Div(
                                                    [dcc.Graph(id="rsa")],
                                                    className="six columns",
                                                ),
                                            ],
                                            className="row",
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [dcc.Graph(id="apl")],
                                                    className="six columns",
                                                ),
                                                html.Div(
                                                    [dcc.Graph(id="alloc")],
                                                    className="six columns",
                                                ),
                                            ],
                                            className="row",
                                        ),
                                    ]
                                ),
                            ],
                        ),
                        # Immobilier
                        dcc.Tab(
                            label="Immobilier",
                            children=[
                                html.H3("Immobilier", className="tab-title"),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4("Prix au m²"),
                                                        html.P(
                                                            id="prix-m2",
                                                            className="green immo-data",
                                                        ),
                                                    ],
                                                    className="immo-div",
                                                ),
                                                html.Div(
                                                    [
                                                        html.H4("Moyenne France"),
                                                        html.P(
                                                            id="prix-moyen",
                                                            className="orange immo-data",
                                                        ),
                                                    ],
                                                    className="immo-div",
                                                ),
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            "Informations complémentaires:"
                                                        ),
                                                        html.P(id="nb-logements"),
                                                    ],
                                                    className="immo-div",
                                                ),
                                            ],
                                            className="four columns infos-immo",
                                            style={"paddingTop": "50px"},
                                        ),
                                        html.Div(
                                            [dcc.Graph(id="residences")],
                                            className="four columns repartition-graph",
                                        ),
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="table-immo",
                                                    style_data_conditional=[
                                                        {
                                                            "if": {
                                                                "column_id": "label"
                                                            },
                                                            "textAlign": "left",
                                                        }
                                                    ]
                                                    + [
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248,248,248)",
                                                        }
                                                    ],
                                                    style_cell={
                                                        "font-family": "Montserrat"
                                                    },
                                                    style_header={
                                                        "backgroundColor": "rgb(230,230,230)",
                                                        "fontWeight": "bold",
                                                    },
                                                )
                                            ],
                                            className="four columns repartition-table",
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Graph(id="logements")],
                                            className="four columns",
                                        ),
                                        html.Div(
                                            [dcc.Graph(id="occupants")],
                                            className="four columns",
                                        ),
                                        html.Div(
                                            [dcc.Graph(id="pieces")],
                                            className="four columns",
                                        ),
                                    ],
                                    className="row",
                                ),
                            ],
                        ),
                        # Emploi
                        dcc.Tab(
                            label="Emploi",
                            children=[
                                html.H3("Emploi / Chômage", className="tab-title"),
                                # html.Div(
                                #     [
                                #         html.Div(
                                #             [
                                #                 dcc.Graph(id="evolution-chomage"),
                                #             ],
                                #             className="twelve columns",
                                #         )
                                #     ],
                                #     className="row",
                                # ),
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Graph(id="emploi-hf")],
                                            className="six columns",
                                        ),
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="table-emploi-hf",
                                                    style_data_conditional=[
                                                        {
                                                            "if": {
                                                                "column_id": "label"
                                                            },
                                                            "textAlign": "left",
                                                        }
                                                    ]
                                                    + [
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248,248,248)",
                                                        }
                                                    ],
                                                    style_cell={
                                                        "font-family": "Montserrat"
                                                    },
                                                    style_header={
                                                        "backgroundColor": "rgb(230,230,230)",
                                                        "fontWeight": "bold",
                                                    },
                                                )
                                            ],
                                            className="six columns repartition-table",
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Graph(id="emploi-age")],
                                            className="six columns",
                                        ),
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="table-emploi-age",
                                                    style_data_conditional=[
                                                        {
                                                            "if": {
                                                                "column_id": "label"
                                                            },
                                                            "textAlign": "left",
                                                        }
                                                    ]
                                                    + [
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248,248,248)",
                                                        }
                                                    ],
                                                    style_cell={
                                                        "font-family": "Montserrat"
                                                    },
                                                    style_header={
                                                        "backgroundColor": "rgb(230,230,230)",
                                                        "fontWeight": "bold",
                                                    },
                                                )
                                            ],
                                            className="six columns repartition-table",
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Graph(id="inactifs")],
                                            className="six columns",
                                        ),
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="table-inactifs",
                                                    style_data_conditional=[
                                                        {
                                                            "if": {
                                                                "column_id": "label"
                                                            },
                                                            "textAlign": "left",
                                                        }
                                                    ]
                                                    + [
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248,248,248)",
                                                        }
                                                    ],
                                                    style_cell={
                                                        "font-family": "Montserrat"
                                                    },
                                                    style_header={
                                                        "backgroundColor": "rgb(230,230,230)",
                                                        "fontWeight": "bold",
                                                    },
                                                )
                                            ],
                                            className="six columns repartition-table",
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Graph(id="salaries")],
                                            className="six columns",
                                        ),
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="table-salaries",
                                                    style_data_conditional=[
                                                        {
                                                            "if": {
                                                                "column_id": "label"
                                                            },
                                                            "textAlign": "left",
                                                        }
                                                    ]
                                                    + [
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248,248,248)",
                                                        }
                                                    ],
                                                    style_cell={
                                                        "font-family": "Montserrat"
                                                    },
                                                    style_header={
                                                        "backgroundColor": "rgb(230,230,230)",
                                                        "fontWeight": "bold",
                                                    },
                                                )
                                            ],
                                            className="six columns repartition-table",
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Graph(id="temps-partiel-hf")],
                                            className="four columns",
                                        ),
                                        html.Div(
                                            [dcc.Graph(id="temps-partiel-age")],
                                            className="four columns",
                                        ),
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="table-temps-partiel",
                                                    style_data_conditional=[
                                                        {
                                                            "if": {
                                                                "column_id": "label"
                                                            },
                                                            "textAlign": "left",
                                                        }
                                                    ]
                                                    + [
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248,248,248)",
                                                        }
                                                    ],
                                                    style_cell={
                                                        "font-family": "Montserrat"
                                                    },
                                                    style_header={
                                                        "backgroundColor": "rgb(230,230,230)",
                                                        "fontWeight": "bold",
                                                    },
                                                )
                                            ],
                                            className="four columns repartition-table",
                                        ),
                                    ],
                                    className="row",
                                ),
                            ],
                        ),
                        # Salaires
                        dcc.Tab(
                            label="Salaires",
                            children=[
                                html.H3("Salaires", className="tab-title"),
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Graph(id="salaires")],
                                            className="six columns",
                                        ),
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="table-salaires",
                                                    style_data_conditional=[
                                                        {
                                                            "if": {
                                                                "column_id": "label"
                                                            },
                                                            "textAlign": "left",
                                                        }
                                                    ]
                                                    + [
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248,248,248)",
                                                        }
                                                    ],
                                                    style_cell={
                                                        "font-family": "Montserrat"
                                                    },
                                                    style_header={
                                                        "backgroundColor": "rgb(230,230,230)",
                                                        "fontWeight": "bold",
                                                    },
                                                )
                                            ],
                                            className="six columns repartition-table",
                                        ),
                                    ],
                                    className="row",
                                ),
                            ],
                        ),
                        # Catégories socioprofessionnelles
                        dcc.Tab(
                            label="CSP",
                            children=[
                                html.H3(
                                    "Catégories socioprofessionnelles",
                                    className="tab-title",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [dcc.Graph(id="niveau-diplome")],
                                            className="six columns",
                                        ),
                                        html.Div(
                                            [dcc.Graph(id="diplome-hf")],
                                            className="six columns",
                                        ),
                                    ],
                                    className="row",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="table-csp",
                                                    style_data_conditional=[
                                                        {
                                                            "if": {
                                                                "column_id": "label"
                                                            },
                                                            "textAlign": "left",
                                                        }
                                                    ]
                                                    + [
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248,248,248)",
                                                        }
                                                    ],
                                                    style_cell={
                                                        "font-family": "Montserrat"
                                                    },
                                                    style_header={
                                                        "backgroundColor": "rgb(230,230,230)",
                                                        "fontWeight": "bold",
                                                    },
                                                )
                                            ],
                                            className="six columns repartition-table",
                                        ),
                                        html.Div(
                                            [dcc.Graph(id="csp")],
                                            className="six columns",
                                        ),
                                    ],
                                    className="row",
                                ),
                            ],
                        ),
                        # Automobile
                        dcc.Tab(
                            label="Automobile",
                            children=[
                                html.H3(
                                    "Automobile / Accidents de la route",
                                    className="tab-title",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.H4("Nombre de voitures"),
                                                        html.P(
                                                            id="total-voitures",
                                                            className="green immo-data",
                                                        ),
                                                    ],
                                                    className="immo-div",
                                                ),
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            "Nombre total d'accidents"
                                                        ),
                                                        html.P(
                                                            id="total-accidents",
                                                            className="orange immo-data",
                                                        ),
                                                    ],
                                                    className="immo-div",
                                                ),
                                                html.Div(
                                                    [
                                                        html.H4(
                                                            "Ménages avec place(s) de stationnement"
                                                        ),
                                                        html.P(id="total-places"),
                                                    ],
                                                    className="immo-div",
                                                ),
                                            ],
                                            className="four columns infos-immo",
                                            style={"paddingTop": "50px"},
                                        ),
                                        html.Div(
                                            [dcc.Graph(id="voitures-menage")],
                                            className="four columns",
                                        ),
                                        html.Div(
                                            [dcc.Graph(id="accidents")],
                                            className="four columns",
                                        ),
                                    ],
                                    className="row",
                                ),
                            ],
                        ),
                        # Délinquance
                        dcc.Tab(
                            label="Délinquance",
                            children=[
                                html.H3("Délinquance", className="tab-title"),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dash_table.DataTable(
                                                    id="table-delinquance",
                                                    style_data_conditional=[
                                                        {
                                                            "if": {
                                                                "column_id": "label"
                                                            },
                                                            "textAlign": "left",
                                                        }
                                                    ]
                                                    + [
                                                        {
                                                            "if": {"row_index": "odd"},
                                                            "backgroundColor": "rgb(248,248,248)",
                                                        }
                                                    ],
                                                    style_cell={
                                                        "font-family": "Montserrat"
                                                    },
                                                    style_header={
                                                        "backgroundColor": "rgb(230,230,230)",
                                                        "fontWeight": "bold",
                                                    },
                                                )
                                            ],
                                            className="six columns repartition-table",
                                        ),
                                        html.Div(
                                            [
                                                dcc.Graph(id="crimes"),
                                                dcc.Graph(id="agressions"),
                                                dcc.Graph(id="vols"),
                                            ],
                                            className="six columns",
                                        ),
                                    ],
                                    className="row",
                                ),
                            ],
                        ),
                    ],
                )
            ]
        ),
    ]
)

## Infos Générales ##

# Afficher infos
@app.callback(
    [Output("table-infos", "data"), Output("table-infos", "columns")],
    [Input("dropdown-ville", "value")],
)
def update_infos(ville):
    cols = df_infos.columns
    cols_off = [
        "ville",
        "lien",
        "Etablissement public de coopération intercommunale (EPCI)",
        "Taux de chômage (2017)",
        "Ville fleurie",
        "Ville d'art et d'histoire",
        "Ville internet",
        "Pavillon bleu",
    ]
    list_infos = [info for info in cols if info not in cols_off]
    infos = {
        "label": list_infos,
        "value": [
            df_infos[df_infos["ville"] == ville][col].iloc[0] for col in list_infos
        ],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = {"id": "label", "name": "  "}, {"id": "value", "name": ville}

    return data, header


# Afficher localisation
@app.callback(Output("map", "children"), [Input("dropdown-ville", "value")])
def update_location(ville):
    longitude = df_infos[df_infos["ville"] == ville]["Longitude"].iloc[0]
    latitude = df_infos[df_infos["ville"] == ville]["Latitude"].iloc[0]

    base_map = folium.Map(location=(latitude, longitude))
    marker = folium.Marker(location=[latitude, longitude])
    marker.add_to(base_map)
    city_map = f"locations/localisation_{ville}.html"

    if not os.path.isfile(city_map):
        base_map.save(city_map)

    return html.Iframe(srcDoc=open(city_map, "r").read(), width="100%", height="600")


## Démographie ##

# Population
@app.callback(Output("population", "figure"), [Input("dropdown-ville", "value")])
def population_graph(ville):
    x_axis = np.array(range(2006, 2019))
    y_axis = [
        df_demographie[df_demographie["ville"] == ville][
            f"Nombre d'habitants ({str(annee)})"
        ].iloc[0]
        for annee in range(2006, 2019)
    ]

    traces = []
    traces.append(
        go.Scatter(
            x=x_axis,
            y=y_axis,
            mode="lines+markers",
            line={"shape": "spline", "smoothing": 1},
        )
    )

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Evolution de la population à {ville}",
            xaxis={"title": "Annees"},
            yaxis=dict(title="Nombre d'habitants"),
            hovermode="closest",
            legend_orientation="h",
        ),
    }


# Naissances et Décès
@app.callback(Output("naissances-deces", "figure"), [Input("dropdown-ville", "value")])
def naissances_deces_graph(ville):
    x_axis = np.array(range(1999, 2019))
    y_axis_naissances = [
        df_demographie[df_demographie["ville"] == ville][
            f"Nombre de naissances ({str(annee)})"
        ].iloc[0]
        for annee in range(1999, 2019)
    ]
    y_axis_deces = [
        df_demographie[df_demographie["ville"] == ville][
            f"Nombre de décès ({str(annee)})"
        ].iloc[0]
        for annee in range(1999, 2019)
    ]

    ville = ville.split("(")[0]

    traces = [
        go.Scatter(
            x=x_axis,
            y=y_axis_naissances,
            mode="lines+markers",
            line={"shape": "spline", "smoothing": 1},
            name=f"Naissances à {ville}",
        ),
        go.Scatter(
            x=x_axis,
            y=y_axis_deces,
            mode="lines+markers",
            line={"shape": "spline", "smoothing": 1},
            name=f"Décès à {ville}",
        ),
    ]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Evolution des Naissances et Décès à {ville}",
            xaxis={"title": "Annees"},
            yaxis=dict(title="Nombre de naissances et décès"),
            hovermode="closest",
            legend_orientation="h",
        ),
    }


# Répartition Hommes/Femmes
@app.callback(Output("hommes-femmes", "figure"), [Input("dropdown-ville", "value")])
def repartition_hf(ville):
    nb_hommes = df_demographie[df_demographie["ville"] == ville]["Hommes"].iloc[0]
    nb_femmes = df_demographie[df_demographie["ville"] == ville]["Femmes"].iloc[0]

    labels = ["Hommes", "Femmes"]
    values = [nb_hommes, nb_femmes]
    total = sum(values)

    traces = [go.Pie(labels=labels, values=values)]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Répartition Hommes / Femmes<br> (Total: {total})",
            legend_orientation="h",
        ),
    }


# Répartition Age
@app.callback(Output("age", "figure"), [Input("dropdown-ville", "value")])
def repartition_ages(ville):
    cols = [
        "Moins de 15 ans",
        "15 - 29 ans",
        "30 - 44 ans",
        "45 - 59 ans",
        "60 - 74 ans",
        "75 ans et plus",
    ]

    labels = cols
    values = [
        df_demographie[df_demographie["ville"] == ville][col].iloc[0] for col in cols
    ]
    values = [float(val) for val in values]
    total = sum(values)

    traces = [go.Pie(labels=labels, values=values)]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Répartition par tranche d'âge<br> (Total: {total})",
            legend_orientation="h",
        ),
    }


# Répartition
@app.callback(
    [Output("repartition", "data"), Output("repartition", "columns")],
    [Input("dropdown-ville", "value")],
)
def table_repartition(ville):
    cols = [
        "Hommes",
        "Femmes",
        "Moins de 15 ans",
        "15 - 29 ans",
        "30 - 44 ans",
        "45 - 59 ans",
        "60 - 74 ans",
        "75 ans et plus",
    ]

    infos = {
        "label": cols,
        "value": [
            df_demographie[df_demographie["ville"] == ville][col].iloc[0]
            for col in cols
        ],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = [{"id": "label", "name": "Label"}, {"id": "value", "name": ville}]

    return data, header


# Répartition Familles
@app.callback(
    Output("composition-famille", "figure"), [Input("dropdown-ville", "value")]
)
def composition_familles(ville):
    cols = [
        "Familles monoparentales",
        "Couples sans enfant",
        "Couples avec enfant",
        "Familles sans enfant",
        "Familles avec un enfant",
        "Familles avec deux enfants",
        "Familles avec trois enfants",
        "Familles avec quatre enfants ou plus",
    ]

    labels = cols
    values = [
        df_demographie[df_demographie["ville"] == ville][col].iloc[0] for col in cols
    ]
    values = [val for val in values]
    total = sum(values)

    traces = [go.Pie(labels=labels, values=values)]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Composition des familles<br> (Total: {total})",
            legend_orientation="h",
        ),
    }


# Statut Marital
@app.callback(Output("statut-marital", "figure"), [Input("dropdown-ville", "value")])
def statut_marital(ville):
    cols = [
        "Personnes célibataires",
        "Personnes mariées",
        "Personnes divorcées",
        "Personnes veuves",
        "Personnes en concubinage",
        "Personnes pacsées",
    ]

    labels = cols
    values = [
        df_demographie[df_demographie["ville"] == ville][col].iloc[0] for col in cols
    ]
    values = [val for val in values]
    total = sum(values)

    traces = [go.Pie(labels=labels, values=values)]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Statut marital<br> (Total: {total})",
            legend_orientation="h",
        ),
    }


# Table
@app.callback(
    [Output("repartition-famille", "data"), Output("repartition-famille", "columns")],
    [Input("dropdown-ville", "value")],
)
def table_repartition_famille(ville):
    cols = [
        "Familles monoparentales",
        "Couples sans enfant",
        "Couples avec enfant",
        "Familles sans enfant",
        "Familles avec un enfant",
        "Familles avec deux enfants",
        "Familles avec trois enfants",
        "Familles avec quatre enfants ou plus",
    ]

    infos = {
        "label": cols,
        "value": [
            df_demographie[df_demographie["ville"] == ville][col].iloc[0]
            for col in cols
        ],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = [{"id": "label", "name": "Label"}, {"id": "value", "name": ville}]

    return data, header


### Etrangers ###

# Population
@app.callback(
    Output("population-etrangers", "figure"), [Input("dropdown-ville", "value")]
)
def population_etrangers_graph(ville):
    x_axis = np.array(range(2006, 2018))
    y_axis = [
        df_demographie[df_demographie["ville"] == ville][
            f"Nombre d'étrangers ({str(annee)})"
        ].iloc[0]
        for annee in range(2006, 2018)
    ]

    traces = []
    traces.append(
        go.Scatter(
            x=x_axis,
            y=y_axis,
            mode="lines+markers",
            line={"shape": "spline", "smoothing": 1},
        )
    )

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Evolution de la population étrangère à {ville}",
            xaxis={"title": "Annees"},
            yaxis=dict(title="Nombre d'étrangers"),
            hovermode="closest",
            legend_orientation="h",
        ),
    }


# Répartition Hommes/Femmes
@app.callback(
    Output("hommes-femmes-etrangers", "figure"), [Input("dropdown-ville", "value")]
)
def repartition_hf_etrangers(ville):
    nb_hommes = df_demographie[df_demographie["ville"] == ville][
        "Hommes étrangers"
    ].iloc[0]
    nb_femmes = df_demographie[df_demographie["ville"] == ville][
        "Femmes étrangères"
    ].iloc[0]

    labels = ["Hommes étrangers", "Femmes étrangères"]
    values = [nb_hommes, nb_femmes]
    total = sum(values)

    traces = [go.Pie(labels=labels, values=values)]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Répartition Hommes / Femmes<br> (Total: {total})",
            legend_orientation="h",
        ),
    }


# Répartition Age
@app.callback(Output("age-etrangers", "figure"), [Input("dropdown-ville", "value")])
def repartition_ages_etrangers(ville):
    cols = [
        "Moins de 15 ans étrangers",
        "15-24 ans étrangers",
        "25-54 ans étrangers",
        "55 ans et plus étrangers",
    ]

    labels = cols
    values = [
        df_demographie[df_demographie["ville"] == ville][col].iloc[0] for col in cols
    ]
    values = [float(val) for val in values]
    total = sum(values)

    traces = [go.Pie(labels=labels, values=values)]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Répartition par tranche d'âge<br> (Total: {total})",
            legend_orientation="h",
        ),
    }


# Répartition
@app.callback(
    [
        Output("repartition-etrangers", "data"),
        Output("repartition-etrangers", "columns"),
    ],
    [Input("dropdown-ville", "value")],
)
def table_repartition_etrangers(ville):
    cols = [
        "Hommes étrangers",
        "Femmes étrangères",
        "Moins de 15 ans étrangers",
        "15-24 ans étrangers",
        "25-54 ans étrangers",
        "55 ans et plus étrangers",
    ]

    infos = {
        "label": cols,
        "value": [
            df_demographie[df_demographie["ville"] == ville][col].iloc[0]
            for col in cols
        ],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = [{"id": "label", "name": ""}, {"id": "value", "name": ville}]

    return data, header


### Immigree ###

# Population
@app.callback(
    Output("population-immigres", "figure"), [Input("dropdown-ville", "value")]
)
def population_immigree_graph(ville):
    x_axis = np.array(range(2006, 2018))
    y_axis = [
        df_demographie[df_demographie["ville"] == ville][
            f"Nombre d'immigrés ({str(annee)})"
        ].iloc[0]
        for annee in range(2006, 2018)
    ]

    traces = []
    traces.append(
        go.Scatter(
            x=x_axis,
            y=y_axis,
            mode="lines+markers",
            line={"shape": "spline", "smoothing": 1},
        )
    )

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Evolution de la population immigrée à {ville}",
            xaxis={"title": "Annees"},
            yaxis=dict(title="Nombre d'immigrés"),
            hovermode="closest",
            legend_orientation="h",
        ),
    }


# Répartition Hommes/Femmes
@app.callback(
    Output("hommes-femmes-immigres", "figure"), [Input("dropdown-ville", "value")]
)
def repartition_hf_immigres(ville):
    nb_hommes = df_demographie[df_demographie["ville"] == ville][
        "Hommes immigrés"
    ].iloc[0]
    nb_femmes = df_demographie[df_demographie["ville"] == ville][
        "Femmes immigrées"
    ].iloc[0]

    labels = ["Hommes immigrés", "Femmes immigrées"]
    values = [nb_hommes, nb_femmes]
    total = sum(values)

    traces = [go.Pie(labels=labels, values=values)]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Répartition Hommes / Femmes<br> (Total: {total})",
            legend_orientation="h",
        ),
    }


# Répartition Age
@app.callback(Output("age-immigres", "figure"), [Input("dropdown-ville", "value")])
def repartition_ages_immigres(ville):
    cols = [
        "Moins de 15 ans immigrés",
        "15-24 ans immigrés",
        "25-54 ans immigrés",
        "55 ans et plus immigrés",
    ]

    labels = cols
    values = [
        df_demographie[df_demographie["ville"] == ville][col].iloc[0] for col in cols
    ]
    values = [float(val) for val in values]
    total = sum(values)

    traces = [go.Pie(labels=labels, values=values)]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Répartition par tranche d'âge<br> (Total: {total})",
            legend_orientation="h",
        ),
    }


# Répartition
@app.callback(
    [
        Output("repartition-immigres", "data"),
        Output("repartition-immigres", "columns"),
    ],
    [Input("dropdown-ville", "value")],
)
def table_repartition_immigres(ville):
    cols = [
        "Hommes immigrés",
        "Femmes immigrées",
        "Moins de 15 ans immigrés",
        "15-24 ans immigrés",
        "25-54 ans immigrés",
        "55 ans et plus immigrés",
    ]

    infos = {
        "label": cols,
        "value": [
            df_demographie[df_demographie["ville"] == ville][col].iloc[0]
            for col in cols
        ],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = [{"id": "label", "name": ""}, {"id": "value", "name": ville}]

    return data, header


## Santé / Social ##

# Sante
@app.callback(Output("practiciens", "figure"), [Input("dropdown-ville", "value")])
def practiciens(ville):
    cols = [
        "Médecins généralistes",
        "Masseurs-kinésithérapeutes",
        "Infirmiers",
        "Spécialistes ORL",
        "Ophtalmologistes",
        "Dermatologues",
        "Sage-femmes",
        "Pédiatres",
        "Gynécologues",
    ]

    labels = cols
    values = [
        df_sante_social[df_sante_social["ville"] == ville][col].iloc[0] for col in cols
    ]
    total = sum(values)

    trace = [go.Pie(labels=labels, values=values)]

    return {
        "data": trace,
        "layout": go.Layout(
            title=f"Practiciens à {ville.split('(')[0].strip()}<br> (Total: {str(total)})",
        ),
    }


@app.callback(Output("etablissements", "figure"), [Input("dropdown-ville", "value")])
def etablissements(ville):
    cols = [
        "Etablissements de santé de court séjour",
        "Etablissements de santé de moyen séjour",
        "Etablissements de santé de long séjour",
        "Etablissement d'accueil du jeune enfant",
        "Maisons de retraite",
        "Etablissements pour enfants handicapés",
        "Etablissements pour adultes handicapés",
    ]

    labels = cols
    values = [
        df_sante_social[df_sante_social["ville"] == ville][col].iloc[0] for col in cols
    ]
    total = sum(values)

    trace = [go.Pie(labels=labels, values=values)]

    return {
        "data": trace,
        "layout": go.Layout(
            title=f"Etablissements à {ville.split('(')[0].strip()}<br> (Total: {str(total)})",
        ),
    }


@app.callback(
    [Output("table-practiciens", "data"), Output("table-practiciens", "columns")],
    [Input("dropdown-ville", "value")],
)
def table_praticiens(ville):
    cols = [
        "Médecins généralistes",
        "Masseurs-kinésithérapeutes",
        "Infirmiers",
        "Spécialistes ORL",
        "Ophtalmologistes",
        "Dermatologues",
        "Sage-femmes",
        "Pédiatres",
        "Gynécologues",
    ]

    infos = {
        "label": cols,
        "value": [
            df_sante_social[df_sante_social["ville"] == ville][col].iloc[0]
            for col in cols
        ],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = [{"id": "label", "name": ""}, {"id": "value", "name": ville}]

    return data, header


@app.callback(
    [Output("table-etablissements", "data"), Output("table-etablissements", "columns")],
    [Input("dropdown-ville", "value")],
)
def table_etablissements(ville):
    cols = [
        "Etablissements de santé de court séjour",
        "Etablissements de santé de moyen séjour",
        "Etablissements de santé de long séjour",
        "Etablissement d'accueil du jeune enfant",
        "Maisons de retraite",
        "Etablissements pour enfants handicapés",
        "Etablissements pour adultes handicapés",
    ]

    infos = {
        "label": cols,
        "value": [
            df_sante_social[df_sante_social["ville"] == ville][col].iloc[0]
            for col in cols
        ],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = [{"id": "label", "name": ""}, {"id": "value", "name": ville}]

    return data, header


# Social
@app.callback(
    [
        Output("caf", "figure"),
        Output("rsa", "figure"),
        Output("apl", "figure"),
        Output("alloc", "figure"),
    ],
    [Input("dropdown-ville", "value")],
)
def presta_sociales(ville):
    x_axis = np.array(range(2009, 2018))
    y_caf = [
        df_sante_social[df_sante_social["ville"] == ville][
            f"Nombre d'allocataires CAF ({str(annee)})"
        ].iloc[0]
        for annee in range(2009, 2018)
    ]
    y_rsa = [
        df_sante_social[df_sante_social["ville"] == ville][
            f"Nombre de bénéficiaires RSA ({str(annee)})"
        ].iloc[0]
        for annee in range(2011, 2018)
    ]
    y_apl = [
        df_sante_social[df_sante_social["ville"] == ville][
            f"Nombre de bénéficiaires APL ({str(annee)})"
        ].iloc[0]
        for annee in range(2009, 2018)
    ]
    y_alloc = [
        df_sante_social[df_sante_social["ville"] == ville][
            f"Nombre de bénéficiaires des allocations familiales ({str(annee)})"
        ].iloc[0]
        for annee in range(2009, 2019)
    ]

    trace_caf = [
        go.Scatter(
            x=x_axis,
            y=y_caf,
            mode="lines+markers",
            line={"shape": "spline", "smoothing": 1},
        )
    ]

    trace_rsa = [
        go.Scatter(
            x=x_axis,
            y=y_rsa,
            mode="lines+markers",
            line={"shape": "spline", "smoothing": 1},
        )
    ]

    trace_apl = [
        go.Scatter(
            x=x_axis,
            y=y_apl,
            mode="lines+markers",
            line={"shape": "spline", "smoothing": 1},
        )
    ]

    trace_alloc = [
        go.Scatter(
            x=x_axis,
            y=y_alloc,
            mode="lines+markers",
            line={"shape": "spline", "smoothing": 1},
        )
    ]

    fig_caf = {
        "data": trace_caf,
        "layout": go.Layout(
            title=f"Evolution du nombre d'allocataires CAF à {ville.split('(')[0]}",
            xaxis=dict(title="Annees"),
            yaxis=dict(title="Nombre de bénéficiaires"),
            hovermode="closest",
        ),
    }

    fig_rsa = {
        "data": trace_rsa,
        "layout": go.Layout(
            title=f"Evolution du nombre de bénéficiaires du RSA à {ville.split('(')[0]}",
            xaxis=dict(title="Annees"),
            yaxis=dict(title="Nombre de bénéficiaires"),
            hovermode="closest",
        ),
    }

    fig_apl = {
        "data": trace_apl,
        "layout": go.Layout(
            title=f"Evolution du nombre de bénéficiaires des APL à {ville.split('(')[0]}",
            xaxis=dict(title="Annees"),
            yaxis=dict(title="Nombre de bénéficiaires"),
            hovermode="closest",
        ),
    }

    fig_alloc = {
        "data": trace_alloc,
        "layout": go.Layout(
            title=f"Evolution du nombre de bénéficiaires des allocations familiales à {ville.split('(')[0]}",
            xaxis=dict(title="Annees"),
            yaxis=dict(title="Nombre de bénéficiaires"),
            hovermode="closest",
        ),
    }

    return fig_caf, fig_rsa, fig_apl, fig_alloc


## Immobilier ##


@app.callback(
    [
        Output("prix-m2", "children"),
        Output("prix-moyen", "children"),
        Output("nb-logements", "children"),
    ],
    [Input("dropdown-ville", "value")],
)
def infos_immo(ville):
    prix_m2 = int(df_immo[df_immo["ville"] == ville]["prix_m2"].iloc[0])
    prix_moyen = round(df_immo["prix_m2"].mean(), 2)
    nb_logements = int(
        df_immo[df_immo["ville"] == ville]["Nombre de logements"].iloc[0]
    )

    prix_moyen = f"{str(prix_moyen)} €"
    prix_m2 = f"{str(prix_m2)} €/m2"
    nb_logements = f"Nombre de logements : {str(nb_logements)}"
    return prix_m2, prix_moyen, nb_logements


@app.callback(
    [
        Output("residences", "figure"),
        Output("logements", "figure"),
        Output("occupants", "figure"),
        Output("pieces", "figure"),
    ],
    [Input("dropdown-ville", "value")],
)
def immobilier(ville):

    # Types de résidences
    labels = [
        "Résidences principales",
        "Résidences secondaires",
        "Logements vacants",
    ]
    values = [df_immo[df_immo["ville"] == ville][col].iloc[0] for col in labels]
    total = sum(values)

    trace_residences = [go.Pie(labels=labels, values=values)]

    fig_residences = {
        "data": trace_residences,
        "layout": go.Layout(
            title=f"Types de résidences à {ville.split('(')[0].strip()}<br> (Total: {str(total)})",
        ),
    }

    # Logements
    labels = [
        "Maisons",
        "Appartements",
        "Autres types de logements",
    ]
    values = [df_immo[df_immo["ville"] == ville][col].iloc[0] for col in labels]
    total = sum(values)

    trace_logements = [go.Pie(labels=labels, values=values)]

    fig_logements = {
        "data": trace_logements,
        "layout": go.Layout(
            title=f"Types de logements à {ville.split('(')[0].strip()}<br> (Total: {str(total)})",
        ),
    }

    # Occupants
    labels = [
        "Propriétaires",
        "Locataires",
        "Locataires hébergés à titre gratuit",
    ]
    values = [df_immo[df_immo["ville"] == ville][col].iloc[0] for col in labels]
    total = sum(values)

    trace_occupants = [go.Pie(labels=labels, values=values)]

    fig_occupants = {
        "data": trace_occupants,
        "layout": go.Layout(
            title=f"Logements par types d'occupants à {ville.split('(')[0].strip()}<br> (Total: {str(total)})",
        ),
    }

    # Pieces
    labels = [
        "Studios",
        "2 pièces",
        "3 pièces",
        "4 pièces",
        "5 pièces et plus",
    ]
    values = [df_immo[df_immo["ville"] == ville][col].iloc[0] for col in labels]
    total = sum(values)

    trace_pieces = [go.Pie(labels=labels, values=values)]

    fig_pieces = {
        "data": trace_pieces,
        "layout": go.Layout(
            title=f"Nombre de pièces des logements principaux à {ville.split('(')[0].strip()}<br> (Total: {str(total)})",
        ),
    }

    return fig_residences, fig_logements, fig_occupants, fig_pieces


@app.callback(
    [Output("table-immo", "data"), Output("table-immo", "columns")],
    [Input("dropdown-ville", "value")],
)
def table_immobilier(ville):
    cols = [
        "Résidences principales",
        "Résidences secondaires",
        "Logements vacants",
        "Maisons",
        "Appartements",
        "Autres types de logements",
        "Propriétaires",
        "Locataires",
        "Locataires hébergés à titre gratuit",
        "Studios",
        "2 pièces",
        "3 pièces",
        "4 pièces",
        "5 pièces et plus",
    ]

    infos = {
        "label": cols,
        "value": [df_immo[df_immo["ville"] == ville][col].iloc[0] for col in cols],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = [{"id": "label", "name": ""}, {"id": "value", "name": ville}]

    return data, header


## Emploi ##

# Emploi Hommes/Femmes
@app.callback(Output("emploi-hf", "figure"), [Input("dropdown-ville", "value")])
def emploi_hf(ville):
    labels_h = [
        "Part des actifs hommes (%)",
        "Taux d'activité hommes (%)",
        "Taux d'emploi hommes (%)",
        "Taux de chômage hommes (%)",
    ]
    labels_f = [
        "Part des actifs femmes (%)",
        "Taux d'activité femmes (%)",
        "Taux d'emploi femmes (%)",
        "Taux de chômage femmes (%)",
    ]

    traces = [
        go.Bar(
            x=[
                "Part des actifs",
                "Taux d'activité",
                "Taux d'emploi",
                "Taux de chômage",
            ],
            y=[df_emploi[df_emploi["ville"] == ville][col].iloc[0] for col in labels_h],
            name="Hommes",
        ),
        go.Bar(
            x=[
                "Part des actifs",
                "Taux d'activité",
                "Taux d'emploi",
                "Taux de chômage",
            ],
            y=[df_emploi[df_emploi["ville"] == ville][col].iloc[0] for col in labels_f],
            name="Femmes",
        ),
    ]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Emploi, activité et chômage<br> à {ville.split('(')[0].strip()}",
        ),
    }


@app.callback(
    [Output("table-emploi-hf", "data"), Output("table-emploi-hf", "columns")],
    [Input("dropdown-ville", "value")],
)
def table_emploi_hf(ville):
    cols = [
        "Actifs en emploi",
        "Chômeurs",
        "Inactifs",
        "Part des actifs femmes (%)",
        "Part des actifs hommes (%)",
        "Taux d'activité femmes (%)",
        "Taux d'activité hommes (%)",
        "Taux d'emploi femmes (%)",
        "Taux d'emploi hommes (%)",
        "Taux de chômage femmes (%)",
        "Taux de chômage hommes (%)",
    ]

    infos = {
        "label": cols,
        "value": [df_emploi[df_emploi["ville"] == ville][col].iloc[0] for col in cols],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = [{"id": "label", "name": ""}, {"id": "value", "name": ville}]

    return data, header


# Emploi Age
@app.callback(Output("emploi-age", "figure"), [Input("dropdown-ville", "value")])
def emploi_age(ville):
    labels_15_24 = [
        "Part des actifs 15-24 ans (%)",
        "Taux d'emploi 15-24 ans (%)",
        "Taux de chômage 15-24 ans (%)",
    ]
    labels_25_54 = [
        "Part des actifs 25-54 ans (%)",
        "Taux d'emploi 25-54 ans (%)",
        "Taux de chômage 25-54 ans (%)",
    ]
    labels_55_64 = [
        "Part des actifs 55-64 ans (%)",
        "Taux d'emploi 55-64 ans (%)",
        "Taux de chômage 55-64 ans (%)",
    ]

    traces = [
        go.Bar(
            x=[
                "Part des actifs",
                "Taux d'emploi",
                "Taux de chômage",
            ],
            y=[
                df_emploi[df_emploi["ville"] == ville][col].iloc[0]
                for col in labels_15_24
            ],
            name="15-24 ans",
        ),
        go.Bar(
            x=[
                "Part des actifs",
                "Taux d'emploi",
                "Taux de chômage",
            ],
            y=[
                df_emploi[df_emploi["ville"] == ville][col].iloc[0]
                for col in labels_25_54
            ],
            name="25-54 ans",
        ),
        go.Bar(
            x=[
                "Part des actifs",
                "Taux d'emploi",
                "Taux de chômage",
            ],
            y=[
                df_emploi[df_emploi["ville"] == ville][col].iloc[0]
                for col in labels_55_64
            ],
            name="55-64 ans",
        ),
    ]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Activité et emploi <br> selon l'âge (%) à {ville.split('(')[0].strip()}",
        ),
    }


@app.callback(
    [Output("table-emploi-age", "data"), Output("table-emploi-age", "columns")],
    [Input("dropdown-ville", "value")],
)
def table_emploi_age(ville):
    cols = [
        "Part des actifs 15-24 ans (%)",
        "Part des actifs 25-54 ans (%)",
        "Part des actifs 55-64 ans (%)",
        "Taux d'emploi 15-24 ans (%)",
        "Taux d'emploi 25-54 ans (%)",
        "Taux d'emploi 55-64 ans (%)",
        "Taux de chômage 15-24 ans (%)",
        "Taux de chômage 25-54 ans (%)",
        "Taux de chômage 55-64 ans (%)",
    ]

    infos = {
        "label": cols,
        "value": [df_emploi[df_emploi["ville"] == ville][col].iloc[0] for col in cols],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = [{"id": "label", "name": ""}, {"id": "value", "name": ville}]

    return data, header


@app.callback(Output("inactifs", "figure"), [Input("dropdown-ville", "value")])
def inactifs(ville):
    labels = [
        "Autres personnes sans activité de 15-64 ans",
        "Retraités et pré-retraités de 15-64 ans",
        "Stagiaires et étudiants de 15-64 ans",
    ]
    values = [df_emploi[df_emploi["ville"] == ville][col].iloc[0] for col in labels]
    total = sum(values)

    traces = [go.Pie(labels=labels, values=values)]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Retraités, étudiants et autres inactifs à {ville.split('(')[0].strip()}<br> (Total: {total})",
        ),
    }


@app.callback(
    [Output("table-inactifs", "data"), Output("table-inactifs", "columns")],
    [Input("dropdown-ville", "value")],
)
def table_inactifs(ville):
    cols = [
        "Autres personnes sans activité de 15-64 ans",
        "Retraités et pré-retraités de 15-64 ans",
        "Stagiaires et étudiants de 15-64 ans",
    ]

    infos = {
        "label": cols,
        "value": [df_emploi[df_emploi["ville"] == ville][col].iloc[0] for col in cols],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = [{"id": "label", "name": ""}, {"id": "value", "name": ville}]

    return data, header


@app.callback(Output("salaries", "figure"), [Input("dropdown-ville", "value")])
def salaries(ville):
    labels = [
        "CDD",
        "CDI et fonction publique",
        "Emplois aidés",
        "Intérimaires",
        "Salariés",
        "Stages et apprentissages",
    ]

    values = [df_emploi[df_emploi["ville"] == ville][col].iloc[0] for col in labels]
    total = sum(values)

    traces = [go.Pie(labels=labels, values=values)]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Salariés à {ville.split('(')[0].strip()}<br> (Total: {total})",
        ),
    }


@app.callback(
    [Output("table-salaries", "data"), Output("table-salaries", "columns")],
    [Input("dropdown-ville", "value")],
)
def table_salaries(ville):
    cols = [
        "CDD",
        "CDI et fonction publique",
        "Emplois aidés",
        "Intérimaires",
        "Salariés",
        "Stages et apprentissages",
    ]

    infos = {
        "label": cols,
        "value": [df_emploi[df_emploi["ville"] == ville][col].iloc[0] for col in cols],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = [{"id": "label", "name": ""}, {"id": "value", "name": ville}]

    return data, header


@app.callback(Output("temps-partiel-hf", "figure"), [Input("dropdown-ville", "value")])
def temps_partiel_hf(ville):
    labels = [
        "Hommes à temps partiel",
        "Femmes à temps partiel",
    ]

    values = [df_emploi[df_emploi["ville"] == ville][col].iloc[0] for col in labels]
    total = sum(values)

    traces = [go.Pie(labels=labels, values=values)]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Salariés H/F à temps partiel<br> (Total: {total})",
        ),
    }


@app.callback(Output("temps-partiel-age", "figure"), [Input("dropdown-ville", "value")])
def temps_partiel_age(ville):
    labels = [
        "Les 15 à 24 ans à temps partiel",
        "Les 25 à 54 ans à temps partiel",
        "Les 55 à 64 ans à temps partiel",
    ]

    values = [df_emploi[df_emploi["ville"] == ville][col].iloc[0] for col in labels]
    total = sum(values)

    traces = [go.Pie(labels=labels, values=values)]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Salariés à temps partiel par âge<br> (Total: {total})",
        ),
    }


@app.callback(
    [Output("table-temps-partiel", "data"), Output("table-temps-partiel", "columns")],
    [Input("dropdown-ville", "value")],
)
def table_temps_partiel(ville):
    cols = [
        "Salariés à temps partiel",
        "Hommes à temps partiel",
        "Femmes à temps partiel",
        "Les 15 à 24 ans à temps partiel",
        "Les 25 à 54 ans à temps partiel",
        "Les 55 à 64 ans à temps partiel",
    ]

    infos = {
        "label": cols,
        "value": [df_emploi[df_emploi["ville"] == ville][col].iloc[0] for col in cols],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = [{"id": "label", "name": ""}, {"id": "value", "name": ville}]

    return data, header


## Salaires ##

# Evolution des salaires
@app.callback(Output("salaires", "figure"), [Input("dropdown-ville", "value")])
def salaires(ville):
    x_axis = np.array(range(2006, 2018))
    y_axis = [
        df_salaire[df_salaire["ville"] == ville][str(annee)].iloc[0]
        for annee in range(2006, 2018)
    ]
    y_mean = [df_salaire[str(annee)].mean() for annee in range(2006, 2018)]

    traces = [
        go.Scatter(
            x=x_axis,
            y=y_axis,
            mode="lines+markers",
            line={"shape": "spline", "smoothing": 1},
            name=f"Salaire moyen de {ville.split('(')[0].strip()}",
        ),
        go.Scatter(
            x=x_axis,
            y=y_mean,
            mode="lines+markers",
            line={"shape": "spline", "smoothing": 1},
            name="Moyenne France",
        ),
    ]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Evolution des salaires à {ville}",
            xaxis={"title": "Annees"},
            yaxis=dict(title="Montant/mois (€)"),
            hovermode="closest",
            legend_orientation="h",
        ),
    }


@app.callback(
    [Output("table-salaires", "data"), Output("table-salaires", "columns")],
    [Input("dropdown-ville", "value")],
)
def table_salaires(ville):
    cols = [
        "Salaire moyen des cadres",
        "Salaire moyen des professions intermédiaires",
        "Salaire moyen des employés",
        "Salaire moyen des ouvriers",
        "Salaire moyen des femmes",
        "Salaire moyen des hommes",
        "Salaire moyen des moins de 26 ans",
        "Salaire moyen des 26-49 ans",
        "Salaire moyen des 50 ans et plus",
        "Revenu mensuel moyen par foyer fiscal",
        "Nombre de foyers fiscaux",
    ]

    infos = {
        "label": cols,
        "value": [
            df_salaire[df_salaire["ville"] == ville][col].iloc[0] for col in cols
        ],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = [{"id": "label", "name": ""}, {"id": "value", "name": ville}]

    return data, header


## CSP ##


@app.callback(Output("niveau-diplome", "figure"), [Input("dropdown-ville", "value")])
def niveau_diplome(ville):
    labels = [
        "Aucun diplôme",
        "CAP / BEP ",
        "Baccalauréat / brevet professionnel",
        "De Bac +2 à Bac +4",
        "Bac +5 et plus",
    ]

    values = [df_csp[df_csp["ville"] == ville][col].iloc[0] for col in labels]
    total = sum(values)

    trace = [go.Pie(labels=labels, values=values)]

    return {
        "data": trace,
        "layout": go.Layout(
            title=f"Niveau de diplôme à {ville.split('(')[0].strip()}<br>(Total: {total})"
        ),
    }


# CSP Hommes/Femmes
@app.callback(Output("diplome-hf", "figure"), [Input("dropdown-ville", "value")])
def diplome_hf(ville):
    labels_h = [
        "Aucun diplôme (%) hommes",
        "CAP / BEP  (%) hommes",
        "Baccalauréat / brevet professionnel (%) hommes",
        "De Bac +2 à Bac +4 (%) hommes",
        "Bac +5 et plus (%) hommes",
    ]

    labels_f = [
        "Aucun diplôme (%) femmes",
        "CAP / BEP  (%) femmes",
        "Baccalauréat / brevet professionnel (%) femmes",
        "De Bac +2 à Bac +4 (%) femmes",
        "Bac +5 et plus (%) femmes",
    ]

    traces = [
        go.Bar(
            x=[
                "Aucun diplôme",
                "CAP / BEP",
                "Baccalauréat / brevet professionnel",
                "De Bac +2 à Bac +4",
                "Bac +5 et plus",
            ],
            y=[df_csp[df_csp["ville"] == ville][col].iloc[0] for col in labels_h],
            name="Hommes",
        ),
        go.Bar(
            x=[
                "Aucun diplôme",
                "CAP / BEP",
                "Baccalauréat / brevet professionnel",
                "De Bac +2 à Bac +4",
                "Bac +5 et plus",
            ],
            y=[df_csp[df_csp["ville"] == ville][col].iloc[0] for col in labels_f],
            name="Femmes",
        ),
    ]

    return {
        "data": traces,
        "layout": go.Layout(
            title=f"Répartition Hommes | Femmes (%)<br> à {ville.split('(')[0].strip()}",
            barmode="stack",
        ),
    }


@app.callback(
    [Output("table-csp", "data"), Output("table-csp", "columns")],
    [Input("dropdown-ville", "value")],
)
def table_salaires(ville):
    cols = [
        "Agriculteurs exploitants",
        "Artisans, commerçants, chefs d'entreprise",
        "Cadres et professions intellectuelles supérieures",
        "Professions intermédiaires",
        "Employés",
        "Ouvriers",
        "Aucun diplôme",
        "CAP / BEP ",
        "Baccalauréat / brevet professionnel",
        "De Bac +2 à Bac +4",
        "Bac +5 et plus",
    ]

    infos = {
        "label": cols,
        "value": [df_csp[df_csp["ville"] == ville][col].iloc[0] for col in cols],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = [{"id": "label", "name": ""}, {"id": "value", "name": ville}]

    return data, header


@app.callback(Output("csp", "figure"), [Input("dropdown-ville", "value")])
def csp(ville):
    labels = [
        "Agriculteurs exploitants",
        "Artisans, commerçants, chefs d'entreprise",
        "Cadres et professions intellectuelles supérieures",
        "Professions intermédiaires",
        "Employés",
        "Ouvriers",
    ]

    values = [df_csp[df_csp["ville"] == ville][col].iloc[0] for col in labels]
    total = sum(values)

    trace = [go.Pie(labels=labels, values=values)]

    return {
        "data": trace,
        "layout": go.Layout(
            title=f"Catégorie socioprofessionnelle à {ville.split('(')[0].strip()}<br>(Total: {total})"
        ),
    }


## Automobile ##
@app.callback(
    [
        Output("total-voitures", "children"),
        Output("total-accidents", "children"),
        Output("total-places", "children"),
    ],
    [Input("dropdown-ville", "value")],
)
def infos_automobile(ville):
    total_voitures = int(
        df_auto[df_auto["ville"] == ville]["total de voitures"].iloc[0]
    )
    total_accidents = int(
        df_auto[df_auto["ville"] == ville]["Nombre total d'accidents"].iloc[0]
    )
    total_places = int(
        df_auto[df_auto["ville"] == ville][
            "Ménages avec place(s) de stationnement"
        ].iloc[0]
    )

    return total_voitures, total_accidents, total_places


@app.callback(Output("voitures-menage", "figure"), [Input("dropdown-ville", "value")])
def voitures_menage(ville):
    labels = [
        "Ménages sans voiture",
        "Ménages avec une voiture",
        "Ménages avec deux voitures ou plus",
    ]

    values = [df_auto[df_auto["ville"] == ville][col].iloc[0] for col in labels]
    total = sum(values)

    trace = [go.Pie(labels=labels, values=values)]

    return {
        "data": trace,
        "layout": go.Layout(
            title=f"Nombre de voitures par ménage à {ville.split('(')[0].strip()}"
        ),
    }


@app.callback(Output("accidents", "figure"), [Input("dropdown-ville", "value")])
def voitures_menage(ville):
    cols = [
        "Nombre de personnes tuées",
        "Nombre de personnes indemnes",
        " - dont blessés graves",
        " - dont blessés légers",
    ]

    labels = [
        "Personnes tuées",
        "Personnes indemnes",
        "Blessés graves",
        "Blessés légers",
    ]

    values = [df_auto[df_auto["ville"] == ville][col].iloc[0] for col in cols]
    total = sum(values)

    trace = [go.Pie(labels=labels, values=values)]

    return {
        "data": trace,
        "layout": go.Layout(
            title=f"Accidents de la route à {ville.split('(')[0].strip()}"
        ),
    }


## Délinquance ##
@app.callback(
    [Output("table-delinquance", "data"), Output("table-delinquance", "columns")],
    [Input("dropdown-ville", "value")],
)
def table_delinquance(ville):
    cols = [
        "Violences aux personnes",
        "Vols et dégradations",
        "Délinquance économique et financière",
        "Autres crimes et délits",
        "Violences gratuites",
        "Violences crapuleuses",
        "Violences sexuelles",
        "Menaces de violence",
        "Atteintes à la dignité",
        "Cambriolages",
        "Vols à main armée (arme à feu)",
        "Vols avec entrée par ruse",
        "Vols liés à l'automobile",
        "Vols de particuliers",
        "Vols d'entreprises",
        "Violation de domicile",
        "Destruction et dégradations de biens",
        "Escroqueries, faux et contrefaçons",
        "Trafic, revente et usage de drogues",
        "Infractions au code du Travail",
        "Infractions liées à l'immigration",
        "Différends familiaux",
        "Proxénétisme",
        "Ports ou détentions d'arme prohibée",
        "Recels",
        "Délits des courses et jeux d'argent",
        "Délits liés aux débits de boisson et de tabac",
        "Atteintes à l'environnement",
        "Délits liés à la chasse et la pêche",
        "Cruauté et délits envers les animaux",
        "Atteintes aux intérêts fondamentaux de la Nation",
    ]

    infos = {
        "label": cols,
        "value": [
            int(df_delinquance[df_delinquance["ville"] == ville][col].iloc[0])
            for col in cols
        ],
    }

    table_infos = pd.DataFrame(infos)
    data = table_infos.to_dict("records")
    header = [{"id": "label", "name": ""}, {"id": "value", "name": ville}]

    return data, header


@app.callback(Output("crimes", "figure"), [Input("dropdown-ville", "value")])
def crimes(ville):
    labels = [
        "Violences aux personnes",
        "Vols et dégradations",
        "Délinquance économique et financière",
        "Autres crimes et délits",
    ]

    values = [
        df_delinquance[df_delinquance["ville"] == ville][col].iloc[0] for col in labels
    ]
    total = sum(values)

    trace = [go.Pie(labels=labels, values=values)]

    return {
        "data": trace,
        "layout": go.Layout(
            title=f"Principaux crimes et délits à {ville.split('(')[0].strip()}<br>(Total: {total})"
        ),
    }


@app.callback(Output("agressions", "figure"), [Input("dropdown-ville", "value")])
def agressions(ville):
    labels = [
        "Violences gratuites",
        "Violences crapuleuses",
        "Violences sexuelles",
        "Menaces de violence",
        "Atteintes à la dignité",
    ]

    values = [
        df_delinquance[df_delinquance["ville"] == ville][col].iloc[0] for col in labels
    ]
    total = sum(values)

    trace = [go.Pie(labels=labels, values=values)]

    return {
        "data": trace,
        "layout": go.Layout(
            title=f"Agressions et violences aux personnes à {ville.split('(')[0].strip()}<br>(Total: {total})"
        ),
    }


@app.callback(Output("vols", "figure"), [Input("dropdown-ville", "value")])
def agressions(ville):
    labels = [
        "Cambriolages",
        "Vols à main armée (arme à feu)",
        "Vols avec entrée par ruse",
        "Vols liés à l'automobile",
        "Vols de particuliers",
        "Vols d'entreprises",
        "Violation de domicile",
        "Destruction et dégradations de biens",
    ]

    values = [
        df_delinquance[df_delinquance["ville"] == ville][col].iloc[0] for col in labels
    ]
    total = sum(values)

    trace = [go.Pie(labels=labels, values=values)]

    return {
        "data": trace,
        "layout": go.Layout(
            title=f"Vols et dégradations à {ville.split('(')[0].strip()}<br>(Total: {total})"
        ),
    }


server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
