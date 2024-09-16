import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração para o layout de largura completa
st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    data = pd.read_csv('top_prefeitos_gastos.csv')
    return data

@st.cache_data
def load_data_vereadores():
    data = pd.read_csv('top_vereadores_gastos.csv')
    return data

# Carregar os dados
top_prefeitos = load_data()
top_vereadores = load_data_vereadores()

# Criar abas para a interface
tab1, tab2 = st.tabs(["Prefeitos", "Vereadores"])

# Aba de Prefeitos
with tab1:
    st.title('Análise de Gastos nas Eleições de 2024 - Prefeitos - Atualizado 16 de Setembro de 2024')
    st.write('Produzido por Christian Basilio - Linkedin: https://www.linkedin.com/in/christianbasilioo/')
    # Criando filtros com opções iniciais vazias
    st.write('Filtros de Seleção - Prefeitos')
    col1, col2, col3 = st.columns(3)  # Cria três colunas

    with col1:  # Primeira coluna para 'Estado'
        estado = st.selectbox('Escolha o estado:', [''] + sorted(top_prefeitos['Estado'].unique()), index=0)
        # Atualizar opções de cidade com base na seleção de estado
        if estado:
            cidade_options = sorted(top_prefeitos[top_prefeitos['Estado'] == estado]['Cidade'].unique())
        else:
            cidade_options = sorted(top_prefeitos['Cidade'].unique())

    with col2:  # Segunda coluna para 'Cidade'
        cidade = st.selectbox('Escolha a cidade:', [''] + cidade_options, index=0)

    with col3:  # Terceira coluna para 'Partido'
        partido = st.selectbox('Escolha o partido:', [''] + sorted(top_prefeitos['Partido'].unique()), index=0)
    # Filtrar os dados com base na seleção do usuário
    filtered_data = top_prefeitos.copy()
    if estado:
        filtered_data = filtered_data[filtered_data['Estado'] == estado]
    if cidade:
        filtered_data = filtered_data[filtered_data['Cidade'] == cidade]
    if partido:
        filtered_data = filtered_data[filtered_data['Partido'] == partido]

    # Ordenar os dados do maior para o menor
    filtered_data = filtered_data.sort_values(by='total', ascending=False)

    # Gráfico Top 10 Prefeitos que mais Gastaram
    fig = px.bar(filtered_data.head(10), 
                 x='total', 
                 y='NM_CANDIDATO', 
                 orientation='h', 
                 title='Top 10 Prefeitos que mais Gastaram',
                 labels={'total': 'Valor da Despesa Contratada (em mil)', 'NM_CANDIDATO': 'Nome do Candidato'},
                 text='total',
                 hover_data={'Partido': True},
                 color='total', 
                 color_continuous_scale='BuGn')

    fig.update_layout(xaxis_tickformat='plain', yaxis=dict(categoryorder='total ascending'))
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    st.plotly_chart(fig, use_container_width=True)

    st.write('Os gráfico mostram os gastos totais por partido nas eleições de 2024, de acordo com os filtros aplicados.')

    # Gráfico Gastos Totais por Partido - Prefeitos
    gastos_por_partido = filtered_data.groupby('Partido')['total'].sum().reset_index()
    gastos_por_partido = gastos_por_partido.sort_values(by='total', ascending=False)

    fig2 = px.bar(gastos_por_partido, 
                  x='total', 
                  y='Partido', 
                  orientation='h', 
                  title='Gastos Totais por Partido - Prefeitos',
                  labels={'total': 'Valor da Despesa Contratada (em mil)', 'Partido': 'Partido'},
                  text='total',
                  color='total', 
                  color_continuous_scale='BuGn')

    fig2.update_layout(
        xaxis_tickformat='plain',
        yaxis=dict(autorange='reversed'), 
        height=600, 
        margin=dict(l=120)
    )

    fig2.update_yaxes(tickfont=dict(size=10))
    fig2.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    st.plotly_chart(fig2, use_container_width=True)

    st.write('Tabela de Total de Gastos')
    # Trocando nome da coluna NM_CANDIDATO para Nome do Candidato
    filtered_data.rename(columns={'NM_CANDIDATO': 'Nome do Candidato'}, inplace=True)
    # Ordenando do maior para o menor
    filtered_data = filtered_data.sort_values(by='total', ascending=False)
    st.dataframe(filtered_data)

