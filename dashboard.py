import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])

#PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# jumbotron = dbc.Jumbotron(
#     [
#         html.H1("Jumbotron", className="display-3"),
#         html.P(
#             "Use a jumbotron to call attention to "
#             "featured content or information.",
#             className="lead",
#         ),
#         html.Hr(className="my-2"),
#         html.P(
#             "Jumbotrons use utility classes for typography and "
#             "spacing to suit the larger container."
#         ),
#         html.P(dbc.Button("Learn more", color="primary"), className="lead"),
#     ]
# )

tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Tab 1", tab_id="tab-1"),
                dbc.Tab(label="Tab 2", tab_id="tab-2"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)


@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return top_card
    elif at == "tab-2":
        return bottom_card
    return html.P("This shouldn't ever be displayed...")


top_card = dbc.Card(
    [
        dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
        dbc.CardBody(
            html.P("This card has an image at the top", className="card-text")
        ),
    ],
    style={"width": "18rem"},
)

bottom_card = dbc.Card(
    [
        dbc.CardBody(html.P("This has a bottom image", className="card-text")),
        dbc.CardImg(src="/static/images/placeholder286x180.png", bottom=True),
    ],
    style={"width": "18rem"},
)

cards = dbc.Row(
    [dbc.Col(top_card, width="auto"), dbc.Col(bottom_card, width="auto")]
)


app.layout = dbc.Container(
    html.Div([
        tabs
        ])
)

if __name__ == "__main__":
    app.run_server(debug=True)
