import pyodbc
import os
from dotenv import load_dotenv

def dw():
    server_dw = os.getenv("server_dw")
    username_dw = os.getenv("username_dw")
    password_dw = os.getenv("password_dw")
    port_dw = os.getenv("port_dw")
    server = server_dw
    database = 'dw'  
    username = username_dw
    password = password_dw
    port = port_dw

    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server},{port};DATABASE={database};UID={username};PWD={password}'
    try:
        conn = pyodbc.connect(connection_string, timeout=60)
        print("Conexão estabelecida com sucesso!")

        return conn
    except Exception as e:
        print(f"Erro ao conectar: {e}")

def dw_local():
    server = '10.0.10.188'
    database = 'DW'
    trusted_connection = 'yes'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};Trusted_Connection={trusted_connection};'
    try:
        conn = pyodbc.connect(connection_string)
        print("Conexão realizada com sucesso!")
        return conn
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return None

def db_local():
    server = 'localhost,1433'
    database = 'master' 
    username = 'sa'
    password = 'Python123'

    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    try:
        conn = pyodbc.connect(connection_string)
        print("Conexão estabelecida com sucesso!")

        return conn
    except Exception as e:
        print(f"Erro ao conectar: {e}")