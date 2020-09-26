# https://towardsdatascience.com/creating-a-financial-dashboard-with-python-6d8583e38b57
# https://dash.plotly.com

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

rows = html.Div(
    [
        dbc.Row(dbc.Col(html.Div(
            [
                html.H1('Financial GROWTH Dashboard'),
                html.Div([dcc.Input(id='company_selection', value='AAPL')], style={'padding': 10}),
                html.Div([html.H3(id='text')], style={'padding': 5}),
                ]
        ))),
        dbc.Row(
            [
                dbc.Col(html.Div(dcc.Graph(id='growth_revenue')), width=5),
                dbc.Col(html.Div(dcc.Graph(id='growthCostOfRevenue')), width=5),
                dbc.Col(html.Div(dcc.Graph(id='growthGrossProfit')), width=5),
                dbc.Col(html.Div(dcc.Graph(id='growthGrossProfitRatio')), width=5),
            ]
        ),
    ]
)

app.layout = dbc.Container(
    html.Div([
        rows
        ])
)


@app.callback(Output('growth_revenue', 'figure'), [Input('company_selection', 'value')])
def retrieve_growth_revenue(company):
    demo = 'b4ec5eef495822971cbf5b88277edbf2'
    IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement-growth/{company}?limit=10&apikey=demo')
    IS = IS.json()

    growth_revenue = []
    Dates = []
    count = 0
    for item in IS:
        growth_revenue.append(float(IS[count]['growthRevenue']))
        Dates.append(IS[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=Dates, y=growth_revenue, marker_color='lightsalmon', name='growth_revenue')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'GROWTH REVENUE'}, )}
    return datapoints


@app.callback(Output('growthCostOfRevenue', 'figure'), [Input('company_selection', 'value')])
def retrieve_growth_cost_of_revenue(company):
    demo = 'b4ec5eef495822971cbf5b88277edbf2'
    IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement-growth/{company}?limit=10&apikey=demo')
    IS = IS.json()

    growth_revenue = []
    Dates = []
    count = 0
    for item in IS:
        growth_revenue.append(float(IS[count]['growthCostOfRevenue']))
        Dates.append(IS[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=Dates, y=growth_revenue, marker_color='lightsalmon', name='growthCostOfRevenue')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'GROWTH COST OF REVENUE'}, )}
    return datapoints


@app.callback(Output('growthGrossProfit', 'figure'), [Input('company_selection', 'value')])
def retrieve_growth_gross_profit(company):
    demo = 'b4ec5eef495822971cbf5b88277edbf2'
    IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement-growth/{company}?limit=10&apikey=demo')
    IS = IS.json()

    growth_revenue = []
    Dates = []
    count = 0
    for item in IS:
        growth_revenue.append(float(IS[count]['growthGrossProfit']))
        Dates.append(IS[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=Dates, y=growth_revenue, marker_color='lightsalmon', name='growthGrossProfit')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'GROWTH GROSS PROFIT'}, )}
    return datapoints


@app.callback(Output('growthGrossProfitRatio', 'figure'), [Input('company_selection', 'value')])
def retrieve_growth_gross_profit_ratio(company):
    demo = 'b4ec5eef495822971cbf5b88277edbf2'
    IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement-growth/{company}?limit=10&apikey=demo')
    IS = IS.json()

    growth_revenue = []
    Dates = []
    count = 0
    for item in IS:
        growth_revenue.append(float(IS[count]['growthGrossProfitRatio']))
        Dates.append(IS[count]['date'])
        count += 1
    datapoints = {'data': [go.Bar(x=Dates, y=growth_revenue, marker_color='lightsalmon', name='growthGrossProfitRatio')],
                  'layout': dict(xaxis={'title': 'Date'}, yaxis={'title': 'GROWTH GROSS PROFIT RATIO'}, )}
    return datapoints


@app.callback(Output(component_id='text', component_property='children'),
              [Input(component_id='company_selection', component_property='value')])
def update_output_div(input_value):
    return 'Displaying Data for "{}"'.format(input_value)


if __name__ == '__main__': app.run_server(debug=True)
