import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')

def create_db_and_table(dbname, user, password, host, port):

    conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    # Criar o banco de dados
    try:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
    except psycopg2.errors.DuplicateDatabase:
        print(f"Banco de dados '{dbname}' já existe.")
    
    cursor.close()
    conn.close()

    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS banco_central (
        Data DATE,
        Quantidade BIGINT,
        Valor NUMERIC,
        Denominacao NUMERIC,
        Especie VARCHAR(50)
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Banco de dados '{dbname}' e tabela 'banco_central' criados com sucesso.")

create_db_and_table('powder_db', db_user, db_password, host, port)
