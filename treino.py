import streamlit as st
import pandas as pd

# Exemplo de dados
data = {
    'Nome': ['Ana', 'Bruno', 'Carlos', 'Diana'],
    'Nota': [85, 60, 92, 70]
}
df = pd.DataFrame(data)

# Função para colorir as células com base em uma condição
def colorir_celulas(val):
    if val >= 80:
        color = 'background-color: lightgreen'
    elif val >= 70:
        color = 'background-color: lightyellow'
    else:
        color = 'background-color: lightcoral'
    return color

# Aplicando o estilo
styled_df = df.style.applymap(colorir_celulas, subset=['Nota'])

# Exibindo no Streamlit
st.dataframe(styled_df)
