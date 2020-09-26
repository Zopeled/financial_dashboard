# https://towardsdatascience.com/creating-a-financial-dashboard-with-python-6d8583e38b57
# https://dash.plotly.com

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

rows = html.Div(
    [
        dbc.Row(dbc.Col(html.Div(
            [
                html.H1('Financial Dashboard'),
                html.Div([dcc.Input(id='company_selection', value='AAPL')], style={'padding': 10}),
                html.Div([html.H3(id='text')], style={'padding': 5}),
                ]
        ))),
        dbc.Row(
            [
                html.H3('Revenue'),
                dbc.Col(html.Div(dcc.Graph(id='revenue')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='revenue_growth')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='cost_of_revenue')), width=3),
            ]
        ),

        dbc.Row(
            [
                html.H3('Bottom Line'),
                dbc.Col(html.Div(dcc.Graph(id='gross_profit')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='operating_income')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='ebitda')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='ebit')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='net_income')), width=3),
            ]
        ),

        dbc.Row(
            [
                html.H3('Margins'),
                dbc.Col(html.Div(dcc.Graph(id='gross_margin')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='ebitda_margin')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='ebit_margin')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='profit_margin')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='free_cf_margin')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='net_profit_margin')), width=3),
            ]
        ),

        dbc.Row(
            [
                html.H3('Share Holders'),
                dbc.Col(html.Div(dcc.Graph(id='eps')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='eps_diluted')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='dividend_per_share')), width=3),
            ]
        ),


        dbc.Row(
            [
                html.H3('Expenses'),
                dbc.Col(html.Div(dcc.Graph(id='rnd_expenses')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='operating_expenses')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='interest_expense')), width=3),
                dbc.Col(html.Div(dcc.Graph(id='earnings_before_tax')), width=3),

            ]
        ),

    ]
)

# app.layout = html.Div(
#     [
#         dbc.Row
#         (
#             dbc.Col
#             (
#                 html.Div
#                     ([
#                         html.H1('Financial Dashboard'),
#                         html.Div([dcc.Input(id='company_selection', value='AAPL')], style={'padding': 10}),
#                         html.Div([html.H3(id='text')], style={'padding': 5}),
#                     ]), width="auto"
#              )
#         ),
#         dbc.Row
#             (
#                 [
#                     dbc.Col
#                     (
#                         dcc.Graph(id='revenue'),
#
#                     ),
#                     dbc.Col
#                     (
#                         dcc.Graph(id='netincome'),
#
#                     )
#                 ]
#             ),
#         dbc.Row
#             (
#                 html.Div([dcc.Graph(id='ebitda')], style={'padding': 5})
#             )
#     ]
# )
# first_card = dbc.Card(
#     dbc.CardBody(
#         [
#             html.H1('Financial Dashboard'),
#             html.Div([dcc.Input(id='company_selection', value='TSLA')], style={'padding': 10}),
#             html.Div([html.H3(id='text')], style={'padding': 5}),
#         ]
#     )
# )
#
#
# second_card = dbc.Card(
#     dbc.CardBody(
#         [
#             html.Div([dcc.Graph(id='revenue')], style={'padding': 5}),
#             html.Div([dcc.Graph(id='netincome')], style={'padding': 5}),
#         ]
#     )
# )
#
# third_card = dbc.Card(
#     dbc.CardBody(
#         [
#             html.Div([dcc.Graph(id='ebitda')], style={'padding': 5})
#         ]
#     )
# )
# cards = dbc.Row([dbc.Col(first_card, width=8), dbc.Col(second_card, width=4), dbc.Col(third_card, width=4)])
# app.layout = html.Div([
#     html.H1('Financial Dashboard'),
#     html.Div([dcc.Input(id='company_selection', value='AAPL')], style={'padding': 10}),
#     html.Div([html.H3(id='text')], style={'padding': 5}),
#     html.Div([dcc.Graph(id='revenue')], style={'padding': 5}),
#     html.Div([dcc.Graph(id='netincome')], style={'padding': 5}),
#     html.Div([dcc.Graph(id='ebitda')], style={'padding': 5})
# ])

app.layout = dbc.Container(
    html.Div([
        rows
        ])
)


# REVENUE
@app.callback(Output('revenue', 'figure'), [Input('company_selection', 'value')])
def retrieve_revenue(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    revenues = []
    dates = []
    count = 0
    for item in req:
        revenues.append(float(req[count]['Revenue']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=revenues)],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'Revenue'}, )}
    return datapoints


@app.callback(Output('revenue_growth', 'figure'), [Input('company_selection', 'value')])
def retrieve_revenue_growth(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials = []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['Revenue Growth']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials)],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'Revenue Growth'}, )}
    return datapoints


