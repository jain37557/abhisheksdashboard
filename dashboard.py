#### This is the primary code for the dashboard. Please make sure that all the input files are intact in the root directory. 
##This all are the necesscary imports. Make sure all the dependencies are installed from the requirements.txt file.
import dash
import dash_auth
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import base64
import json

colors = {   
    'background': '#ffffff',  #Background color for the application, this is used everywhere
    'text': '#002f66',
    'solar':'#fff3e0',
    'wind':'#e0ebff'       #Text color for the application, this is used everywhere
}
config = {"toImageButtonOptions": {"width": None, "height": None}}   #This ensures that when the plot is downloaded from the dashboard, it retains the original dimensions. 
image_filename='logo.png' #Image fill needs to be in the root directory
encoded_image = base64.b64encode(open(image_filename, 'rb').read()) 
solardf=pd.read_csv(r'2018solardata_noedit.csv')
solardf=solardf.dropna(subset=['Capacity Factor'])
winddf=pd.read_csv(r'2018winddata_noedit.csv')
winddf=winddf.dropna(subset=['Capacity Factor'])

def getsolarmap(value1):
    solardf2=solardf[(solardf['Capacity Factor']>value1[0]) & (solardf['Capacity Factor']<value1[1])]
    map1=px.scatter_mapbox(solardf2,lat="Latitude",lon="Longitude",hover_name="Plant Name",color='Capacity Factor',size='Nameplate Capacity',hover_data=["State","Balancing Authority Name"],color_continuous_scale='Jet',zoom=3,size_max=20)
    map1.update_layout(mapbox_style="open-street-map",margin={"r":0,"t":0,"l":0,"b":0})  
    map1.update_traces(opacity=1.0)
    return map1

def getsolarplot(value1):
    solardf2=solardf[(solardf['Capacity Factor']>value1[0]) & (solardf['Capacity Factor']<value1[1])]
    fig1 = px.histogram(solardf2, y="Nameplate Capacity", x="Capacity Factor", marginal="box",color_discrete_sequence=['#86919c'],labels={'Nameplate Capacity':'Nameplate Capacity (MW)'})
    fig1.update_layout(title="Histogram and Boxplot for the solar projects shown above",paper_bgcolor='#fff3e0')
    return fig1

def getwindmap(value1):
    winddf2=winddf[(winddf['Capacity Factor']>value1[0]) & (winddf['Capacity Factor']<value1[1])]
    map2=px.scatter_mapbox(winddf2,lat="Latitude",lon="Longitude",hover_name="Plant Name",color='Capacity Factor',size='Nameplate Capacity',hover_data=["State","Balancing Authority Name"],color_continuous_scale='Jet',zoom=3,size_max=20)
    map2.update_layout(mapbox_style="open-street-map",margin={"r":0,"t":0,"l":0,"b":0})  
    map2.update_traces(opacity=1.0)
    return map2

def getwindplot(value1):
    winddf2=winddf[(winddf['Capacity Factor']>value1[0]) & (winddf['Capacity Factor']<value1[1])]
    fig2 = px.histogram(winddf2, y="Nameplate Capacity", x="Capacity Factor", marginal="box",color_discrete_sequence=['#86919c'],labels={'Nameplate Capacity':'Nameplate Capacity (MW)'})
    fig2.update_layout(title="Histogram and Boxplot for the wind projects shown above",paper_bgcolor='#e0ebff')
    return fig2


