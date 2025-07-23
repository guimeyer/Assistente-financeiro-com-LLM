import streamlit as st

# Dicionário para mapear números dos meses para nomes
mes_nome = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

st.set_page_config(layout='wide')
st.title('Dashboard de Finanças Pessoais')

# Garantir que coluna Mês é inteira e sem nulos
meses_disponiveis = sorted(df['Mês'].dropna().astype(int).unique())
# Criar lista de nomes dos meses para o selectbox
meses_opcoes = [mes_nome[m] for m in meses_disponiveis]

# Seleção do mês pelo nome, com valor padrão o primeiro disponível
mes_escolhido_nome = st.sidebar.selectbox('Mês', meses_opcoes, index=0)
# Converter nome do mês escolhido para número
mes_escolhido = [num for num, nome in mes_nome.items() if nome == mes_escolhido_nome][0]

# Categorias ordenadas e sem nulos
categories = sorted(df['Categoria'].dropna().unique())
selected_categories = st.sidebar.multiselect(
    'Filtrar por Categorias',
    categories,
    default=categories
)

# Usa o mês selecionado já convertido para número
df_filtered = filter_data(df, mes=mes_escolhido, selected_categories=selected_categories)

c1, c2 = st.columns([0.6, 0.4])

c1.subheader("📋 Transações Filtradas")
c1.dataframe(df_filtered, use_container_width=True)

import plotly.express as px

category_distribution = df_filtered.groupby('Categoria')['Valor'].sum().reset_index()
fig = px.pie(category_distribution, values = 'Valor',
             names = 'Categoria',
             title = 'Distribuição por Categoria', 
             hole = 0.3)

if not df_filtered.empty:
    category_distribution = df_filtered.groupby('Categoria')['Valor'].sum().reset_index()
    fig = px.pie(
        category_distribution,
        values='Valor',
        names='Categoria',
        title='Distribuição por Categoria',
        hole=0.3
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhuma transação encontrada para os filtros selecionados.")