@app.callback(Output('cost_of_revenue', 'figure'), [Input('company_selection', 'value')])
def retrieve_cost_of_revenue(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials = []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['Cost of Revenue']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials)],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'Cost of Revenue'}, )}
    return datapoints


# Bottom Line
@app.callback(Output('gross_profit', 'figure'), [Input('company_selection', 'value')])
def retrieve_gross_profit(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials = []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['Gross Profit']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials)],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'Gross Profit'}, )}
    return datapoints


@app.callback(Output('operating_income', 'figure'), [Input('company_selection', 'value')])
def retrieve_operating_income(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials = []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['Operating Income']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials, marker_color='lightsalmon', name='Operating Income')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'Operating Income'}, )}
    return datapoints


@app.callback(Output('ebit', 'figure'), [Input('company_selection', 'value')])
def retrieve_ebit(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials = []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['EBIT']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials, marker_color='lightsalmon', name='EBIT')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'EBIT'}, )}
    return datapoints


@app.callback(Output('ebitda', 'figure'), [Input('company_selection', 'value')])
def retrieve_ebitda(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials= []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['EBITDA']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials, marker_color='lightsalmon', name='EBITDA')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'EBITDA'}, )}
    return datapoints


@app.callback(Output('net_income', 'figure'), [Input('company_selection', 'value')])
def retrieve_net_income(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials = []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['Net Income']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials, marker_color='lightsalmon', name='Net Income')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'Net Income'}, )}
    return datapoints


# Margins
@app.callback(Output('gross_margin', 'figure'), [Input('company_selection', 'value')])
def retrieve_gross_margin(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials = []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['Gross Margin']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials, marker_color='lightsalmon', name='Gross Margin')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'Gross Margin'}, )}
    return datapoints


@app.callback(Output('ebitda_margin', 'figure'), [Input('company_selection', 'value')])
def retrieve_ebitda_margin(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials = []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['EBITDA Margin']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials, marker_color='lightsalmon', name='EBITDA Margin')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'EBITDA Margin'}, )}
    return datapoints


@app.callback(Output('ebit_margin', 'figure'), [Input('company_selection', 'value')])
def retrieve_ebit_margin(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials = []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['EBIT Margin']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials, marker_color='lightsalmon', name='EBIT Margin')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'EBIT Margin'}, )}
    return datapoints


@app.callback(Output('profit_margin', 'figure'), [Input('company_selection', 'value')])
def retrieve_profit_margin(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials = []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['Profit Margin']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials, marker_color='lightsalmon', name='Profit Margin')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'Profit Margin'}, )}
    return datapoints


@app.callback(Output('free_cf_margin', 'figure'), [Input('company_selection', 'value')])
def retrieve_free_cf_margin(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials = []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['Free Cash Flow margin']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials, marker_color='lightsalmon', name='Free Cash Flow margin')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'Free Cash Flow margin'}, )}
    return datapoints


@app.callback(Output('net_profit_margin', 'figure'), [Input('company_selection', 'value')])
def retrieve_net_profit_margin(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials = []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['Net Profit Margin']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials, marker_color='lightsalmon', name='Net Profit Margin')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'Net Profit Margin'}, )}
    return datapoints


# Share Holders
@app.callback(Output('eps', 'figure'), [Input('company_selection', 'value')])
def retrieve_eps(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials = []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['EPS']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials, marker_color='lightsalmon', name='EPS')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'EPS'}, )}
    return datapoints


@app.callback(Output('eps_diluted', 'figure'), [Input('company_selection', 'value')])
def retrieve_eps_diluted(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials = []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['EPS Diluted']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials, marker_color='lightsalmon', name='EPS Diluted')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'EPS Diluted'}, )}
    return datapoints


@app.callback(Output('dividend_per_share', 'figure'), [Input('company_selection', 'value')])
def retrieve_dividend_per_share(company):
    # demo = 'b4ec5eef495822971cbf5b88277edbf2'
    req = requests.get(f'https://financialmodelingprep.com/api/v3/financials/income-statement/{company}?apikey=demo')
    req = req.json()
    req = req['financials']
    financials = []
    dates = []
    count = 0
    for item in req:
        financials.append(float(req[count]['Dividend per Share']))
        dates.append(req[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=dates, y=financials, marker_color='lightsalmon', name='Dividend per Share')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'Dividend per Share'}, )}
    return datapoints


@app.callback(Output(component_id='text', component_property='children'),
              [Input(component_id='company_selection', component_property='value')])
def update_output_div(input_value):
    return 'Displaying Data for "{}"'.format(input_value)


if __name__ == '__main__': app.run_server(debug=True)
