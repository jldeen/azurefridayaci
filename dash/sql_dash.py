import os
import socket, struct
import sys
import time
import warnings
import requests
import dns.resolver
import psycopg2
import datetime

import plotly
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

# Database modules
import pyodbc
import pymysql


# Style
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Layout
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = dbc.Container([
        dbc.Row(
            html.Table([
                html.Tr([
                    html.Td(html.A('Github repo', href='https://github.com/jldeen/azurefridayaci'), style={'width': '20%'}),
                    html.Td(html.H4('Application dashboard'), style={'width': '60%', 'textAlign': 'center'}),
                    html.Td(html.Img(src = app.get_asset_url('azurelogo.png'), width = 200), style={'width': '20%'})
                ])
            ], style={'width': '100%'})
        ),
        html.Div(html.P("The following image describes the overall architecture: Azure Application Gateway acts as frontend to production and staging farms, using Azure private DNS zones for service discovery. Traffic is encrypted end-to-end.")),
        html.Div(html.Img(src = app.get_asset_url('nginx-sidecar.png'), width = '100%'), style={'width':'75%', 'margin':25, 'textAlign': 'center'}),
        html.Div(html.P("This chart shows the source IP addresses that have sent traffic to the production database. All traffic is coming from private addresses, and the configuration for the application gateway backends does not need to be modified thanks the the DNS-based service discovery mechanism.")),
        html.Div(id='accessgraph'),
        html.Div(html.P("The previous chart is updated in real time every 2s")),
        dcc.Interval(
            id='interval-component',
            interval=1*2000, # in milliseconds
            n_intervals=0
        )
    ])

# Callbacks
@app.callback(Output(component_id='accessgraph', component_property='children'),
              Input('interval-component', 'n_intervals'))
def render_graph(n):
    try:
        # Get info and build the connection to the SQL server
        if sql_engine == "sqlserver":
            drivers = pyodbc.drivers()
            # print('Available ODBC drivers:', drivers)   # DEBUG
            if len(drivers) == 0:
                # app.logger.error('Oh oh, it looks like you have no ODBC drivers installed :(')
                print('Oh oh, it looks like you have no ODBC drivers installed :(')
            else:
                # Take first driver, for our basic stuff any should do
                driver = drivers[0]
                if sql_server_db == None:
                    # app.logger.info("Building connection string with no Database")
                    print("Building connection string with no Database")
                    cx_string = "Driver={{{0}}};Server=tcp:{1},1433;Uid={2};Pwd={3};Encrypt=yes;TrustServerCertificate=yes;Connection Timeut=30;".format(driver, sql_server_fqdn, sql_server_username, sql_server_password)
                else:
                    # app.logger.info("Building connection string with Database")
                    print("Building connection string with Database")
                    cx_string = "Driver={{{0}}};Server=tcp:{1},1433;Database={2};Uid={3};Pwd={4};Encrypt=yes;TrustServerCertificate=yes;Connection Timeut=30;".format(driver, sql_server_fqdn, sql_server_db, sql_server_username, sql_server_password)
                # app.logger.info('connection string: ' + cx_string)
                print('connection string: ' + cx_string)
            # Connect to DB
            # app.logger.info('Connecting to database server ' + sql_server_fqdn + ' - ' + get_ip(sql_server_fqdn) + '...')
            print('Connecting to database server ' + sql_server_fqdn + ' - ' + get_ip(sql_server_fqdn) + '...')
            try:
                cx = init_odbc(cx_string)
                cx.add_output_converter(-150, handle_sql_variant_as_string)
                cursor = cx.cursor()
            except Exception as e:
                if is_valid_ipv4_address(sql_server_fqdn):
                    error_msg = 'SQL Server FQDN should not be an IP address when targeting Azure SQL Database, maybe this is a problem?'
                else:
                    error_msg = 'Connection to server ' + sql_server_fqdn + ' failed, you might have to update the firewall rules or check your credentials?'
                # app.logger.info(error_msg)
                # app.logger.error(e)
                print(error_msg)
                print(e)
        else:
            app.logger.error('Sorry, this dashboard only supports the SQL Server, MySQL and Postgres are on the roadmap')

        # Send Query
        app.logger.info("Sending SQL query to cursor...")
        print("Sending SQL query...")
        sql_query = "SELECT ip, COUNT(ip) FROM srciplog GROUP BY ip;"
        cursor.execute(sql_query)
        sql_result = cursor.fetchall()
        app.logger.info("Data retrieved: {0}".format(str(sql_result)))
        # Separate data in two lists, one for each axis
        x_axis=[sql_result[i][0] for i in range(0, len(sql_result))]
        y_axis=[sql_result[i][1] for i in range(0, len(sql_result))]
    except Exception as e:
        app.logger.info("Error: {0}".format(str(e)))
        x_axis = []
        y_axis = []
    # Return graph object
    app.logger.info("Graphing x: {0} and y: {1}".format(str(x_axis), str(y_axis)))
    return [dcc.Graph(
        figure={
            'data': [
                {'x': x_axis, 'y': y_axis, 'type': 'bar', 'name': 'Source IP'}
            ],
            'layout': go.Layout(title='SQL connections to database')
         }
    )]

# Get variable values from environment variables or from the file system
def get_variable_value(variable_name, default_value = None):
    variable_value = os.environ.get(variable_name)
    basis_path='/secrets'
    variable_path = os.path.join(basis_path, variable_name)
    if variable_value == None and os.path.isfile(variable_path):
        with open(variable_path, 'r') as file:
            variable_value = file.read().replace('\n', '')
    if (variable_value == None) and (default_value != None):
        variable_value = default_value
    return variable_value

# Gets the web port out of an environment variable, or defaults to 8080
def get_web_port():
    web_port=os.environ.get('PORT')
    if web_port==None or not web_port.isnumeric():
        print("Using default port 8050")
        web_port=8050
    else:
        print("Port supplied as environment variable:", web_port)
    return web_port

# Gets the current IP
def get_ip(d):
    try:
        return socket.gethostbyname(d)
    except Exception:
        return False

# Return True if string argument is a valid IP address
def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False
    return True

# Initialize ODBC connection to database
def init_odbc(cx_string):
    cnxn = pyodbc.connect(cx_string)
    return cnxn

# To add to SQL cx to handle output
def handle_sql_variant_as_string(value):
    # return value.decode('utf-16le')
    return value.decode('utf-8')

# Global variables
print ("Initializing variables...")
sql_server_fqdn = get_variable_value('SQL_SERVER_FQDN')
sql_server_db = get_variable_value('SQL_SERVER_DB')
sql_server_username = get_variable_value('SQL_SERVER_USERNAME')
sql_server_password = get_variable_value('SQL_SERVER_PASSWORD')
sql_engine = get_variable_value('SQL_ENGINE', default_value='sqlserver')
use_ssl = get_variable_value('USE_SSL')

if __name__ == '__main__':
    # Initialize
    cx_string=''
    web_port=get_web_port()

    # Start web server
    print ("Starting web server...")
    app.run_server(use_reloader=False,
        debug=True,
        host="0.0.0.0")
