#---------------------------- VISÃO POR ESTADOS  --------------------------------------#

import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
from funcoes import (definicao_parametros_graficos, filtra_df, bignumbers, ler_df_drive)

#------------------------------ CONFIGURAÇÃO -------------------------------------------#

st.set_page_config(page_title = 'Análise das Vendas por Estado', layout = 'wide')
st.title('Análise das Vendas por Estado')  #Título da página

definicao_parametros_graficos()

#Leitura dos dados:
#order_items_df = ler_df_drive('1OTzGaimK_k8ZJKmaSxrvevQH2KFmIL8e')

order_items_df = pd.read_csv('datasets/orders_items_cleaned.csv')

#------------------------------- FUNÇÕES ----------------------------------------------#

def visoes_gerais(c_df, s_df):
       st.subheader('Volume de Vendas')  #Subtítulo

       col1, col2, col3 = st.columns(3) #Criando as colunas na página

       #TOTAL DE VENDAS POR ESTADO:
       vendas_estado =  c_df[['customer_state', 'total_price']].groupby('customer_state').sum().reset_index()

       #Gráfico na coluna 1:
       fig1, ax1 = plt.subplots()
       sns.barplot(data = vendas_estado, x = 'customer_state', y = 'total_price', ax = ax1)
       ax1.set_title("Total de Vendas por Estado")
       plt.xlabel('UF')
       plt.ylabel('Vendas (R$)')
       col1.pyplot(fig1)

       #TOTAL DE CLIENTES ÚNICOS POR ESTADO:
       clientes_estado =  c_df[['customer_state', 'customer_unique_id']].groupby('customer_state').nunique().reset_index()

       #Gráfico na coluna 2:
       fig2, ax2 = plt.subplots()
       sns.barplot(data = clientes_estado, x = 'customer_state', y = 'customer_unique_id', ax = ax2)
       ax2.set_title('Quantidade de Clientes Únicos por Estado')
       plt.xlabel('UF')
       plt.ylabel('Clientes Únicos')
       col2.pyplot(fig2)

       #TOTAL DE VENDEDORES ÚNICOS POR ESTADO:
       venedores_estado = s_df[['seller_state', 'seller_id']].groupby('seller_state').nunique().reset_index()

       #Gráfico na coluna 3:
       fig3, ax3 = plt.subplots()
       sns.barplot(data = venedores_estado, x = 'seller_state', y = 'seller_id', ax = ax3)
       ax3.set_title('Quantidade de Vendedores Únicos por Estado')
       plt.xlabel('UF')
       plt.ylabel('Vendedores Únicos')
       col3.pyplot(fig3)

       return None

def visoes_temporais(c_df, s_df):
       st.subheader('Visão Temporal')

       col1, col2, col3 = st.columns(3) #Criando as colunas na página

       # Dataframes dos gráficos:
       vendas_tempo = (c_df[['order_purchase_year_month', 'total_price']]
                            .groupby('order_purchase_year_month').sum().reset_index())

       clientes_tempo = (c_df[['order_purchase_year_month', 'customer_unique_id']]
                            .groupby('order_purchase_year_month').nunique().reset_index())

       vendedores_tempo = (s_df[['order_purchase_year_month', 'seller_id']]
                            .groupby('order_purchase_year_month').nunique().reset_index())

       #VENDAS POR ESTADO:
       fig1, ax1 = plt.subplots()
       sns.lineplot(vendas_tempo, x = 'order_purchase_year_month', y = 'total_price', ax = ax1)
       ax1.set_title(f'Vendas Mensais (R$)')
       plt.xlabel('Ano-Mês')
       plt.ylabel('Vendas (R$)')
       plt.xticks(rotation = 60)
       col1.pyplot(fig1)

       #CLIENTES ÚNICOS POR ESTADO:
       fig2, ax2 = plt.subplots()
       sns.lineplot(clientes_tempo, x = 'order_purchase_year_month', y = 'customer_unique_id', ax = ax2)
       ax2.set_title(f'Quantidade de Clientes Únicos por Mês')
       plt.xlabel('Ano-Mês')
       plt.ylabel('Clientes Únicos')
       plt.xticks(rotation = 60)
       col2.pyplot(fig2)

       #VENDEDORES POR ESTADO:
       fig3, ax3 = plt.subplots()
       sns.lineplot(vendedores_tempo, x = 'order_purchase_year_month', y = 'seller_id', ax = ax3)
       ax3.set_title(f'Quantidade de Vendedores Únicos por Mês')
       plt.xlabel('Ano-Mês')
       plt.ylabel('Vendedores')
       plt.xticks(rotation = 60)
       col3.pyplot(fig3)

       return None


#------------------------------------- DASHBOARD ----------------------------------------#

if __name__ == '__main__':

       customers_df_filtred, sellers_df_filtred, datas_selecionadas, estados_selecionados, status_selecionados = filtra_df(order_items_df)

       bignumbers(customers_df_filtred, sellers_df_filtred)

       visoes_gerais(customers_df_filtred, sellers_df_filtred)

       visoes_temporais(customers_df_filtred, sellers_df_filtred)

