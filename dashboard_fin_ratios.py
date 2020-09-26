# https://towardsdatascience.com/creating-a-financial-dashboard-with-python-6d8583e38b57
# https://dash.plotly.com

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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
                dbc.Col(html.Div(dcc.Graph(id='grossProfitRatio')), width=5),
                dbc.Col(html.Div(dcc.Graph(id='ebitdaratio')), width=5),
                dbc.Col(html.Div(dcc.Graph(id='operatingIncomeRatio')), width=5),
                dbc.Col(html.Div(dcc.Graph(id='incomeBeforeTaxRatio')), width=5),
                dbc.Col(html.Div(dcc.Graph(id='netIncomeRatio')), width=5),
            ]
        ),
    ]
)

app.layout = dbc.Container(
    html.Div([
        rows
        ])
)


@app.callback(Output('grossProfitRatio', 'figure'), [Input('company_selection', 'value')])
def retrieve_gross_profit_ratio(company):
    #demo = 'b4ec5eef495822971cbf5b88277edbf2'
    IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?apikey=demo')
    IS = IS.json()
    Revenues = []
    Dates = []
    count = 0
    for item in IS:
        Revenues.append(float(IS[count]['grossProfitRatio']))
        Dates.append(IS[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=Dates, y=Revenues)],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'grossProfitRatio'}, )}
    return datapoints


@app.callback(Output('ebitdaratio', 'figure'), [Input('company_selection', 'value')])
def retrieve_ebitda_ratio(company):
    #demo = 'b4ec5eef495822971cbf5b88277edbf2'
    IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?apikey=demo')
    IS = IS.json()
    Revenues = []
    Dates = []
    count = 0
    for item in IS:
        Revenues.append(float(IS[count]['ebitdaratio']))
        Dates.append(IS[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=Dates, y=Revenues, marker_color='lightsalmon', name='ebitdaratio')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'ebitdaratio'}, )}
    return datapoints


@app.callback(Output('operatingIncomeRatio', 'figure'), [Input('company_selection', 'value')])
def retrieve_operating_income_ratio(company):
    demo = 'b4ec5eef495822971cbf5b88277edbf2'
    IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?apikey=demo')
    IS = IS.json()
    Ebitda = []
    Dates = []
    count = 0
    for item in IS:
        Ebitda.append(float(IS[count]['operatingIncomeRatio']))
        Dates.append(IS[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=Dates, y=Ebitda, marker_color='lightsalmon', name='operatingIncomeRatio')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'operatingIncomeRatio'}, )}
    return datapoints


@app.callback(Output('incomeBeforeTaxRatio', 'figure'), [Input('company_selection', 'value')])
def retrieve_income_before_tax_ratio(company):
    demo = 'b4ec5eef495822971cbf5b88277edbf2'
    stock = company
    IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?apikey=demo')
    IS = IS.json()

    growth_revenue = []
    Dates = []
    count = 0
    for item in IS:
        growth_revenue.append(float(IS[count]['incomeBeforeTaxRatio']))
        Dates.append(IS[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=Dates, y=growth_revenue, marker_color='lightsalmon', name='incomeBeforeTaxRatio')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'incomeBeforeTaxRatio'}, )}
    return datapoints


@app.callback(Output('netIncomeRatio', 'figure'), [Input('company_selection', 'value')])
def retrieve_net_income_ratio(company):
    demo = 'b4ec5eef495822971cbf5b88277edbf2'
    stock = company
    IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?apikey=demo')
    IS = IS.json()

    growth_revenue = []
    Dates = []
    count = 0
    for item in IS:
        growth_revenue.append(float(IS[count]['netIncomeRatio']))
        Dates.append(IS[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=Dates, y=growth_revenue, marker_color='lightsalmon', name='netIncomeRatio')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'netIncomeRatio'}, )}
    return datapoints


@app.callback(Output(component_id='text', component_property='children'),
              [Input(component_id='company_selection', component_property='value')])
def update_output_div(input_value):
    return 'Displaying Data for "{}"'.format(input_value)


if __name__ == '__main__': app.run_server(debug=True)
