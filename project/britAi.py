import openai
from dotenv import load_dotenv, find_dotenv
import os
import sys
import json
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connections.all_connections import db_local, dw


load_dotenv(find_dotenv())


client = openai.OpenAI()

def obter_dados_do_banco():
    connection = db_local()
    c = connection.cursor()
    query = """
    SELECT
        orderid,
        id_vtexsalesChannel,
        id_client_cpf,
        transactionId,
        id_status,
        items_totals,
        discounts_totals,
        shipping_totals,
        tax_totals,
        [sequence],
        marketplaceOrderId,
        sellerOrderId,
        origin,
        CONVERT(DATE, creationDate) as creationDate,
        CONVERT(DATE, lastChange) as lastChange, 
        orderGroup,
        hostname,
        openTextField,
        isCompleted,
        roundingError,
        orderFormId,
        allowCancellation,
        CONVERT(DATE, cancellationDate) as cancellationDate,
        CONVERT(DATE, authorizedDate) as authorizedDate,
        CONVERT(DATE, invoicedDate) as invoicedDate,
        cancelReason,
        cancelledBy,
        mlOrderids,
        mlPackid,
        value
    FROM
        vtex_orders;

    """
    c.execute(query)
    
    colunas = [desc[0].strip() for desc in c.description]  
    resultados = c.fetchall()  

    connection.close()

    print(f"Total de registros: {len(resultados)}")
    print(f"Colunas encontradas: {colunas}")
    print(f"Exemplo de registro retornado: {resultados[0] if resultados else 'Nenhum dado encontrado'}")

    if not resultados:
        print("Nenhum dado encontrado.")
        return None

    df = pd.DataFrame([list(row) for row in resultados], columns=colunas)

    json_dados = df.head(10).to_json(orient="records")

    return json_dados

def analisar_dados_openai(dados_json):
    if not dados_json:
        return "Não há dados disponíveis para análise."

    prompt = f"""
    Análise os seguintes dados extraídos do banco de dados:
    
    {dados_json}
    
    Identifique qual foi o salesChannel que mais vendeu.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


dados = obter_dados_do_banco()

if dados:
    resultado = analisar_dados_openai(dados)
    print("🔹 Análise da OpenAI 🔹")
    print(resultado)
