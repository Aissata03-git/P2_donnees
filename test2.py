import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP],
    use_pages=True,
    pages_folder='pages',
    prevent_initial_callbacks=True,
    suppress_callback_exceptions=True,
)

########### Navbar design section####################
quickLinksLabels = {
    "home": "Home page",
    "analysis": "KPIs analysis",
}

nav = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem(quickLinksLabels.get(page["name"], page["name"]), href=page["path"])
        for page in dash.page_registry.values()
        if page["module"] != "pages.not_found_404"
    ],
    nav=True,
    in_navbar=True,
    label="Quick Links",
    className="me-5 text-primary fw-bold",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Img(
                                    src=dash.get_asset_url("rh_logo.jpg"),
                                    height="30px",
                                ),
                            ],
                            className="me-2 text-primary",
                        ),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "WatchTower: Disinformation Reporting Platform",
                                className="ms-2 text-primary",
                            )
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
            ),
            nav,
        ]
    ),
    dark=True,
    className="opacity-100 p-2  text-white fw-bold rounded",
)

content = html.Div(id="page-content", children=[dash.page_container], className="content")

# main app layout
app.layout = dbc.Container(
    [dbc.Row([dbc.Col([navbar, content], width=12)])],
    fluid=False,
    style={},
    className="bg-opacity-10 p-2 bg-primary text-dark fw-bold rounded border border-light mh-100",
)

if __name__ == "__main__":
    app.run_server(debug=True, port=6886)
