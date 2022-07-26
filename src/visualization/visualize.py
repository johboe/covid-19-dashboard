import pandas as pd
import numpy as np
import plotly.graph_objects as go

import dash
from dash import dcc as doc
from dash.dependencies import Input, Output
from dash import html
import dash_daq as daq

import numpy as np

fig = go.Figure()
df_covid = pd.read_csv("../data/processed/data_doubling_filtered.csv", sep=";")
countries = df_covid['location'].unique()

app = dash.Dash()
app.layout = html.Div([
    html.H1('Dynamic Covid-19 Dashboard'),
    daq.BooleanSwitch(id='loglin_switch', on=False, label="Logarithmic scale", labelPosition="top"),
    html.Label('This dynamic dashboard implements '),
    html.Label('Select the countries to display:'),
    doc.Dropdown(
        id = 'country_drop_down',
        options=[{'label': country, 'value': country} for country in countries],
        value=['Germany'],        # which are pre-selected
        multi=True
    ),
     doc.Markdown('''
        ## Select Timeline of confirmed COVID-19 cases or the approximated doubling time
        '''),


    doc.Dropdown(
    id='doubling_time',
    options=[
        {'label': 'Timeline Confirmed ', 'value': 'total_cases'},
        {'label': 'Timeline Confirmed Filtered', 'value': 'total_cases_filtered'},
        {'label': 'Timeline Doubling Rate', 'value': 'total_cases_DR'},
        {'label': 'Timeline Doubling Rate Filtered', 'value': 'total_cases_filtered_DR'},
        {'label': 'Percentage Of Fully Vaccinated People', 'value': 'people_vaccinated_per_hundred'},
    ],
    value='total_cases',
    multi=False
    ),
    doc.Graph(figure=fig,id='main_window_slope')
])
@app.callback(
    Output('main_window_slope', 'figure'),
    [Input('country_drop_down', 'value'), Input('loglin_switch', 'on'), Input('doubling_time', 'value')])
def update_figure(countries_to_show, switch_state, show_doubling):
    traces = []
    for country in countries_to_show:
        df_plot=df_covid[df_covid['location']==country]

        if show_doubling=='doubling_rate_filtered':
            df_plot=df_plot[['location','total_cases','total_cases_filtered','total_cases_DR','total_cases_filtered_DR','date', 'people_vaccinated_per_hundred']].groupby(['location','date']).agg(np.mean).reset_index()
        else:
            df_plot=df_plot[['location','total_cases','total_cases_filtered','total_cases_DR','total_cases_filtered_DR','date', 'people_vaccinated_per_hundred']].groupby(['location','date']).agg(np.sum).reset_index()
        
        
        traces.append(dict(x=df_plot.date[60:],
                             y=df_plot[show_doubling][60:],
                             name=country,
                             opacity=0.9,
                             line_width=2,
                             marker_size=4,
                             mode='markers+lines'
                          )
                     )
        
    return {
        'data': traces,
        'layout': dict(width=1280,
                        height=720,
                        title="Covid-19 Cases",
                        xaxis_title='Time',
                        yaxis_title='Confirmed infected people (source: Our World in Data)',
                      xaxis={'tickangle':-45,
                            'nticks':20,
                            'tickfont':dict(size=14,color='#7f7f7f'),
                            },
                      yaxis={
                          'type': ('log' if switch_state else 'linear'),
                          'range':('[0.1,100]' if switch_state else '[0,100000000]'),
                      })
    }

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)