# Aba de Vereadores
with tab2:
    st.title('Análise de Gastos nas Eleições de 2024 - Vereadores - Atualizado 16 de Setembro de 2024')
    st.write('Produzido por Christian Basilio - Linkedin: https://www.linkedin.com/in/christianbasilioo/')
    
    
    estado_options_vereadores = [''] + list(top_vereadores['Estado'].unique())
    cidade_options_vereadores = [''] + list(top_vereadores['Cidade'].unique())
    partido_options_vereadores = [''] + list(top_vereadores['Partido'].unique())

    # Filtros de Seleção - Vereadores
    st.write('Filtros de Seleção - Vereadores')
    col1_ver, col2_ver, col3_ver = st.columns(3)  # Cria três colunas para vereadores

    with col1_ver:  # Primeira coluna para 'Estado'
        estado_vereadores = st.selectbox('Escolha o estado:', estado_options_vereadores, index=0, key='estado_vereadores')
        # Atualizar opções de cidade com base na seleção de estado
        if estado_vereadores:
            cidade_options_vereadores = sorted(top_vereadores[top_vereadores['Estado'] == estado_vereadores]['Cidade'].unique())
        else:
            cidade_options_vereadores = sorted(top_vereadores['Cidade'].unique())

    with col2_ver:  # Segunda coluna para 'Cidade'
        cidade_vereadores = st.selectbox('Escolha a cidade:', [''] + cidade_options_vereadores, index=0, key='cidade_vereadores')

    with col3_ver:  # Terceira coluna para 'Partido'
        partido_vereadores = st.selectbox('Escolha o partido:', partido_options_vereadores, index=0, key='partido_vereadores')

    filtered_data_vereadores = top_vereadores.copy()
    if estado_vereadores:
        filtered_data_vereadores = filtered_data_vereadores[filtered_data_vereadores['Estado'] == estado_vereadores]
    if cidade_vereadores:
        filtered_data_vereadores = filtered_data_vereadores[filtered_data_vereadores['Cidade'] == cidade_vereadores]
    if partido_vereadores:
        filtered_data_vereadores = filtered_data_vereadores[filtered_data_vereadores['Partido'] == partido_vereadores]

    filtered_data_vereadores = filtered_data_vereadores.sort_values(by='total', ascending=False)

    # Gráfico Top 10 Vereadores que mais Gastaram
    fig3 = px.bar(filtered_data_vereadores.head(10), 
                  x='total', 
                  y='NM_CANDIDATO', 
                  orientation='h', 
                  title='Top 10 Vereadores que mais Gastaram',
                  labels={'total': 'Valor da Despesa Contratada (em mil)', 'NM_CANDIDATO': 'Nome do Candidato'},
                  text='total',
                  hover_data={'Partido': True},
                  color='total', 
                  color_continuous_scale='BuGn')

    fig3.update_layout(xaxis_tickformat='plain', yaxis=dict(categoryorder='total ascending'))
    fig3.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    st.plotly_chart(fig3, use_container_width=True)

    st.write('Os gráficos mostram os gastos totais por partido nas eleições de 2024, de acordo com os filtros aplicados.')

    # Gráfico Gastos Totais por Partido - Vereadores
    gastos_por_partido_vereadores = filtered_data_vereadores.groupby('Partido')['total'].sum().reset_index()
    gastos_por_partido_vereadores = gastos_por_partido_vereadores.sort_values(by='total', ascending=False)

    fig4 = px.bar(gastos_por_partido_vereadores, 
                  x='total', 
                  y='Partido', 
                  orientation='h', 
                  title='Gastos Totais por Partido - Vereadores',
                  labels={'total': 'Valor da Despesa Contratada (em mil)', 'Partido': 'Partido'},
                  text='total',
                  color='total', 
                  color_continuous_scale='BuGn')

    fig4.update_layout(
        xaxis_tickformat='plain',
        yaxis=dict(autorange='reversed'), 
        height=600, 
        margin=dict(l=120)
    )

    fig4.update_yaxes(tickfont=dict(size=10))
    fig4.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    st.plotly_chart(fig4, use_container_width=True)

    st.write('Tabela de Gastos - Vereadores')
    # Trocando nome da coluna NM_CANDIDATO para Nome do Candidato
    filtered_data_vereadores.rename(columns={'NM_CANDIDATO': 'Nome do Candidato'}, inplace=True)
    # Ordenando do maior para o menor
    filtered_data_vereadores = filtered_data_vereadores.sort_values(by='total', ascending=False)
    st.dataframe(filtered_data_vereadores)