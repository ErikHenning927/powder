import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

df = pd.read_csv("finances.csv", delimiter=';')
del df['ID']    

#df = df[df["Categoria"]!="Receitas"]
df["Valor"] = df["Valor"]

def filter_data(df, mes, selected_categories):
    df_filtered = df[df['Mês'] == mes]
    if selected_categories:
        df_filtered = df_filtered[df_filtered['Categoria'].isin(selected_categories)]
    return df_filtered

# Título do Dashboard
st.title("Controle financeiro")

# Filtros de data
st.sidebar.header("Filtros")

# Definir intervalo de data
mes = st.sidebar.selectbox("Mês", df["Mês"].unique())

# Filtro de categoria
categories = df["Categoria"].unique().tolist()
selected_categories = st.sidebar.multiselect("Filtrar por Categorias", categories, default=categories)

df_filtered = filter_data(df, mes, selected_categories)
total = df_filtered[df_filtered["Categoria"] != "Receitas"]["Valor"].sum()
st.sidebar.write(f"Total {mes}: R$ {total:.2f}")

# ====================
c1, c2 = st.columns([0.6, 0.4])

c1.subheader("Tabela de Finanças")
c1.dataframe(df_filtered)
 

c2.subheader("Distribuição de Categorias")
category_distribution = df_filtered.groupby("Categoria")["Valor"].sum().reset_index()
fig = px.pie(category_distribution, values='Valor', names='Categoria', 
            title='Distribuição por Categoria', hole=0.3
                )
c2.plotly_chart(fig, use_container_width=True)

# Subtítulo
st.subheader("Receita vs Despesas")

# Filtra os dados por mês
df_mes = df[df['Mês'] == mes]

# Calcula os totais
receita_total = df_mes[df_mes["Categoria"] == "Receitas"]["Valor"].sum()
despesa_total = df_mes[df_mes["Categoria"] != "Receitas"]["Valor"].sum()
percentual = (despesa_total / receita_total) * 100 if receita_total != 0 else 0
st.subheader(f"Receita x Despesas ({mes}) - Despesas são {percentual:.2f}% da Receita")

# Prepara dados para gráfico
df_grafico = pd.DataFrame({
    "Tipo": ["Receita", "Despesa"],
    "Valor": [receita_total, despesa_total]
})

# Gráfico de pizza
fig = px.pie(df_grafico, values='Valor', names='Tipo', title='Distribuição Receita vs Despesa', hole=0.4)
st.plotly_chart(fig)