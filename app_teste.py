from dicionario_dados import dic

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")


def carregar_dados():
    dados = pd.read_parquet('data/dataset_streamlit.parquet')
    return dados


def home():
    
    dados = carregar_dados()

    # Análise exploratória de dados
    st.header('Análise Exploratória de Dados')

    # Variáveis quantitativas
    st.subheader('Variáveis Quantitativas')
    quantitativas = dados.select_dtypes(include=['int', 'float'])
    st.dataframe(quantitativas.describe())

    # Variáveis qualitativas
    st.subheader('Variáveis Qualitativas')
    qualitativas = dados.select_dtypes(include=['object'])
    st.dataframe(qualitativas.describe())

    # Gráficos interativos
    st.header('Gráficos Interativos')

    # Gráfico de barras para variáveis qualitativas
    st.subheader('Gráfico de Barras (Variáveis Qualitativas)')
    coluna_qualitativa = st.selectbox('Selecione uma coluna qualitativa', qualitativas.columns)
    contagem_qualitativa = dados[coluna_qualitativa].value_counts()
    fig_bar_qualitativa = px.bar(x=contagem_qualitativa.index, y=contagem_qualitativa.values)
    st.plotly_chart(fig_bar_qualitativa)

    # Gráfico de histograma para variáveis quantitativas
    st.subheader('Histograma (Variáveis Quantitativas)')
    coluna_quantitativa = st.selectbox('Selecione uma coluna quantitativa', quantitativas.columns)
    fig_hist_quantitativa = px.histogram(dados, x=coluna_quantitativa, nbins=30)
    st.plotly_chart(fig_hist_quantitativa)

    # Gráfico de dispersão com marcação de cores para variáveis quantitativas e qualitativas
    st.subheader('Gráfico de Dispersão (Quantitativas x Qualitativas)')
    coluna_x = st.selectbox('Selecione uma coluna quantitativa para o eixo X', quantitativas.columns)
    coluna_y = st.selectbox('Selecione uma coluna quantitativa para o eixo Y', quantitativas.columns)
    coluna_cor = st.selectbox('Selecione uma coluna qualitativa para a cor', qualitativas.columns)

    fig_scatter = px.scatter(dados, x=coluna_x, y=coluna_y, color=coluna_cor)
    st.plotly_chart(fig_scatter)

    from sklearn.cluster import KMeans


   # Selecionar as colunas para a análise de agrupamento
    colunas_analise = st.multiselect('Selecione as colunas para a análise de agrupamento', list(dados.columns))

    if colunas_analise:
        # Realizar a análise de agrupamento
        dados_analise = dados[colunas_analise]

        # Normalizar os dados (opcional, dependendo das características das variáveis)
        # dados_analise = (dados_analise - dados_analise.mean()) / dados_analise.std()

        # Aplicar o algoritmo de agrupamento K-means
        modelo = KMeans(n_clusters=3)  # Defina o número de clusters desejado
        modelo.fit(dados_analise)
        dados['grupo'] = modelo.labels_

        # Visualizar os grupos usando Plotly
        fig = px.scatter_3d(dados, x=colunas_analise[0], y=colunas_analise[1], z=colunas_analise[2], color='grupo')
        st.plotly_chart(fig)


pages = {
    'Página 1 - Introdução': home,
    'Página 2 - Dicionário': dic,
    #'Página 3 - Gráficos': exibir_paginaX,
}

# Seletor de página na barra lateral
page = st.sidebar.selectbox('Selecione a página', tuple(pages.keys()))

# Renderiza a página selecionada
pages[page]()