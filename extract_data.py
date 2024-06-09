import requests
import pandas as pd
import psycopg2

def fetch_data_bcb(base_url, top, skip):
    url = f'{base_url}?$top={top}&$skip={skip}&$orderby=Data%20desc&$format=json'
    resposta = requests.get(url)
    resposta.raise_for_status()  # Levanta um erro se a requisição falhar
    dados = resposta.json()
    return pd.DataFrame(dados["value"])

def insert_data(dataframe, conn):
    cursor = conn.cursor()
    for _, row in dataframe.iterrows():
        cursor.execute(
            """
            INSERT INTO banco_central (Data, Quantidade, Valor, Denominacao, Especie)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (row['Data'], row['Quantidade'], row['Valor'], row['Denominacao'], row['Especie'])
        )
    conn.commit()
    cursor.close()

def main():
    base_url = 'https://olinda.bcb.gov.br/olinda/servico/mecir_dinheiro_em_circulacao/versao/v1/odata/informacoes_diarias'
    top = 10000
    skip = 0
    tabela_final = pd.DataFrame()

    while True:
        tabela = fetch_data_bcb(base_url, top, skip)
        if tabela.empty:
            break
        tabela_final = pd.concat([tabela_final, tabela], ignore_index=True)
        skip += top

    conn = psycopg2.connect(dbname='powder_db', user='postgres', password='postgres', host='localhost', port='5432')

    insert_data(tabela_final, conn)

    conn.close()

    print('Dados inseridos no banco de dados com sucesso')
    print(tabela_final)

if __name__ == '__main__':
    main()