app = dash.Dash(__name__) #The application gets created with this line. 
app.title = "Abhishek's Dashboard" ##This is what the tab on the browser says. 
server = app.server
app.layout = html.Div(id='primary',children=[
    html.Div(id='header',children=[
        html.Div(children=[
            html.Div(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),style={'textAlign':'center','height':'12%','width':'12%'}),style={'justify-content':'center'}), #The logo comes on here.
            html.Div(id='buffer1',style={'height':'20px'}),
            html.H1('Abhishek Sanjay Jain',style={'fontSize':'250%'}),
            html.H3('Master of Environmental Management Candidate 2021',style={'fontSize':'150%'}),
            html.Div(children=[
                html.A(children='LinkedIn Profile  |', id='link',
                        href='https://www.linkedin.com/in/abhisheksjain/', target='_blank'),
                html.A(children='  GitHub Repository', id='link2',
                        href='https://github.com/jain37557/abhisheksdashboard', target='_blank'),
                html.Div(id='buffer2',style={'height':'20px'}),                 
                html.P('''This dashboard is made using only open source tools! The data is sourced from EPA's Emissions & Generation Resource
                        Integrated Database (eGRID) 2018. It represents the performance characterisitics of almost all 
                        solar and wind electric power generated in the United States. Through this dasboard, we can manifest a powerful way
                        of visualizing and analyzing interactive data.
                        The visualizations below represent the relationship between the capacity factor and nameplate capacity (MW) of all
                        solar and wind electric power stations. The histogram tells a deeper story
                        around the distribution of capacity with increasing capacity factor. Hover over the data points to examine the metadata.''',style={'border':'1px black solid','fontSize':'110%'})
            ])],style={'display':'center','width':'100%','display':'inline-block'})
        ],style={"border":"1px black",'width':'100%','display':'center','textAlign':'center'}),
        html.Div(id='all',children=[ 
                html.Div(id='allsolar',children=[
                        html.H4('[Solar] Nameplate Capacity (MW, Size) and Capacity Factor (Adjust slider below, Color)'),
                        dcc.RangeSlider(
                            id='solar-slider',
                            min=0,
                            max=1,
                            step=0.05,
                            value=[0,1],
                            marks={
                                0:{'label':'0'},
                                0.2:{'label':'0.2'},
                                0.4:{'label':'0.4'},
                                0.6:{'label':'0.6'},
                                0.8:{'label':'0.8'},
                                1:{'label':'1'}
                            }
                        ),
                        dcc.Graph(id='solarmap',config=config),
                        dcc.Graph(id='solarplot',config=config)
                ],style={'textAlign':'center',"border":"1px orange solid",'backgroundColor':colors['solar'],'width':'49.5%','display':'inline-block'}),
                html.Div(id='spacer',style={'width':'1%','display':'inline-block'}),
                html.Div(id='allwind',children=[
                        html.H4('[Wind] Nameplate Capacity (MW, Size) and Capacity Factor (Adjust slider below, Color)'),
                        dcc.RangeSlider(
                            id='wind-slider',
                            min=0,
                            max=1,
                            step=0.05,
                            value=[0,1],
                            marks={
                                0:{'label':'0'},
                                0.2:{'label':'0.2'},
                                0.4:{'label':'0.4'},
                                0.6:{'label':'0.6'},
                                0.8:{'label':'0.8'},
                                1:{'label':'1'}
                            }
                        ),
                        dcc.Graph(id='windmap',config=config),
                        dcc.Graph(id='windplot',config=config)
                ],style={'backgroundColor':colors['wind'],'textAlign':'center',"border":"1px skyblue solid",'width':'49%','display':'inline-block'})
        ],style={'width':'100%','display':'center'}),
],style={'color':colors['text'],'backgroundColor':colors['background']})


@app.callback(dash.dependencies.Output('solarmap','figure'),
            [dash.dependencies.Input('solar-slider','value')])
def output_fig(value):
    return getsolarmap(value)

@app.callback(dash.dependencies.Output('solarplot','figure'),
            [dash.dependencies.Input('solar-slider','value')])
def output_fig(value):
    return getsolarplot(value)

@app.callback(dash.dependencies.Output('windmap','figure'),
            [dash.dependencies.Input('wind-slider','value')])
def output_fig(value):
    return getwindmap(value)

@app.callback(dash.dependencies.Output('windplot','figure'),
            [dash.dependencies.Input('wind-slider','value')])
def output_fig(value):
    return getwindplot(value)


if __name__ == '__main__':
    app.run_server() ##Remove Debug argument before hosting