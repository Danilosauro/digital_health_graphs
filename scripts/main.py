import streamlit as st
import pandas as pd  
import matplotlib.pyplot as plt 
import plotly.express as px

# leitura de dados
data = pd.read_parquet('../data/mock_data.parquet', engine='pyarrow') 
min_year = data['data'].min() 
min_year = min_year.year
max_year = data['data'].max() 
max_year = max_year.year 

# título da página
st.title("Análise dos dados da clínica")
st.write(f'### Dados referentes ao período {min_year} e {max_year}')


# agregação de soma dos dados
data_agg_sum = data.groupby('plano').agg({
    'pagamento': 'sum',
    'saida': 'sum',
    'saldo': 'sum',
    'plano': 'count'
}).rename(columns={'plano': 'frequencia'}).reset_index() 


# frequencia dos planos
st.subheader("Frequência dos Planos")

plan_frequencies = px.bar(data_agg_sum.sort_values(by='frequencia', ascending=False),
                  x='plano', y='frequencia',
                  labels={'plano': 'Plano', 'frequencia': 'Frequência'},
                  title='Planos Mais Frequentes')

st.plotly_chart(plan_frequencies, use_container_width=True)


# entradas, saídas e saldo 
st.subheader("Entradas, Saídas e Saldo por Plano")

for col in ['pagamento', 'saida', 'saldo']:
    fig = px.bar(data_agg_sum.sort_values(by=col, ascending=False),
                 x='plano', y=col,
                 labels={'plano': 'Plano', col: col.capitalize()},
                 title=f'{col.capitalize()} por Plano')
    st.plotly_chart(fig, use_container_width=True)


# grafico entrada por mes 
data['data'] = pd.to_datetime(data['data'], errors='coerce')
data['mes_nome'] = data['data'].dt.strftime('%b')
data['mes_num'] = data['data'].dt.month

# Agrupamento por plano e mês
data_mes = data.groupby(['plano', 'mes_num', 'mes_nome'], as_index=False).agg({
    'pagamento': 'sum',
    'saida': 'sum'
})

# Ordenar os meses corretamente
data_mes = data_mes.sort_values('mes_num') 


st.subheader("📅 Entradas e Saídas por Mês e Plano")

# Melt para formato longo
data_melt = data_mes.melt(id_vars=['plano', 'mes_num', 'mes_nome'],
                      value_vars=['pagamento', 'saida'],
                      var_name='tipo', value_name='valor')

# Filtro de plano
planos = data_melt['plano'].unique()
plano_selecionado = st.selectbox("Selecione um plano", planos)

df_filtrado = data_melt[data_melt['plano'] == plano_selecionado]

# Gráfico
fig = px.line(df_filtrado, 
              x='mes_nome', y='valor', color='tipo', 
              category_orders={'mes_nome': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']},
              markers=True,
              labels={'valor': 'Valor', 'mes_nome': 'Mês', 'tipo': 'Tipo'},
              title=f'Evolução Mensal de Entradas e Saídas - {plano_selecionado}')

st.plotly_chart(fig, use_container_width=True)