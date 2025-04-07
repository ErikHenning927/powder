import pandas as pd
import os
from datetime import datetime

df = pd.read_csv("finances.csv", delimiter=",")


# ===============
# LLM

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
template = """
Você é um analista de dados, trabalhando em um projeto de limpeza de dados.
Seu trabalho é escolher uma categoria adequada para cada lançamento financeiro
que vou te enviar.

Todos são transações financeiras de uma pessoa física.

Escolha uma dentre as seguintes categorias:
- Alimentação
- Receitas
- Saúde
- Mercado
- Saúde
- Educação
- Compras
- Transporte
- Investimento
- Transferências para terceiros
- Telefone
- Moradia

Escola a categoria deste item:
{text}

Responda apenas com a categoria.
"""

# Local LLM
prompt = PromptTemplate.from_template(template=template)


# Groq
chat = ChatGroq(model="llama3-8b-8192")
chain = prompt | chat | StrOutputParser()

categorias = chain.batch(list(df["Descrição"].values))
df["Categoria"] = categorias

df.to_csv("finances_att.csv", index=False)