# Run this app with `python app.py` and
from ast import keyword
from dash import Dash, html, dcc
import plotly.express as px
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import base64
import random
import itertools
from dash.exceptions import PreventUpdate
import os
random.seed(42)
import requests
import json

app = Dash(external_stylesheets=[dbc.themes.LUX])
app.title = 'Recommendation System'
app._favicon = ("logo.png")

similar_user_url = 'http://10.138.0.2:2333/similar_user'
similar_product_url = 'http://10.138.0.2:2333/similar_product'
recom_user_url = 'http://10.138.0.2:2333/user_recommend'
recom_product_url = 'http://10.138.0.2:2333/product_recommend'


app.layout = html.Div(
    [
        # add the text header
        html.H2("GNN Recommendation System", style={'textAlign': 'center'}),
        # present the logo.png image
        html.Img(src=app.get_asset_url('logo.png'),
                 style={'width': '20%', 'height': '20%', 
                        'display': 'block', 'margin-left': 'auto',
                        'margin-right': 'auto'}),
        html.Br(),
        html.Br(),
        html.P("This recommendation system can do four different jobs.",
               style={'textAlign': 'center'}),
        html.P("1. Find the emails of similar users given a user email. Input the user email and a topk number",
               style={'textAlign': 'center'}),
        html.P("2. Find the skus of similar products given a product sku. Input the product sku and a topk number",
               style={'textAlign': 'center'}),
        html.P("3. Recommend the skus of similar products given a user email. Input the user email and a topk number",
               style={'textAlign': 'center'}),
        html.P("4. Recommend the emails of users given a product sku. Input the product sku and a topk number",
               style={'textAlign': 'center'}),
        dcc.Dropdown(
            id = 'functionality',
            options = [
                "Find Similar Users",
                "Find Similar Products",
                "Recommend Products",
                "Recommend Users"
            ],
            placeholder="Select the functionality you want to use",
            value = None,
            style={'width': '75%', 
                    'display': 'inline-block',
                    'align-items': 'center',
                    'justify-content': 'center'}
        ),
        html.Br(),
        html.Br(),
        dcc.Input(id="input1", type="text", placeholder="Email or SKU", style={'marginRight':'10px'}),
        dcc.Input(id="input2", type="text", placeholder="Topk number", debounce=True),
        
        html.Button('QUERY', id='generate_button', n_clicks=0),
        html.Div(id='generated_result')
    ],
    style={'margin-bottom': '10px',
           'textAlign':'center',
           'width': '1000px',
           'margin':'auto'}
)


@app.callback(Output('generated_result', 'children'),
              Input('generate_button', 'n_clicks'),
              State('input1', 'value'),
              State('input2', 'value'),
              State('functionality', 'value'))
def update_graph(n_clicks, input1, input2, functionality):
    if n_clicks == 0 or not functionality or not input1 or not input2:
        raise PreventUpdate
    url = ""
    if functionality == "Find Similar Users":
        url = similar_user_url
    elif functionality == "Find Similar Products":
        url = similar_product_url
    elif functionality == "Recommend Products":
        url = recom_product_url
    else:
        url = recom_user_url
    
    if functionality in {"Find Similar Users", "Recommend Products"}:
        keyword1 = 'user_email'
    else:
        keyword1 = 'product_sku'
        
        
    payload = json.dumps({
        keyword1: str(input1),
        "topk": int(input2)
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # get dict from json format
    dict_response = json.loads(response.text)
    results = list(dict_response.values())[0]
    
    if functionality in {"Find Similar Users", "Recommend Users"}:
        keyword2 = 'user_email'
    else:
        keyword2 = 'product_sku'
    if type(results) == list:
        return html.Ol([html.Li(str(res[keyword2])) for res in results],
                   style={'textAlign': 'center'})
    else:
        return html.P("Current search is not supported! Try different email or sku.",
                      style={'textAlign': 'center'})
    


if __name__ == '__main__':
    app.run_server(port=5438,host='0.0.0.0',debug=False)
