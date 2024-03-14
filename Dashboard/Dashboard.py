import dash
from dash import callback
import plotly.graph_objs as go
import dash.dependencies as dd
import dash_bootstrap_components as dbc
from dash import dcc, html 
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# reading data
data = pd.read_csv("CAR_SALE_DATA.csv")
data.drop_duplicates(inplace=True)
data.dropna(inplace=True)

# data is clean


# grouping data for donut charts


pink_shades_hex = ['#FC6C85', '#FC8EAC', '#F88379', '#FF9999', '#FFD1DC']

# Create Pie Charts (these will call by Graph component in layout)
brand_price = data.groupby(by="Brand", as_index=False).agg({"Price" : "mean"})
brand_price_fig = px.pie(brand_price, values='Price', names='Brand', hole=0.5,  color_discrete_sequence=pink_shades_hex)
brand_price_fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=False,
                               width=180, height=180, plot_bgcolor='#dfdae6', paper_bgcolor='#dfdae6',)



body_price = data.groupby(by="Body", as_index=False).agg({"Price" : "mean"})
body_price_fig = px.pie(body_price, values='Price', names='Body', hole=0.5, color_discrete_sequence=pink_shades_hex)
body_price_fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=False,
                              width=180, height=180, plot_bgcolor='#dfdae6',paper_bgcolor='#dfdae6',)




enginetype_milage = data.groupby(by="Engine Type", as_index=False).agg({"Body" : "count"})
enginetype_milage_fig = px.pie(enginetype_milage, values='Body', names='Engine Type', hole=0.5, color_discrete_sequence=pink_shades_hex)
enginetype_milage_fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=False,
                                     width=180, height=180, plot_bgcolor='#dfdae6',paper_bgcolor='#dfdae6',)


# Creating Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

marks_style = {'color': 'blue', 'font-family': 'Arial', 'font-weight': 'bold', 'fontSize': '14px', 'transform': 'rotate(-30deg)'}  # Change font size here


# create layout
app.layout = dbc.Container(
    
    
                            [dbc.Row(
                                [
                                    html.Br(),
                                    html.H2("Overview of the warehouse's cars", style={"color":"#ab00ff"}),
                                    html.Br()
                                      ]),
                         
                            dbc.Row([

                                dbc.Col([
                                    html.Div([
                                    html.H6("Select desired properties:", style={"color":"#ab00ff"}),
                                    dcc.Dropdown(data["Brand"].unique(), placeholder="Brand:", id='brand-dropdown', style={"position" : "relative", "width":"100%", 'responsive' : True}),
                                    html.Div(id='dd-output-container1'),

                                    html.Br(),
                                    dcc.Dropdown(data["Body"].unique(), placeholder="Body Type:", id='body-dropdown', style={"position" : "relative", "width":"100%", 'responsive' : True}),
                                    html.Div(id='dd-output-container2'),

                                    html.Br(),
                                    dcc.Dropdown(data["Engine Type"].unique(), placeholder="Engine Type:", id='engine-dropdown', style={"position" : "relative", "width":"100%", 'responsive' : True}),
                                    html.Div(id='dd-output-container3'),
                             
                                 
                                    html.H4("EngineV:", style={"color":"#ab00ff", 'paddingTop': '10%'} ),
                                    dcc.RangeSlider(
                                        id='range-slider-engine',
                                        marks={data["EngineV"].min(): str(data["EngineV"].min()),  # Display min value as the label
                                            data["EngineV"].max(): str(data["EngineV"].max())},
                                        min=data["EngineV"].min(),
                                        max=data["EngineV"].max(),
                                        value=[data["EngineV"].min(), data["EngineV"].max()],
                                        allowCross=True,
                                        included=True,
                                        pushable=1,
                                        step=1,
                                        updatemode='mouseup',
                                        vertical=False,
                                        verticalHeight=900,
                                        className='range-slider-engine',
                                        tooltip={"placement": "bottom", "always_visible": True},
                                                   
                                                                    ),

                                    


                                    ],style={'position': 'relative','responsive':True, 'top': '5%', 'left': '1%', 'z-index': '1'}),
                                
                     
                                    ], width=2),
                                    
                                dbc.Col([
                                  
                                  # Create a Scatter plot
                                    dcc.Graph(id="scatter-plot",),
                                 
                                    html.H6("Select year interval", style={'paddingTop': '5%', "color":"#ab00ff"}),
                                    dcc.RangeSlider(
                                        id='range-slider',
                                        marks={i: {'label': str(i)} for i in range(data["Year"].min(), data["Year"].max() + 1)},
                                        min=data["Year"].min(),
                                        max=data["Year"].max(),
                                        value=[data["Year"].min(), data["Year"].max()],
                                        allowCross=True,
                                        included=True,
                                        pushable=1,
                                        step=1,
                                        updatemode='mouseup',
                                        vertical=False,
                                        verticalHeight=900,
                                        
                                    
                                    ),
                                    


                                ]  ,style={'responsive':True, "position": "relative", "top":"10%"}, width=10) # this is for column



                                    ]), # this is for row


                        dbc.Row([

                                dbc.Col([
                                        
                                        html.Br(),
                                        html.H6("Average Price per Brand", style={"color":"#ab00ff"}),
                                        dcc.Graph(figure=brand_price_fig, config={ 'displaylogo': False , 'responsive' : True}, id="donut_chart1"),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),
                                        html.Br(),

                                       
                                ], width=2),


                                
                                dbc.Col([
                                        
                                        html.Br(),
                                        html.H6("AVG Price per BodyType", style={"color":"#ab00ff"}),
                                        dcc.Graph(figure=body_price_fig, config={ 'displaylogo': False , 'responsive':True}, id="donut_chart2"),

                                ], width=2),


                                dbc.Col([
                                        
                                        html.Br(),
                                        html.H6('Total Cars per Engine type', style={"color":"#ab00ff"}),
                                        dcc.Graph(figure=enginetype_milage_fig, config={ 'displaylogo': False, 'responsive':True }, id="donut_chart3"),
                                ], width=2),

                                html.Br(),
                                html.Br(),
                                dbc.Col([
                                    html.H6("Scroll:", style={"color":"#ab00ff"}),
                                    html.Div(id='table-container', style={'responsive':True, "position": "relative"})], width=6)
                                


                        ]) # this is for row

                                       

                             


                            


                           #   ] # container children

  #for Html div

], fluid=True,  style={'backgroundColor': '#dfdae6'}, className='my-container' ) # this is for main container










