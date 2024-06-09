import requests
import pandas as pd
import psycopg2

def fetch_data_bcb(base_url, top, skip):
    print(f'Fetching data: top={top}, skip={skip}')
    url = f'{base_url}?$top={top}&$skip={skip}&$orderby=Data%20desc&$format=json'
    resposta = requests.get(url)
    resposta.raise_for_status()  # Levanta um erro se a requisição falhar
    dados = resposta.json()
    print(f'Fetched {len(dados["value"])} records')
    return pd.DataFrame(dados["value"])

def insert_data(dataframe, conn):
    cursor = conn.cursor()
    total_rows = len(dataframe)
    print(f'Inserting {total_rows} records into the database')
    for i, (_, row) in enumerate(dataframe.iterrows(), start=1):
        cursor.execute(
            """
            INSERT INTO banco_central (Data, Quantidade, Valor, Denominacao, Especie)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (row['Data'], row['Quantidade'], row['Valor'], row['Denominacao'], row['Especie'])
        )
        if i % 100 == 0 or i == total_rows:
            print(f'{i} records inserted')
    conn.commit()
    cursor.close()
    print('Data insertion completed')

def main():
    base_url = 'https://olinda.bcb.gov.br/olinda/servico/mecir_dinheiro_em_circulacao/versao/v1/odata/informacoes_diarias'
    top = 10000
    skip = 0
    tabela_final = pd.DataFrame()

    print('Starting data fetching process...')
    while True:
        tabela = fetch_data_bcb(base_url, top, skip)
        if tabela.empty:
            print('No more data to fetch')
            break
        tabela_final = pd.concat([tabela_final, tabela], ignore_index=True)
        skip += top
    print('Data fetching process completed')

    print('Connecting to the database...')
    conn = psycopg2.connect(dbname='powder_db', user='postgres', password='postgres', host='localhost', port='5432')
    print('Database connection established')

    insert_data(tabela_final, conn)

    conn.close()
    print('Database connection closed')

    print('Process completed successfully')
    print(tabela_final)

if __name__ == '__main__':
    main()
