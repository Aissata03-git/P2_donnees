from dash import Dash,html, dcc, callback, Input, Output, ctx
import dash_bootstrap_components as dbc
import dash
import pandas as pd
import numpy as np

# dash.register_page(__name__, path="/", order=0)


dash.register_page(__name__, name="home",path="/", order=0)

card_icon = {
    "color": "primary",
    "textAlign": "center",
    "fontSize": 80,
    "margin": "auto",
}
data = pd.read_csv('Data/RH data.csv')

updateTime = (
    f"Last Update on {pd.to_datetime(pd.Timestamp.today()).strftime('%Y-%m-%d')}"
)
NbrEmploye = f'{data.shape[0]}'
Departs = f"{data[data['Attrition']=='Yes'].shape[0]}"
Actifs = f"{data[data['Attrition']!='Yes'].shape[0]}"
taux_depart = f"{np.round(data[data['Attrition']=='Yes'].shape[0]/data.shape[0]*100,2)} %"
age_moyen = f"{int(np.round(data['Age'].mean(),0))}"

def create_card(ico, title, value, note):
    card = dbc.CardGroup(
        [
            dbc.Card(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                # dbc.CardImg(
                                #     src=dash.get_asset_url("VOST_LOGO.png"),
                                #     className="img-fluid rounded-start",
                                # ),
                                html.I(className=ico),
                                className="col-md-4 ",
                                style=card_icon,
                            ),
                            dbc.Col(
                                dbc.CardBody(
                                    [
                                        html.H4(title, className="card-title"),
                                        html.H1(
                                            value,
                                            className="card-text",
                                        ),
                                        html.Small(
                                            note,
                                            className="card-text text-muted",
                                        ),
                                    ]
                                ),
                                className="col-md-8 ",
                            ),
                        ],
                        className="g-0 d-flex align-items-center",
                    )
                ],
                className="mb-3 bg-opacity-10  mt-3 shadow my-2 bg-light text-primary  rounded  ",
            ),
            dbc.Card(
                className="mb-3 mt-3 bg-primary shadow my-2 bg-opacity-80  ",
                style={"maxWidth": 75},
            ),
        ],
        className="",
    )

    return card
# create card instances
card1 = create_card(
    "bi bi-sunrise-fill me-2",
    "Active Since",
    "June 2024",
    "A data decision tools for human resources",
)
card2 = create_card(
    "bi bi-people  me-2", "Nombre d'Employés Total", NbrEmploye, updateTime
)
card3 = create_card(
    "bi bi-person-dash me-2", "Nombre de Départs", Departs, updateTime
)
card4 = create_card("bi bi-person-fill-check me-2", "Employés Actifs", Actifs, updateTime)
card5 = create_card(
    "bi bi-person-down me-2", "Taux de Departs", taux_depart, updateTime
)
card6 = create_card(
    "bi bi-calendar-date me-2", "Age Moyen des Employés", age_moyen, updateTime
)

# app = Dash(
#     __name__,
#     external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP],
#     use_pages=True,
#     pages_folder="pages",
#     prevent_initial_callbacks=True,
#     suppress_callback_exceptions=True,
# )




layout = dbc.Container(
    [
        dcc.Interval(
            id="card_interval-id",
            disabled=False,
            n_intervals=0,
            interval=1 * 3000,
        ),
        # dbc.Row(
        #     [
        #         dbc.Col([
        #             dbc.Container(
        #                 html.Img(
        #                     src=dash.get_asset_url("rh_logo.jpg"),
        #                     style={
        #                             "margin-left": "auto",
        #                             "margin-right": "auto",
        #                             "display": "block",
        #                             "width": "80%",
        #                             "height":"20%"
        #                         },
        #                     ),
        #                 className="p-1 ",
        #                 fluid=False,
        #             ),
        #     ])
        #     ],align="center",
        # ),
        dbc.Row([
            dbc.Col([
                dbc.Container([
                    dbc.Row([
                        dbc.Col([],width=1),
                        dbc.Col(
                            html.H2('Valeurs Totales des indicateurs',
                                    className="text-primary fw-bold mt-2 ms-5 m",)
                        )
                    ], align='center',
                    className ="me-5 ms-5"),
                    dbc.Row([
                        dbc.Col([],width=1),
                        dbc.Col(
                            dbc.Container(
                                [
                                    dbc.Row([
                                        dbc.Col([], width=2),
                                        dbc.Col(
                                            [card1],
                                            id="card-id",
                                            width=7,
                                        ),
                                        dbc.Col([],width=3),
                                    ],className="my-4 "),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    dbc.Pagination(
                                                        max_value=0,
                                                        first_last=True,
                                                        previous_next=True,
                                                        id="pagination-id",
                                                    ),
                                                ],
                                                width=1,
                                            ),
                                        ],
                                        className="",
                                        align="center",
                                    ),
                            ],
                                fluid=False,
                                className="",
                            )
                        )
                    ],
                        align="center",
                        className=" ",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.Hr())
                        ],
                        align="center",
                        className=" ",
                            ),
                ],className=" shadow text-primary fw-bold rounded p-5  ",)
            ], width=10)
        ],align='center',
        class_name="mt-5 d-flex justify-content-center")
    ]
)

@callback(
    Output("card-id", "children"),
    [
        Input("pagination-id", "active_page"),
        Input("card_interval-id", "n_intervals"),
    ],
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
)
def change_page(page, num):
    event_in = ctx.triggered_id

    pageMap = {"k3": card3, "k1": card1, "k2": card2, "k4": card4, "k5": card5, "k6": card6}
    if event_in == "pagination-id":

        if page > 6:
            page = 1
        currentCard = pageMap[f"k{page}"]
        # print(type(page))
    else:
        page = num % 6 + 1
        # pageMap = {"k3": card3, "k1": card1, "k2": card2, "k4": card4}
        # if page > 4:
        #     page = 1
        currentCard = pageMap[f"k{page}"]
    # print(type(page))
    return currentCard
