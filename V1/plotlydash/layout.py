from dash import dcc, html



marks = ['one Day', 'one Week', 'one Month', 'six Month']

Layout = html.Div(children =[html.Div([
                                html.H2(children="Stat_calculator Graph", style={'textAlign': 'center'}),
                                html.Br(),
                                html.H4(children="Categories :"),
                                html.Br(),
                                dcc.Dropdown(
                                    ['Cryptocurrency', 'Forex', 'Commodities'],
                                    'Cryptocurrency',
                                    id = 'category-dropdown',
                                    style={'width':500, 'padding-left':'100px'}
                                )]),
                            html.Div([
                                html.Br(),
                                html.H4(children='Periods :')
                                ]),
                            html.Div([
                                dcc.Slider(0, 3,step=1, marks={i: marks[i] for i in range(4)}, value=1, id='period-slider',vertical=True,verticalHeight=200)
                                ],style={'padding-left':'100px'}),
                            
                            html.Div([
                                html.Br(),
                                html.H4(children='Enter Currency Name :'),
                                dcc.Input(value='all', type='search', debounce=True, placeholder='Insert Currency Name', style={'padding-left':'100px'}, id='keyword_input'),
                                html.Br(),
                                
                            ]),
                            html.Div([
                                html.Br(),
                                html.Br(),
                                dcc.Graph(id = 'fig1', style={'textAlign': 'center','width': 1500, 'padding-left':'250px'}),
                                html.Br(),
                                html.H4(children="Number of News per Author", style={'textAlign': 'center'}),
                                html.Br()
                            ]),
                            html.Div([
                                html.Br(),
                                html.Br(),
                                dcc.Graph(id='fig6', style={'textAlign': 'center','width': 1500, 'padding-left':'250px'}),
                                html.Br(),
                                html.H4(children="Average Sentiment Ratio plot", style={'textAlign': 'center'}),
                                html.Br()

                            ]),
                            html.Div([
                                html.Br(),
                                html.Br(),
                                dcc.Graph(id='fig7', style={'textAlign': 'center','width': 1500, 'padding-left':'250px'}),
                                html.Br(),
                                html.H4(children="Positive Ratio and Negative Ratio", style={'textAlign': 'center'}),
                                html.Br()
                            ]),
                            html.Div([
                                html.Br(),
                                html.Br(),
                                dcc.Graph(id='fig8', style={'textAlign': 'center','width': 1500, 'padding-left':'250px'}),
                                html.Br(),
                                html.H4(children="Number of News Each as a Bar", style={'textAlign': 'center'}),
                                html.Br()
                            ]),
                             html.Div([
                                html.Br(),
                                html.Br(),
                                dcc.Graph(id='fig12', style={'textAlign': 'center','width': 1500, 'padding-left':'250px'}),
                                html.Br(),
                                html.H4(children="Stacked Horizontal Number of News", style={'textAlign': 'center'}),
                                html.Br()
                            ]),
                            html.Div([
                                html.Br(),
                                html.Br(),
                                dcc.Graph(id='fig4', style={'textAlign': 'center','width': 1500, 'padding-left':'250px'}),
                                html.Br(),
                                html.H4(children="Scatter Plot of Authors and News", style={'textAlign': 'center'}),
                                html.Br()
                            ]),
                            html.Div([
                                html.Br(),
                                html.Br(),
                                dcc.Graph(id='fig10', style={'textAlign': 'center','width': 1500, 'padding-left':'250px'}),
                                html.Br(),
                                html.H4(children="Portion of Each Author Based on Total Number of News", style={'textAlign': 'center'}),
                                html.Br()
                            ]),
                            html.Div([
                                html.Br(),
                                html.Br(),
                                dcc.Graph(id='fig9', style={'textAlign': 'center','width': 1500, 'padding-left':'250px'}),
                                html.Br(),
                                html.H4(children="the Ratio of Each Weight (for all Authors)", style={'textAlign': 'center'}),
                                html.Br()
                            ]),
                            html.Div([
                                html.Br(),
                                html.Br(),
                                dcc.Graph(id='fig13', style={'textAlign': 'center','width': 1500, 'padding-left':'250px'}),
                                html.Br(),
                                html.H4(children="Portion of Each Author + It's Corresponding Number of Each Weight", style={'textAlign': 'center'}),
                                html.Br()
                            ]),
                            ])