@app.callback(
Output('dd-output-container1', 'children'),
    Input('brand-dropdown', 'value')
)
def update_output(value):
     return html.Div(f'You have selected {value}', style={'color': '#ab00ff'})


@app.callback(
Output('dd-output-container2', 'children'),
    Input('body-dropdown', 'value')
)
def update_output(value):
    return html.Div(f'You have selected {value}', style={'color': '#ab00ff'})

@app.callback(
Output('dd-output-container3', 'children'),
    Input('engine-dropdown', 'value')
)
def update_output(value):
    return html.Div(f'You have selected {value}', style={'color': '#ab00ff'})


# Define the callback to update the graph
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('brand-dropdown', 'value'),
     Input('body-dropdown', 'value'),
     Input('engine-dropdown', 'value'),
     Input('range-slider', 'value'),
     Input('range-slider-engine', 'value')]
)
def update_scatter_plot(brand_value, body_value, engine_value, year_range, selected_engine_value):
    # Filter data based on dropdown and range slider values
    filtered_data = data[
        (data['Brand'] == brand_value if brand_value else True) &
        (data['Body'] == body_value if body_value else True) &
        (data['Engine Type'] == engine_value if engine_value else True) &
        (data['Year'].between(year_range[0], year_range[1]))&
        (data['EngineV'] >= selected_engine_value[0])&
        (data['EngineV'] <= selected_engine_value[1])
    ]


    # Plot the filtered data
    scatter_data = go.Scatter(
        x=filtered_data['Price'],  # Replace 'x_column' with your actual column name
        y=filtered_data['Mileage'],  # Replace 'y_column' with your actual column name
        mode='markers',
        marker=dict(color='#F88379', size=5),
        name='Price Based on mileage',
        text=data.apply(lambda row: f"Brand: {row['Brand']}<br>Price: {row['Price']}<br>Body: {row['Body']}<br>Mileage: {row['Mileage']}<br>EngineV: {row['EngineV']}<br>Engine Type: {row['Engine Type']}<br>Registration: {row['Registration']}<br>Year: {row['Year']}<br>Model: {row['Model']}", axis=1),
        hoverinfo='text'  
    )

    # Layout of the scatter plot
    scatter_layout = go.Layout(
        title='Price Based on mileage',
        xaxis=dict(title='Mileage'),
        yaxis=dict(title='Price'),
        hovermode='closest',
        plot_bgcolor='#dfdae6',
        paper_bgcolor='#dfdae6',
        hoverlabel=dict(bgcolor='#ffd1dc'),
        margin=dict(r=5, l=50, t=50, b=50)
        
    )



    return {'data': [scatter_data], 'layout': scatter_layout}


@app.callback(
    Output('range-slider', 'marks'),
    [Input('range-slider', 'value')]
)
def update_slider_marks(selected_range):
    # Define the default color for non-selected marks
    default_style = {'color': '#ab00ff', 'font-family': 'Arial', 'fontSize': '10px', 'transform': 'rotate(-30deg)'}
    # Define the color for selected marks
    selected_style = {'color': '#F88379', 'font-family': 'Arial', 'font-weight': 'bold', 'fontSize': '10px', 'transform': 'rotate(-30deg)'}

    # Create a dictionary for all marks with the default style
    marks = {i: {'label': str(i), 'style': default_style.copy()} for i in range(data["Year"].min(), data["Year"].max() + 1)}

    # Update the style for the selected marks
    for i in selected_range:
        marks[i]['style'] = selected_style

    return marks




@app.callback(
    Output('table-container', 'children'),
    [Input('brand-dropdown', 'value'),
     Input('body-dropdown', 'value'),
     Input('engine-dropdown', 'value'),
     Input('range-slider', 'value'),
     Input('range-slider-engine', 'value')]
)
def update_table(selected_brand, selected_body, selected_engine, selected_years, selected_engine_value):
    # Filter the DataFrame based on the dropdown selections and year range
    filtered_data = data[
        (data['Brand'].isin([selected_brand]) if selected_brand else True) &
        (data['Body'].isin([selected_body]) if selected_body else True) &
        (data['Engine Type'].isin([selected_engine]) if selected_engine else True) &
        (data['Year'] >= selected_years[0]) &
        (data['Year'] <= selected_years[1]) &
        (data['EngineV'] >= selected_engine_value[0])&
        (data['EngineV'] <= selected_engine_value[1])

    ]

    # Create the table figure with the filtered data
    table_figure = go.Figure(data=[go.Table(
        header=dict(values=list(filtered_data.columns),
                    fill_color='#F88379',
                    align='center'),
        cells=dict(values=[filtered_data[col] for col in filtered_data.columns],
                   fill_color='lavender',
                   align='left')
    )])



    table_figure.update_layout(margin=dict(r=0, l=0, t=0, b=0), height=200)




    # Return a dcc.Graph component that contains the table figure
    return dcc.Graph(figure=table_figure)








if __name__ == '__main__':
    app.run_server(debug=True, port=8080)







