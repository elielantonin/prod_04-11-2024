import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Função para calcular o total de pagamentos
def calcular_total_pagamentos():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(valor) FROM pagamentos")
    total = cursor.fetchone()[0]  # Retorna None se não houver valores
    conn.close()
    return total if total is not None else 0

# Função para obter dados de pagamentos com filtros
def obter_dados_pagamentos(unidade=None, data_inicio=None, data_fim=None):
    conn = sqlite3.connect('database.db')
    query = "SELECT unidade, data_pagamento, plano, valor FROM pagamentos WHERE 1=1"
    params = []

    if unidade:
        query += " AND unidade = ?"
        params.append(unidade)
    if data_inicio:
        query += " AND data_pagamento >= ?"
        params.append(data_inicio.strftime('%Y-%m-%d'))
    if data_fim:
        query += " AND data_pagamento <= ?"
        params.append(data_fim.strftime('%Y-%m-%d'))

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

# Configuração do Streamlit
st.title("Dashboard de Pagamentos")

# Exibe o total dos pagamentos
total_pagamentos = calcular_total_pagamentos()
st.write(f"O total dos pagamentos é: R$ {total_pagamentos:.2f}")

# Filtros de seleção
data_atual = pd.to_datetime("today").normalize()  # Data atual sem hora
data_inicio = st.date_input("Data de início", value=data_atual)
data_fim = st.date_input("Data de fim", value=data_atual)

# Configuração das abas
tab1, tab2, tab3 = st.tabs(["\U0001F4C1 Dados Gerais", "\U0001F4C1 Por Plano", "\U0001F4C1 Editar/Excluir"])

# Aba 1: Dados Gerais
with tab1:
    # Obter dados filtrados para ambas as academias
    df_academia_i = obter_dados_pagamentos(unidade='Academia I', data_inicio=data_inicio, data_fim=data_fim)
    df_academia_ii = obter_dados_pagamentos(unidade='Academia II', data_inicio=data_inicio, data_fim=data_fim)

    # Verificar e exibir dados para Academia I
    if not df_academia_i.empty:
        df_academia_i['data_pagamento'] = pd.to_datetime(df_academia_i['data_pagamento'])
        df_mensal_i = df_academia_i.groupby(df_academia_i['data_pagamento'].dt.to_period("M"))['valor'].sum().reset_index()

        fig, ax = plt.subplots()
        bars = ax.bar(df_mensal_i['data_pagamento'].astype(str), df_mensal_i['valor'], color="skyblue")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Valor dos Pagamentos")
        ax.set_title("Pagamentos Mensais - Academia I")
        plt.xticks(rotation=45)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, f'R$ {yval:.2f}', ha='center', va='bottom')

        st.pyplot(fig)
    else:
        st.write("Nenhum dado encontrado para Academia I no período selecionado.")

    # Verificar e exibir dados para Academia II
    if not df_academia_ii.empty:
        df_academia_ii['data_pagamento'] = pd.to_datetime(df_academia_ii['data_pagamento'])
        df_mensal_ii = df_academia_ii.groupby(df_academia_ii['data_pagamento'].dt.to_period("M"))['valor'].sum().reset_index()

        fig, ax = plt.subplots()
        bars = ax.bar(df_mensal_ii['data_pagamento'].astype(str), df_mensal_ii['valor'], color="blue")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Valor dos Pagamentos")
        ax.set_title("Pagamentos Mensais - Academia II")
        plt.xticks(rotation=45)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, f'R$ {yval:.2f}', ha='center', va='bottom')

        st.pyplot(fig)
    else:
        st.write("Nenhum dado encontrado para Academia II no período selecionado.")

# Aba 2: Por Plano
with tab2:
    # Verificar e exibir dados para Academia I por plano
    if not df_academia_i.empty:
        df_plano_i = df_academia_i.groupby('plano')['valor'].sum().reset_index()

        fig, ax = plt.subplots()
        bars = ax.bar(df_plano_i['plano'], df_plano_i['valor'], color="lightgreen")
        ax.set_xlabel("Plano")
        ax.set_ylabel("Valor dos Pagamentos")
        ax.set_title("Pagamentos por Plano - Academia I")

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, f'R$ {yval:.2f}', ha='center', va='bottom')

        st.pyplot(fig)
    else:
        st.write("Nenhum dado encontrado para Academia I no período selecionado.")

    # Verificar e exibir dados para Academia II por plano
    if not df_academia_ii.empty:
        df_plano_ii = df_academia_ii.groupby('plano')['valor'].sum().reset_index()

        fig, ax = plt.subplots()
        bars = ax.bar(df_plano_ii['plano'], df_plano_ii['valor'], color="orange")
        ax.set_xlabel("Plano")
        ax.set_ylabel("Valor dos Pagamentos")
        ax.set_title("Pagamentos por Plano - Academia II")

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, f'R$ {yval:.2f}', ha='center', va='bottom')

        st.pyplot(fig)
    else:
        st.write("Nenhum dado encontrado para Academia II no período selecionado.")

# Aba 3: Editar/Excluir (Pode ser implementada posteriormente com opções de edição e exclusão de registros)
with tab3:
    st.write("Funcionalidade de edição e exclusão em desenvolvimento.")
