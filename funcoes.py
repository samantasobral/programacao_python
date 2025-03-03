#---------------------------- SCRIPT DAS FUNÇÕES EM COMUM DAS PÁGINAS -------------------------------#

import gdown
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

def definicao_parametros_graficos():
       sns.set_theme()     
       plt.rcParams['figure.figsize'] = (6,3)  #Tamanho das figuras
       plt.rcParams['axes.titlesize'] = 16     #Tamanho dos títulos dos eixos
       plt.rcParams['axes.labelsize'] = 10      #Tamanho dos rótulos dos eixos
       plt.rcParams['xtick.labelsize'] = 8     #Tamanho dos números no eixo x
       plt.rcParams['ytick.labelsize'] = 8     #Tamanho dos números no eixo y
       plt.rcParams['legend.fontsize'] = 10     #Tamanho da fonte da legenda
       plt.rcParams['lines.markersize'] = 4    #Tamanho dos marcadores nas linhas

       return None

def filtra_df(df):
    # Side Bar:
    st.sidebar.header('Filtros')

    # Certifique-se de que a coluna 'order_purchase_timestamp' está no formato datetime
    df['order_purchase_year_month'] = pd.to_datetime(df['order_purchase_year_month'], format = '%Y-%m')
    data_minima = df['order_purchase_year_month'].min().to_pydatetime()
    data_maxima = df['order_purchase_year_month'].max().to_pydatetime()

    # Criando o slider para selecionar o intervalo de datas
    datas_selecionadas = st.sidebar.slider("Selecione o intervalo de data:", 
                                           min_value=data_minima,
                                           max_value=data_maxima,
                                           value=(data_minima, data_maxima))

    # Filtro de Estado:
    lista_estados = sorted(list(df['seller_state'].unique()))
    estados_selecionados = st.sidebar.multiselect("Selecione um Estado", 
                                        options = lista_estados, 
                                        default=lista_estados)

    # Filtro de Status do Pedido:
    lista_status = sorted(list(df['order_status'].unique()))
    status_selecionados = st.sidebar.multiselect("Selecione o Status do Pedido", 
                                     options = lista_status, 
                                     default=lista_status)

    # Aplicando Filtros:
    df_filtered = df[(df['order_status'].isin(status_selecionados)) &
                     ((df['order_purchase_year_month'] >= datas_selecionadas[0]) & 
                      (df['order_purchase_year_month'] <= datas_selecionadas[1]))]

    customers_df_filtred = df_filtered[df_filtered['customer_state'].isin(estados_selecionados)]
    sellers_df_filtred = df_filtered[df_filtered['seller_state'].isin(estados_selecionados)]
    
    return customers_df_filtred, sellers_df_filtred, datas_selecionadas, estados_selecionados, status_selecionados



def bignumbers(c_df, s_df):
       st.subheader('Indicadores Gerais')   #Subtítulo da Sessão de Big Numbers

       total_vendas = c_df['total_price'].sum()
       total_customers = c_df['customer_unique_id'].nunique()
       total_sellers = s_df['seller_id'].nunique()
       total_categorias = c_df['product_category_name'].nunique()

       col1, col2, col3, col4 = st.columns(4)    #Cria 4 colunas

       col1.metric('Total de Vendas', f'R$ {total_vendas:,.2f}')
       col2.metric('Quantidade de Clientes Únicos', f'{total_customers:,.0f}')
       col3.metric('Quantidade de Vendedores Únicos', f'{total_sellers:,.0f}')
       col4.metric('Quantidade de Categorias', f'{total_categorias:,.0f}') 

       return None

def ler_df_drive(file_id):

       # URL do arquivo no Google Drive
       url = f'https://drive.google.com/uc?id={file_id}'

       # Baixando o arquivo
       output = 'arquivo.csv'
       gdown.download(url, output, quiet=False)

       # Lendo o arquivo CSV
       df = pd.read_csv(output)

       return df
