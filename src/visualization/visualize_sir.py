import pandas as pd
import numpy as np

import plotly.graph_objects as go

import dash
from dash import dcc as doc
from dash.dependencies import Input, Output
from dash import html
import dash_daq as daq

from scipy import optimize

fig_sir = go.Figure()
app = dash.Dash()

df_covid = pd.read_csv("../data/raw/covid_full_data.csv", sep=";")
countries = df_covid['location'].unique()

app.layout = html.Div([
    html.H1('Dynamic Covid-19 Dashboard'),
    daq.BooleanSwitch(id='loglin_switch', on=False, label="Logarithmic scale", labelPosition="top"),
    html.Label('Select the countries to display:'),
    doc.Dropdown(
        id = 'country_drop_down',
        options=[{'label': country, 'value': country} for country in countries],
        value=['Germany'],        # which are pre-selected
        multi=True
    ),
    doc.Graph(figure=fig_sir,id='main_window_sir')
])

@app.callback(
    Output('main_window_sir', 'figure'),
    [Input('country_drop_down', 'value'), Input('loglin_switch', 'on')])
def update_figure(countries_to_show, switch_state):
    global N0, S0, I0, R0, t
    traces = []
    for country in countries_to_show:
        total_cases_country = df_covid.total_cases[df_covid.location==country]
        ydata = np.array(total_cases_country.iloc[50:180])
        t=np.arange(len(ydata))
        
        # use population of country from dataframe
        N0 = df_covid.population[df_covid.location==country].iloc[60];
        I0=ydata[0]          # Initial value of infected people
        S0=N0-I0             # Initial value for sususceptible people
        R0=0                 # Initial value for recovered people
        # the resulting curve has to be fitted
        # free parameters are here beta and gamma
        
        popt, pcov = optimize.curve_fit(fit_odeint, t, ydata)       # popt contains fitted beta and gamma
        perr = np.sqrt(np.diag(pcov))
        print('standard deviation errors : ',str(perr), ' start infect:',ydata[0])
        print("Optimal parameters: beta =", popt[0], " and gamma = ", popt[1])
        # get the final fitted curve
        fitted = fit_odeint(t, *popt)
        print(N0, I0, S0)
        
        traces.append(dict(x=t,
                             y=ydata,
                             name=f"Total (Summed) Cases {country}",
                             opacity=0.9,
                             line_width=2,
                             marker_size=4,
                             mode='markers'
                          )
                     )
        traces.append(dict(x=t,
                             y=fitted,
                             name=f"Total Cases according to SIR-model {country} (=N0-S)",
                             line_width=2,
                             marker_size=4,
                             mode='lines'
                          )
                     )
        
    return {
        'data': traces,
        'layout': dict(width=1280,
                        height=720,
                        title="Fit of SIR model for selected countries",
                        xaxis={'tickangle':-45,
                              'nticks':20,
                              'tickfont':dict(size=14,color='#7f7f7f'),
                               'title':'Days',
                              },
                        yaxis={
                            'type': ('log' if switch_state else 'linear'),
                            'range':('[0.1,100]' if switch_state else '[0,100000000]'),
                            'title':'Summed Infections'
                        })
    }

app.run(debug=True, use_reloader=False, port=8051)